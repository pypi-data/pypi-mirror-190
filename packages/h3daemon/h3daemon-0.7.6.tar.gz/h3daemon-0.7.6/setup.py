# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['h3daemon']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=23.0,<24.0',
 'platformdirs>=2.6.2,<3.0.0',
 'podman>=4.3.0,<5.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['h3daemon = h3daemon.cli:app']}

setup_kwargs = {
    'name': 'h3daemon',
    'version': '0.7.6',
    'description': 'Run HMMER daemon on containers',
    'long_description': '# Welcome to h3daemon 👋\n\n> Command-line for running HMMER server on arm64 and amd64 machines via containers.\n\n### 🏠 [Homepage](https://github.com/EBI-Metagenomics/h3daemon)\n\n## ⚡️ Requirements\n\n- Python >= 3.9\n- Pip\n- [Podman](https://podman.io) >= 3.4\n- [Homebrew](https://brew.sh) on MacOS (recommended)\n- [Pipx](https://pypa.github.io/pipx/) for Python package management (recommended)\n\n### MacOS\n\nInstall Python and Podman:\n\n```sh\nbrew update && brew install python podman pipx\n```\n\nEnsure that your `PATH` environment variable is all set:\n\n```sh\npipx ensurepath\n```\n\n💡 You might need to close your terminal and reopen it for the changes to take effect.\n\n### Ubuntu (and Debian-based distros)\n\nInstall Python and Podman:\n\n```sh\nsudo apt update && \\\n    sudo apt install python3 python3-pip python3-venv podman --yes && \\\n    python3 -m pip install --user pipx\n```\n\nEnsure that your `PATH` environment variable is all set:\n\n```sh\npython3 -m pipx ensurepath\n```\n\n💡 You might need to close your terminal and reopen it for the changes to take effect.\n\n## 📦 Install\n\n```sh\npipx install h3daemon\n```\n\n## Usage\n\n```\n Usage: h3daemon [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ─────────────────────────────────────────────────────╮\n│ --version                                                     │\n│ --help             Show this message and exit.                │\n╰───────────────────────────────────────────────────────────────╯\n╭─ Commands ────────────────────────────────────────────────────╮\n│ info        Show namespace information.                       │\n│ ls          List namespaces.                                  │\n│ press       Press hmmer3 ASCII file.                          │\n│ start       Start daemon.                                     │\n│ stop        Stop namespace.                                   │\n│ sys         Show Podman information.                          │\n╰───────────────────────────────────────────────────────────────╯\n```\n\n### Example\n\nDownload `minifam.hmm` database:\n\n```sh\npipx run blx get \\\n  fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960 \\\n  minifam.hmm\n```\n\nPress it:\n\n```sh\nh3daemon press minifam.hmm\n```\n\nStart the daemon to listen on a random (available) port:\n\n```sh\nh3daemon start minifam.hmm\n```\n\nAnd stop it:\n\n```sh\nh3daemon stop minifam.hmm\n```\n\n## 👤 Author\n\n- [Danilo Horta](https://github.com/horta)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n',
    'author': 'Danilo Horta',
    'author_email': 'danilo.horta@pm.me',
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
