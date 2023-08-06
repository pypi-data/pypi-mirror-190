import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, Literal, Optional, TypeVar

import dataclasses_json
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from .data import BindingSite, QDXV1Energy, QDXV1QCInput, QDXV1QCMol

ProcId = str


quantum_energy_mutation = gql(
    """
    mutation calculate_quantum_energy($input: CalculateQuantumEnergyArgs, $tags: [String]) {
        calculateQuantumEnergy(input: $input, tags: $tags)
    }
    """
)

delete_proc_mutation = gql(
    """
    mutation delete_proc($procId: ProcId) {
        deleteProc(procId: $procId)
    }
    """
)

tag_proc_mutation = gql(
    """
    mutation tag_proc($procId: ProcId, $tags: [String]) {
        tagProc(procId: $procId, tags: $tags)
    }
    """
)

untag_proc_mutation = gql(
    """
    mutation untag_proc($procId: ProcId, $tag: String) {
        untagProc(procId: $procId, tag: $tag)
    }
    """
)

pdb_to_complex_query = gql(
    """
    query pdb_to_complex($pdb: String!, $withConnectivity: Boolean!) {
        pdbToComplex(pdb: $pdb, withConnectivity: $withConnectivity) {
            topology {
                symbols
                geometry
                connectivity
                fragments
                fragment_charges
                atom_charges
            }
            amino_acids
            amino_acid_atoms
            atoms
            atom_alts
            atom_alt_charges
            residues
            residue_atoms
            subunits
        }
    }
    """
)

combine_complexes_query = gql(
    """
    query combine_complexes($complex: ComplexInput!, $complex_b: ComplexInput!) {
        combineComplexes(complex: $complex, complexB: $complex_b) {
            topology {
                symbols
                geometry
                connectivity
                fragments
                fragment_charges
                atom_charges
            }
            amino_acids
            amino_acid_atoms
            atoms
            atom_alts
            atom_alt_charges
            residues
            residue_atoms
            subunits
        }
    }
    """
)


fragment_complex_query = gql(
    """
    query fragment($complex: ComplexInput!, $backboneSteps: Int!, $skipCharges: Boolean!) {
        fragmentComplex(complex: $complex, backboneSteps: $backboneSteps, skipExplicitCharges: $skipCharges) {
            topology {
                symbols
                geometry
                connectivity
                fragments
                fragment_charges
                atom_charges
            }
            amino_acids
            amino_acid_atoms
            atoms
            atom_alts
            atom_alt_charges
            residues
            residue_atoms
            subunits
        }
    }
    """
)

complex_to_xyz_query = gql(
    """
    query complex_xyz($complex: ComplexInput!) {
        complexToXyz(complex: $complex)
    }
    """
)

complex_to_xyz_fragments_query = gql(
    """
    query complex_xyz($complex: ComplexInput!) {
        complexToXyzFragments(complex: $complex)
    }
    """
)

dock_mutation = gql(
    """
    mutation dock($protein: ComplexInput!, $sdf: String!, $binding_site: BindingSiteInput!, $tags: [String]){
        dock(input: { sdf: { string: $sdf }, complex: $protein, binding_site: $binding_site }, tags: $tags)
    }
    """
)

prepare_ligand_mutation = gql(
    """
    mutation prep_lig($sdf: String!, $tags: [String], $prep_for: PrepTypes!){
        prepareLigand(input: { sdf: { string: $sdf }, prep_for: $prep_for }, tags: $tags)
    }
    """
)

prepare_protein_mutation = gql(
    """
    mutation prep_prot($input: ComplexInput!, $tags: [String], $prep_for: PrepTypes!) {
        prepareProtein(input: { complex: $input, prep_for: $prep_for }, tags: $tags)
    }
    """
)


