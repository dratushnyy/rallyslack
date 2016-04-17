import rally_commands
import requests
from rq.decorators import job

from db import redis_connection
from settings import RallyConfig
from settings import ApiConfig
from settings import SlackConfig
from user import get_user_key, update_slack_user_info, get_rally_user_token, \
    get_rally_user

import logging
logger = logging.getLogger(__name__)
logger.setLevel(ApiConfig.LOG_LEVEL)
logger.addHandler(logging.FileHandler(ApiConfig.WORKER_LOG_FILE))


def create_rally_access_token(user_id, team_id, reply_to):
    user_key = get_user_key(user_id, team_id)
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


def get_command_with_args(command_string):
    if not command_string:
        return rally_commands.DEFAULT_COMMAND, []
    command = command_string.split(" ")[0]
    command_args = command_string.split(" ")[1:]
    return command, command_args


@job(queue=ApiConfig.RQ_WORKER_QUEUE_NAME, connection=redis_connection)
def process_user_command(user_id, team_id, command_string, reply_to):
    user_key = get_user_key(user_id, team_id)
    rally_user = get_rally_user(user_key)
    rally_token = get_rally_user_token(user_key)
    cmd, command_args = get_command_with_args(command_string)
    if not rally_token:
        create_rally_access_token(user_id, team_id, reply_to)
    else:
        if cmd not in rally_commands.RALLY_COMMANDS.keys():
            return requests.post(reply_to, json={
                "text": ":confused: I am sorry, but I don't know what to do "
                        "with '{}'".format(cmd)
            })

    result = rally_commands.get_command(cmd)(rally_token, rally_user,
                                             command_args)
    requests.post(reply_to, json={"text": "Here you go:",
                                  "attachments": result
                                  })


def get_rally_user_info(access_token):
    response = requests.get(RallyConfig.USER_URL,
                            headers={"zsessionid": access_token})
    if response.ok:
        return response.json()
    else:
        return response.errors()
