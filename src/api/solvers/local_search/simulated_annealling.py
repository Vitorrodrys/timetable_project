from api.models import Course, Discipline, Environment
from api.solvers.solution import Solution

from .local_search import LocalSearch


class SA(LocalSearch):
    def improve(
        self,
        current_sol: Solution,
        courses: list[Course],
        disciplines: list[Discipline],
        environments: list[Environment],
    ) -> Solution:
        pass
