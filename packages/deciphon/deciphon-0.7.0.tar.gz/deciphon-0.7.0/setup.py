# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deciphon']

package_data = \
{'': ['*']}

install_requires = \
['cffi',
 'deciphon-core>=0.1.10,<0.2.0',
 'h3daemon>=0.7.6,<0.8.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dcp = deciphon.cli:app']}

setup_kwargs = {
    'name': 'deciphon',
    'version': '0.7.0',
    'description': 'Individually annotate long, error-prone nucleotide sequences into proteins',
    'long_description': '# Welcome to deciphon 👋\n\n> Individually annotate long, error-prone nucleotide sequences into proteins\n\n### 🏠 [Homepage](https://github.com/EBI-Metagenomics/deciphon-py)\n\n## ⚡️ Requirements\n\n- Python >= 3.9\n- Pip\n- [Podman](https://podman.io) >= 3.4\n- [Homebrew](https://brew.sh) on MacOS (recommended)\n- [Pipx](https://pypa.github.io/pipx/) for Python package management (recommended)\n\n### MacOS\n\nInstall Python and Podman:\n\n```sh\nbrew update && brew install python podman pipx\n```\n\nEnsure that your `PATH` environment variable is all set:\n\n```sh\npipx ensurepath\n```\n\n💡 You might need to close your terminal and reopen it for the changes to take effect.\n\n### Ubuntu (and Debian-based distros)\n\nInstall Python and Podman:\n\n```sh\nsudo apt update && \\\n    sudo apt install python3 python3-pip python3-venv podman --yes && \\\n    python3 -m pip install --user pipx\n```\n\nEnsure that your `PATH` environment variable is all set:\n\n```sh\npython3 -m pipx ensurepath\n```\n\n💡 You might need to close your terminal and reopen it for the changes to take effect.\n\n## Install\n\n```sh\npipx install deciphon\n```\n\n## Usage\n\n```\n Usage: dcp [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ────────────────────────────────────────────────────────────────────╮\n│ --version                                                                    │\n│ --help             Show this message and exit.                               │\n╰──────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ───────────────────────────────────────────────────────────────────╮\n│ press        Press HMM ASCII file into a Deciphon database one.              │\n│ scan         Annotate nucleotide sequences into proteins a protein database. │\n╰──────────────────────────────────────────────────────────────────────────────╯\n```\n\n## Example\n\nDownload the `minifam.hmm` protein database:\n\n```sh\npipx run blx get \\\n  fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960 \\\n  minifam.hmm\n```\n\nDownload the `consensus.json` file of sequences:\n\n```sh\npipx run blx get \\\n  af483ed5aa42010e8f6c950c42d81bac69f995876bf78a5965f319e83dc3923e \\\n  consensus.hmm\n```\n\nPress it:\n\n```sh\ndcp press minifam.hmm\n```\n\nScan it:\n\n```sh\ndcp scan minifam.hmm consensus.json\n```\n\n## 👤 Author\n\n- [Danilo Horta](https://github.com/horta)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n',
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
