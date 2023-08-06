# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qdx']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'datargs>=0.11.0,<0.12.0',
 'gql[requests]>=3.4.0,<4.0.0',
 'typed-argument-parser>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'qdx',
    'version': '0.1.0',
    'description': '',
    'long_description': '# QDX-py: Python SDK for the QDX API\n\nThis package exposes a simple provider and CLI for the different tools exposed by the QDX GraphQL API.\n\n## Usage\n\n### As a library\n\n``` python\nfrom qdx.api import QDXProvider\n\nURL = "url to the qdx api"\nTOKEN = "your qdx access token"\n\nprovider = QDXProvider(URL, TOKEN)\n\ninput = # Some QDXV1QCInput\n\ntask_id = provider.start_quantum_energy_calculation(input) # will return a TaskId - reference to the job\n\ntask = provider.get_quantum_energy_calculation(task_id) # will return a task, with its status, progress, and result if completed\n\n# NOTE: tasks may take a while to run, so you will have to poll the task until it\'s done\n```\n\n\n### As a CLI\n\n``` sh\n# All cli calls have these standard arguments, referred to as … in future examples\nqdx --url QDX_API_URL --access-token QDX_ACCESS_TOKEN\n\n# Post a hermes job, returning a task id\n… --post-quantum-energy < ./path_to_qdxv1_input.json\n\n# Retrieve the hermes job, or its progress\n… --get-proc TASK_ID\n\n## Other functions\n# Return a qdx complex json object and save it as complex.json\n… --pdb-to-complex PATH_TO_PDB_FILE > complex.json\n\n# Prepare a protein for quauntum energy calculation\n… --prepare-protein simulation --poll < ./complex.json > prepped_protein_complex.json\n\n# Fragment a qdx complex json object\n… --fragment-complex [MIN_STEPS_ALONG_PROTEIN_BACKBONE_BEFORE_CUTTING_AT_C-C_BOND] < prepped_protein_complex.json > fragmented_protein_complex.json\n\n# Prepare a ligand for quauntum energy calculation\n… --prepare-ligand simulation --poll < ./path_to_ligand.sdf > prepped_ligand_complex.json\n\n# Combine protein and ligand complexes for simulation\n\n… --combine-complexes ./prepped_protein_complex.json < ./prepped_ligand_complex.sdf > protein_ligand_complex.json\n\n# Convert a qdx complex into a qdx input file\n… --convert ./protein_ligand_complex.json --direction qdxcomplex2qdxv1 > qdx_input.json\n\n# Convert a qdx complex into a exess input file\n… --convert ./protein_ligand_complex.json --direction qdxcomplex2exess > exess_input.json\n\n# Convert a qdx input file into an exess input file\n… --convert qdx_input.json --direction qdxv12exess > exess_input.json\n```\n\n',
    'author': 'Ryan Swart',
    'author_email': 'ryan@talosystems.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
