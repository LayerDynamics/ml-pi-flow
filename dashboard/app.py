import os
import streamlit as st
import requests
from utils.mlflow_utils import get_mlflow_metrics, get_tensorboard_logdir_for_run, get_ge_report_for_run, get_gitea_commit_link_for_run
from utils.tensorboard_utils import parse_tensorboard_logs
from utils.vector_db_utils import vector_db_stats
from utils.label_studio_utils import get_label_studio_stats
from utils.great_expectations_utils import get_ge_reports
from utils.gitea_utils import get_gitea_stats

st.set_page_config(
    page_title="ML Platform Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

SERVICE_URLS = {
    "MLflow": os.getenv("MLFLOW_URL", "http://mlflow:5000"),
    "Label Studio": os.getenv("LABEL_STUDIO_URL", f"http://label_studio:{os.getenv('LABEL_STUDIO_PORT', '8890')}/"),
    "TensorBoard": os.getenv("TENSORBOARD_URL", "http://tensorboard:6006"),
    "Chroma": os.getenv("CHROMA_URL", "http://vector_db:8000"),
    "Gitea": os.getenv("GITEA_URL", "http://gitea:3000"),
    "Great Expectations": os.getenv("GE_URL", "http://great_expectations:4000"),
}

st.title("ML-Pi-Flow Unified Dashboard")

cols = st.columns(len(SERVICE_URLS))
for idx, (name, url) in enumerate(SERVICE_URLS.items()):
    with cols[idx]:
        try:
            resp = requests.get(url, timeout=2)
            status = f"🟢 {resp.status_code}"
        except Exception:
            status = "🔴 Offline"
        st.markdown(f"### [{name}]({url})\nStatus: {status}")

st.markdown("---")
st.markdown("#### Quick Links")
for name, url in SERVICE_URLS.items():
    st.write(f"- [{name}]({url})")

# MLflow Section
st.header("🟢 MLflow Experiments")
mlflow_metrics_df = get_mlflow_metrics()
if not mlflow_metrics_df.empty:
    for idx, row in mlflow_metrics_df.iterrows():
        st.write(f"Experiment: {row.get('Experiment', '')}, Run ID: {row.get('Run ID', '')}")
        run_id = row.get('Run ID', '')
        # Cross-service links
        tb_logdir = get_tensorboard_logdir_for_run(run_id)
        ge_report = get_ge_report_for_run(run_id)
        gitea_commit = get_gitea_commit_link_for_run(run_id)
        if tb_logdir:
            st.markdown(f"- [TensorBoard Logs](/component/tensorboard?run_id={run_id})")
        if ge_report:
            st.markdown(f"- [GE Report]({ge_report})")
        if gitea_commit:
            st.markdown(f"- [Gitea Commit]({gitea_commit})")
        st.markdown("---")
else:
    st.info("No MLflow runs found.")

# TensorBoard Section
st.header("🟠 TensorBoard Training Summaries")
tensorboard_summary_df = parse_tensorboard_logs()
st.dataframe(tensorboard_summary_df)

# VectorDB Section
st.header("🔵 Vector Database Statistics")
vector_stats = vector_db_stats()
st.json(vector_stats)

# Label Studio Section
st.header("🟡 Label Studio Annotation Status")
label_stats_df = get_label_studio_stats()
st.dataframe(label_stats_df)

# Great Expectations Section
st.header("🟣 Data Validation Reports")
ge_reports = get_ge_reports()
for report in ge_reports:
    st.markdown(f"- [{report['name']}]({report['link']}) ({report['status']})")

# Show MLflow metrics
st.header("MLflow Metrics")
try:
    mlflow_metrics = get_mlflow_metrics()
    st.json(mlflow_metrics)
except Exception as e:
    st.warning(f"Could not fetch MLflow metrics: {e}")

# Show TensorBoard logs
st.header("TensorBoard Logs")
try:
    tb_logs = parse_tensorboard_logs()
    st.json(tb_logs)
except Exception as e:
    st.warning(f"Could not fetch TensorBoard logs: {e}")

# Show VectorDB stats
st.header("VectorDB Stats")
try:
    vdb_stats = vector_db_stats()
    st.json(vdb_stats)
except Exception as e:
    st.warning(f"Could not fetch VectorDB stats: {e}")

# Show Label Studio stats
st.header("Label Studio Stats")
try:
    ls_stats = get_label_studio_stats()
    st.json(ls_stats)
except Exception as e:
    st.warning(f"Could not fetch Label Studio stats: {e}")

# Show Great Expectations reports
st.header("Great Expectations Reports")
try:
    ge_reports = get_ge_reports()
    st.json(ge_reports)
except Exception as e:
    st.warning(f"Could not fetch GE reports: {e}")

# Gitea link
st.header("Gitea Repository Management")
st.markdown(f"[Open Gitea]({SERVICE_URLS['Gitea']})")

# Set Streamlit config to help with websocket issues
def _patch_streamlit_websocket():
    import streamlit.web.server.websocket_headers
    streamlit.web.server.websocket_headers._get_websocket_headers = lambda *a, **kw: {}
try:
    _patch_streamlit_websocket()
except Exception:
    pass

# Gitea Section
st.header("🟤 Gitea Repositories")
gitea_stats = get_gitea_stats()
if "error" in gitea_stats:
    st.warning(f"Gitea API error: {gitea_stats['error']}")
else:
    st.write(f"Total Repositories: {gitea_stats['repo_count']}")
    st.write(gitea_stats["repos"])
