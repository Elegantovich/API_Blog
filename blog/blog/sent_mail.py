from django.core.mail import send_mail


def send_message_to_mail(email, first_name, last_post):
    "Отправка письма с уникальным кодом новому пользователю."

    posts = [post for post in last_post]
    send_mail(
        subject='Новый пост',
        message=f'Здравствуйте {first_name}!'
                f'Ознакомьтесь с последними постами!'
                f'Ссылка на пост "posts/{posts[0].id}"'
                f'Ссылка на пост "posts/{posts[1].id}"'
                f'Ссылка на пост "posts/{posts[2].id}"'
                f'Ссылка на пост "posts/{posts[3].id}"'
                f'Ссылка на пост "posts/{posts[4].id}"',
        from_email='mail-service@yambd.qwerty',
        recipient_list=[email],
    )
