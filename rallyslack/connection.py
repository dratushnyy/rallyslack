import logging

import requests
from rq.decorators import job

import rally
from db import redis_connection
from settings import ApiConfig
from settings import SlackConfig
from user import get_user_key, update_slack_user_info, get_rally_user_token, \
    get_rally_user

logger = logging.getLogger(__name__)
logger.setLevel(ApiConfig.LOG_LEVEL)
logger.addHandler(logging.FileHandler(ApiConfig.WORKER_LOG_FILE))


@job(queue=ApiConfig.RQ_WORKER_QUEUE_NAME, connection=redis_connection)
def process_user_command(user_id, team_id, command, reply_to):
    user_key = get_user_key(user_id, team_id)
    rally_token = get_rally_user_token(user_key)
    command = command or rally.DEFAULT_COMMAND
    if not rally_token:
        response = requests.post(SlackConfig.USER_INFO_URL,
                                 data={'user': user_id,
                                       'token': SlackConfig.API_TOKEN})
        if response.ok:
            response_json = response.json()
            if not response_json["ok"]:
                logger.error(response_json)
                return requests.post(reply_to, json={
                    "text": "Sorry, something went wrong:",
                    "attachments": [{
                        "text": response_json["error"]
                    }]
                })
            else:
                update_slack_user_info(user_key, response_json['user'])
                return requests.post(reply_to, json={
                    "text": "Here is login link for you:",
                    "attachments": [{
                        "text": ApiConfig.RALLY_LOGIN_PAGE.format(user_key)
                    }]

                })
        else:
            logger.error(response.reason())
    else:
        if command not in rally.RALLY_COMMANDS.keys():
            return requests.post(reply_to, json={
                "text": ":confused: I am sorry, but I don't know what to do "
                        "with '{}'".format(command)
            })
    rally_user = get_rally_user(user_key)
    command = getattr(rally, rally.RALLY_COMMANDS[command])
    result = command(rally_token, rally_user)
    requests.post(reply_to, json={
        "text": "Here you go:",
        "attachments": [{
                "text": "\n".join(result)
            }]
    })
