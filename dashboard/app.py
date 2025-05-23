import streamlit as st
import psutil
import plotly.express as px
from utils.mlflow_utils import get_mlflow_metrics
from utils.tensorboard_utils import parse_tensorboard_logs
from utils.vector_db_utils import vector_db_stats
from utils.label_studio_utils import get_label_studio_stats
from utils.great_expectations_utils import get_ge_reports
from streamlit import st_autorefresh

st.set_page_config(
    page_title="ML Platform Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🖥️ ML Platform Monitoring Dashboard")

# System Resource Usage Section
st.header("🔴 System Resource Usage")
cpu_usage = psutil.cpu_percent(interval=1)
memory_info = psutil.virtual_memory()
disk_usage = psutil.disk_usage('/')
st.metric("CPU Usage", f"{cpu_usage}%")
st.metric("Memory Usage", f"{memory_info.percent}%")
st.metric("Disk Usage", f"{disk_usage.percent}%")

# MLflow Section
st.header("🟢 MLflow Experiments")
mlflow_metrics_df = get_mlflow_metrics()
st.dataframe(mlflow_metrics_df)

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

# Real-time Data Updates
st_autorefresh(interval=10000)  # Refresh every 10 seconds

# Interactive Visualizations
st.header("📊 Interactive Visualizations")
fig = px.line(mlflow_metrics_df, x="Run ID", y="metric_name",
              title="MLflow Metrics Over Time")
st.plotly_chart(fig)
