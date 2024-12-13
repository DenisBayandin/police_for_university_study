Создать database.
Установить библиотеку poetry для управления зависимостями в проекте Python: pipx install poetry
Ввести в terminal: poetry install
Создать файл - .env
Ввести туда:
DBNAME = созданная database на шаге 1
DBUSER = имя пользователя базы данных
DBPASSWORD = пароль для доступа к базе данных
Вводим для запуска проекта: poetry run python -m main.py
