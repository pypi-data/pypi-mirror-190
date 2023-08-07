# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paradigm_manager']

package_data = \
{'': ['*']}

install_requires = \
['hfst-optimized-lookup>=0.0.13,<0.1.0',
 'more-itertools>=8.7.0,<8.8.0',
 'pathlib',
 'typing-extensions>=3.7,<4.0']

setup_kwargs = {
    'name': 'paradigm-manager',
    'version': '0.3.5',
    'description': 'Paradigm panes meant to provide layout specification to be reused elsewhere.',
    'long_description': '# paradigm-panes\n\nInstallable package that produces a paradigm for a given word, given a pointer to paradigm layouts and FST file. Originally\nbuilt for [itwêwina](https://itwewina.altlab.app/).\n\n# PyPi Package\n\nLatest version of the package posted to PyPi: [paradigm-panes 0.3.2](https://pypi.org/project/paradigm-panes/)\n\n# Install\n\n```\npip install paradigm-panes\n```\n\n# Developing\n\nDeveloping is done and managed through [Python Poetry](https://python-poetry.org/) package manager.\n\nTo start development:\n\n```\n# Download the repo\ngit clone https://github.com/UAlbertaALTLab/paradigm-panes.git\n\n# Set up virutal env\nvirtualenv venv --python=python3.9\nsource venv/bin/activate\n\n# Install dependencies\npoetry install\n\n# Now cd into main directory and try out the package\ncd paradigm_panes\npython\n    >>> import paradigm_manager\n    >>> ...\n```\n\n# Package Documentation:\nThe package is very simple to use and requires two types of linguistic files to operate. First:\n\n## Installing\nInstall the paradigm manager with:\n```shell\npip install paradigm-manager\n```\n\n## Usage and Configuration\n\nImport the library:\n\n```\nimport paradigm_manager\n```\n\nCreate PaneManager and specify path to FST file and layouts resources:\n\n```\npm = paradigm_manager.ParadigmManager(\n            layout_directory="/home/ubuntu/paradigm_panes/resources/layouts", \n            generation_fst="/home/ubuntu/paradigm_panes/resources/fst/crk-strict-generator.hfstol")\n```\n\nPaths to the layout directory and generation FST are required arguments.\n\nPass lemma and paradigm type to generate a paradigm:\n\n```\nlemma = "amisk"\np_type = "NA"\npm.set_lemma(lemma)\npm.set_paradigm(p_type)\n```\n\nGenerate the paradigm:\n\n```python\nparadigm = pm.generate()\n```\n\nOptionally add recordings to the paradigm with the following steps:\n```python\nwordforms = pm.get_all_wordforms()\nmatched_recordings = <fetch recordings for all wordforms>\nparadigm = pm.bulk_add_recordings(matched_recordings)\n```\n\n# Testing\n\nTo run the tests you need to install required dependencies, it is easier by using a virtual environment like this:\n\n```\n# Set up virutal env\nvirtualenv venv --python=python3.9\nsource venv/bin/activate\n\n# Install dependencies\npoetry install\n```\n\nOnce the dependencies are installed you can run tests by calling pytest.\n\n```\npytest\n```\n\n# Release\n\nPackage version number is sorted in pyproject.toml. With every release to PyPi the version needs to be updated. \\\nBuild the package from the main directory before publishing it:\n\n```\npoetry build\n```\n\nTo publish to Test PyPi use poetry and enter credentials associated with Test PyPi account\n\n```\npoetry publish -r testpypi\n```\n\nTo publish to real PyPi use poetry and enter credentials associated with PyPi\n\n```\npoetry publish\n```\n\nAll relevant package specifications and dependencies are managed in `pyproject.toml` file.\n',
    'author': 'Jolene Poulin',
    'author_email': 'jcpoulin@ualberta.ca',
    'maintainer': 'Jolene Poulin',
    'maintainer_email': 'jcpoulin@ualberta.ca',
    'url': 'https://github.com/UAlbertaALTLab/paradigm-panes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
