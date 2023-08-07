# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['venture']

package_data = \
{'': ['*']}

install_requires = \
['arc-cli==8.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'ujson>=4.0.2,<5.0.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['venture = venture.cli:cli']}

setup_kwargs = {
    'name': 'venture',
    'version': '3.0.0',
    'description': 'Rofi / Wofi based project selector',
    'long_description': '# Venture\n\nA Dmenu / Rofi / Wofi menu to open projects and files in your favorite editor!\n\n\n\n### Dependancies\n- Venture supports three UI providers: dmenu, rofi, and wofi. It is expected that you have the one you intend to use installed.\n\n- Venture uses [Nerdfonts](https://www.nerdfonts.com/) for icons\n\n## Installation\n\n```\n$ pip install venture\n```\n\n## Docs\n[Here](./docs)\n\nNote this may installing into `~/.local/bin` which is not part of the default path on some Linux systems',
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/seanrcollings/venture',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
