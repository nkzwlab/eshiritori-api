from typing import Optional, List
import urllib.request
from tqdm.auto import tqdm
from pathlib import Path
import requests
import math
import numpy as np
import torch

def get_quickdraw_class_names():
    url = "https://raw.githubusercontent.com/googlecreativelab/quickdraw-dataset/master/categories.txt"
    r = requests.get(url)
    classes = [x.replace(' ', '_') for x in r.text.splitlines()]
    return classes


def download_quickdraw_dataset(root="./data", limit: Optional[int] = None, class_names: List[str]=None):
    if class_names is None:
        class_names = get_quickdraw_class_names()

    root = Path(root)
    root.mkdir(exist_ok=True, parents=True)
    url = 'https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/'

    print("Downloading Quickdraw Dataset...")
    for class_name in tqdm(class_names[:limit]):
        fpath = root / f"{class_name}.npy"
        if not fpath.exists():
            urllib.request.urlretrieve(f"{url}{class_name.replace('_', '%20')}.npy", fpath)


def load_quickdraw_data(root="./data", max_items_per_class=5000):
    all_files = Path(root).glob('*.npy')

    x = np.empty([0, 784], dtype=np.uint8)
    y = np.empty([0], dtype=np.long)
    class_names = []

    print(f"Loading {max_items_per_class} examples for each class from the Quickdraw Dataset...")
    for idx, file in enumerate(tqdm(sorted(all_files))):
        data = np.load(file, mmap_mode='r+')
        data = data[0: max_items_per_class, :]
        labels = np.full(data.shape[0], idx)
        x = np.concatenate((x, data), axis=0)
        y = np.append(y, labels)

        class_names.append(file.stem)

    return x, y, class_names


class QuickDrawDataset(torch.utils.data.Dataset):
    def __init__(self, root, max_items_per_class=5000, class_limit=None, is_download=False):
        super().__init__()
        self.root = root
        self.max_items_per_class = max_items_per_class
        self.class_limit = class_limit
        
        if is_download: download_quickdraw_dataset(self.root, self.class_limit)
        self.X, self.Y, self.classes = load_quickdraw_data(self.root, self.max_items_per_class)

    def __getitem__(self, idx):
        x = (self.X[idx] / 255.).astype(np.float32).reshape(1, 28, 28) 
        y = self.Y[idx]

        # x = torch.from_numpy(x)
        # y = y.item()

        return torch.from_numpy(x), y.item()

    def __len__(self):
        return len(self.X)

    def split(self, pct=0.1):
        indices = torch.randperm(len(self)).tolist()
        n_val = math.floor(len(indices) * pct)
        train_ds = torch.utils.data.Subset(self, indices[:-n_val])
        val_ds = torch.utils.data.Subset(self, indices[-n_val:])
        return train_ds, val_ds

def get_loader(dataset, batch_size, shuffle, num_workers):
    return torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=collate_fn,
    )
    
def collate_fn(data):
    x = torch.stack([item[0] for item in data])
    y = torch.LongTensor([item[1] for item in data])
    return x, y

if __name__ == '__main__':
    data_dir = './data'
    max_examples_per_class = 20000
    train_val_split_pct = .1

    ds = QuickDrawDataset(data_dir, max_examples_per_class, is_download=True)
    num_classes = len(ds.classes)
    train_ds, val_ds = ds.split(train_val_split_pct)