import logging
import re

from django.db import transaction
import pandas

from api import models

def _fix_column_names(df: pandas.DataFrame) -> None:
    new_cols = [next(column_name for column_name in df.columns if not re.match(r"Unnamed: \d+", column_name))]
    for col in df.columns[1:]:
        col = col.strip()
        if re.match(r"Unnamed: \d+", col):
            new_cols.append(new_cols[-1])
        else:
            new_cols.append(col)
    df.columns = new_cols


def _course_curriculum_atomic_import(course_curriculum: pandas.DataFrame):
    COURSE_CLASS_ROW = 6  # assuming the course and class name is in the 7th row
    FIRST_DISCIPLINE_ROW = 10  # assuming the first discipline is in the 11th row
    course_school_class_row = course_curriculum.iloc[COURSE_CLASS_ROW][1]
    regex_match = re.search(
        r"(?P<course_code>\w+)\s*-\s*(?P<course_name>.+)\s*(?P<semester_class>\d{4}\.\d)",
        course_school_class_row,
    )
    if not regex_match:
        raise ValueError("Invalid course and class format. Please check the file.")
    course_code = regex_match.group("course_code").strip()
    course_name = regex_match.group("course_name").strip()
    semester_class = regex_match.group("semester_class").strip()
    db_course, _ = models.Course.objects.get_or_create(
        code=course_code,
        defaults={
            "code": course_code,
            "name": course_name,
        },
    )
    db_class, _ = models.SchoolClass.objects.get_or_create(
        name=semester_class,
        defaults={
            "name": semester_class,
            "course": db_course,
        },
    )
    course_curriculum = course_curriculum.iloc[FIRST_DISCIPLINE_ROW:]
    course_curriculum.fillna("", inplace=True)
    course_curriculum.columns = [f"col{i}" for i in range(course_curriculum.shape[1])]
    for _, row in course_curriculum.iterrows():
        discipline_code = row['col5'] or row['col6'] or ""
        discipline_name = row['col9'] or row['col10'] or ""
        discipline_workload = row['col11'] or row['col12'] or ""
        discipline_code = discipline_code.strip()
        discipline_name = discipline_name.strip()
        if discipline_code == "" or discipline_name == "":
            # Skip empty rows
            continue
        if discipline_code == "CÓD." or discipline_name == "DISCIPLINA":
            # Skip header rows
            continue
        _, created = models.Discipline.objects.get_or_create(
            code=discipline_code,
            defaults={
                "code": discipline_code,
                "name": discipline_name,
                "school_class": db_class,
                "workload": discipline_workload
            },
        )
        if created:
            logging.debug("Discipline %s - %s imported successfully.", discipline_code, discipline_name)
        else:
            logging.debug("Discipline %s - %s already exists.", discipline_code, discipline_name)
    return True, "Course curriculum imported successfully."

def import_course_curriculum(course_curriculum: pandas.DataFrame) -> tuple[bool, str]:
    """
    Import the course curriculum from an excel file.

    The course curriculum is a file where is specified the disciplines
    of a specific course and class
    """
    try:
        with transaction.atomic():
            _course_curriculum_atomic_import(course_curriculum)
            return True, "Course curriculum imported successfully."
    except ValueError as e:
        return False, str(e)


def _environments_atomic_import(teaching_plan: pandas.DataFrame):
    for environment in teaching_plan['AMBIENTE']:
        environment = environment.strip()
        if environment == "":
            # Skip empty rows
            continue
        models.Environment.objects.get_or_create(
            name=environment,
            defaults={
                "name": environment,
            },
        )
        logging.debug("Importing environment: %s", environment)

def _professor_atomic_import(teaching_plan: pandas.DataFrame):
    professors_df = teaching_plan['PROFESSORES']
    new_headers = professors_df.iloc[0]
    professors_df = professors_df[1:].copy()
    professors_df.columns = new_headers
    for professor_name in professors_df['NOME COMPLETO']:
        professor_name = professor_name.strip()
        if professor_name == "":
            # Skip empty rows
            continue
        _, created = models.Professor.objects.get_or_create(
            name=professor_name,
            defaults={
                "name": professor_name,
            },
        )
        if created:
            logging.debug("Importing professor: %s", professor_name)

def _teaching_plan_atomic_import(teaching_plan: pandas.DataFrame):
    iterator = zip(
        teaching_plan['COD. DISCIPLINA'],
        teaching_plan['PROFESSOR']
    )
    for discipline_code, professor in iterator:
        discipline_code = discipline_code.strip()
        professor = professor.strip()
        if discipline_code == "" or professor == "":
            continue

        db_discipline = models.Discipline.objects.filter(code=discipline_code).first()
        logging.debug("Assigning professor %s to discipline %s", professor, discipline_code)
        if not db_discipline:
            logging.warning("Discipline %s not found in the database.", discipline_code)
            raise ValueError(f"Discipline {discipline_code} not found.")
        db_professor, _ = models.Professor.objects.get_or_create(
            name=professor,
            defaults={
                "name": professor,
            },
        )
        db_discipline.professor = db_professor
        db_discipline.save()
    return True, "Teaching plan imported successfully."


def import_teaching_plan(
    teaching_plan: pandas.DataFrame,
) -> tuple[bool, str]:
    """
    Import the teaching plan from an excel file.

    The teaching plan file specifies the disciplines that each professor
    will teach in a given semester.
    """
    for _, df in teaching_plan.items():
        df.fillna("", inplace=True)
    _fix_column_names(teaching_plan['NÃO DELETAR'])
    _fix_column_names(teaching_plan['Disciplinas oferta 2024.1'])
    try:
        with transaction.atomic():
            _environments_atomic_import(teaching_plan['NÃO DELETAR'])
            _professor_atomic_import(teaching_plan['NÃO DELETAR'])
            _teaching_plan_atomic_import(teaching_plan['Disciplinas oferta 2024.1'])
            return True, "Teaching plan imported successfully."
    except ValueError as e:
        return False, str(e)
