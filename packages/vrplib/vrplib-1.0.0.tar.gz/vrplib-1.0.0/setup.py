# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vrplib',
 'vrplib.download',
 'vrplib.parse',
 'vrplib.parse.distances',
 'vrplib.read']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'vrplib',
    'version': '1.0.0',
    'description': 'Python library for reading vehicle routing problem instances.',
    'long_description': '# VRPLIB\n[![PyPI version](https://badge.fury.io/py/vrplib.svg)](https://badge.fury.io/py/vrplib)\n[![vrplib](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml/badge.svg)](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml)\n[![codecov](https://codecov.io/gh/leonlan/VRPLIB/branch/master/graph/badge.svg?token=X0X66LBNZ7)](https://codecov.io/gh/leonlan/VRPLIB)\n\n`vrplib` is a Python package for reading Vehicle Routing Problem (VRP) instances. The main features are:\n- reading VRPLIB and Solomon instances and solutions, and\n- downloading instances and best known solutions from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).\n\n# Installation\nThis library works with Python 3.8+ and only depends on `numpy`. Install the latest version of `vrplib`:\n\n```shell\npip install vrplib\n```\n\n# Example usage\n## Reading instances and solutions\n```python\nimport vrplib\n\n# Read VRPLIB formatted instances (default)\ninstance = vrplib.read_instance("/path/to/X-n101-k25.vrp")\nsolution = vrplib.read_solution("/path/to/X-n101-k25.sol")\n\n# Read Solomon formatted instances\ninstance = vrplib.read_instance("/path/to/C101.txt", instance_format="solomon")\nsolution = vrplib.read_solution("/path/to/C101.sol") # only 1 solution format\n```\n\n`instance` and `solution` are dictionaries that contain all parsed data. \n``` python\ninstance.keys()\n# dict_keys([\'name\', \'comment\', \'type\', \'dimension\', ..., \'edge_weight\'])\n\nsolutions.keys()\n# dict_keys([\'routes\', \'cost\'])\n```\n\n\n## Downloading instances from CVRPLIB \n``` python\nimport vrplib\n\ninstance = vrplib.download_instance("X-n101-k25.vrp")\nsolution = vrplib.download_solution("X-n101-k25.sol")\n\n# List instance names that can be downloaded \nvrplib.list_names()                      # All instance names\nvrplib.list_names(low=100, high=200)     # Instances with between [100, 200] customers\nvrplib.list_names(vrp_type=\'cvrp\')       # Only CVRP instances\nvrplib.list_names(vrp_type=\'vrptw\')      # Only VRPTW instances\n```\n\n\n# Notes\nThis section contains additional notes about the `vrplib` package.\n\n## Instance formats\nCurrently, two VRP instance formats are supported:\n- **VRPLIB**: this format is most commonly used for Capacitated Vehicle Routing Problem (CVRP) instances.  See the [X-n101-k25](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/X/X-n101-k25.vrp) instance for an example. VRPLIB is an extension of the [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) format. Additional information about the VRPLIB format can be found [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf). \n- **Solomon**: this format was used to introduce the Solomon instances for the Vehicle Routing Problem with Time Window (VRPTW) and also the extended instance set by Homberger and Gehring. See the [C101](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/Solomon/C101.txt) instance for an example.\n\n## How instances are parsed\n`vrplib` parses an instance and returns a dictionary of keyword-value pairs. There are two types of instance data: \n- Problem specifications, which may contain metadata or problem-specific information such as the max number of vehicles. \n- Problem data, which are often arrays of values describing, for example, customer service times and time windows. \n\n### On parsing distances \nThe `vrplib` library tries to follow the instance specifications as strictly as possible to compute the distances. \n\nFor VRPLIB instances, the distances computation is determined by the `EDGE_WEIGHT_TYPE` and possibly the `EDGE_WEIGHT_FORMAT` specifications. We currently support two categories of edge weight types:\n- `*_2D`: compute the Euclidean distances using the node coordinate data.\n    - `EUC_2D`: Double precision distances without rounding.\n    - `FLOOR_2D`: Round down all distances to down to an integer.\n    - `EXACT_2D`: Multiply the distances by 1000, round to the nearest integer.\n- `EXPLICIT`: the distance data is explicitly provided, in partial or full form. For explicit matrices, the `EDGE_WEIGHT_FORMAT` must be specified. We support the following two formats:\n  - `LOWER_ROW`: Lower row triangular matrix without diagonal entries.  \n  - `FULL_MATRIX`: Explicit full matrix representation.\n  \nMore information about how VRPLIB specifications can be found [here](  http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) and [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf).\n\nNote that there are VRPLIB instances that use different rounding conventions in the literature, which may not be specified in the instance. For example, the X instance set proposed by [Uchoa et al. (2017)](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/new-instances) assumes that the distances are rounded to the nearest integer. When you use the `vrplib` package to read instances from the X set, it will return unrounded Euclidean distances because the instance specifies the `EUC_2D` edge weight type, i.e., no rouding. This can be easily solved by rounding the distances matrix manually.\n\nFor Solomon-type instances, the distance computation is not specified in the instance file, hence we compute the Euclidean distances without rounding. A recent convention that was proposed during the [2021 DIMACS Vehicle Routing Implementation Challenge](http://dimacs.rutgers.edu/programs/challenge/vrp/vrptw/) is to truncate the Euclidean distances to one decimal. Similar to the X instance set, you can manually modify the distances matrix.\n\n## Additional remarks\n- Downloading instances may take up to a few seconds. \n- The `XML100` benchmark set is not listed in `list_names` and cannot be downloaded through this package. You can download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).\n\n    \n',
    'author': 'Leon Lan',
    'author_email': 'leon.lanyidong@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/leonlan/VRPLIB',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
