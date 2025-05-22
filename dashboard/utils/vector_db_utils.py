import requests


def vector_db_stats():
    url = "http://localhost:8000/api/v1/collections"
    response = requests.get(url)
    collections = response.json()
    stats = {}
    for col in collections:
        col_name = col["name"]
        col_info = requests.get(f"{url}/{col_name}").json()
        stats[col_name] = {"embeddings_count": col_info["count"], "dimension": col_info["dimension"]}
    return stats
