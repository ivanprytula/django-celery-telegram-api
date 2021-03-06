import telegram
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.template.loader import render_to_string

from .models import Post

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("^^^ The sample task just ran. ^^^")


@shared_task
def post_unpublished_to_telegram():
    fresh_posts = Post.objects.filter(is_published_to_telegram=False)

    if fresh_posts:
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
                return True
            except Exception as common_exec:
                raise telegram.error.TelegramError(
                    'Something is wrong with Telegram '
                    'channel.') from common_exec
    return False