proc_query = gql(
    """query s($input: String) {
  proc(procId: $input) {
    id
    completed_at
    created_at
    deleted_at
    runtime
    queued_at
    scheduled_at
    tags
    data {
      ... on Dock {
        output {
            complex {
                topology {
                    symbols
                    geometry
                    connectivity
                    fragments
                    fragment_charges
                    atom_charges
                }
                amino_acids
                amino_acid_atoms
                atoms
                atom_alts
                atom_alt_charges
                residues
                residue_atoms
                subunits
                }
            score
        }
      }
      ... on PrepareProtein {
        output {
            topology {
                symbols
                geometry
                connectivity
                fragments
                fragment_charges
                atom_charges
            }
            amino_acids
            amino_acid_atoms
            atoms
            atom_alts
            atom_alt_charges
            residues
            residue_atoms
            subunits
        }
      }
      ... on PrepareLigand {
        output {
            topology {
                symbols
                geometry
                connectivity
                fragments
                fragment_charges
                atom_charges
            }
            amino_acids
            amino_acid_atoms
            atoms
            atom_alts
            atom_alt_charges
            residues
            residue_atoms
            subunits
        }
      }
      ... on CalculateQuantumEnergy {
        state {
            current_step
            total_steps
            estimated_completed_at
            stderr_path
            stdout_path
        }
        err {
            msg
        }
        output {
          stderr_path
          stdout_path
          energy {
            energy_type
            n_mers
            n_mer_distances
            hf
            hf_total
            mp_ss
            mp_ss_total
            mp_os
            mp_os_total
          }
        }
      }
    }
  }
}
"""
)


class DataClassJsonMixin(dataclasses_json.DataClassJsonMixin):
    """Override dataclass mixin so that we don't have `"property": null,`s in our output"""

    dataclass_json_config = dataclasses_json.config(  # type: ignore
        undefined=dataclasses_json.Undefined.EXCLUDE,
        exclude=lambda f: f is None,  # type: ignore
    )["dataclasses_json"]


@dataclass
class QDXEnergyResult(DataClassJsonMixin):
    energy: QDXV1Energy
    stderr_path: str
    stdout_path: str


@dataclass
class DDProgress(DataClassJsonMixin):
    """Dataclass representing progress of a workflow step."""

    stderr_path: str
    stdout_path: str
    total_steps: int = 0
    started_at: int = 0
    current_step: int = 0
    estimated_finish: int = 0


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")


class ProcState(Generic[T1, T2, T3], DataClassJsonMixin):
    input: Optional[T1] = None
    state: Optional[T2] = None
    output: Optional[T3] = None


T = TypeVar("T", bound=ProcState)


QDXEnergyState = ProcState[QDXV1QCInput, DDProgress, QDXEnergyResult]

PrepTypes = Literal["docking", "simulation"]


@dataclass
class Proc(Generic[T], DataClassJsonMixin):
    id: str
    completed_at: int | None
    created_at: int
    deleted_at: int | None
    runtime: int
    tags: list[str]
    queued_at: int | None
    scheduled_at: int | None
    data: T
    # error: str | None


