from pathlib import Path
from typing import Union, Callable, Dict, Optional

from torch import nn
from torch.optim import Optimizer
from torch.utils.data import Dataset, Sampler

from dnn_cool_train_loop.eval_loop import eval_for_one_epoch
from dnn_cool_train_loop.train_loop import train_for_one_epoch


def train_for_epochs(
        n_epochs: int,
        model: nn.Module,
        train_dataset: Dataset,
        val_dataset: Dataset,
        criterion_dict: Dict[str, Callable],
        batch_size_effective: int,
        metrics_dir: Optional[Union[str, Path]] = None,
        metrics_dict: Dict[str, Dict[str, Callable]] = None,
        optimizer: Optional[Optimizer] = None,
        lr: Optional[float] = 1e-4,
        sampler: Optional[Sampler] = None,
        n_flush_metrics: int = 1_000,
):
    n_str_epoch = len(str(n_epochs))
    for i in range(n_epochs):
        epoch = str(i).zfill(n_str_epoch)
        train_metrics_dir = None
        if metrics_dir is not None:
            train_metrics_dir = metrics_dir / 'train' / epoch
            train_metrics_dir.mkdir(exist_ok=True, parents=True)
        print(f'Train epoch {epoch} ...')
        train_for_one_epoch(
            model=model,
            dataset=train_dataset,
            criterion_dict=criterion_dict,
            batch_size_effective=batch_size_effective,
            metrics_dir=train_metrics_dir,
            metrics_dict=metrics_dict,
            optimizer=optimizer,
            lr=lr,
            sampler=sampler,
            n_flush_metrics=n_flush_metrics
        )
        print(f'Valid epoch {epoch} ...')
        val_metrics_dir = None
        if metrics_dir is not None:
            val_metrics_dir = metrics_dir / 'val' / epoch
            val_metrics_dir.mkdir(exist_ok=True, parents=True)
        eval_for_one_epoch(
            model=model,
            dataset=val_dataset,
            criterion_dict=criterion_dict,
            batch_size_effective=batch_size_effective,
            metrics_dir=val_metrics_dir,
            metrics_dict=metrics_dict,
            n_flush_metrics=n_flush_metrics
        )
