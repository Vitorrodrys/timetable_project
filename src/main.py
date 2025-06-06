from pathlib import Path

from argparse import ArgumentParser




def create_parser():
    parser = ArgumentParser(description="Import data from Excel files into the system.")
    parser.add_argument(
        "-dd", "--dataset-dir",
        type=Path,
        required=True,
        help="Directory containing the JSONs dataset to be solved"
    )
    parser.add_argument(
        "-rfp", "--result-file-path",
        type=Path,
        required=True,
        help="Path to the result file where the result will be saved",
    )
    return parser

def parse_args(parser: ArgumentParser):
    args = parser.parse_args()
    if not args.dataset_dir.exists():
        parser.error(f"The dataset directory {args.dataset_dir} does not exist.")
    if not args.result_file_path.parent.exists():
        args.result_file_path.parent.mkdir(parents=True, exist_ok=True)
    return args

def main():
    parser = create_parser()
    args = parse_args(parser)
