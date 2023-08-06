from pathlib import Path
from typing import Dict, List

import numpy as np
from mmap_ninja import numpy as np_ninja


def _flush_all_metrics(
        metrics_dir: Path,
        metric_values_dict: Dict[str, List[float]]
):
    for k, v in metric_values_dict.items():
        task, metric, key = k
        _flush_datapoint(metrics_dir, task, metric, key, v)
        metric_values_dict[k] = []


def _store_datapoint(
        metric_values_dict: Dict,
        task: str,
        metric: str,
        idx: int,
        value: float
):
    metric_values_dict[(task, metric, "idx")].append(idx)
    metric_values_dict[(task, metric, "value")].append(value)


def _flush_datapoint(metrics_dir: Path, task: str, metric: str, key: str, values: List[float]):
    out_dir = metrics_dir / task / metric
    out_dir.mkdir(exist_ok=True, parents=True)
    if not (out_dir / key).exists():
        np_ninja.from_ndarray(str(out_dir / key), np.asarray(values))
        return
    np_ninja.extend_dir(str(out_dir / key), np.asarray(values))
