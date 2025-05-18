from django.urls import path

from .views import (
    CourseCurriculumViewSet,
    TeachingPlanViewSet
)

urlpatterns = [
    path("course-curriculum/", CourseCurriculumViewSet.as_view(), name="course_curriculum"),
    path("teaching-plan/", TeachingPlanViewSet.as_view(), name="teaching_plan"),
]
