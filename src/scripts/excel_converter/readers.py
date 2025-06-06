from datetime import datetime
from itertools import zip_longest
from pathlib import Path
import re

import pandas

from core.types import Discipline, Environment, SchoolGroup, Teacher
from scripts.excel_converter import utils


def _get_course_name(df: pandas.DataFrame) -> str:
    course_line = df.iloc[6, 1]
    regex = re.compile(r".+ +\- +(.+)")
    match_result = regex.search(course_line)
    if match_result:
        return match_result.group(1).strip()
    else:
        raise ValueError("Could not extract course name from the provided DataFrame.")


def read_course_curriculum(file: Path) -> list[Discipline]:
    df = pandas.read_excel(file)
    utils.remove_na(df)
    course_name = _get_course_name(df)
    df = utils.make_subdf(df, 9)
    utils.fix_column_names(df)
    df = utils.merge_duplicated_columns(df, utils.MergeStrategy.FIRST_NON_EMPTY)
    headers = {"CÓD.", "DISCIPLINA", "CH"}
    disciplines_iter = utils.strip_iterator(df, "CÓD.", "DISCIPLINA", "CH")
    disciplines = []
    for code, disc, ch in disciplines_iter:
        if not code or not disc or not ch:
            continue
        if headers & {code, disc, ch}:
            continue
        disciplines.append(
            Discipline(code=code, name=disc, workload=int(ch), course=course_name)
        )
    return disciplines


def read_teaching_plan(
    file: Path,
) -> tuple[list[Environment], list[SchoolGroup], list[Teacher]]:
    df = pandas.read_excel(file, sheet_name=None)
    school_group_sheet = next(
        (sname for sname in df if "Disciplinas oferta" in sname), None
    )
    if not school_group_sheet:
        raise ValueError("No valid sheet found in the teaching plan file.")
    school_group_df = df[school_group_sheet]
    teacher_and_environment_sheet = df.get("NÃO DELETAR", None)
    if teacher_and_environment_sheet is None:
        raise ValueError("No 'NÃO DELETAR' sheet found in the teaching plan file.")
    utils.fix_column_names(school_group_df)
    utils.fix_column_names(teacher_and_environment_sheet)
    utils.remove_na(school_group_df)
    utils.remove_na(teacher_and_environment_sheet)
    sg_df_iter = utils.strip_iterator(school_group_df, "TURMA")
    env_df_iter = utils.strip_iterator(teacher_and_environment_sheet, "AMBIENTE")
    teachers_df = teacher_and_environment_sheet["PROFESSORES"]
    teachers_df.columns = teachers_df.iloc[0].to_list()
    teachers_iter = utils.strip_iterator(
        teachers_df, "SIAPE", "NOME", "SOBRENOME", "DEPARTAMENTO"
    )
    environments = []
    school_groups = []
    teachers = []
    for school_group, environment, teacher_datas in zip_longest(
        sg_df_iter, env_df_iter, teachers_iter
    ):
        if school_group:
            school_group = (
                school_group.strftime("%Y.%m")
                if isinstance(school_group, datetime)
                else school_group
            )
            school_groups.append(SchoolGroup(school_group))
        if environment:
            environments.append(Environment(environment))
        if teacher_datas:
            tcod, tname, tlastname, dep = teacher_datas
            teacher = Teacher(cod=tcod, name=tname, last_name=tlastname, depart=dep)
            teachers.append(teacher)
    return environments, school_groups, teachers
