# API_Blog
Api service for blog

### Tech
Python 3.7, Django 3.2, Rest Framework 3.13, Docker, Postman

## Описание.

Проект **API_Blog** является REST API для приложения формата соц. сети с пользователями, блогами и постами.

## Установка на локальном компьютере.
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

### Установка Docker.
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта.
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/Elegantovich/API_Blog/`
- Перейдите в папку 'infra' `cd infra`
- Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432 
DJANGO_KEY='your_key'
```
Запустите docker-compose:
```
docker-compose up -d --build
```
Накатите миграции:
```
docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Соберите статику в единую папку:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Создать пользователя можно через джанго-админгу
```
http//localhost/admin/
```
Создать необходимое количество объектов модели можно набором команд:
- зайдите в web контейнер:
```
docker exec -it <id_container> bash
```
- запустите shell:
```
python manage.py shell
```
- установите mixer:
```
pip install mixer
```
- импортируйте необходимый объект
```
from mixer.backend.django import mixer
```
- создайте необходимое количество объектов любой модели
```
posts = mixer.cycle(<количество объекто>).blend('api.<models_name>')
```
- можно выходить
```
exit()
```
Для дампа БД необходимо находится в диретории API_Blog.blog и ввести команду:
```
./manage.py dumpdata > db.json
```
### Важно знать.
Для работы с приложением необходимо:
- создать пользователя в джанго-админке
- пройти авторизацию посредством получения Bearer токена, срок годности которого 1 сутки
- в момент получения токена за созданным ранее пользователем закрепится блог
- описание блога и посты можно добавить по endpoints ниже
- настроена система пермишенов, которая не позволить не автору блога или поста изменять его
- пермишены отключены на авторизации, для беспрепятственного получения токена
- на блоги можно подписываться и отписывать
- в случае подписки, подсты блога можно посмотреть на отдельной странице news
- посты можно помечать прочитанными. Отображение только на странице news
Поддерживаемы endpoints:

| URL| method | Description |
| ------ | ------ | ------ |
| http://localhost/api/auth/token/login/ | POST | Получить токен |
| http://localhost/api/blogs/ | GET | Получить список блогов |
| http://localhost/api/blogs/<blog_id>/ | UPDATE, GET | Получить нужный блог и обновить описание своего |
| http://localhost/api/blogs/<blog_id>/subscribe/ | POST, DELETE | Подписаться и отписаться от блога |
| http://localhost/api/blogs/<blog_id>/posts/ | POST, GET | Создать пост или получить список постов блога |
| http://localhost/api/blogs/<blog_id>/posts/<post_id> | GET, UPDATE, DELETE | Получить нужный пост, обновить или удалить пост своего блога |
| http://localhost/api/news/ | GET | Получить посты из блогов на которые пользователь ранее подписался |
| http://localhost/api/news/<post_id>/read/ | POST, DELETE | Пометить пост прочитанным или нет |

### Авторы

[Хачатрян Максим](https://github.com/Elegantovich)<br>
