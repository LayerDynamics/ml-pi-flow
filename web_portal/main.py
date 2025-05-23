import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import json
import aiofiles
import mlflow
import shutil

app = FastAPI()

# serve our custom CSS/js
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Service URLs from environment or defaults
SERVICE_URLS = {
    "MLflow": os.getenv("MLFLOW_URL", "http://mlflow:5000"),
    "Label Studio": os.getenv("LABEL_STUDIO_URL", f"http://label_studio:{os.getenv('LABEL_STUDIO_PORT', '8890')}/"),
    "TensorBoard": os.getenv("TENSORBOARD_URL", "http://tensorboard:6006"),
    "Chroma": os.getenv("CHROMA_URL", "http://vector_db:8000"),
    "Gitea": os.getenv("GITEA_URL", "http://gitea:3000"),
    "Great Expectations": os.getenv("GE_URL", "http://great_expectations:4000"),
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Check health/status of each service
    statuses = {}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in SERVICE_URLS.items():
            try:
                resp = await client.get(url)
                statuses[name] = resp.status_code
            except Exception:
                statuses[name] = None
    return templates.TemplateResponse("index.html", {
        "request": request,
        "services": SERVICE_URLS,
        "statuses": statuses
    })


@app.get("/api/services")
async def api_services():
    # Return service URLs and status as JSON
    statuses = {}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in SERVICE_URLS.items():
            try:
                resp = await client.get(url)
                statuses[name] = resp.status_code
            except Exception:
                statuses[name] = None
    return {"services": SERVICE_URLS, "statuses": statuses}


@app.get("/component/{name}", response_class=HTMLResponse)
async def get_component(name: str, request: Request):
    valid_components = ["mlflow", "tensorboard", "vector_db", "label_studio", "great_expectations", "gitea"]
    if name not in valid_components:
        name = "mlflow"
    return templates.TemplateResponse(f"components/{name}.html", {"request": request})


@app.post("/api/mlflow/trigger_run")
async def trigger_run(experiment_name: str = Form(...), params: str = Form(...)):
    try:
        client = mlflow.tracking.MlflowClient("http://mlflow:5000")
        experiment = client.get_experiment_by_name(experiment_name)
        if not experiment:
            experiment_id = client.create_experiment(experiment_name)
        else:
            experiment_id = experiment.experiment_id
        params_dict = json.loads(params)
        run = client.create_run(experiment_id)
        for k, v in params_dict.items():
            client.log_param(run.info.run_id, k, v)
        return JSONResponse({"status": "success", "run_id": run.info.run_id})
    except Exception as e:
        return JSONResponse({"status": "error", "detail": str(e)})


@app.post("/api/mlflow/upload_artifact")
async def upload_artifact(run_id: str = Form(...), artifact_file: UploadFile = File(...)):
    try:
        temp_path = f"/tmp/{artifact_file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(artifact_file.file, buffer)
        client = mlflow.tracking.MlflowClient("http://mlflow:5000")
        client.log_artifact(run_id, temp_path)
        os.remove(temp_path)
        return JSONResponse({"status": "success", "msg": "Artifact uploaded."})
    except Exception as e:
        return JSONResponse({"status": "error", "detail": str(e)})


@app.post("/api/labelstudio/sync_to_mlflow")
async def sync_labelstudio_to_mlflow():
    # Example: fetch data from Label Studio and log as MLflow artifact
    import requests
    try:
        api_url = os.getenv("LABEL_STUDIO_URL", f"http://label_studio:{os.getenv('LABEL_STUDIO_PORT', '8890')}/api/projects")
        api_key = os.getenv("LABEL_STUDIO_API_KEY", "")
        headers = {"Authorization": f"Token {api_key}"}
        projects = requests.get(api_url, headers=headers).json()
        # Save to file and log as artifact
        temp_path = "/tmp/labelstudio_projects.json"
        with open(temp_path, "w") as f:
            json.dump(projects, f)
        client = mlflow.tracking.MlflowClient("http://mlflow:5000")
        # Log to a default experiment
        experiment_name = "labelstudio_sync"
        experiment = client.get_experiment_by_name(experiment_name)
        if not experiment:
            experiment_id = client.create_experiment(experiment_name)
        else:
            experiment_id = experiment.experiment_id
        run = client.create_run(experiment_id)
        client.log_artifact(run.info.run_id, temp_path)
        os.remove(temp_path)
        return JSONResponse({"status": "success", "msg": "Label Studio data synced to MLflow."})
    except Exception as e:
        return JSONResponse({"status": "error", "detail": str(e)})
