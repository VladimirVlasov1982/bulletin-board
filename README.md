# Курсовая работа 6. Доска объявлений
***
### Подготовка проекта
Перейдите в папку market-postgres и выполните команду: 
```
docker-compose up --build -d
```
Перейдите в папку skymarket

Для начала нужно создать необходимые таблицы в базе данных с помощью команды:
```
python manage.py migrate
```
Затем загрузить фикстуры:
```
python manage.py loadall
```
Запустить сервер:
```
python manage.py runserver
```

