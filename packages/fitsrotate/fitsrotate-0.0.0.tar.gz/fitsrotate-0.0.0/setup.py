# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fitsrotate']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5,<6', 'dask>=2023,<2024', 'numpy>=1.24,<2.0']

entry_points = \
{'console_scripts': ['fitsrotate = fitsrotate:cli']}

setup_kwargs = {
    'name': 'fitsrotate',
    'version': '0.0.0',
    'description': 'Rotate a FITS file to put spectral axis first',
    'long_description': '# PyFITSRotate\n\n## Description\nA simple Python script to rotate FITS cube axes. It uses the [astropy](http://www.astropy.org/) package to read and write FITS files.\n\nThe default action is to rotate the spectral axis to be the first axis. This is useful for heavy IO operations on FITS cubes/\n\n## Installation\nFrom github:\n```\npip install git+git://github.com/alecthomson/pyfitsrotate.git\n```\nFrom PyPI:\n```\npip install pyfitsrotate\n```\n\n## Usage\n```\n❯ fitsrotate -h\nusage: fitsrotate [-h] [-o [OUTFILE]] [-e EXT] [-s SWAP_AX] filename\n\nRotate a FITS file to put spectral axis first.\n\npositional arguments:\n  filename              Input filename.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o [OUTFILE], --outfile [OUTFILE]\n                        Output filename. Defaults to input filename with .rot.fits extension.\n  -e EXT, --ext EXT     Extension number. Defaults to 0.\n  -s SWAP_AX, --swap-ax SWAP_AX\n                        Axis to swap with spectral axis (numpy convention). Defaults to -1.\n```\n',
    'author': 'Alec Thomson',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
