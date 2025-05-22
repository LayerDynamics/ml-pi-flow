import requests
import pandas as pd

API_URL = "http://localhost:8080/api"
API_KEY = "YOUR_LABEL_STUDIO_API_KEY"


def get_label_studio_stats():
    headers = {"Authorization": f"Token {API_KEY}"}
    projects = requests.get(f"{API_URL}/projects", headers=headers).json()
    data = []
    for project in projects["results"]:
        data.append({
            "Project": project["title"],
            "Annotations": project["task_number"],
            "Completed": project["num_tasks_with_annotations"],
        })
    return pd.DataFrame(data)
