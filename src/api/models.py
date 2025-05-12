from django.db import models

class Professor(models.Model):
    """
    Represents a professor responsible for teaching subjects.
    """
    name: str = models.CharField(max_length=100)

class Course(models.Model):
    """
    Represents an academic course (e.g., Computer Science, Mechanical Engineering).
    """
    name: str = models.CharField(max_length=100)

class CourseSection(models.Model):
    """
    Represents a specific section or group within a course (e.g., "Class A", "Evening Group").
    """
    name: str = models.CharField(max_length=100)
    course: Course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Subject(models.Model):
    """
    Represents a subject taught within a course section (e.g., "Mathematics I", "Algorithms").
    """
    name: str = models.CharField(max_length=100)
    professor: Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course_section: CourseSection = models.ForeignKey(CourseSection, on_delete=models.CASCADE)

class Environment(models.Model):
    """
    Represents an environment a subject is taught in (e.g., "Room 101", "Lab A").
    """
    name: str = models.CharField(max_length=100)

