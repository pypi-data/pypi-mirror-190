import shutil
from collections import defaultdict
from pathlib import Path
from typing import Union, Callable, Dict, Optional

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from dnn_cool_train_loop.metrics import _flush_all_metrics
from dnn_cool_train_loop.task_loop import _process_batch


@torch.no_grad()
def eval_for_one_epoch(
        model: nn.Module,
        dataset: Dataset,
        criterion_dict: Dict[str, Callable],
        batch_size_effective: int,
        metrics_dir: Optional[Union[str, Path]] = None,
        metrics_dict: Dict[str, Dict[str, Callable]] = None,
        n_flush_metrics: int = 1_000,
):
    model.eval()
    if metrics_dir is not None and metrics_dir.exists():
        shutil.rmtree(metrics_dir)
    train_loader = DataLoader(dataset=dataset, batch_size=1)
    device = next(model.parameters()).device
    metric_values_dict = defaultdict(list)
    for i, data in enumerate(tqdm(train_loader)):
        _process_batch(
            model=model,
            batch_size_effective=batch_size_effective,
            criterion_dict=criterion_dict,
            metrics_dir=metrics_dir,
            metrics_dict=metrics_dict,
            metric_values_dict=metric_values_dict,
            data=data,
            device=device
        )
        if (i + 1) % n_flush_metrics == 0:
            _flush_all_metrics(metrics_dir, metric_values_dict)
    # Flush metrics for last batch.
    if len(dataset) % n_flush_metrics != 0:
        _flush_all_metrics(metrics_dir, metric_values_dict)
