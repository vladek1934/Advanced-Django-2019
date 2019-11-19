import os
from django.core.exceptions import ValidationError
from datetime import date

from Initial import settings

ALLOWED_EXTS = ['.jpg', '.png', '.docx', '.pdf']


def validate_file_size(value):
    if value.size > 1000000:
        raise ValidationError('max file size: 1Mb')


def validate_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in ALLOWED_EXTS:
        raise ValidationError(f'not allowed file ext, allowed: {ALLOWED_EXTS}')


def task_document_path(instance, filename):
    return f'tasks/{date.today()}/{filename}'


# def task_delete_path(document):
#     file_path = document.path
#     if os.path.isfile(file_path):
#         os.remove(file_path)


def task_delete_path(document):
    print(document.document)
    file_path = os.path.join(settings.MEDIA_ROOT, document.document.name)
    print(file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
