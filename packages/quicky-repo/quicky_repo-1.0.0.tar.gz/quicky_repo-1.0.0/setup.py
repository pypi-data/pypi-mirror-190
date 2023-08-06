# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.commands', 'src.core', 'src.ui']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pyfiglet>=0.8.post1,<0.9', 'rich>=13.3.1,<14.0.0']

setup_kwargs = {
    'name': 'quicky-repo',
    'version': '1.0.0',
    'description': '⚡ Initialize your projects as fast as you want.',
    'long_description': '<div align="center">\n  <h1><code>Fast Repo</code></h1>\n\n  <p>\n    <strong>⚡ Initialize your projects as fast as you want. ⚡</strong>\n  </p>\n\n  <p>\n    <img\n      alt="GitHub top language"\n      src="https://img.shields.io/github/languages/top/kauefraga/fast-repo.svg"\n    />\n    <img\n      alt="Repository size"\n      src="https://img.shields.io/github/repo-size/kauefraga/fast-repo.svg"\n    />\n    <a href="https://github.com/kauefraga/fast-repo/commits/main">\n      <img\n        alt="GitHub last commit"\n        src="https://img.shields.io/github/last-commit/kauefraga/fast-repo.svg"\n      />\n    </a>\n    <img\n      alt="GitHub LICENSE"\n      src="https://img.shields.io/github/license/kauefraga/fast-repo.svg"\n    />\n  </p>\n</div>\n\n<!-- ## ✨ Features\n\n- **Simple**: You just run it, choose your boilerplate and done!\n- **Pretty UI**: A minimal UI that exposes everything you need.\n- **Colorized Outputs**: Everything looks better with some colors.\n- **Easy Usage**: If you need some help, just use the flag `--help` -->\n\n## 🎲 Prerequisites\n\nTo run this project you will need to have [Python](https://www.python.org) and [Node](https://nodejs.org/en).\n- Node Version Managers: [fnm](https://github.com/Schniz/fnm), [nvm](https://github.com/nvm-sh/nvm), [asdf](https://asdf-vm.com)...\n- Python Version Managers: [pyenv](https://github.com/pyenv/pyenv), [virtualenv](https://virtualenv.pypa.io/en/latest)...\n\n## ⬇️ How to install and use it\n\n```bash\ngit clone https://github.com/kauefraga/fast-repo.git\ncd fast-repo\n\npip install -r requirements.txt\n# Has nothing to try out now...\n```\nYou are welcome to open issues and pull requests!\n\n## 🛠 Technologies\n\nThe following tools have been used to build the project:\n\n- 🐍 [Python](https://www.python.org) - A programming language that lets you work quickly\nand integrate systems more effectively.\n- 🕶 [Click](https://pypi.org/project/click) - Composable command line interface toolkit\n- 🎨 [Rich](https://pypi.org/project/rich) - Rich is a Python library for rich text and beautiful formatting in the terminal.\n\n<!-- ## 📜 Coming soon... -->\n\n## 📝 License\n\nThis project is licensed under the MIT License - See the [LICENSE](https://github.com/kauefraga/fast-repo/blob/main/LICENSE) for more information.\n\n---\n\n<div align="center" display="flex">\n  <img alt="Built with love" src="https://forthebadge.com/images/badges/built-with-love.svg">\n  <img alt="Powered by coffee" src="https://forthebadge.com/images/badges/powered-by-coffee.svg">\n</div>\n',
    'author': 'Kauê Fraga Rodrigues',
    'author_email': 'kauefragarodrigues456@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
