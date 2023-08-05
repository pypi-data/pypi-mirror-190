# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyntegrant']

package_data = \
{'': ['*']}

install_requires = \
['icontract>=2.6.0,<3.0.0',
 'networkx>=2.6,<3.0',
 'pyrsistent>=0.18.0,<0.19.0',
 'toolz>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'pyntegrant',
    'version': '0.2.0',
    'description': 'A system assembly framework based on Integrant',
    'long_description': "==========\nPyntegrant\n==========\n\nWhile IoC and dependency injection aren't as much of a thing in Python\nas they are in many compiled languages, that doesn't mean they don't\nhave their place in decomposition of a complex architecture and\nassembly of systems; there's something very nice about completely\nseparated modules that communicate based on shared abstractions which\nare then assembled by a separate piece of code into running systems.\n\nBut despite the many microframeworks for dependency injection that\nI've seen for Python, I haven't seen any that seem as elegant as the\n`Integrant <https://github.com/weavejester/integrant>`_ microframework\nenjoyed by Clojurists.  This is an effort to remedy that, but as I\nhaven't loads of time to invest in it, it's a pale shadow of the\noriginal.\n\nStill, shadows have power.  It can already do the initialization portion\nof a system, although items like prep, halt, suspend, etc remain,\nas do derived keys and refsets.  But one thing at a time.\n\nAs of the 0.1.0 prerelease, all that works is the basic assembly of a\nsystem from a configuration (in Python, JSON, or TOML) and it's\nsurprising how effective that actually can be.  Unfortunately error\nmessages are lightly cryptic and documentation is nonexistent, but\nmore will be coming shortly.\n",
    'author': 'Vic Putz',
    'author_email': 'vbputz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vputz/pyntegrant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
