#!/usr/bin/env python3
from json import loads
from enum import Enum
import requests
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)

# CDN Docs: https://docs.altv.mp/articles/cdn_links.html

# This is the config object for this package
# Here can you configure stuff like the api endpoint or the url format
base_link = "https://cdn.altv.mp"
update_json = "https://cdn.altv.mp/{}/{}/{}/update.json"


class Platform(Enum):
    Windows = "x64_win32"
    Linux = "x64_linux"


class Branch(Enum):
    Dev = "dev"
    RC = "rc"
    Release = "release"


class Files(Enum):
    # modules
    Csharp = "coreclr-module"
    JavaScript = "js-module"
    JSByte = "js-bytecode-module"
    # servers
    VoiceServer = "voice-server"
    GameServer = "server"
    # client
    GameClient = "client"


def get_version_info(branch: Branch, file: Files, platform: Platform):
    return request(update_json.format(file.value, branch.value, platform.value))


def request(url):
    req_headers = {
        'User-Agent': 'AltPublicAgent',
        'content-type': 'application/json; charset=utf-8'
    }
    response = requests.get(url, headers=req_headers)
    if response.status_code != 200:
        logging.warning(f"the request returned nothing.")
        return None
    else:
        return loads(response.content.decode("utf-8", errors='ignore'))


if __name__ == "__main__":
    print("This is a Module!")
    sys.exit()
