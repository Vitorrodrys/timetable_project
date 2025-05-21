from abc import ABC, abstractmethod

from api.models import Course, Discipline, Environment
from api.solvers.solution import Solution


class LocalSearch(ABC):
    @abstractmethod
    def improve(
        self,
        current_sol: Solution,
        courses: list[Course],
        disciplines: list[Discipline],
        environments: list[Environment],
    ) -> Solution:
        pass
