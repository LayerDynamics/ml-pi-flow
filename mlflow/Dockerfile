# /mlflow/Dockerfile

FROM python:3.10-slim

RUN pip install mlflow

EXPOSE 5000

CMD mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root /mlflow/storage \
  --host 0.0.0.0
