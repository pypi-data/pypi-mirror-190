from __future__ import annotations

import pickle, numpy as np
from typing import Any, Dict, Optional, Union, Callable
import orjson
from torch.utils.data import Dataset
from pathlib import Path
from ream.dataset_helper import DatasetDict


class MyDataset(Dataset):
    """A columnar dataset"""

    def __init__(
        self,
        examples: Union[dict, list],
        dtypes: Optional[Dict[str, Any]] = None,
        collate_fn: Union[Callable, None] = None,
    ):
        self.is_dict = isinstance(examples, dict)
        self.collate_fn = collate_fn

        if self.is_dict:
            self.examples = examples.copy()
            self.size = len(next(iter(self.examples.values())))

            if dtypes is not None:
                for name, feat in self.examples.items():
                    if name in dtypes and isinstance(feat, np.ndarray):
                        self.examples[name] = feat.astype(dtypes[name])
                        dtypes.pop(name)
        else:
            self.examples = examples
            self.size = len(self.examples)

        self.dtypes = dtypes

    def __len__(self):
        return self.size

    @property
    def shape(self):
        return self.size

    def __getitem__(self, idx: int):
        if self.is_dict:
            out = {name: feat[idx] for name, feat in self.examples.items()}
        else:
            out = self.examples[idx]

        if self.dtypes is not None:
            for name, dtype in self.dtypes.items():
                out[name] = out[name].astype(dtype)
        return out

    @staticmethod
    def load_from_disk(path: Path):
        with open(str(path), "rb") as f:
            return pickle.load(f)

    def save_to_disk(self, path: Path):
        with open(str(path), "wb") as f:
            pickle.dump(self, f)


class MyDatasetDict(DatasetDict[MyDataset]):
    serde = (MyDataset.save_to_disk, MyDataset.load_from_disk, "pkl")

    @property
    def shape(self):
        return {subset: dataset.shape for subset, dataset in self.items()}
