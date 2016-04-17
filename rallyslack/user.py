from db import redis_connection

SLACK_USER_INFO = ["name", "deleted", "is_bot"]
SLACK_USER_PROFILE = ["first_name", "last_name", "real_name",
                      "real_name_normalized", "email"]

RALLY_USER_INFO = ["UserName", "EmailAddress"]


def get_user_key(team_id, user_id):
    return "{}_{}".format(team_id, user_id)


def get_rally_user_token(user_key):
    return redis_connection.hget(user_key, "rally_access_token")


def get_rally_user(user_key):
    return redis_connection.hget(user_key, "rally_UserName")


def update_slack_user_info(user_key, user_data):
    for k in SLACK_USER_INFO:
        redis_connection.hset(user_key, "slack_{}".format(k), user_data[k])
    for k in SLACK_USER_PROFILE:
        redis_connection.hset(user_key, "slack_{}".format(k),
                              user_data["profile"][k])


def is_user_exists(user_key):
    return redis_connection.exists(user_key)


def update_rally_user_token(user_key, token_data):
    for k in token_data.keys():
        redis_connection.hset(user_key, "rally_{}".format(k), token_data[k])


def update_rally_user_info(user_key, user_info):
    for k in RALLY_USER_INFO:
        redis_connection.hset(user_key, "rally_{}".format(k),
                              user_info["User"][k])
