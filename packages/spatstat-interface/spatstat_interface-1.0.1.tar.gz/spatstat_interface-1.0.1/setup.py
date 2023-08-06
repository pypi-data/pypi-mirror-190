# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spatstat_interface']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0', 'rpy2>=3.4.5,<4.0.0']

extras_require = \
{'notebook': ['jupyter>=1.0.0,<2.0.0',
              'numpy>=1.20.3,<2.0.0',
              'matplotlib>=3.5.2,<4.0.0']}

setup_kwargs = {
    'name': 'spatstat-interface',
    'version': '1.0.1',
    'description': 'Simple Python interface with the spatstat R package using rpy2',
    'long_description': '# spatstat-interface\n\n[![Build](https://github.com/For-a-few-DPPs-more/spatstat-interface/actions/workflows/main.yml/badge.svg)](https://github.com/For-a-few-DPPs-more/spatstat-interface/actions/workflows/main.yml)\n[![PyPi version](https://badgen.net/pypi/v/spatstat-interface/)](https://pypi.org/project/spatstat-interface/)\n[![codecov](https://codecov.io/gh/For-a-few-DPPs-more/spatstat-interface/branch/main/graph/badge.svg?token=BHTI6L66P2)](https://codecov.io/gh/For-a-few-DPPs-more/spatstat-interface)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n- [spatstat-interface](#spatstat-interface)\n  - [Dependencies](#dependencies)\n  - [Installation](#installation)\n    - [Install the project as a dependency](#install-the-project-as-a-dependency)\n    - [Install in editable mode and potentially contribute to the project](#install-in-editable-mode-and-potentially-contribute-to-the-project)\n      - [Editable install with `poetry`](#editable-install-with-poetry)\n      - [Editable install with `pip`](#editable-install-with-pip)\n  - [Documentation](#documentation)\n    - [Main resources](#main-resources)\n    - [Notes about `spatstat`](#notes-about-spatstat)\n    - [Calling functions](#calling-functions)\n      - [Calling function.variant](#calling-functionvariant)\n      - [Keyword arguments](#keyword-arguments)\n\nSimple Python interface with the spatial statistics [R](https://www.r-project.org/) package [`spatstat`](https://github.com/spatstat/spatstat) using [`rpy2`](https://github.com/rpy2/rpy2).\n\n## Dependencies\n\n- [R](https://www.r-project.org/) (programming language)\n  - [`spatstat`](https://github.com/spatstat/spatstat) package, which [has recently been split into multiple sub-packages and extensions](https://github.com/spatstat/spatstat#spatstat-has-been-split-into-a-family-of-packages). **Warning: potential new splits may break your code!**\n- Python >= 3.7, with dependencies listed in the [`pyproject.toml`](./pyproject.toml) file. Note that they mostly correspond to the latest version.\n  - non-optional dependencies are [`pandas`](https://pandas.pydata.org/) and [`rpy2`](https://rpy2.github.io/).\n\n## Installation\n\nYou may consider using `poetry` to manage your whole project as described here <https://github.com/guilgautier/template-python-project>.\n\n### Install the project as a dependency\n\n- Install the latest version published on [![PyPi version](https://badgen.net/pypi/v/spatstat-interface/)](https://pypi.org/project/spatstat-interface/)\n\n  ```bash\n  # activate your virtual environment an run\n  poetry add spatstat-interface\n  # pip install spatstat-interface\n  ```\n\n- Install from source (this may be broken)\n\n  ```bash\n  # activate your virtual environment an run\n  poetry add git+https://github.com/For-a-few-DPPs-more/spatstat-interface.git\n  # pip install git+https://github.com/For-a-few-DPPs-more/spatstat-interface.git\n  ```\n\n### Install in editable mode and potentially contribute to the project\n\nYou may consider [forking the repository](https://github.com/For-a-few-DPPs-more/spatstat-interface/fork).\n\nIn any case, your can clone the repository\n\n- if you have forked the repository\n\n  ```bash\n  git clone https://github.com/your_user_name/spatstat-interface.git\n  ```\n\n- if you have **not** forked the repository\n\n  ```bash\n  git clone https://github.com/For-a-few-DPPs-more/spatstat-interface.git\n  ```\n\n#### Editable install with `poetry`\n\nThe package can be installed in **editable** mode along with\n\n- main (non-optional) dependencies, see `[tool.poetry.dependencies]` in [`pyproject.toml`](./pyproject.toml)\n- development dependencies, `[tool.poetry.group.dev.dependencies]` in [`pyproject.toml`](./pyproject.toml)\n\n```bash\ncd spatstat-interface\n# poetry shell  # to create/activate local .venv (see poetry.toml)\npoetry install\n# poetry install --with dev\n# poetry install --with dev --extras "notebook"\n```\n\n#### Editable install with `pip`\n\nConsider using [`pip>=21.3.1`](https://pip.pypa.io/en/stable/news/#v21-3-1), when installing packages defined by a `pyproject.toml` file.\n\n```bash\ncd spatstat-interface\n# activate your virtual environment and run\npip install --editable .\n# pip install --editable ".[notebook]" to install notebook dependencies\n```\n\nSee also the [`pip install`](https://pip.pypa.io/en/stable/cli/pip_install/) optional commands.\n\n## Documentation\n\n### Main resources\n\n- [`notebooks`](./notebooks) showcase detailed examples\n- [`rpy2` documentation](https://rpy2.github.io/doc.html)\n- [`spatstat` documentation](https://rdocumentation.org/search?q=spatstat)\n\n### Notes about `spatstat`\n\nThe [`spatstat`](https://github.com/spatstat/spatstat) package [has recently been split into multiple sub-packages and extensions](https://github.com/spatstat/spatstat#spatstat-has-been-split-into-a-family-of-packages).\n**Warning: potential new splits may break your code!**\n\nUsing `spatstat-interface`, sub-packages and extensions are accessible in the following way\n\n```python\nfrom spatstat_interface.interface import SpatstatInterface\n\nspatstat = SpatstatInterface()\n# spatstat.spatstat is None\n# spatstat.model is None\n# spatstat.explore is None\n# spatstat.geom is None\n\n# load/import sub-packages or extensions\nspatstat.import_package("model", "explore", "geom", update=True)\nspatstat.model\nspatstat.explore\nspatstat.geom\n```\n\n### Calling functions\n\n#### Calling function.variant\n\nTo call the R `function.variant`\n\n```R\n# R code pcf.ppp\nspatstat.explore::pcf.ppp(X)\n```\n\nReplace `.` by `_` to call `function_variant` in Python\n\n```Python\n# Python code pcf_ppp\nspatstat.explore.pcf_ppp(X)\n```\n\n#### Keyword arguments\n\nConsider using Python dictionaries to pass keyword arguments.\nBelow are a few examples.\n\n- dot keywords, for example passing `var.approx` keyword argument won\'t work in Python\n\n  ```R\n  # R code\n  spatstat.explore::pcf.ppp(X, kernel="epanechnikov", var.approx=False)\n  ```\n\n  ```Python\n  # Python code\n  params = {"kernel": "epanechnikov", "var.approx": False}\n  spatstat.explore.pcf_ppp(X, **params)\n  ```\n\n- reserved keywords, for example `lambda` is a reserved Python keyword; it can\'t be used as a keyword argument\n\n  ```R\n  # R code\n  spatstat.model::dppGauss(lambda=rho, alpha=alpha, d=d)\n  ```\n\n  ```Python\n  # Python code\n  params = {"lambda": rho, "alpha": alpha, "d": d}\n  spatstat.model.dppGauss(**params)\n  ```\n',
    'author': 'Guillaume Gautier',
    'author_email': 'guillaume.gga@gmail.com',
    'maintainer': 'Guillaume Gautier',
    'maintainer_email': 'guillaume.gga@gmail.com',
    'url': 'https://github.com/For-a-few-DPPs-more/spatstat-interface',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
