# from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import slacky

from .tasks import slack_message_task

@csrf_exempt
@require_POST
def slack_events_endpoint(request):
    json_data = {}
    allowed_data_type = ["url_verification", "event_callback"]

    try:
        json_data = json.loads(request.body.decode("utf-8"))
    except Exception as e:
        pass

    data_type = json_data.get("type")

    if data_type not in allowed_data_type:
        return HttpResponse("Not Allowed", status=400)

    if data_type == "url_verification":
        challenge = json_data.get("challenge")

        if challenge is None:
            return HttpResponse("Not Allowed", status=400)
        return HttpResponse(challenge, status=200)
    elif data_type == "event_callback":
        event = json_data.get("event") or {}

        try:
            message = event["blocks"][0]["elements"][0]["elements"][1]["text"]
        except:
            message = " ".join(event.get("text").split()[1:])

        channel_id = event.get("channel")
        user_id = event.get("user")
        message_timestamp = event.get("ts")
        thread_timestamp = event.get("thread_ts") or message_timestamp

        # response = slacky.send_message(message, channel_id=channel_id, user_id=user_id, thread_ts=thread_timestamp)
        # slack_message_task.delay(message, channel_id=channel_id, user_id=user_id, thread_ts=thread_timestamp)
        slack_message_task.apply_async(
            kwargs = {
                "message": message,
                "channel_id": channel_id,
                "user_id": user_id,
                # "thread_ts": thread_timestamp
            },
            countdown = 0
        )

        return HttpResponse("Success", status=200)
    return HttpResponse("Success", status=200)
