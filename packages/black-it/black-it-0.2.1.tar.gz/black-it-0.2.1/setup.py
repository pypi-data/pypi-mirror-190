# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['black_it',
 'black_it.loss_functions',
 'black_it.plot',
 'black_it.samplers',
 'black_it.utils']

package_data = \
{'': ['*']}

install_requires = \
['GPy>=1.10.0,<2.0.0',
 'ipywidgets>=7.7.0,<8.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.23.3,<1.24.0',
 'pandas>=1.4.2,<2.0.0',
 'scikit-learn>=1.1.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'statsmodels>=0.13.2,<0.14.0',
 'tables>=3.7.0,<4.0.0',
 'xgboost>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'black-it',
    'version': '0.2.1',
    'description': 'black-it: Black-box abm calibration kit',
    'long_description': '\n<p align="center">\n<img src="https://raw.githubusercontent.com/bancaditalia/black-it/main/docs/logo/logo_1024.png" width="500">\n<sup><a href="#footnote-1">*</a></sup>\n</p>\n\n<a href="https://pypi.org/project/black-it">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/black-it" />\n</a>\n\n<a href="https://github.com/bancaditalia/black-it/blob/main/LICENSE">\n    <img alt="GitHub" src="https://img.shields.io/github/license/bancaditalia/black-it">\n</a>\n\n<a style="border-width:0" href="https://doi.org/10.21105/joss.04622">\n  <img src="https://joss.theoj.org/papers/10.21105/joss.04622/status.svg" alt="DOI badge" >\n</a>\n\n<a href="https://codecov.io/gh/bancaditalia/black-it">\n  <img src="https://codecov.io/gh/bancaditalia/black-it/branch/main/graph/badge.svg" />\n</a>\n\n# Black-box abm calibration kit\n\nBlack-it is an easy-to-use toolbox designed to help you calibrate the parameters\nin your agent-based models and simulations (ABMs), using state-of-the-art\ntechniques to sample the parameter search space, with no need to reinvent the\nwheel.\n\nModels from economics, epidemiology, biology, logistics, and more can be dealt\nwith. The software can be used as-is - if your main interest is the ABM model\nitself. However, in case your research thing is to, e.g., devise new sampling\nstrategies for ginormous search spaces and highly non-linear model, then you can\ndeploy and test your new ideas on a solid, reusable, modular foundation, in a\nmatter of days, with no need to reimplement all the plumbings from scratch.\n\n## Installation\n\nThis project requires Python v3.8 or later.\n\nTo install the latest version of the package from [PyPI](https://pypi.org/project/black-it/):\n```\npip install black-it\n```\n\nOr, directly from GitHub:\n\n```\npip install git+https://github.com/bancaditalia/black-it.git#egg=black-it\n```\n\nIf you\'d like to contribute to the package, please read the [CONTRIBUTING.md](./CONTRIBUTING.md) guide.\n\n## Quick Example\n\nThe GitHub repo of Black-it contains a series ready-to-run calibration examples.\n\nTo experiment with them, simply clone the repo and enter the `examples` folder\n\n```\ngit clone https://github.com/bancaditalia/black-it.git\ncd black-it/examples\n```\n\nYou\'ll find several scripts and notebooks. The following is the script named `main.py`, note that copying and pasting \nthe lines below will not work in general as the script needs to be inside the "examples" folder in order to run correctly. \n\n```python\nimport models.simple_models as md\n\nfrom black_it.calibrator import Calibrator\nfrom black_it.loss_functions.msm import MethodOfMomentsLoss\nfrom black_it.samplers.best_batch import BestBatchSampler\nfrom black_it.samplers.halton import HaltonSampler\nfrom black_it.samplers.random_forest import RandomForestSampler\n\ntrue_params = [0.20, 0.20, 0.75]\nbounds = [\n    [0.10, 0.10, 0.10],  # LOWER bounds\n    [1.00, 1.00, 1.00],  # UPPER bounds\n]\nbounds_step = [0.01, 0.01, 0.01]  # Step size in range between bounds\n\nbatch_size = 8\nhalton_sampler = HaltonSampler(batch_size=batch_size)\nrandom_forest_sampler = RandomForestSampler(batch_size=batch_size)\nbest_batch_sampler = BestBatchSampler(batch_size=batch_size)\n\n# define a model to be calibrated\nmodel = md.MarkovC_KP\n\n# generate a synthetic dataset to test the calibrator\nN = 2000\nseed = 1\nreal_data = model(true_params, N, seed)\n\n# define a loss\nloss = MethodOfMomentsLoss()\n\n# define the calibration seed\ncalibration_seed = 1\n\n# initialize a Calibrator object\ncal = Calibrator(\n    samplers=[halton_sampler, random_forest_sampler, best_batch_sampler],\n    real_data=real_data,\n    model=model,\n    parameters_bounds=bounds,\n    parameters_precision=bounds_step,\n    ensemble_size=3,\n    loss_function=loss,\n    random_state=calibration_seed,\n)\n\n# calibrate the model\nparams, losses = cal.calibrate(n_batches=5)\n\nprint(f"True parameters:       {true_params}")\nprint(f"Best parameters found: {params[0]}")\n```\n\nWhen the calibration terminates (~half a minute), towards the end  of the output\nyou should see the following messages:\n```\nTrue parameters:       [0.2, 0.2, 0.75]\nBest parameters found: [0.19 0.19 0.74]\n```\n\n## Docs\n\nBlack-it calibration is initiated via the [Calibrator](https://bancaditalia.github.io/black-it/calibrator/) which,\nwhen called, performs three main steps.\n\nFirst, a [Sampler](https://bancaditalia.github.io/black-it/samplers/) is summoned to suggest a set of promising \nparameter configurations to explore.\n\nSecond, the [model](https://bancaditalia.github.io/black-it/simulator_interface/) to be calibrated is simulated for \nall the selected parameters.\n\nThird, a specific [loss function](https://bancaditalia.github.io/black-it/losses/), measuring the goodness of fitness \nof the simulation data with respect to the real data, is evaluated.\n\nThese steps are performed in a loop, and this allows the samplers to progress towards better parameter values \nby exploiting the knowledge of previously computed loss functions.\n\nA more detailed explanation of how Black-it works is available \n[here](https://bancaditalia.github.io/black-it/description/), while the full documentation -complete with examples \nand tutorials- is available [here](https://bancaditalia.github.io/black-it/). \n\n## Citing *Black-it*\n\nA description of the package is available [here](https://joss.theoj.org/papers/10.21105/joss.04622).\n\nPlease consider citing it if you found this package useful for your research\n\n```bib\n@article{black_it, \n  title = {Black-it: A Ready-to-Use and Easy-to-Extend Calibration Kit for Agent-based Models}, \n  journal = {Journal of Open Source Software},\n  publisher = {The Open Journal}, \n  year = {2022}, \n  volume = {7}, \n  number = {79}, \n  pages = {4622}, \n  doi = {10.21105/joss.04622}, \n  url = {https://doi.org/10.21105/joss.04622}, \n  author = {Marco Benedetti and \n            Gennaro Catapano and \n            Francesco {De Sclavis} and \n            Marco Favorito and \n            Aldo Glielmo and \n            Davide Magnanimi and \n            Antonio Muci} \n}\n```\n\n## Disclaimer\n\nThis package is an outcome of a research project. All errors are those of the authors. All views expressed are personal views, not those of Bank of Italy.\n\n---\n\n<p id="footnote-1">\n* Credits to <a href="https://www.bankit.art/people/sara-corbo">Sara Corbo</a> for the logo.\n</p>\n',
    'author': 'Applied Research Team',
    'author_email': 'appliedresearchteam@bancaditalia.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bancaditalia/black-it',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
