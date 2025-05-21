from abc import ABC, abstractmethod

from api.models import Course, Discipline, Environment
from api.solvers.local_search import LocalSearch
from api.solvers.solution import Solution


class ConstructiveSolver(ABC):
    @abstractmethod
    def build(
        self,
        courses: list[Course],
        disciplines: list[Discipline],
        environments: list[Environment],
        *,
        local_search: LocalSearch | None = None,
    ) -> Solution:
        pass
