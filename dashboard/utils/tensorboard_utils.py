import os
import pandas as pd
from tensorboard.backend.event_processing.event_accumulator import \
    EventAccumulator

LOG_DIR = "/home/ryan/ml_platform/tensorboard/logs"


def parse_tensorboard_logs():
    runs = []
    for root, _, files in os.walk(LOG_DIR):
        for file in files:
            if "events.out.tfevents" in file:
                path = os.path.join(root, file)
                ea = EventAccumulator(path).Reload()
                tags = ea.Tags()["scalars"]
                summary = {tag: ea.Scalars(tag)[-1].value for tag in tags}
                runs.append({"Run": root, **summary})
    return pd.DataFrame(runs)
