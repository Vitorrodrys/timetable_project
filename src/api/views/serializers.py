from rest_framework import serializers
import pandas
from openpyxl.utils.exceptions import InvalidFileException


class ExcelFileSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False)

    def validate_files(self, value):
        validated_files = []
        for file in value:
            try:
                # only validate if the file is a valid Excel file
                pandas.read_excel(file, sheet_name=None)
                validated_files.append(file)
            except (ValueError, InvalidFileException) as e:
                raise serializers.ValidationError(
                    f"Invalid file format: {file.name}. Please upload a valid Excel file."
                ) from e
        return validated_files
