from django import get_version

"""
    Для проверки версии, и что все корректно установлено
    Или в терминале:
    py -m django version

    Создание проекта: 
    django-admin startproject <project_name>
"""

print(get_version())