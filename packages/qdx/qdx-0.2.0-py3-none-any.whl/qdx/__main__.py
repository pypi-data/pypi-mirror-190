import sys
from pathlib import Path
from typing import Literal, Optional
import json

from datargs import argsclass, parse

from .data import QDXV1QCInput, run_convert
from .api import PrepTypes, QDXProvider


@argsclass(description="QDX CLI")
class QDXArgs:
    url: str
    access_token: str
    # input: str = arg(positional=True, help="QDXV1 Input json")
    post_quantum_energy: Optional[bool]
    get_quantum_energy: Optional[str]
    delete_proc: Optional[str]
    tag_proc: Optional[str]
    untag_proc: Optional[str]
    pdb_to_complex: Optional[Path]
    fragment_complex: Optional[int]
    tags: Optional[list[str]]
    convert: Optional[Path]
    prepare_protein: Optional[PrepTypes]
    prepare_ligand: Optional[PrepTypes]
    combine_complexes: Optional[Path]
    poll: Optional[bool]
    direction: Optional[Literal["qdxv12exess", "exess2qdxv1", "qdxcomplex2qdxv1", "qdxcomplex2exess"]]


def main():
    args = parse(QDXArgs)

    provider = QDXProvider(args.url, args.access_token)

    if args.delete_proc:
        print(provider.delete_proc(args.delete_proc))
    elif args.tag_proc:
        print(provider.tag_proc(args.tag_proc, args.tags or []))
    elif args.untag_proc:
        for tag in args.tags or []:
            print(provider.untag_proc(args.untag_proc, tag))
    elif args.post_quantum_energy:
        print(
            provider.start_quantum_energy_calculation(
                QDXV1QCInput.from_json(sys.stdin.read()), tags=args.tags or []
            )
        )
    elif args.prepare_protein:
        id = provider.start_protein_prep(
            json.load(sys.stdin), prep_for=args.prepare_protein, tags=args.tags or []
        )
        print(json.dumps(provider.poll_proc(id).state["term"]) if args.poll else id)
    elif args.prepare_ligand:
        id = provider.start_ligand_prep(sys.stdin.read(), prep_for=args.prepare_ligand, tags=args.tags or [])
        print(json.dumps(provider.poll_proc(id).state["term"]) if args.poll else id)
    elif args.get_quantum_energy:
        print(provider.get_proc(args.get_quantum_energy).to_json())
    elif args.pdb_to_complex:
        print(json.dumps(provider.pdb_to_complex(args.pdb_to_complex)))
    elif args.combine_complexes:
        print(
            json.dumps(
                provider.combine_complexes(
                    json.loads(args.combine_complexes.read_text()), json.load(sys.stdin)
                )
            )
        )
    elif args.fragment_complex:
        print(json.dumps(provider.fragment_complex(json.load(sys.stdin), args.fragment_complex)))
    elif args.convert and args.direction:
        with open(args.convert) as f:
            print(run_convert(f.read(), args.direction).to_json(indent=2))


if __name__ == "__main__":
    main()
