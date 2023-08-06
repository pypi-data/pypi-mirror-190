# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nospace']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['nospace = nospace.nospace:main']}

setup_kwargs = {
    'name': 'nospace',
    'version': '0.1.1',
    'description': 'recursively rename files and folders to remove spaces and format with optional flags',
    'long_description': "# NoSpace\n##### Video Demo: https://www.youtube.com/watch?v=j8HY4FUUE9w\n---\n##### Description:\nDo you use the command line a lot? Are you tired of spaces and/or capitalization \nin your files that you have to waste precious keystrokes to put quotes around or\nhold the shift key?\nNoSpace might be for you!\n\nI built this script as my final project for Harvard's CS50P, Introduction to \nProgramming With Python.\n\n---\n### Installation\n---\n---\n```py\npip install nospace\n```\n\n---\n### Usage\n---\n_example usage_\n```py\nnospace -p test_directory -c lower -d 1 -o files -s -\n```\n\n```py\nusage: nospace [-h] [-d DEPTH] [-c {lower,title,upper}] [-o {both,files,folders}] [-s SEPERATOR] [-p PATH]\n\nrename files in bulk to remove spaces\n\noptions:\n  -h, --help            show this help message and exit\n  -d DEPTH, --depth DEPTH\n                        maximum depth of folders to traverse\n  -c {lower,title,upper}, --case {lower,title,upper}\n                        case of the renamed files and folders (lower, title, or upper)\n  -o {both,files,folders}, --objects {both,files,folders}\n                        objects to process (files, folders, or both)\n  -s SEPERATOR, --seperator SEPERATOR\n                        separator to replace spaces with (default is _)\n  -p PATH, --path PATH  optional file path to start with\n```\n---\n##### LICENSE\n\n---\nThis repo is licensed under the permissive MIT license.  You can do whatever you want with it.\n",
    'author': 'yenaras',
    'author_email': 'brandon82890@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yenaras/nospace',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
