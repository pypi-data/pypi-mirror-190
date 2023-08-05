# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai2_kit', 'ai2_kit.core', 'ai2_kit.domain', 'ai2_kit.workflow']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0,<3.0.0',
 'cp2k-input-tools>=0.8.2,<0.9.0',
 'dpdata>=0.2.13,<0.3.0',
 'fabric>=2.7.1,<3.0.0',
 'fire>=0.4.0,<0.5.0',
 'invoke>=1.7.3,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'shortuuid>=1.0.11,<2.0.0']

entry_points = \
{'console_scripts': ['ai2-kit = ai2_kit.main:main']}

setup_kwargs = {
    'name': 'ai2-kit',
    'version': '0.1.0',
    'description': '',
    'long_description': '# ai<sup>2</sup>-kit\n\nA toolkit featured ***a**rtificial **i**ntelligence × **a**b **i**nitio* for computational chemistry research.\n\n*Please be advised that `ai2-kit` is still under heavy development and you should expect things to change often. We encourage people to play and explore with `ai2-kit`, and stay tuned with us for more features to come.*\n\n\n## Feature Highlights\n* A general purpose automated workflow that implements Closed-Loop Learning (CLL) pattern to train Machine Learning Potential (MLP) models.\n* Featured tools for Electrochemistry research:\n    * Automated FEP workflows to train MLP models and calculate redox potential, pKa, solvation, etc.\n* Utilities to execute and manage jobs in local or remote HPC job scheduler.\n* Utilities to simplified automated workflows development with reusable components. \n\n## Installation\n```bash\n# It requires Python >= 3.8\npip install ai2-kit  \n```\n\n## Use Cases\n\n### Train MLP model with CLL workflow\n\n```bash\nai2-kit cll-mlp train-mlp \n```\n\nCCL-MLP workflow implements the Closed-Loop Learning pattern to train MLP models automatically. For each iteration, the workflow will train MLP models and use them to generate new training data for the next round, until the quality of MLP models meets preset criteria. Configurations of each iteration can be updated dynamically to further improve training efficiency.\n\n![cll-mlp-diagram](./doc/img/cll-mlp-diagram.svg)\n\n### Train MLP models for FEP simulation\n\n```bash\nai2-kit ec fep train-mlp\n```\n\n`ec fep` is a dedicated workflow to train MLP models for FEP simulation. Unlike the general purpose `cll-mlp` workflow, `ec fep` workflow uses two different configurations to generate two different labeled structures to train MLP models respectively. And then use the two different models to run FEP simulation.\n\n#### Citation\nIf you use `ec fep` workflow in your research, please cite it:\n> Feng Wang and Jun Cheng, Automated Workflow for Computation of Redox Potentials, Acidity Constants and Solvation Free Energies Accelerated by Machine Learning. J. Chem. Phys, 2022. 157(2), 024103. DOI: https://doi.org/10.1063/5.0098330\n\n\n## TODO\n* Finalize configurations format and provide documents.\n* Provide tools for data format transformation.\n* Provide tools to run MD simulation and properties calculations.\n',
    'author': 'weihong.xu',
    'author_email': 'xuweihong.cn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