class QDXProvider:
    def __init__(self, url: str, access_token: str):
        transport = RequestsHTTPTransport(url=url, headers={"authorization": f"bearer {access_token}"})

        self.client = Client(transport=transport)

    def tag_proc(self, id: ProcId, tags: list[str]):
        response = self.client.execute(tag_proc_mutation, variable_values={"procId": id, "tags": tags})
        taskId = response.get("tagProc")
        if taskId:
            return ProcId(taskId)
        else:
            raise RuntimeError(response)

    def untag_proc(self, id: ProcId, tag: str):
        response = self.client.execute(untag_proc_mutation, variable_values={"procId": id, "tag": tag})
        taskId = response.get("untagProc")
        if taskId:
            return ProcId(taskId)
        else:
            raise RuntimeError(response)

    def delete_proc(self, id: ProcId):
        response = self.client.execute(delete_proc_mutation, variable_values={"procId": id})

        taskId = response.get("deleteProc")
        if taskId:
            return ProcId(taskId)
        else:
            raise RuntimeError(response)

    def start_quantum_energy_calculation(self, input: QDXV1QCInput, tags: list[str]) -> ProcId:
        input.keywords.scf.debug = None
        input_dict = input.to_dict()

        response = self.client.execute(
            quantum_energy_mutation, variable_values={"input": input_dict, "tags": tags}
        )

        taskId = response.get("calculateQuantumEnergy")
        if taskId:
            return ProcId(taskId)
        else:
            raise RuntimeError(response)

    def poll_proc(self, id: ProcId, n_retries: int = 10, poll_rate: int = 30) -> Proc:
        """Keep querying proc until it is completed."""
        n_try = 0

        while n_try < n_retries:
            n_try += 1
            response = self.client.execute(proc_query, variable_values={"input": id})
            proc: dict[str, Any] | None = response.get("proc")
            if proc and proc["data"]["output"]:
                deserialized = Proc.from_dict(proc)
                return deserialized
            if proc and proc["data"].get("err"):
                msg = proc["data"]["err"]["msg"]
                raise Exception(f"Proc failed: {msg}")

            time.sleep(poll_rate)


        raise Exception("Proc polling timed out")


    def get_proc(self, id: ProcId) -> Proc:
        response = self.client.execute(proc_query, variable_values={"input": id})
        proc: dict[str, Any] | None = response.get("proc")
        if proc:
            print(proc)
            deserialized = Proc.from_dict(proc)
            return deserialized

        raise Exception("Failed to find task")

    def start_ligand_prep(self, sdf: str, prep_for: PrepTypes, tags: list[str] = []):
        response = self.client.execute(
            prepare_ligand_mutation,
            variable_values={
                "sdf": sdf,
                "tags": tags,
                "prep_for": prep_for.upper()
            },
        )

        taskId = response.get("prepareLigand")
        if taskId:
            return ProcId(taskId)
        else:
            raise RuntimeError(response)

    def start_protein_prep(self, complex: Any, prep_for: PrepTypes, tags: list[str] = []):
        response = self.client.execute(
            prepare_protein_mutation,
            variable_values={
                "input": complex,
                "tags": tags,
                "prep_for": prep_for.upper()
            },
        )

        taskId = response.get("prepareProtein")
        if taskId:
            return ProcId(taskId)
        else:
            raise RuntimeError(response)

    def start_dock(self, complex: Any, sdf: str, binding_site: BindingSite, tags: list[str] = []):
        response = self.client.execute(
            dock_mutation,
            variable_values={
                "binding_site": binding_site.to_dict(),
                "protein": complex,
                "sdf": sdf,
                "tags": tags,
            },
        )

        taskId = response.get("dock")
        if taskId:
            return ProcId(taskId)
        else:
            raise RuntimeError(response)

    def pdb_to_complex(self, pdb: str | Path, with_connectivity: bool = True) -> Any:
        if isinstance(pdb, str):
            response = self.client.execute(
                pdb_to_complex_query,
                variable_values={"pdb": pdb, "withConnectivity": with_connectivity},
                upload_files=True,
            )
        else:
            with pdb.open(mode="r") as f:
                response = self.client.execute(
                    pdb_to_complex_query,
                    variable_values={"pdb": f.read(), "withConnectivity": with_connectivity},
                )

        complex: dict[str, Any] | None = response.get("pdbToComplex")

        if complex:
            return complex

        raise Exception("Failed convert pdb")

    def fragment_complex(self, complex: Any, backbone_steps: int, skip_explicit_charges: bool = False):
        response = self.client.execute(
            fragment_complex_query,
            variable_values={
                "complex": complex,
                "backboneSteps": backbone_steps,
                "skipCharges": skip_explicit_charges,
            },
        )
        complex = response.get("fragmentComplex")

        if complex:
            return complex

        raise Exception("Failed to fragment complex")

    def combine_complexes(self, complex: Any, complexB: Any):
        response = self.client.execute(
            combine_complexes_query,
            variable_values={
                "complex": complex,
                "complex_b": complexB,
            },
        )
        complex = response.get("combineComplexes")

        if complex:
            return complex

        raise Exception("Failed to fragment complex")
