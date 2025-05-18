from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.utils import excel_handler

from .serializers import ExcelFileSerializer


class CourseCurriculumViewSet(GenericAPIView):
    serializer_class = ExcelFileSerializer
    parser_classes = [MultiPartParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "binary",
                        },
                    },
                },
                "required": ["files"],
            }
        },
        responses={200: dict},
        description="Upload one or more course curriculums through Excel files.",
    )
    def post(self, request, *_, **__):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_curriculums = serializer.validated_data["files"]
        errors = []
        for filename, curriculum in course_curriculums:
            imported, import_status = excel_handler.import_course_curriculum(
                curriculum["Sheet"]
            )
            if not imported:
                errors.append((filename, import_status))
        if errors:
            error_messages = [
                f"File: {file_name} - Error: {error}" for file_name, error in errors
            ]
            return Response(
                {"message": "Errors occurred during import.", "errors": error_messages},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Files uploaded successfully."}, status=status.HTTP_200_OK
        )


class TeachingPlanViewSet(GenericAPIView):
    serializer_class = ExcelFileSerializer
    parser_classes = [MultiPartParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "binary",
                        },
                    },
                },
                "required": ["files"],
            }
        },
        responses={200: dict},
        description="Upload a course curriculum through an Excel file.",
    )
    def post(self, request, *_, **__):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teaching_plans = serializer.validated_data["files"]
        errors = []
        for filename, teaching_plan in teaching_plans:
            imported, import_status = excel_handler.import_teaching_plan(teaching_plan)
            if not imported:
                errors.append((filename, import_status))
        if errors:
            error_messages = [
                f"File: {file_name} - Error: {error}" for file_name, error in errors
            ]
            return Response(
                {"message": "Errors occurred during import.", "errors": error_messages},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Files uploaded successfully."}, status=status.HTTP_200_OK
        )
