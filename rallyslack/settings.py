import os
import logging


class ApiConfig(object):
    DEBUG = True
    SECRET_KEY = ""
    API_HOST = ""
    QUICK_REPLY = ":timer_clock:"
    RQ_WORKER_QUEUE_NAME = 'rallyslack'
    LOGIN_PARAM_NAME = "login_me"
    RALLY_LOGIN_PAGE = "{}/?{}={{}}".format(API_HOST, LOGIN_PARAM_NAME)
    LOG_LEVEL = logging.DEBUG
    WORKER_LOG_FILE = os.path.join(os.path.abspath(__file__),
                                   "../../",
                                   "logs",
                                   "rq_worker.log")


class SlackConfig(object):
    REQUEST_TOKEN = ""
    API_TOKEN = ""
    USER_INFO_URL = "https://slack.com/api/users.info"


class RallyConfig(object):
    SCOPE = "alm"
    OAUTH_CLIENT_ID = ""
    OAUTH_CLIENT_SECRET = ""
    RALLY_URL = "https://rally1.rallydev.com"
    AUTH_ENDPOINT = "{}/login/oauth2/auth".format(RALLY_URL)
    TOKEN_ENDPOINT = "{}/login/oauth2/token".format(RALLY_URL)
    OAUTH_CALLBACK_URL = "{}/auth/rally/callback/".format(ApiConfig.API_HOST)
    USER_URL = "{}{}".format(RALLY_URL, "/slm/webservice/v2.x/user")
    STORIES_URL = "{}{}".format(RALLY_URL,
                                "/slm/webservice/v2.x/hierarchicalrequirement")


# RQ Workers and jobs section
REDIS_URL = 'redis://127.0.0.1:6379'
QUEUES = [ApiConfig.RQ_WORKER_QUEUE_NAME]
