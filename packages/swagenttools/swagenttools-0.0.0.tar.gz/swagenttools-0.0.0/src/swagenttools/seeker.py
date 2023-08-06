import random
import requests

class UserAgent():
    def __init__(self, browser) -> None:
        self.path = "user_agent_list/{}.txt".format(browser)
        self.user_agents = open(self.path).read().splitlines()

    def random_agent(self):
        return random.choice(self.user_agents)

class Seeker():
    def __init__(self, userAgent, pageSize=10, playerName="") -> None:

        # static url where replays are found
        self.url = "https://m.swranking.com/api/player/replayallist"

        # this is the definitions of the query. player is almost always empty
        self.querystring = {
            "pageSize": pageSize,
            "playerName": playerName
        }

        # header will be sent with a specified User-Agent.
        self.headers = {
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,es-US;q=0.6,es;q=0.5",
            'Authentication': "null",
            'Connection': "keep-alive",
            'Referer': "https://m.swranking.com/",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-origin",
            'User-Agent': userAgent,
            }

    def get_matches(self):
        try:
            r = requests.request("GET", self.url, data="", headers=self.headers, params=self.querystring).json()
        except Exception as error:
            print('Error encounterd when requesting data, ', error)
        return r



if __name__ == '__main__':
    ua = UserAgent('Firefox').random_agent()
    seeker = Seeker(ua)
    print(seeker.get_matches())
