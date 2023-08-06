#!/usr/bin/env python3
from json import loads, dumps
from re import compile
import requests
import logging
import secrets
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


# Masterlist API Docs: https://docs.altv.mp/articles/master_list_api.html

# This is the config object for this package
# Here can you configure stuff like the api endpoint or the url format
class Config:
    base_link = "https://api.altv.mp"
    all_server_stats_link = f"{base_link}/servers"
    all_servers_link = f"{base_link}/servers/list"
    server_link = f"{base_link}/server" + "/{}"
    server_average_link = f"{base_link}/avg" + "/{}/{}"
    server_max_link = f"{base_link}/max" + "/{}/{}"


logging.debug(f'starting with base link: {Config.base_link}')


# This is the server object
class Server:
    # initialize the object with all values that are available in the alt:V masterlist API
    def __init__(self, active, id, maxPlayers, players, name, locked, host, port, gameMode, website, language,
                 description, verified, promoted, useEarlyAuth, earlyAuthUrl, useCdn, cdnUrl, useVoiceChat, tags,
                 bannerUrl, branch, build, version, lastUpdate):
        self.active = active
        self.id = id
        self.maxPlayers = maxPlayers
        self.players = players
        self.name = name
        self.locked = locked
        self.host = host
        self.port = port
        self.gameMode = gameMode
        self.website = website
        self.language = language
        self.description = description
        self.verified = verified
        self.promoted = promoted
        self.useEarlyAuth = useEarlyAuth
        self.earlyAuthUrl = earlyAuthUrl
        self.useCdn = useCdn
        self.cdnUrl = cdnUrl
        self.useVoiceChat = useVoiceChat
        self.tags = tags
        self.bannerUrl = bannerUrl
        self.branch = branch
        self.build = build
        self.version = version
        self.lastUpdate = lastUpdate

    # return the current server data as JSON object
    def get_json(self):
        return {
            "active": self.active,
            "id": self.id,
            "maxPlayers": self.maxPlayers,
            "players": self.players,
            "name": self.name,
            "locked": self.locked,
            "host": self.host,
            "port": self.port,
            "gameMode": self.gameMode,
            "website": self.website,
            "language": self.language,
            "description": self.description,
            "verified": self.verified,
            "promoted": self.promoted,
            "useEarlyAuth": self.useEarlyAuth,
            "earlyAuthUrl": self.earlyAuthUrl,
            "useCdn": self.useCdn,
            "cdnUrl": self.cdnUrl,
            "useVoiceChat": self.useVoiceChat,
            "tags": self.tags,
            "bannerUrl": self.bannerUrl,
            "branch": self.branch,
            "build": self.build,
            "version": self.version,
            "lastUpdate": self.lastUpdate
        }

    def __repr__(self):
        return self.get_json()

    def __str__(self):
        return dumps(self.__repr__())

    # fetch the server data and replace it
    def update(self):
        temp_server = get_server_by_id(self.id)

        # check if the server is returned
        if temp_server is None:
            # don`t update the server object because the API returned invalid, broken, or no data
            logging.warning(f"the alt:V API returned nothing.")
            return

        # check if the server is online
        if temp_server.active:
            # these values are only available when the server is online
            self.active = temp_server.active
            self.maxPlayers = temp_server.maxPlayers
            self.players = temp_server.players
            self.name = temp_server.name
            self.locked = temp_server.locked
            self.host = temp_server.host
            self.port = temp_server.port
            self.gameMode = temp_server.gameMode
            self.website = temp_server.website
            self.language = temp_server.language
            self.description = temp_server.description
            self.verified = temp_server.verified
            self.promoted = temp_server.promoted
            self.useEarlyAuth = temp_server.useEarlyAuth
            self.earlyAuthUrl = temp_server.earlyAuthUrl
            self.useCdn = temp_server.useCdn
            self.cdnUrl = temp_server.cdnUrl
            self.useVoiceChat = temp_server.useVoiceChat
            self.tags = temp_server.tags
            self.bannerUrl = temp_server.bannerUrl
            self.branch = temp_server.branch
            self.build = temp_server.build
            self.version = temp_server.version
            self.lastUpdate = temp_server.lastUpdate
        else:
            # set the server to be offline and the players to 0, because the server is offline
            self.active = False
            self.players = 0

    # use this function to fetch the server connect json
    # this file has every resource of the server with a hash and name
    def fetch_connect_json(self, proxy=None):
        if not self.useCdn and not self.locked and self.active:
            # This Server is not using a CDN.
            cdn_request = request(f"http://{self.host}:{self.port}/connect.json", True, self, proxy)
            if cdn_request is None:
                # possible server error or blocked by alt:V
                return None
            else:
                return cdn_request
        else:
            # let`s try to get the connect.json
            cdn_request = request(f"{self.cdnUrl}/connect.json", proxy=proxy)
            if cdn_request is None:
                # maybe the CDN is offline
                return None
            else:
                return cdn_request

    # get the "Direct Connect Protocol" url
    # e.g. altv://connect/127.0.0.1:7788?password=xyz
    # https://docs.altv.mp/articles/connectprotocol.html
    # cdn off: altv://connect/${IP_ADDRESS}:${PORT}?password=${PASSWORD}
    # cdn on: altv://connect/{CDN_URL}?password=${PASSWORD}
    def get_dtc_url(self, password=None):
        dtc_url = ""
        if self.useCdn:
            if not "http" in self.cdnUrl:
                dtc_url += f"altv://connect/http://{self.cdnUrl}"
            else:
                dtc_url += f"altv://connect/{self.cdnUrl}"
        else:
            dtc_url += f"altv://connect/{self.host}:{self.port}"

        if self.locked and password is None:
            logging.warning(
                "Your server is password protected but you did not supply a password for the Direct Connect Url.")

        if password is not None:
            dtc_url += f"?password={password}"

        return dtc_url

    # fetch the required and optional permissions of the server
    # available permissions:
    # Screen Capture: This allows a screenshot to be taken of the alt:V process (just GTA) and any webview
    # WebRTC: This allows peer-to-peer RTC inside JS
    # Clipboard Access: This allows to copy content to users clipboard
    def get_permissions(self, proxy=None):
        permissions = {
            "required": {
                "Screen Capture": False,
                "WebRTC": False,
                "Clipboard Access": False
            },
            "optional": {
                "Screen Capture": False,
                "WebRTC": False,
                "Clipboard Access": False
            }
        }

        # fetch connect json
        data = self.fetch_connect_json(proxy)
        if data is None:
            return None
        optional = data["optional-permissions"]
        required = data["required-permissions"]

        if optional is not []:
            for permission in optional:
                permissions["optional"][permission] = True

        if required is not []:
            for permission in required:
                permissions["required"][permission] = True

        return permissions

    def get_resource_size(self, resource, decimal=2, proxy=None):
        if self.useCdn:
            resource_url = f"{self.cdnUrl}/{resource}.resource"
        else:
            resource_url = f"http://{self.host}:{self.port}/{resource}.resource"

        data = requests.head(resource_url, headers={"User-Agent": "AltPublicAgent"}, timeout=60, proxies=proxy)

        if data.ok:
            return round((int(data.headers["Content-Length"]) / 1048576), decimal)
        else:
            return None


