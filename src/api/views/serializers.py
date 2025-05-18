from rest_framework import serializers
import pandas
from openpyxl.utils.exceptions import InvalidFileException


class ExcelFileSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False)

    def validate_files(self, value):
        validated_files = []
        for file in value:
            try:
                validated_files.append(pandas.read_excel(file, sheet_name=None))
            except (ValueError, InvalidFileException) as e:
                raise serializers.ValidationError(
                    f"Invalid file format: {file.name}. Please upload a valid Excel file."
                ) from e
        return validated_files
