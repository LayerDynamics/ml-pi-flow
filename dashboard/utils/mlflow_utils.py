import mlflow
import pandas as pd


def get_mlflow_metrics():
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiments = client.list_experiments()
    data = []
    for exp in experiments:
        runs = client.search_runs(exp.experiment_id)
        for run in runs:
            metrics = run.data.metrics
            data.append({"Experiment": exp.name, "Run ID": run.info.run_id, **metrics})
    return pd.DataFrame(data)

def get_mlflow_experiment_names():
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiments = client.list_experiments()
    return [exp.name for exp in experiments]

def get_mlflow_run_ids(experiment_name):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        runs = client.search_runs(experiment.experiment_id)
        return [run.info.run_id for run in runs]
    else:
        return []
    
def get_mlflow_run_metrics(experiment_name, run_id):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    run = client.get_run(run_id)
    if run:
        return run.data.metrics
    else:
        return {}
    
def get_mlflow_run_params(experiment_name, run_id):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    run = client.get_run(run_id)
    if run:
        return run.data.params
    else:
        return {}
    
def get_mlflow_run_tags(experiment_name, run_id):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    run = client.get_run(run_id)
    if run:
        return run.data.tags
    else:
        return {}
def get_mlflow_run_artifacts(experiment_name, run_id):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    run = client.get_run(run_id)
    if run:
        return run.data.tags
    else:
        return {}
    
def get_mlflow_run_info(experiment_name, run_id):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    run = client.get_run(run_id)
    if run:
        return run.info
    else:
        return {}
    
def get_mlflow_experiment_info(experiment_name):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        return experiment
    else:
        return {}
def get_mlflow_experiment_runs(experiment_name):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        runs = client.search_runs(experiment.experiment_id)
        return [run.info.run_id for run in runs]
    else:
        return []
def get_mlflow_experiment_metrics(experiment_name):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        runs = client.search_runs(experiment.experiment_id)
        metrics = {}
        for run in runs:
            metrics[run.info.run_id] = run.data.metrics
        return metrics
    else:
        return {}
def get_mlflow_experiment_params(experiment_name):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        runs = client.search_runs(experiment.experiment_id)
        params = {}
        for run in runs:
            params[run.info.run_id] = run.data.params
        return params
    else:
        return {}
def get_mlflow_experiment_tags(experiment_name):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        runs = client.search_runs(experiment.experiment_id)
        tags = {}
        for run in runs:
            tags[run.info.run_id] = run.data.tags
        return tags
    else:
        return {}
def get_mlflow_experiment_artifacts(experiment_name):
    client = mlflow.tracking.MlflowClient("http://localhost:5000")
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        runs = client.search_runs(experiment.experiment_id)
        artifacts = {}
        for run in runs:
            artifacts[run.info.run_id] = run.data.artifacts
        return artifacts
    else:
        return {}