# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cleanml']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3']

setup_kwargs = {
    'name': 'cleanml',
    'version': '0.2.0',
    'description': 'A package for cleaning and preparing data for ML models',
    'long_description': '# cleanml\n\nA python package for cleaning and preparing data for downstream analysis or ML modeling.\n\n## Installation\n\n```bash\n$ pip install cleanml\n```\n\n## Usage\n`cleanml` can be used to clean and prepare data.\n\n```python\nfrom cleanml.cleanml import make_column_names\nimport pandas as pd\n\nfile_path = "data"  # path to your file\ndata = pd.read_csv(file_path)\ndata = make_column_names(data)\ncolumn_names = data.columns.to_list()\nprint(column_names)\n```\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cleanml` was created by Thulasiram Gunipati. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cleanml` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Thulasiram Gunipati',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
