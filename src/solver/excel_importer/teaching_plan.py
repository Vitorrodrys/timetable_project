import logging
from typing import IO, override

from openpyxl.utils.exceptions import InvalidFileException
import pandas

from .base import Importer



class TeachingPlanImporter(Importer):

    def __import_environments(self, teaching_plan: pandas.DataFrame) -> dict:
        environments_data = {}
        for environment in self._strip_iterator(teaching_plan, "AMBIENTE"):
            if environment == "":
                # Skip empty rows
                continue
            #Fow now we mapping the environment to itself, in the future,
            # maybe the information about the type of that environment (e.g, 
            # lab, room) maybe usefull
            environments_data[environment] = environment
            logging.debug("Importing environment: %s", environment)
        return environments_data

    def __import(self, disciplines_offered: pandas.DataFrame) -> dict:
        disc_offered_dict = {}
        iterator = self._strip_iterator(
            disciplines_offered,
            "COD. DISCIPLINA",
            "DISCIPLINA",
            "CH",
            "PROFESSOR"
        )
        for disc_code, disc, ch, professor in iterator:
            if '' in {disc_code, disc, ch, professor}:
                continue
            if disc_code in disc_offered_dict:
                logging.warning("duplicated disc %s in excel file", disc_code)
            disc_offered_dict[disc_code] = {
                "disc": disc,
                "ch": ch,
                "prof": professor
            }
        return disc_offered_dict

    @override
    def import_data(self, readable_buffer: IO[bytes]) -> dict:
        try:
            teaching_plan = pandas.read_excel(readable_buffer, sheet_name=None)
            self._remove_na(teaching_plan)
            self._fix_column_names(teaching_plan['NÃO DELETAR'])
            self._fix_column_names(teaching_plan["Disciplinas oferta 2024.1"])
            disc_offered = self.__import(teaching_plan["Disciplinas oferta 2024.1"])
            envs = self.__import_environments(teaching_plan["NÃO DELETAR"])
            return {
                "discs": disc_offered,
                "envs": envs
            }
        except KeyError as e:
            logging.error("KeyError: %s", e)
            raise ValueError("Invalid file format. Please check the file") from e
        except InvalidFileException as e:
            raise ValueError(
                f"Invalid file format: {readable_buffer.name}, please check the file"
            ) from e
