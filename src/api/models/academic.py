from django.db import models


class Professor(models.Model):
    name: str = models.CharField(max_length=100, unique=True)


class Course(models.Model):
    code: str = models.CharField(max_length=15, unique=True)
    name: str = models.CharField(max_length=100, unique=True)


class SchoolClass(models.Model):
    name: str = models.CharField(max_length=15)
    course: Course = models.ForeignKey(Course, on_delete=models.RESTRICT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "course"], name="unique_class_per_course")
        ]


class Discipline(models.Model):
    code = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    workload = models.IntegerField()
    professor = models.ForeignKey(
        Professor, on_delete=models.RESTRICT, null=True, blank=True
    )
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.RESTRICT
    )
