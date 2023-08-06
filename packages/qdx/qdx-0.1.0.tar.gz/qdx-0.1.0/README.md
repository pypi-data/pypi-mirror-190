# QDX-py: Python SDK for the QDX API

This package exposes a simple provider and CLI for the different tools exposed by the QDX GraphQL API.

## Usage

### As a library

``` python
from qdx.api import QDXProvider

URL = "url to the qdx api"
TOKEN = "your qdx access token"

provider = QDXProvider(URL, TOKEN)

input = # Some QDXV1QCInput

task_id = provider.start_quantum_energy_calculation(input) # will return a TaskId - reference to the job

task = provider.get_quantum_energy_calculation(task_id) # will return a task, with its status, progress, and result if completed

# NOTE: tasks may take a while to run, so you will have to poll the task until it's done
```


### As a CLI

``` sh
# All cli calls have these standard arguments, referred to as … in future examples
qdx --url QDX_API_URL --access-token QDX_ACCESS_TOKEN

# Post a hermes job, returning a task id
… --post-quantum-energy < ./path_to_qdxv1_input.json

# Retrieve the hermes job, or its progress
… --get-proc TASK_ID

## Other functions
# Return a qdx complex json object and save it as complex.json
… --pdb-to-complex PATH_TO_PDB_FILE > complex.json

# Prepare a protein for quauntum energy calculation
… --prepare-protein simulation --poll < ./complex.json > prepped_protein_complex.json

# Fragment a qdx complex json object
… --fragment-complex [MIN_STEPS_ALONG_PROTEIN_BACKBONE_BEFORE_CUTTING_AT_C-C_BOND] < prepped_protein_complex.json > fragmented_protein_complex.json

# Prepare a ligand for quauntum energy calculation
… --prepare-ligand simulation --poll < ./path_to_ligand.sdf > prepped_ligand_complex.json

# Combine protein and ligand complexes for simulation

… --combine-complexes ./prepped_protein_complex.json < ./prepped_ligand_complex.sdf > protein_ligand_complex.json

# Convert a qdx complex into a qdx input file
… --convert ./protein_ligand_complex.json --direction qdxcomplex2qdxv1 > qdx_input.json

# Convert a qdx complex into a exess input file
… --convert ./protein_ligand_complex.json --direction qdxcomplex2exess > exess_input.json

# Convert a qdx input file into an exess input file
… --convert qdx_input.json --direction qdxv12exess > exess_input.json
```

