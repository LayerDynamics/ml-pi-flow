import streamlit as st
from utils.mlflow_utils import get_mlflow_metrics
from utils.tensorboard_utils import parse_tensorboard_logs
from utils.vector_db_utils import vector_db_stats
from utils.label_studio_utils import get_label_studio_stats
from utils.great_expectations_utils import get_ge_reports

st.set_page_config(
    page_title="ML Platform Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🖥️ ML Platform Monitoring Dashboard")

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
