from pathlib import Path
import re
from typing import Generator


from solver.excel_importer import TeachingPlanImporter

def _xlsx_iterator(directory: Path) -> Generator[Path]:
    return (f for f in directory.glob("*") if re.match(r".*\.(xls|xlsx|xlsm|xlsb|xltx|xltm)$", f.name))

def _merge_dict(dict1: dict, dict2:dict):
    if dict2 == {}:
        dict2.update(dict1)
        return
    for key, value in dict2.items():
        value.update(dict1[key])

def import_files(
    teaching_plan_dir: Path | None,
    teaching_plan_files: list[Path] | None,
    course_curriculum_dir: Path | None,
    course_curriculum_files: list[Path] | None
):
    teaching_plan_files = teaching_plan_files or []
    course_curriculum_files = course_curriculum_files or []
    tp_importer = TeachingPlanImporter()
    imported_datas = {}
    for teaching_plan_file in _xlsx_iterator(teaching_plan_dir):
        new_data = tp_importer.import_data(teaching_plan_file)
        _merge_dict(new_data, imported_datas)
    for teaching_plan_file in teaching_plan_files:
        new_data = tp_importer.import_data(teaching_plan_file)
        _merge_dict(new_data, imported_datas)
    print(imported_datas)