def request(url, cdn=False, server=[], proxy=None):
    # Use the User-Agent: AltPublicAgent, because some servers protect their CDN with
    # a simple User-Agent check e.g. https://luckyv.de does that
    if "http://" in url and cdn:
        req_headers = {
            "host": "",
            'user-agent': 'AltPublicAgent',
            "accept": '*/*',
            'alt-debug': 'false',
            'alt-password': '17241709254077376921',
            'alt-branch': server.branch,
            'alt-version': server.version,
            'alt-player-name': secrets.token_urlsafe(10),
            'alt-social-id': secrets.token_hex(9),
            'alt-hardware-id2': secrets.token_hex(19),
            'alt-hardware-id': secrets.token_hex(19)
        }
    else:
        req_headers = {
            'User-Agent': 'AltPublicAgent',
            'content-type': 'application/json; charset=utf-8'
        }

    try:
        api_data = requests.get(url, headers=req_headers, timeout=60, proxies=proxy)

        if api_data.status_code != 200:
            logging.warning(f"the request returned nothing.")
            return None
        else:
            return loads(api_data.content.decode("utf-8", errors='ignore'))
    except Exception as e:
        logging.error(e)
        return None


# Fetch the stats of all servers that are currently online
# e.g. {"serversCount":121,"playersCount":1595}
def get_server_stats():
    data = request(Config.all_server_stats_link)
    if data is None:
        return None
    else:
        return data


