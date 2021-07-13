import telegram
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string

from .models import Post


@shared_task
def add(x_var, y_var):
    return x_var + y_var


@shared_task
def print_hello_every_1_min():
    print('Hello from periodic task by Celery beat___')


@shared_task
def post_unpublished_to_telegram():
    fresh_posts = Post.objects.filter(is_published_to_telegram=False)

    if not fresh_posts:
        pass
    else:
        telegram_settings = settings.TELEGRAM_API
        bot = telegram.Bot(token=telegram_settings['bot_token'])

        for fresh_post in fresh_posts:
            msg_html = render_to_string('telegram_post_template.html',
                                        {'post': fresh_post})

            try:
                bot.send_message(
                    chat_id=f'@{telegram_settings["channel_name"]}',
                    text=msg_html, parse_mode=telegram.ParseMode.HTML)
                fresh_post.is_published_to_telegram = True
                fresh_post.save()
            except Exception:
                raise telegram.error.TelegramError(
                    'Something is wrong with Telegram '
                    'channel.')
