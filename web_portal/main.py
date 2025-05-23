from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# serve our custom CSS/js
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for notifications
notifications: List[str] = []


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "notifications": notifications}
    )


@app.get("/component/{name}", response_class=HTMLResponse)
async def get_component(name: str, request: Request):
    valid_components = [
        "mlflow",
        "tensorboard",
        "vector_db",
        "label_studio",
        "great_expectations",
    ]
    if name not in valid_components:
        name = "mlflow"
    return templates.TemplateResponse(
        f"components/{name}.html", {"request": request}
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        notifications.append(data)
        await websocket.send_text(f"Notification received: {data}")
