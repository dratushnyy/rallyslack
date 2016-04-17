from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from requests_oauthlib import OAuth2Session
from connection import process_user_command
from rally import get_rally_user_info
from settings import SlackConfig, ApiConfig, RallyConfig


from user import is_user_exists, update_rally_user_token, \
    update_rally_user_info

api = Flask(__name__, template_folder="../templates/")
api.secret_key = ApiConfig.SECRET_KEY

# TODO handle 404 as unknown command


@api.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if request.form.get('token') == SlackConfig.REQUEST_TOKEN:
            process_user_command.delay(request.form['user_id'],
                                       request.form['team_id'],
                                       request.form['text'],
                                       request.form['response_url'])
            return ApiConfig.QUICK_REPLY

    else:
        login_user = request.args.get(ApiConfig.LOGIN_PARAM_NAME)
        if is_user_exists(login_user):
            return render_template("rally_auth.html",
                                   rally_auth_url="/auth/rally/",
                                   login_user=login_user)

    return render_template("index.html")


@api.route("/auth/rally/", methods=["POST"])
def rally_auth():
    if request.method == "POST":
        rally_session = OAuth2Session(
            RallyConfig.OAUTH_CLIENT_ID,
            scope=[RallyConfig.SCOPE],
            redirect_uri=RallyConfig.OAUTH_CALLBACK_URL)

        rally_auth_url, state = rally_session.authorization_url(
            RallyConfig.AUTH_ENDPOINT)

        session["auth_state"] = state
        session['login_user'] = request.form.get("login_user")
        return redirect(rally_auth_url)
    return render_template("index.html")


@api.route("/auth/rally/callback/", methods=["GET"])
def rally_auth_callback():
    rally_session = OAuth2Session(RallyConfig.OAUTH_CLIENT_ID,
                                  redirect_uri=RallyConfig.OAUTH_CALLBACK_URL,
                                  state=session['auth_state'])

    token = rally_session.fetch_token(
        RallyConfig.TOKEN_ENDPOINT,
        client_secret=RallyConfig.OAUTH_CLIENT_SECRET,
        authorization_response=request.url.replace("http://", "https://"))

    login_user = session['login_user']
    update_rally_user_token(login_user, token)
    rally_user = get_rally_user_info(token.get('access_token'))
    update_rally_user_info(login_user, rally_user)
    session.clear()
    return render_template("commands.html")


if __name__ == '__main__':
    api.run(debug=ApiConfig.DEBUG, port=8000)
