from django import get_version

"""
    Для проверки версии, и что все корректно установлено
    Или в терминале:
    py -m django version

    Создание проекта: 
    django-admin startproject <project_name>

    Запуск сервера:
    py manage.py runserver <host>:<port>
        <host>: [0-255].[0-255].[0-255].[0-255]

    Создание приложения:
    py manage.py startapp <application_name>

    Выполнение миграций:
    py manage.py migrate 
"""

print(get_version())