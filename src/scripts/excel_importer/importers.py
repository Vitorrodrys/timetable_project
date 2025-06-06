import json
from pathlib import Path
from typing import Any

import pandas

from core.types import Discipline, Environment, SchoolGroup, Teacher


def _read_if_exists(fp: Path) -> dict[str, Any]:
    if fp.exists():
        return json.loads(
            fp.read_text(encoding="utf-8"),
            object_hook=lambda d: {int(k): v for k, v in d.items()},
        )
    return {}


def import_school_class(fp: Path, outfile: Path, *json_args, **json_kwargs):
    sc_datas = _read_if_exists(outfile)

    df = pandas.read_excel(fp)
    for sc in df["school_group"]:
        if sc not in sc_datas:
            sc_datas[len(sc_datas) + 1] = SchoolGroup(sc)
    outfile.write_text(
        json.dumps(sc_datas, *json_args, **json_kwargs), encoding="utf-8"
    )


def import_environment(fp: Path, outfile: Path, *json_args, **json_kwargs):
    env_datas = _read_if_exists(outfile)

    df = pandas.read_excel(fp)
    for env in df["environment"]:
        if env not in env_datas:
            env_datas[len(env_datas) + 1] = Environment(env)
    outfile.write_text(
        json.dumps(env_datas, *json_args, **json_kwargs), encoding="utf-8"
    )


def import_professor(fp: Path, outfile: Path, *json_args, **json_kwargs):
    prof_datas = _read_if_exists(outfile)

    df = pandas.read_excel(fp)
    for code, depart, name, last_name in df[
        ["code", "depart", "name", "last_name"]
    ].values:
        teacher = Teacher(cod=code, depart=depart, name=name, last_name=last_name)
        if teacher not in prof_datas:
            prof_datas[len(prof_datas) + 1] = teacher
    outfile.write_text(
        json.dumps(prof_datas, *json_args, **json_kwargs), encoding="utf-8"
    )


def import_discipline(fp: Path, outfile: Path, *json_args, **json_kwargs):
    disc_datas = _read_if_exists(outfile)

    df = pandas.read_excel(fp)
    for code, name, workload, course in df[
        ["code", "name", "workload", "course"]
    ].values:
        discipline = Discipline(code=code, name=name, workload=workload, course=course)
        if discipline not in disc_datas:
            disc_datas[len(disc_datas) + 1] = discipline
    outfile.write_text(
        json.dumps(disc_datas, *json_args, **json_kwargs), encoding="utf-8"
    )
