# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_session',
 'np_session.components',
 'np_session.databases',
 'np_session.jobs']

package_data = \
{'': ['*']}

install_requires = \
['np_config', 'psycopg2-binary>=2.9,<3.0', 'requests', 'typing-extensions']

extras_require = \
{'dev': ['pip-tools', 'isort', 'mypy', 'black', 'pytest', 'poetry']}

setup_kwargs = {
    'name': 'np-session',
    'version': '0.1.1',
    'description': 'Tools for managing files and metadata associated with ecephys and behavior sessions for the Mindscope Neuropixels team.',
    'long_description': "```python\nfrom np_session import Session\n\n# initialize with a lims session ID or a string containing one: \n>>> session = Session('c:/1116941914_surface-image1-left.png') \n>>> session.id\n'1116941914'\n>>> session.folder\n'1116941914_576323_20210721'\n>>> session.project\n'BrainTV Neuropixels Visual Behavior'\n>>> session.is_ecephys_session\nTrue\n\n# some properties are objects with richer information:\n\n# - `pathlib` objects for filesystem paths:\n>>> session.lims_path.as_posix()\n'//allen/programs/braintv/production/visualbehavior/prod0/specimen_1098595957/ecephys_session_1116941914'\n>>> session.data_dict['es_id']\n'1116941914'\n\n# - `datetime` objects for easy date manipulation:\n>>> session.date\ndatetime.date(2021, 7, 21)\n\n# - dictionaries from databases (loaded lazily):\n>>> session.mouse['id']\n1098595953\n>>> session.mouse['full_genotype']\n'wt/wt'\n>>> session.lims['stimulus_name']\n'EPHYS_1_images_H_3uL_reward'\n>>> session.mtrain\n\n# - rig info (see `np_config.Rig`)\n>>> session.rig.acq\n'W10DT713843'\n\n# with useful string representation:\n>>> str(session.mouse)\n'576323'\n>>> str(session)\n'1116941914_576323_20210721'\n>>> str(session.rig)\n'NP.0'\n```",
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
