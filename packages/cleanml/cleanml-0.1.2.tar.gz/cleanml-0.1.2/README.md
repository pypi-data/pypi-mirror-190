# cleanml

A python package for cleaning and preparing data for downstream analysis or ML modeling.

## Installation

```bash
$ pip install cleanml
```

## Usage
`cleanml` can be used to clean and prepare data.

```python
from cleanml.cleanml import make_column_names
import pandas as pd

file_path = "data"  # path to your file
data = pd.read_csv(file_path)
data = make_column_names(data)
column_names = data.columns.to_list()
print(column_names)
```
## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`cleanml` was created by Thulasiram Gunipati. It is licensed under the terms of the MIT license.

## Credits

`cleanml` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
