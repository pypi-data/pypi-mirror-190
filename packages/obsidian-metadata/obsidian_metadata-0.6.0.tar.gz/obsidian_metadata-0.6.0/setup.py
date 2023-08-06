# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['obsidian_metadata',
 'obsidian_metadata._config',
 'obsidian_metadata._utils',
 'obsidian_metadata.models']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'questionary>=1.10.0,<2.0.0',
 'regex>=2022.10.31,<2023.0.0',
 'rich>=13.2.0,<14.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'shellingham>=1.4.0,<2.0.0',
 'tomlkit>=0.11.6,<0.12.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['obsidian-metadata = obsidian_metadata.cli:app']}

setup_kwargs = {
    'name': 'obsidian-metadata',
    'version': '0.6.0',
    'description': 'Make batch updates to Obsidian metadata',
    'long_description': '[![PyPI version](https://badge.fury.io/py/obsidian-metadata.svg)](https://badge.fury.io/py/obsidian-metadata) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/obsidian-metadata) [![Python Code Checker](https://github.com/natelandau/obsidian-metadata/actions/workflows/automated-tests.yml/badge.svg)](https://github.com/natelandau/obsidian-metadata/actions/workflows/automated-tests.yml) [![codecov](https://codecov.io/gh/natelandau/obsidian-metadata/branch/main/graph/badge.svg?token=3F2R43SSX4)](https://codecov.io/gh/natelandau/obsidian-metadata)\n\n# obsidian-metadata\n\nA script to make batch updates to metadata in an Obsidian vault. No changes are\nmade to the Vault until they are explicitly committed.\n\n[![asciicast](https://asciinema.org/a/555789.svg)](https://asciinema.org/a/555789)\n\n## Important Disclaimer\n\n**It is strongly recommended that you back up your vault prior to committing changes.** This script makes changes directly to the markdown files in your vault. Once the changes are committed, there is no ability to recreate the original information unless you have a backup. Follow the instructions in the script to create a backup of your vault if needed. The author of this script is not responsible for any data loss that may occur. Use at your own risk.\n\n## Install\n\nRequires Python v3.10 or above.\n\n```bash\npip install obsidian-metadata\n```\n\n## Usage\n\n### CLI Commands\n\n-   `--config-file`: Specify a custom configuration file location\n-   `--dry-run`: Make no destructive changes\n-   `--export-csv`: Specify a path and create a CSV export of all metadata\n-   `--export-json`: Specify a path and create a JSON export of all metadata\n-   `--help`: Shows interactive help and exits\n-   `--log-file`: Specify a log file location\n-   `--log-to-file`: Will log to a file\n-   `--vault-path`: Specify a path to an Obsidian Vault\n-   `--verbose`: Set verbosity level (0=WARN, 1=INFO, 2=DEBUG, 3=TRACE)\n-   `--version`: Prints the version number and exits\n\n### Running the script\n\nOnce installed, run `obsidian-metadata` in your terminal to enter an interactive menu of sub-commands.\n\n**Vault Actions**\n\n-   Backup: Create a backup of the vault.\n-   Delete Backup: Delete a backup of the vault.\n\n**Inspect Metadata**\n\n-   **View all metadata in the vault**\n-   View all **frontmatter**\n-   View all **inline metadata**\n-   View all **inline tags**\n-   **Export all metadata to CSV or JSON file**\n\n**Filter Notes in Scope**: Limit the scope of notes to be processed with one or more filters.\n\n-   **Path filter (regex)**: Limit scope based on the path or filename\n-   **Metadata filter**: Limit scope based on a key or key/value pair\n-   **Tag filter**: Limit scope based on an in-text tag\n-   **List and clear filters**: List all current filters and clear one or all\n-   **List notes in scope**: List notes that will be processed.\n\n**Add Metadata**: Add new metadata to your vault.\n\n-   **Add new metadata to the frontmatter**\n-   **Add new inline metadata** - Set `insert_location` in the config to control where the new metadata is inserted. (Default: Bottom)\n-   **Add new inline tag** - Set `insert_location` in the config to control where the new tag is inserted. (Default: Bottom)\n\n**Rename Metadata**: Rename either a key and all associated values, a specific value within a key. or an in-text tag.\n\n-   **Rename a key**\n-   **Rename a value**\n-   **Rename an inline tag**\n\n**Delete Metadata**: Delete either a key and all associated values, or a specific value.\n\n-   **Delete a key and associated values**\n-   **Delete a value from a key**\n-   **Delete an inline tag**\n\n**Transpose Metadata**: Move metadata from inline to frontmatter or the reverse.\n\n-   **Transpose all metadata** - Moves all frontmatter to inline metadata, or the reverse\n-   **Transpose key** - Transposes a specific key and all it\'s values\n-   **Transpose value**- Transpose a specific key:value pair\n\n**Review Changes**: Prior to committing changes, review all changes that will be made.\n\n-   **View a diff of the changes** that will be made\n\n**Commit Changes**: Write the changes to disk. This step is not undoable.\n\n-   **Commit changes to the vault**\n\n### Configuration\n\n`obsidian-metadata` requires a configuration file at `~/.obsidian_metadata.toml`. On first run, this file will be created. You can specify a new location for the configuration file with the `--config-file` option.\n\nTo add additional vaults, copy the default section and add the appropriate information. The script will prompt you to select a vault if multiple exist in the configuration file\n\nBelow is an example with two vaults.\n\n```toml\n["Vault One"] # Name of the vault.\n\n    # Path to your obsidian vault\n    path = "/path/to/vault"\n\n    # Folders within the vault to ignore when indexing metadata\n    exclude_paths = [".git", ".obsidian"]\n\n    # Location to add metadata. One of:\n    #    TOP:            Directly after frontmatter.\n    #    AFTER_TITLE:    After a header following frontmatter.\n    #    BOTTOM:         The bottom of the note\n    insert_location = "BOTTOM"\n\n["Vault Two"]\n    path = "/path/to/second_vault"\n    exclude_paths = [".git", ".obsidian", "daily_notes"]\n    insert_location = "AFTER_TITLE"\n```\n\nTo bypass the configuration file and specify a vault to use at runtime use the `--vault-path` option.\n\n# Contributing\n\n## Setup: Once per project\n\nThere are two ways to contribute to this project.\n\n### 1. Containerized development\n\n1. Clone this repository. `git clone https://github.com/natelandau/obsidian-metadata`\n2. Open the repository in Visual Studio Code\n3. Start the [Dev Container](https://code.visualstudio.com/docs/remote/containers). Run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Remote-Containers: Reopen in Container_.\n4. Run `poetry env info -p` to find the PATH to the Python interpreter if needed by VSCode.\n\n### 2. Local development\n\n1. Install Python 3.10 and [Poetry](https://python-poetry.org)\n2. Clone this repository. `git clone https://github.com/natelandau/obsidian-metadata`\n3. Install the Poetry environment with `poetry install`.\n4. Activate your Poetry environment with `poetry shell`.\n5. Install the pre-commit hooks with `pre-commit install --install-hooks`.\n\n## Developing\n\n-   This project follows the [Conventional Commits](https://www.conventionalcommits.org/) standard to automate [Semantic Versioning](https://semver.org/) and [Keep A Changelog](https://keepachangelog.com/) with [Commitizen](https://github.com/commitizen-tools/commitizen).\n    -   When you\'re ready to commit changes run `cz c`\n-   Run `poe` from within the development environment to print a list of [Poe the Poet](https://github.com/nat-n/poethepoet) tasks available to run on this project. Common commands:\n    -   `poe lint` runs all linters\n    -   `poe test` runs all tests with Pytest\n-   Run `poetry add {package}` from within the development environment to install a run time dependency and add it to `pyproject.toml` and `poetry.lock`.\n-   Run `poetry remove {package}` from within the development environment to uninstall a run time dependency and remove it from `pyproject.toml` and `poetry.lock`.\n-   Run `poetry update` from within the development environment to upgrade all dependencies to the latest versions allowed by `pyproject.toml`.\n',
    'author': 'Nate Landau',
    'author_email': 'github@natenate.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/natelandau/obsidian-metadata',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
