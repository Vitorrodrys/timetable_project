from api.models import Course, Discipline, Environment

from .solution import Solution
from .solver import Solver



class ACO(Solver):

    def __init__(
        self,
        local_search: Solver | None
    ):
        super().__init__()
        self.__local_search = local_search

    def solve(
        self,
        courses: list[Course],
        disciplines: list[Discipline],
        environments: list[Environment],
    ) -> Solution:
        pass
