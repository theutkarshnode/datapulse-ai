import os
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from agent.graph import agent_graph

app = FastAPI()

os.makedirs("outputs", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/")
async def get_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    file_path = os.path.join("uploads", "data.csv")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "ok", "csv_path": file_path, "filename": file.filename}

@app.websocket("/ws")
async def agent_ws(ws: WebSocket):
    await ws.accept()
    try:
        data = await ws.receive_json()
        question = data.get("question", "")
        csv_path = data.get("csv_path", "uploads/data.csv")

        if not os.path.exists(csv_path):
            await ws.send_json({"type": "error", "text": "Please upload a CSV dataset first."})
            return

        initial_state = {
            "question": question,
            "csv_path": csv_path,
            "csv_info": "",
            "code": "",
            "output": "",
            "error": None,
            "charts": [],
            "retries": 0,
            "final_answer": "",
        }

        await ws.send_json({"type": "status", "text": "Inspector: Profiling dataset schema and types..."})

        for event in agent_graph.stream(initial_state):
            for node_name, node_output in event.items():
                if node_name == "inspector":
                    await ws.send_json({"type": "status", "text": "Coder: Synthesizing Python analytics & charts..."})
                elif node_name == "coder":
                    await ws.send_json({"type": "code", "code": node_output.get("code", "")})
                    await ws.send_json({"type": "status", "text": "Sandbox: Executing Python in isolated environment..."})
                elif node_name == "executor":
                    if node_output.get("error"):
                        retries = node_output.get("retries", 1)
                        await ws.send_json({
                            "type": "retry",
                            "text": f"Self-Healing Triggered (Attempt {retries}/3) — Patching code...",
                            "error": node_output.get("error")
                        })
                    else:
                        await ws.send_json({
                            "type": "output",
                            "output": node_output.get("output", ""),
                            "charts": node_output.get("charts", [])
                        })
                        await ws.send_json({"type": "status", "text": "Strategist: Compiling verified executive brief..."})
                elif node_name == "summarizer":
                    await ws.send_json({"type": "done", "answer": node_output.get("final_answer", "")})
            await asyncio.sleep(0.05)

    except Exception as e:
        await ws.send_json({"type": "error", "text": f"Runtime Error: {str(e)}"})
