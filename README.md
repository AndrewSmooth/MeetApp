Чтобы запустить проект нужно:
1) Клонировать репозиторий, установить питон и необходимые библиотеки
2) Создать базу данных и подключить её
3) Запустить проект

1) Клонируем репозиторий в нужную папку командой git clone
   Устанавливаем python и библиотеки: pip install -r requirements.txt
2) Установим всё для БД: 
sudo apt update
sudo apt install python3-pip python3-dev 
libpq-dev postgresql postgresql-contrib

создадим БД: 
sudo -u postgres psql
CREATE DATABASE myproject;

Создадим пользователя:
CREATE USER myprojectuser WITH PASSWORD 'password';

Изменим несколько параметров:
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';

Дадим привелении:
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;

В файле "settings.py" добавим в настройке DATABASES -> default -> ENGINE: django.db.backends.postgresql

Создадим миграции: 
cd ~/myproject
python manage.py makemigrations
python manage.py migrate

Создадим суперпользователя: 
python manage.py createsuperuser

Теперь можно запустить проект:
Для этого сначала создадим переменные окружения в консоли:
export USER_PASSWORD="password"
export SECRET_KEY="daskflfe7a90fue89fu0few89fh0ew9fh"
export EMAIL_HOST_PASSWORD="gegegegege232r"

Затем, находясь в корне проекта, зайдем в виртуальное окружение и запустим приложение на порте 9000
source meetappenv/bin/activate
cd meetapp
python3 manage.py runserver 9000

   
