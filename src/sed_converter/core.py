import os
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List
from zipfile import ZipFile

from sed_converter.sed.sed_core import SedCore

SED_MODE = "Sed"
SEDML_MODE = "SedML"


def setup(archive_location: str, convert: bool, mode: str) -> None:
    abs_archive_path: Path = Path(archive_location).resolve()
    with TemporaryDirectory() as temp_dir:
        sed_files: List[str] = []
        sedml_files: List[str] = []

        with ZipFile(abs_archive_path, "r") as original_omex:
            original_omex.extractall(temp_dir)
        for root, _, files in os.walk(temp_dir, topdown=False, followlinks=False):
            for file in files:
                full_path: str = str((Path(root) / file).resolve())
                if full_path.endswith(".sed"):
                    sed_files.append(full_path)
                elif full_path.endswith(".sedml"):
                    sedml_files.append(full_path)

        if mode == SED_MODE:
            sed_core = SedCore(sed_files=sed_files)
            sed_core.validate_all_files()
            if convert:
                # call convertToSedML() on sed_core
                pass

        if mode == SEDML_MODE:
            # Validate SedML Files
            if convert:
                # Convert SedML to SEDML
                pass


def main() -> None:
    parser = ArgumentParser(
        description="Verify or Convert a COMBINE archive with either Sed or SED_ML documents"
    )
    parser.add_argument("starting_type", choices=["Sed", "sed", "SED-ML", "SedML", "sedml"])
    parser.add_argument("archive_location", help="The path to the archive to execute")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="do not convert the archive, "
        "just confirm if the archive contains verified Sed/SED-ML documents.",
    )
    args: Namespace = parser.parse_args()

    mode: str
    if args.starting_type == "Sed" or args.starting_type == "sed":
        mode = SED_MODE
    else:
        mode = SEDML_MODE

    setup(args.archive_location, not args.verify, mode)


if __name__ == "__main__":
    main()
