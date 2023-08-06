# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panama', 'panama.fluxes']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'corsikaio>=0.2.6.post1,<0.3.0',
 'crflux>=1.0.6,<2.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'particle>=0.21.0,<0.22.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['panama = panama.parallel_run:cli']}

setup_kwargs = {
    'name': 'corsika-panama',
    'version': '0.1.0',
    'description': 'PArallel ruN of corsikA on MAny cores and other python utils to work with CORSIKA',
    'long_description': "PANAMA\n===\n**PAN**das **A**nd **M**ulticore utils for corsik**A**7\n\nThanks [@Jean1995](https://github.com/Jean1995) for the silly naming idea.\n\n# What this is\n\n## CORSIKA7 parallelization\nThis started a little while ago while I was looking into the `EHIST` option\nof corsika.\nI wanted a way of conveniently running CORSIKA7 on more than 1 core.\nI ended in the same place where most CORSIKA7 users end (see e.g. [fact-project/corsika_wrapper](https://github.com/fact-project/corsika_wrapper))\nand wrote a small wrapper. Once this package is installed, you can use it with the `panama` command (see `panama --help` for options).\n\nThis wrapper has a nice progress bar, so you get an estimate for how long your simulation needs.\n\n### Pitfalls\n- The whole `run` folder of CORSIKA7 must be copied for each proccess, so very high parallel runs have high overhead\n- If you simulate to low energies, python can't seem to hold up with the corsika output to `stdin` and essentially slows down corsika this is still a bug in investigation #1\n\n## CORSIKA7 DAT files to pandas dataframe with working EHIST\nMade possible by [cta-observatory/pycorsikaio](https://github.com/cta-observatory/pycorsikaio).\n\n# What this is not\nBug-free or stable\n\n# Installation\nTo install this module, clone it\n```\ngit clone git@github.com:The-Ludwig/PANAMA.git\n```\nand run\n```\npip install ./PANAMA\n```\n\nA future PyPi release is planned.\n",
    'author': 'Ludwig Neste',
    'author_email': 'ludwig.neste@tu-dortmund.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/The-Ludwig/PANAMA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
