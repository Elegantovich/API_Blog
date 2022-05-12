from django.core.mail import send_mail


def send_message_to_mail(email, username, last_post):
    "Отправка письма с уникальным кодом новому пользователю."

    posts = [post for post in last_post]
    send_mail(
        subject='Новый пост',
        message=f'Здравствуйте {username}!'
                'Ознакомьтесь с последними постами! '
                f'Ссылка /localhost/blog/{posts[0].blog.id}/{posts[0].id} '
                f'Ссылка /localhost/blog/{posts[1].blog.id}/{posts[1].id} '
                f'Ссылка /localhost/blog/{posts[2].blog.id}/{posts[2].id} '
                f'Ссылка /localhost/blog/{posts[3].blog.id}/{posts[3].id} '
                f'Ссылка /localhost/blog/{posts[4].blog.id}/{posts[4].id}',
        from_email='mail-service@yambd.qwerty',
        recipient_list=[email],
    )
