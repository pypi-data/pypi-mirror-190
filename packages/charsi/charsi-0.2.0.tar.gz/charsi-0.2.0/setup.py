# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['charsi']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['charsi = charsi.__main__:cli']}

setup_kwargs = {
    'name': 'charsi',
    'version': '0.2.0',
    'description': 'A command-line tool to help game modders build string resources for Diablo II: Resurrected.',
    'long_description': "# Charsi\n\n![Charis](./docs/images/charsi-x16.png) **Charsi** is a command-line tool to\nhelp game modders build string resources for [Diablo II: Resurrected][1].\n\n## Quickstart\n\n1. Extract `item-names.json` file at `/data/local/lng/strings` from game data\n   storage by [CascView](http://www.zezula.net/en/casc/main.html).\n\n2. Write a recipe file `example.recipe` with following:\n\n```\nText[qf1]: Example\n```\n\n3. Run the following command to build a new string table:\n\n```\ncharsi build --recipe-file=example.recipe item-names.json > new-item-names.json\n```\n\n4. Replace file `/data/local/lng/strings/item-names.json`\n   with `new-item-names.json` in your mods.\n\n5. Check in game, item name `Khalim's Flail` has been replaced with `Example`.\n\n## License\n\nCopyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>\n\nThe GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).\n\n[1]: https://diablo2.blizzard.com\n",
    'author': 'HE Yaowen',
    'author_email': 'he.yaowen@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
