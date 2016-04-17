from list_user_stories import RallyListUserStories


def get_help(access_token, user_name, *args):
    data = []
    for cmd_name, command in RALLY_COMMANDS.iteritems():
        if cmd_name == "help":
            continue
        data.append({
            "title": cmd_name,
            "text": command.help(),
            "mrkdwn_in": ["text"],
        })
    return data


def get_command(command):
    return RALLY_COMMANDS[command]


DEFAULT_COMMAND = "help"
RALLY_COMMANDS = {
    "help": get_help,
    "us": RallyListUserStories()
}
