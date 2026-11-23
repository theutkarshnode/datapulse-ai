<div align="center">

<img src="assets/banner.svg" alt="DataPulse AI Banner" width="100%" />

<br /><br />

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-WebSockets-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent_State_Machine-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Live_Model_Router-6366F1?style=for-the-badge&logo=openai&logoColor=white)](https://openrouter.ai)
[![Pandas](https://img.shields.io/badge/Pandas-Analytics_Engine-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-160_DPI_Charts-11557C?style=for-the-badge&logo=plotly&logoColor=white)](https://matplotlib.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

[Architecture](#architecture) · [Product Showcase](#product-showcase) · [Why This Exists](#why-this-exists) · [Tech Stack](#tech-stack) · [Quick Start](#quick-start)

</div>

---

## Architecture

<div align="center">
  <img src="assets/architecture.svg" alt="DataPulse AI System Architecture" width="100%" />
</div>

### Execution Pipeline
1. **Inspector Node (`agent/nodes.py`):** Profiles the uploaded CSV (`df.shape`, `df.dtypes`, `df.head(5)`) so the LLM understands the exact schema without overflowing the context window.
2. **Coder Node (`agent/nodes.py`):** Uses dynamic OpenRouter model discovery to synthesize a standalone `pandas` + `matplotlib` script styled in a clean executive palette (`160 DPI`).
3. **Self-Healing Python Sandbox (`executor_node`):** Runs the script in an isolated subprocess with a 20-second timeout. If a `SyntaxError`, `KeyError`, or `ValueError` occurs, the traceback loops back to the Coder Node for up to **3 autonomous self-healing retries**.
4. **Executive Strategist (`summarizer_node`):** Generates a boardroom-ready brief (headline, bold KPIs, actionable recommendation) strictly from verified terminal stdout.

---

## Product Showcase

### 1. Autonomous Analytics Studio & Live Data Profiler
<div align="center">
  <img src="assets/dashboard.png" alt="DataPulse AI Dashboard" width="95%" />
</div>

### 2. Multi-Chart Visual Analytics Suite (160 DPI)
<div align="center">
  <img src="assets/charts.png" alt="Visual Analytics Suite" width="95%" />
</div>

### 3. Verified Executive Brief & LangGraph Execution Log
<div align="center">
  <img src="assets/brief.png" alt="Executive Brief and Execution Log" width="95%" />
</div>

---

## Why This Exists

| Capability | Standard Chat-with-CSV Tools | DataPulse AI |
| :--- | :--- | :--- |
| **Math & Aggregations** | Prone to LLM token-prediction hallucinations | **100% deterministic Python (`pandas`) execution** |
| **Large Datasets** | Fails on context-window token limits | **Profiles schema only — scales to thousands of rows** |
| **Runtime Bugs** | Crashes and exposes raw tracebacks to user | **Autonomous 3x self-healing code patching** |
| **Visual Output** | Basic single static plots | **Multi-chart 160-DPI executive dashboards** |

---

## Tech Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Backend & Streaming** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) `Uvicorn` + `WebSockets` | Async CSV upload API & real-time step streaming |
| **Agent Orchestration** | ![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white) `StateGraph` | Cyclic multi-node workflow with retry routing |
| **LLM Inference** | ![OpenRouter](https://img.shields.io/badge/OpenRouter-6366F1?style=flat-square&logo=openai&logoColor=white) `OpenAI SDK` | Live `:free` model discovery + empty-response fallback |
| **Data & Visuals** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) + `Matplotlib (Agg)` | Headless data processing & publication-grade PNGs |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) ![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | Stripe/Linear-inspired SaaS UI with live step tracker |

---

## Quick Start

```bash
git clone [https://github.com/theutkarshnode/datapulse-ai.git](https://github.com/theutkarshnode/datapulse-ai.git)
cd datapulse-ai

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
uvicorn app:app --reload
```

Open **`http://127.0.0.1:8000`** in your browser.

---

## License

Released under the [MIT License](LICENSE).