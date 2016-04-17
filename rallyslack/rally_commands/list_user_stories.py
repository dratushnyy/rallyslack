from bs4 import BeautifulSoup
from pyral import Rally


class RallyListUserStories(object):
    RALLY_URL = "https://rally1.rallydev.com"
    ARGS = ["all", "completed", "accepted"]

    @staticmethod
    def _build_query(user_name, *args):
        query = ["Owner = {}".format(user_name),
                 "ScheduleState != \"Completed\"",
                 "ScheduleState != \"Accepted\""]
        return query

    def __call__(self, access_token, user_name, *args):
        rally = Rally(apikey=access_token, user=user_name)
        query = self._build_query(user_name, *args)
        result = rally.get("HierarchicalRequirement", fetch=True, query=query)
        data = []
        for item in result:
            project = getattr(item, "Project")
            project_link = "{}/#/{}/userstories".format(
                RallyListUserStories.RALLY_URL, getattr(project, "oid"))

            us_link = "{}/#/{}/detail/userstory/{}".format(
                RallyListUserStories.RALLY_URL, getattr(project, "oid"),
                getattr(item, "oid"))

            soup = BeautifulSoup(getattr(item, "Description"), "html.parser")
            data.append({
                "author_name": getattr(project, "Name"),
                "author_link": project_link,
                "title": "{} {}".format(getattr(item, "FormattedID"),
                                        getattr(item, "Name")),
                "title_link": us_link,
                "text": soup.get_text()
            })
        return data

    @staticmethod
    def help():
        return "List user stories. By default lists only \"Defined\"" \
               "and \"In Progress\".\n" \
               "*/rally us all* to list all user stories \n " \
               "*/rally us completed*  list only completed \n " \
               "*/rally us accepted* to list only accepted \n" \
               "*/rally us defined* to list defined \n " \
               "*/rally us progress* to list us in progress \n "
