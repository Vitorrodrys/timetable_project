# Excel Importers

This module implements Excel importers to make it easier to import data such as course
curricula, teaching plans, and time slot schemas (the time slot schemas importer is not implemented yet).

The `base.py` file defines a minimal interface for creating new importers, along with some basic methods
that any importer subclass can use.

There are two example Excel files in this directory that demonstrate the basic format required
by the importers: `course_curriculum_example.xlsx` and `teaching_plan.xlsx`.
