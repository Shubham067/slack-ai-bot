import slacky
from celery import shared_task

from . import utils

@shared_task
def slack_message_task(message, channel_id=None, user_id=None, thread_ts=None):
    gemini_response = utils.chat_with_gemini(message, model="gemini-1.5-flash-8b")
    response = slacky.send_message(gemini_response, channel_id=channel_id, user_id=user_id, thread_ts=thread_ts)

    return response.status_code