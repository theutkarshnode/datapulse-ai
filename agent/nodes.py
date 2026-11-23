import os
import re
import sys
import glob
import subprocess
import pandas as pd
from openai import OpenAI
from agent.state import AgentState

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "DataPulse AI",
    },
)

def _get_live_free_models() -> list:
    try:
        all_models = [m.id for m in client.models.list().data]
        free = [m for m in all_models if m.endswith(":free")]
        # Prefer strong coding/general models first
        ordered = ["openrouter/free"]
        for pref in ("qwen", "deepseek", "llama", "mistral", "gemma", "gemini"):
            for m in free:
                if pref in m.lower() and m not in ordered:
                    ordered.append(m)
        ordered += [m for m in free if m not in ordered]
        print(f"✅ Found {len(free)} live free models on OpenRouter")
        return ordered
    except Exception as e:
        print(f"⚠️ Could not fetch model list: {e}")
        return ["openrouter/free"]

FREE_MODELS = _get_live_free_models()

def _call_llm(prompt: str) -> str:
    last_err = None
    for model_id in FREE_MODELS[:12]:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2048,
                timeout=45,
            )
            content = response.choices[0].message.content
            if not content:
                print(f"⚠️ Empty response from {model_id}, trying next...")
                continue
            print(f"✅ OpenRouter Model Used: {model_id}")
            return content
        except Exception as e:
            print(f"⚠️ Skipping {model_id}: {str(e)[:80]}")
            last_err = e
            continue
    raise last_err or RuntimeError("All free OpenRouter models failed.")

def _clean_code(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    text = re.sub(r"^```(?:python)?\s*\n?", "", text.strip())
    text = re.sub(r"\n?```\s*$", "", text.strip())
    return text.strip()

def inspector_node(state: AgentState) -> dict:
    df = pd.read_csv(state["csv_path"])
    info = (
        f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
        f"Columns & Types:\n{df.dtypes.to_string()}\n\n"
        f"First 5 Rows:\n{df.head(5).to_string()}"
    )
    return {"csv_info": info, "retries": 0, "error": None, "charts": []}

def coder_node(state: AgentState) -> dict:
    for old_chart in glob.glob("outputs/chart*.png"):
        os.remove(old_chart)

    error_context = ""
    if state.get("error"):
        error_context = f"""
        PREVIOUS EXECUTION FAILED.
        Previous Code:
        {state['code']}

        Traceback:
        {state['error']}

        Fix the bug completely and return the full working Python script.
        """

    prompt = f"""
    You are a Principal Data Scientist building executive-grade analytics visuals.
    Write a concise, standalone Python script using pandas and matplotlib to answer the user's request.

    CSV Path: "{state['csv_path']}"
    Dataset Schema & Sample:
    {state['csv_info']}

    User Request: {state['question']}
    {error_context}

    Strict Rules:
    1. Load data with: df = pd.read_csv("{state['csv_path']}")
    2. Print all key metrics clearly using print().
    3. Visual Design Standards:
       - Clean white background (#FFFFFF), remove top and right spines, subtle light gridlines (alpha=0.3).
       - Palette: Royal Blue (#2563EB), Indigo (#4F46E5), Sky Blue (#0EA5E9), Deep Navy (#0F172A).
       - Save charts at dpi=160, bbox_inches='tight'.
       - If multiple charts are requested, save them as "outputs/chart_1.png", "outputs/chart_2.png", "outputs/chart_3.png", "outputs/chart_4.png" using DIVERSE chart types (Bar, Donut/Pie, Horizontal Bar, Line). Otherwise save "outputs/chart_1.png".
       - Always call plt.close() after each figure.
    4. Return ONLY valid Python code inside ```python ``` blocks. Keep the code clean and concise.
    """

    text = _call_llm(prompt)
    return {"code": _clean_code(text)}

def executor_node(state: AgentState) -> dict:
    safe_code = "import matplotlib\nmatplotlib.use('Agg')\n" + state["code"]

    try:
        result = subprocess.run(
            [sys.executable, "-c", safe_code],
            capture_output=True,
            text=True,
            timeout=20
        )
        if result.returncode == 0:
            charts = sorted(glob.glob("outputs/chart*.png"))
            return {
                "output": result.stdout.strip() or "Execution completed successfully.",
                "error": None,
                "charts": charts
            }
        else:
            return {
                "error": result.stderr.strip(),
                "retries": state.get("retries", 0) + 1
            }
    except subprocess.TimeoutExpired:
        return {
            "error": "TimeoutError: Script exceeded 20 seconds execution limit.",
            "retries": state.get("retries", 0) + 1
        }

def summarizer_node(state: AgentState) -> dict:
    if state.get("error"):
        return {
            "final_answer": f"Execution failed after 3 self-healing attempts.\n\nLast Error:\n```\n{state['error']}\n```"
        }

    prompt = f"""
    You are an Executive Data Strategist. Write a crisp, boardroom-ready English summary based ONLY on the verified Python output below.

    User Request: {state['question']}
    Verified Output:
    {state['output']}

    Format:
    - Start with a 1-sentence headline takeaway.
    - Follow with 3-4 concise bullet points highlighting exact numbers in **bold**.
    - End with 1 actionable recommendation.
    """
    return {"final_answer": _call_llm(prompt)}
