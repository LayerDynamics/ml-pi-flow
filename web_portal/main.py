from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# serve our custom CSS/js
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/component/{name}", response_class=HTMLResponse)
async def get_component(name: str, request: Request):
    valid_components = ["mlflow", "tensorboard", "vector_db", "label_studio", "great_expectations"]
    if name not in valid_components:
        name = "mlflow"
    return templates.TemplateResponse(f"components/{name}.html", {"request": request})
