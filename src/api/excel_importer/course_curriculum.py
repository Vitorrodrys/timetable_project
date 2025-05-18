import logging
import re
from typing import IO

from django.db import transaction
import pandas

from api import models

from .base import ExcelImporter


class CourseCurriculumImporter(ExcelImporter):
    def __course_curriculum_atomic_import(
        self, course_curriculum: pandas.DataFrame
    ) -> None:
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
        course_curriculum.columns = [
            f"col{i}" for i in range(course_curriculum.shape[1])
        ]
        for _, row in course_curriculum.iterrows():
            discipline_code = row["col5"] or row["col6"] or ""
            discipline_name = row["col9"] or row["col10"] or ""
            discipline_workload = row["col11"] or row["col12"] or ""
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
                    "workload": discipline_workload,
                },
            )
            if created:
                logging.debug(
                    "Discipline %s - %s imported successfully.",
                    discipline_code,
                    discipline_name,
                )
            else:
                logging.debug(
                    "Discipline %s - %s already exists.",
                    discipline_code,
                    discipline_name,
                )

    def import_data(self, readbable_buffer: IO[bytes]) -> tuple[bool, str]:
        """
        Import the course curriculum from an excel file.

        The course curriculum is a file where is specified the disciplines
        of a specific course and class
        """
        course_curriculum = pandas.read_excel(readbable_buffer)
        try:
            with transaction.atomic():
                self.__course_curriculum_atomic_import(course_curriculum)
                return True, "Course curriculum imported successfully."
        except ValueError as e:
            return False, str(e)
