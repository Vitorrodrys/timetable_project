from abc import ABC, abstractmethod

from api.models import Course, Discipline, Environment

from .solution import Solution

class Solver(ABC):

    @abstractmethod
    def solve(
        self,
        courses: list[Course],
        disciplines: list[Discipline],
        environments: list[Environment],
    ) -> Solution:
        """
        Should calculate and return a timetable solution
        based on the given courses, disciplines and environments.
        """
