# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_import_conventions']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0', 'flake8>=5']

entry_points = \
{'flake8.extension': ['IC = flake8_import_conventions:Plugin']}

setup_kwargs = {
    'name': 'flake8-import-conventions',
    'version': '0.1.0',
    'description': 'An opinionated plugin for Flake8 on how certain packages should be imported or aliased.',
    'long_description': '# flake8-import-conventions\n\n<p align="center">\n  <img alt="" src="https://raw.githubusercontent.com/joaopalmeiro/flake8-import-conventions/main/assets/logo_round.png" width="100" height="100" />\n</p>\n\n[![PyPI](https://img.shields.io/pypi/v/flake8-import-conventions.svg)](https://pypi.org/project/flake8-import-conventions/)\n\nAn opinionated plugin for Flake8 on how certain packages should be imported or aliased.\n\nIt is based on the [`pandas-vet`](https://github.com/deppen8/pandas-vet) and [`flake8-2020`](https://github.com/asottile/flake8-2020) plugins.\n\n## Installation\n\nVia [Pipenv](https://pipenv.pypa.io/):\n\n```bash\npipenv install --dev flake8 flake8-import-conventions\n```\n\n## Flake8 codes\n\n| Package                                     | Code  | Description                                                                    |\n| ------------------------------------------- | ----- | ------------------------------------------------------------------------------ |\n| [Altair](https://altair-viz.github.io/)     | IC001 | altair should be imported as `import altair as alt`                            |\n| [GeoPandas](https://geopandas.org/)         | IC002 | geopandas should be imported as `import geopandas`                             |\n| [Matplotlib](https://matplotlib.org/)       | IC003 | matplotlib.pyplot should be imported as `import matplotlib.pyplot as plt`      |\n| [NetworkX](https://networkx.org/)           | IC004 | networkx should be imported as `import networkx as nx`                         |\n| [NumPy](https://numpy.org/)                 | IC005 | numpy should be imported as `import numpy as np`                               |\n| [pandas](https://pandas.pydata.org/)        | IC006 | pandas should be imported as `import pandas as pd`                             |\n| [Plotly](https://plotly.com/python/)        | IC007 | plotly.express should be imported as `import plotly.express as px`             |\n| [Plotly](https://plotly.com/python/)        | IC008 | plotly.graph_objects should be imported as `import plotly.graph_objects as go` |\n| [seaborn](https://seaborn.pydata.org/)      | IC009 | seaborn should be imported as `import seaborn as sns`                          |\n| [statsmodels](https://www.statsmodels.org/) | IC010 | statsmodels.api should be imported as `import statsmodels.api as sm`           |\n\n## Development\n\n```bash\npoetry install --with dev\n```\n\n```bash\npoetry shell\n```\n\nOpen the `manual_test.py` file in VS Code to see the error messages.\n\n```bash\npytest tests/ -v\n```\n\nor (to see `print()`s)\n\n```bash\npytest tests/ -v -s\n```\n\nCopy the output of the following script and paste it in the [Flake8 codes](#flake8-codes) section:\n\n```bash\npython gen_table.py\n```\n\nIf changes are not reflected in VS Code after changing something in the package, close it and open it again.\n\n## Deployment\n\n```bash\npoetry check\n```\n\n```bash\npoetry version minor\n```\n\nor\n\n```bash\npoetry version patch\n```\n\nCommit the change in the `pyproject.toml` file.\n\n```bash\ngit tag\n```\n\n```bash\ngit tag "v$(poetry version --short)"\n```\n\n```bash\ngit push origin "v$(poetry version --short)"\n```\n\n## References\n\n- Anthony Sottile\'s "[a flake8 plugin from scratch (intermediate) anthony explains #025](https://youtu.be/ot5Z4KQPBL8)" tutorial.\n- [flake8-pie](https://github.com/sbdchd/flake8-pie).\n- [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide).\n',
    'author': 'João Palmeiro',
    'author_email': 'joaopalmeiro@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
