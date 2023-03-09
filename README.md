# Библиотека 
## Stack :
* Python 3.10
* DRF 
* PostgreSQL 15.1
## Значение проекта :
 - Созданная библиотека позволяет создавать пользователя для приобретения книг в библиотеке (не более 3 штук);
 - Создание книг и авторов и связи между ними с помощью учетки администратора ( реализованы Permissions);
 ## Установка :
* Установить все зависимости : 
    `pip install requirements.txt `
* Бекап базы : 
 - `createdb -U username -T template0 newdb`
 - `pg_restore -U postgres -d newdb backupfile.dump`
 
 Где: `postgres` - имя пользователя базы данных PostgreSQL. `newdb` - имя новой базы данных PostgreSQL.
 
 ## Пользователи для тестирования
1. Username: admin, 
    password: admin - тестовый юзер админ
2. Username: reader_test, password: reader_test - тестовый юзер читателя

### Для заполнения базы тестовыми данными:
 - `python manage.py populate_db --authors=10 --books=20 --readers=10`


Где `authors` - кол-во авторов, `books` - кол-во книг, `readers` - кол-во читателей
