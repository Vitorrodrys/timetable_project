from typing import NamedTuple, NewType


class Discipline(NamedTuple):
    code: str
    name: str
    workload: int
    course: str


class Teacher(NamedTuple):
    cod: str
    depart: str
    name: str
    last_name: str


Environment = NewType("Environment", str)
SchoolGroup = NewType("SchoolGroup", str)
