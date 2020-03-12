# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['maybe_unsqueeze', 'show_array', 'TSeries', 'get_ucr', 'load_df_ucr']

# Cell
from fastcore.test import *
from .imports import *

# Cell
import pandas as pd
from fastcore.all import *
from scipy.io import arff

# Cell
def maybe_unsqueeze(x):
    "Add empty dimension if it is a rank 1 tensor/array"
    if isinstance(x, np.ndarray): return x[None,:] if len(x.shape)==1 else x
    if isinstance(x, Tensor): return x.unsqueeze(0) if len(x.shape)==1 else x
    else: return None

# Cell
def show_array(array, ax=None, figsize=None, title=None, ctx=None, tx=None, **kwargs):
    "Show an array on `ax`."
    # Handle pytorch axis order
    if hasattrs(array, ('data','cpu','permute')):
        array = array.data.cpu()
    elif not isinstance(array,np.ndarray):
        array=array(array)
    arrays = maybe_unsqueeze(array)
    ax = ifnone(ax,ctx)
    if figsize is None: figsize = (5,5)
    if ax is None: _,ax = plt.subplots(figsize=figsize)
    tx = ifnone(tx,np.arange(arrays[0].shape[0]))
    label = kwargs.pop('label', 'x')
    for a, c in zip(arrays, ['b', 'c', 'm', 'y', 'k',]):
        ax.plot(tx, a, '-'+c,label=label, **kwargs)
    if title is not None: ax.set_title(title)
    ax.legend()
    return ax

# Cell
class TSeries(TensorBase):
    "Basic Timeseries wrapper"
    @classmethod
    def create(cls, x):
        return cls(maybe_unsqueeze(as_tensor(x)))

    @property
    def channels(self): return self.shape[0]

    @property
    def len(self): return self.shape[-1]

    def __repr__(self):
        return f'TSeries(ch={self.channels}, len={self.len})'

    def show(self, ctx=None, **kwargs):
        return show_array(self, ctx=ctx, **kwargs)

# Cell
URLs.UCR = 'http://www.timeseriesclassification.com/Downloads/Archives/Univariate2018_arff.zip'

# Cell
@delegates(untar_data)
def get_ucr(**kwargs):
    "zipped file has different name as .zip"
    ucr_path = untar_data(URLs.UCR, **kwargs)
    if not ucr_path.exists():
        zf = zipfile.ZipFile(URLs.path(URLs.UCR))
        actual_folder = ucr_path.parent/zf.namelist()[0]
        actual_folder.rename(ucr_path)
        print(f'Renaming {actual_folder} to {ucr_path}')
    return ucr_path

# Cell
# "this functions are based on https://github.com/mb4310/Time-Series"
def load_df_ucr(path, task):
    "Loads arff files from UCR"
    try:
        print(f'Loading files from: {path}/{task}')
        dfs = []
        for file in ['TRAIN', 'TEST']:
            filename = f'{task}/{task}_{file}.arff'
            data = arff.loadarff(str(path/filename))
            dfs.append(pd.DataFrame(data[0]))
        return dfs
    except:
        print(f'Error loading files: {path}/{task}')