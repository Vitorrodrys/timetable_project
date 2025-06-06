from argparse import ArgumentParser, ArgumentError, Namespace

from solver import excel_handler
from solver import runner

from .validators import dir_path, file_path



def create_excel_reader_parser(subparser: ArgumentParser) -> ArgumentParser:
    def check_and_run(args: Namespace) -> None:
        if not args.teaching_plan_dir and not args.teaching_plan_fp:
            raise ArgumentError(None, "You must provide either a teaching plan dir or a teaching plan file to import")
        if not args.course_curriculum_dir and not args.course_curriculum_fp:
            raise ArgumentError(None, "You must provide either a course curriculum dir or a course curriculum file to import")
        excel_handler.import_files(
            args.teaching_plan_dir,
            args.teaching_plan_fp,
            args.course_curriculum_dir,
            args.course_curriculum_fp
        )

    parser_excel_reader = subparser.add_parser(
        'excel_reader',
        help="Parse a new dataset specified as an Excel file"
    )

    # Teaching plan CLI options
    parser_excel_reader.add_argument(
        "-tpd", '--teaching-plan-dir',
        type=dir_path,
        help="A path to a directory containing a set of teaching plan Excel files"
    )
    parser_excel_reader.add_argument(
        '-tpfp', '--teaching-plan-fp',
        type=file_path,
        action="append",
        help="A path to a single Excel teaching plan file (can be used multiple times)"
    )

    # Course curriculum CLI options
    parser_excel_reader.add_argument(
        "-ccd", "--course-curriculum-dir",
        type=dir_path,
        help="A path to a directory containing a set of course curriculum Excel files"
    )
    parser_excel_reader.add_argument(
        "-ccfp", "--course-curriculum-fp",
        type=file_path,
        action="append",
        help="A path to a single Excel course curriculum file (can be used multiple times)"
    )

    parser_excel_reader.set_defaults(func=check_and_run)

    return parser_excel_reader

def create_solver_parser(subparser: ArgumentParser) -> ArgumentParser:
    def check_and_run(args: Namespace) -> None:
        runner.run(args.dataset_fp)
    parser_solver = subparser.add_parser(
        'solver',
        help="Run the solver on a parsed dataset"
    )

    parser_solver.add_argument(
        "-df", "--dataset-fp",
        type=file_path,
        required=True,
        help="A path to a JSON file where the parsed dataset is stored to be scheduled by solver"
    )
    parser_solver.set_defaults(func=check_and_run)
    return parser_solver

def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="A solver for timetable university problem"
    )
    subparser = parser.add_subparsers(
        dest="command",
        required=True,
        help="Submodule to call: can be the solver or the parser of files (usually called to parse a new dataset)"
    )

    create_excel_reader_parser(subparser)
    create_solver_parser(subparser)

    return parser
