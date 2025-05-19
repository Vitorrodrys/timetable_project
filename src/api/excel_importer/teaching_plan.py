import logging
from typing import IO

from django.db import transaction
from openpyxl.utils.exceptions import InvalidFileException
import pandas

from api import models

from .base import ExcelImporter


class TeachingPlanImporter(ExcelImporter):
    def __environments_atomic_import(self, teaching_plan: pandas.DataFrame):
        for environment in teaching_plan["AMBIENTE"]:
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

    def __professor_atomic_import(self, teaching_plan: pandas.DataFrame):
        professors_df = teaching_plan["PROFESSORES"]
        new_headers = professors_df.iloc[0]
        professors_df = professors_df[1:].copy()
        professors_df.columns = new_headers
        for professor_name in professors_df["NOME COMPLETO"]:
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

    def __teaching_plan_atomic_import(self, teaching_plan: pandas.DataFrame):
        iterator = zip(teaching_plan["COD. DISCIPLINA"], teaching_plan["PROFESSOR"])
        for discipline_code, professor in iterator:
            discipline_code = discipline_code.strip()
            professor = professor.strip()
            if discipline_code == "" or professor == "":
                continue

            db_discipline = models.Discipline.objects.filter(
                code=discipline_code
            ).first()
            logging.debug(
                "Assigning professor %s to discipline %s", professor, discipline_code
            )
            if not db_discipline:
                logging.warning(
                    "Discipline %s not found in the database.", discipline_code
                )
                raise ValueError(f"Discipline {discipline_code} not found.")
            db_professor, _ = models.Professor.objects.get_or_create(
                name=professor,
                defaults={
                    "name": professor,
                },
            )
            db_discipline.professor = db_professor
            db_discipline.save()

    def import_data(self, readbable_buffer: IO[bytes]) -> tuple[bool, str]:
        """
        Import the teaching plan from an excel file.

        The teaching plan file specifies the disciplines that each professor
        will teach in a given semester.
        """
        teaching_plan = pandas.read_excel(readbable_buffer, sheet_name=None)
        self._remove_na(teaching_plan)
        try:
            self._fix_column_names(teaching_plan["NÃO DELETAR"])
            self._fix_column_names(teaching_plan["Disciplinas oferta 2024.1"])
            with transaction.atomic():
                self.__environments_atomic_import(teaching_plan["NÃO DELETAR"])
                self.__professor_atomic_import(teaching_plan["NÃO DELETAR"])
                self.__teaching_plan_atomic_import(
                    teaching_plan["Disciplinas oferta 2024.1"]
                )
                return True, "Teaching plan imported successfully."
        except KeyError as e:
            logging.error("KeyError: %s", e)
            return False, "Invalid file format. Please check the file."
        except ValueError as e:
            return False, str(e)
        except InvalidFileException:
            return (
                False,
                f"Invalid file format: {readbable_buffer.name}, please check the file",
            )