# Get all Servers that are online as Server object
def get_servers():
    return_servers = []
    servers = request(Config.all_servers_link)
    if servers is None or servers == "{}":
        return None
    else:
        for server in servers:
            # Now change every JSON response to a server object that we can e.g. update it when we want
            temp_server = Server("unknown", server["id"], server["maxPlayers"], server["players"], server["name"],
                                 server["locked"], server["host"], server["port"], server["gameMode"],
                                 server["website"],
                                 server["language"], server["description"], server["verified"], server["promoted"],
                                 server["useEarlyAuth"], server["earlyAuthUrl"], server["useCdn"], server["cdnUrl"],
                                 server["useVoiceChat"], server["tags"], server["bannerUrl"], server["branch"],
                                 server["build"], server["version"], server["lastUpdate"])
            return_servers.append(temp_server)

        return return_servers


# get a single server by their server id
def get_server_by_id(server_id):
    temp_data = request(Config.server_link.format(server_id))
    if temp_data is None or temp_data == {}:
        # the api returned no data
        return None
    elif not temp_data["active"]:
        # the server is offline
        return Server(False, server_id, 0, 0, "", False, "", 0, "", "", "", "", False, False, False, "", False, "",
                      False, "",
                      "", "", 0, 0, "")
    else:
        # Create a Server object with the data and return that
        return Server(temp_data["active"], server_id, temp_data["info"]["maxPlayers"], temp_data["info"]["players"],
                      temp_data["info"]["name"], temp_data["info"]["locked"], temp_data["info"]["host"],
                      temp_data["info"]["port"], temp_data["info"]["gameMode"], temp_data["info"]["website"],
                      temp_data["info"]["language"], temp_data["info"]["description"],
                      temp_data["info"]["verified"], temp_data["info"]["promoted"],
                      temp_data["info"]["useEarlyAuth"], temp_data["info"]["earlyAuthUrl"],
                      temp_data["info"]["useCdn"], temp_data["info"]["cdnUrl"], temp_data["info"]["useVoiceChat"],
                      temp_data["info"]["tags"], temp_data["info"]["bannerUrl"], temp_data["info"]["branch"],
                      temp_data["info"]["build"], temp_data["info"]["version"], temp_data["info"]["lastUpdate"])


# get the average player count with a specified time range
# returns a JSON object e.g. [{"t":1652096100,"c":50},{"t":1652096400,"c":52},{"t":1652096700,"c":57}]
# time: 1d, 7d, 31d
def get_server_by_id_avg(server_id, time):
    avg_data = request(Config.server_average_link.format(server_id, time))
    if avg_data is None:
        return None
    else:
        return avg_data


# works like get_server_by_id_avg() but returns a integer/number
# time: 1d, 7d, 31d
def get_server_by_id_avg_result(server_id, time):
    avg_result_response = get_server_by_id_avg(server_id, time)
    if avg_result_response is None:
        return None
    else:
        players_all = 0
        for entry in avg_result_response:
            players_all = players_all + entry["c"]
        result = players_all / len(avg_result_response)
        return round(result)


# get the maximum player count with a specified time range
# returns a JSON object e.g. [{"t":1652096100,"c":50},{"t":1652096400,"c":52},{"t":1652096700,"c":57}]
# time: 1d, 7d, 31d
def get_server_by_id_max(server_id, time):
    max_data = request(Config.server_max_link.format(server_id, time))
    if max_data is None:
        return None
    else:
        return max_data


# validate a given alt:V server id
def validate_id(server_id):
    regex = compile(r"^[\da-zA-Z]{32}$")
    result = regex.match(server_id)
    if result is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    print("This is a Module!")
    sys.exit()
