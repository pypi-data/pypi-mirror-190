# mpath: simple tool to get path information 
[![PyPI Latest Release](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.org/project/mpath/)

## What is it?
For now it's quit simple and `get_path_info()` method returns information about given path. It can be either a directory or a file path.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/MosesDastmard/mpath

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/mapth/)

```sh
# or PyPI
pip install mpath
```

## Example

```sh
# or PyPI
from mpath import get_path_info

path = "/home/user/data.csv"
path_info = get_path_info(path)
print(path)
```