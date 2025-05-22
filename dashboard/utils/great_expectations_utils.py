import os
from bs4 import BeautifulSoup

REPORTS_DIR = "/home/ryan/ml_platform/great_expectations/data_docs/local_site/validations"


def get_ge_reports():
    reports = []
    for root, _, files in os.walk(REPORTS_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path) as f:
                    soup = BeautifulSoup(f, "html.parser")
                    title = soup.title.string
                    status = "Success" if "Success" in title else "Failure"
                    reports.append({
                        "name": title,
                        "link": path.replace("/home/ryan/ml_platform/", "http://localhost:5050/"),
                        "status": status,
                    })
    return reports
