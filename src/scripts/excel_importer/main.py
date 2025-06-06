from pathlib import Path

from argparse import ArgumentParser

from scripts.excel_importer.importers import (
    import_school_class,
    import_environment,
    import_professor,
    import_discipline,
)


def create_parser():
    parser = ArgumentParser(description="Import data from Excel files into the system.")
    parser.add_argument(
        "-scfp",
        "--student-class-file-path",
        type=Path,
        required=True,
        action="append",
        dest="school_class_file_paths",
        help="Path to a student class Excel file (can be used multiple times)",
    )

    parser.add_argument(
        "-efp",
        "--environment-file-path",
        type=Path,
        required=True,
        action="append",
        dest="environment_file_paths",
        help="Path to an environment Excel file (can be used multiple times)",
    )
    parser.add_argument(
        "-pfp",
        "--professor-file-path",
        type=Path,
        required=True,
        action="append",
        dest="professor_file_paths",
        help="Path to a professor Excel file (can be used multiple times)",
    )
    parser.add_argument(
        "-dfp",
        "--discipline-file-path",
        type=Path,
        required=True,
        action="append",
        dest="discipline_file_paths",
        help="Path to a discipline Excel file (can be used multiple times)",
    )
    parser.add_argument(
        "-od",
        "--output-dir",
        type=Path,
        required=True,
        dest="output_dir",
        help="Directory where the imported data will be saved",
    )
    parser.add_argument(
        "-jpp",
        "--json-pretty-print",
        action="store_true",
        dest="json_pretty_print",
        default=False,
        help="If set, the JSON files will be pretty-printed",
    )
    return parser


def parse_args(parser: ArgumentParser):
    args = parser.parse_args()
    if not args.output_dir.exists():
        args.output_dir.mkdir(parents=True, exist_ok=True)
    unexistent_files = [
        file
        for file in (
            args.school_class_file_paths
            + args.environment_file_paths
            + args.professor_file_paths
            + args.discipline_file_paths
        )
        if not file.exists()
    ]
    if unexistent_files:
        parser.error(
            f"The following files does not exist: {', '.join(str(file) for file in unexistent_files)}"
        )
    return args


def main():
    parser = create_parser()
    args = parse_args(parser)
    school_group_outfile = args.output_dir / "school_groups.json"
    environment_outfile = args.output_dir / "environments.json"
    professor_outfile = args.output_dir / "professors.json"
    discipline_outfile = args.output_dir / "disciplines.json"
    json_args = {"indent": 4, "sort_keys": True, "ensure_ascii":False} if args.json_pretty_print else {}

    for school_class_file in args.school_class_file_paths:
        import_school_class(school_class_file, school_group_outfile, **json_args)
    for environment_file in args.environment_file_paths:
        import_environment(environment_file, environment_outfile, **json_args)
    for professor_file in args.professor_file_paths:
        import_professor(professor_file, professor_outfile, **json_args)
    for discipline_file in args.discipline_file_paths:
        import_discipline(discipline_file, discipline_outfile, **json_args)


if __name__ == "__main__":
    main()
