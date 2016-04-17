import requests
from pyral import Rally
from settings import RallyConfig

DEFAULT_COMMAND = 'us'

RALLY_COMMANDS = {
    'us': 'get_user_stories',
}


def get_rally_user_info(access_token):
    response = requests.get(RallyConfig.USER_URL,
                            headers={"zsessionid": access_token})
    if response.ok:
        return response.json()
    else:
        return response.errors()


def get_user_stories(access_token, user_name):
    rally = Rally(apikey=access_token, user=user_name)
    data = []
    query = "Owner = {}".format(user_name)
    result = rally.get("HierarchicalRequirement", fetch=True, query=query)
    for item in result:
        project = getattr(item, "Project")
        us_link = "{}/#/{}/detail/userstory/{}".format(
            RallyConfig.RALLY_URL, getattr(project, 'oid'),
            getattr(item, "oid"))
        data.append("{} {} {}".format(getattr(item, "FormattedID"),
                                      getattr(item, "Name"), us_link))
    return data
