from argparse import ArgumentParser

import pandas
from pathlib import Path

from scripts.excel_converter.readers import read_course_curriculum, read_teaching_plan


def create_parser():
    parser = ArgumentParser(
        description="Convert Excel files to a format understandable by the solver."
    )
    parser.add_argument(
        "-cc",
        "--course-curriculum",
        type=Path,
        required=True,
        action="append",
        dest="course_curriculum",
        help="Path to a course curriculum Excel file (can be used multiple times)",
    )
    parser.add_argument(
        "-tp",
        "--teaching-plan",
        type=Path,
        required=True,
        action="append",
        dest="teaching_plan",
        help="Path to a teaching plan Excel file (can be used multiple times)",
    )
    parser.add_argument(
        "-od",
        "--output-dir",
        type=Path,
        required=True,
        dest="output_dir",
        help="Directory where the converted JSON files will be saved",
    )
    return parser


def parse_args(parser: ArgumentParser):
    args = parser.parse_args()
    if not args.output_dir.exists():
        args.output_dir.mkdir(parents=True, exist_ok=True)
    unexistent_files = [
        file
        for file in args.course_curriculum + args.teaching_plan
        if not file.exists()
    ]
    if unexistent_files:
        parser.error(
            f"The following files does not exist: {', '.join(str(file) for file in unexistent_files)}"
        )
    return args


def save_excel(title_columns: tuple[str], data: list, out: Path):
    df = pandas.DataFrame(data, columns=title_columns)
    df.to_excel(out, index=False)


def main():
    parser = create_parser()
    args = parse_args(parser)

    disciplines = []
    for course_curriculum in args.course_curriculum:
        disciplines.extend(read_course_curriculum(course_curriculum))
    disciplines = set(disciplines)

    teachers = []
    environments = []
    school_groups = []
    for teaching_plan in args.teaching_plan:
        current_envs, current_school_groups, current_teachs = read_teaching_plan(
            teaching_plan
        )
        environments.extend(current_envs)
        teachers.extend(current_teachs)
        school_groups.extend(current_school_groups)
    environments = set(environments)
    teachers = set(teachers)
    school_groups = set(school_groups)

    save_excel(
        title_columns=("code", "name", "workload", "course"),
        data=disciplines,
        out=args.output_dir / "disciplines.xlsx",
    )
    save_excel(
        title_columns=("code", "depart", "name", "last_name"),
        data=teachers,
        out=args.output_dir / "teachers.xlsx",
    )
    save_excel(
        title_columns=("environment",),
        data=environments,
        out=args.output_dir / "environments.xlsx",
    )
    save_excel(
        title_columns=("school_group",),
        data=school_groups,
        out=args.output_dir / "school_groups.xlsx",
    )


if __name__ == "__main__":
    main()
