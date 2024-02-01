import uvicorn
import os
from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import websockets
import json
from break_into_units import process_text
from celery import Celery

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task
def process_text_to_json(input_text):
    process_text(input_text)

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-audio", response_class=HTMLResponse)
async def generate_audio(request: Request, background_tasks: BackgroundTasks, text_input: str = Form(...)):
    # return templates.TemplateResponse("result.html", {"request": request, "audio_url": audio_url})
    background_tasks.add_task(process_text, text_input)

    return json.dumps({"response": "success", "message": "Request is in progress"})

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             background_tasks = BackgroundTasks()
#             background_tasks.add_task(process_text, data, websocket, background_tasks)
#     except WebSocketDisconnect:
#         pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", port=port, log_level="info", reload=True)