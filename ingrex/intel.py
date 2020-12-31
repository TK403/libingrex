"""Ingrex is a python lib for ingress"""
import requests
import re
import json
from ingrex.utils import BadRequest, IngrexError, ServerError
from json import JSONDecodeError
from requests.exceptions import ConnectionError, Timeout

HOST_URL = "https://intel.ingress.com"
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)" \
             " CriOS/85.0.4183.109 Mobile/15E148 Safari/604.1"


class Intel(object):
    """main class with all Intel functions"""
    def __init__(self, sessionid: str):
        self.session = requests.session()
        self.headers = {
            "accept-encoding": "gzip, deflate",
            "content-type": "application/json; charset=UTF-8",
            "cookie": f"sessionid={sessionid}",
            "origin": f"{HOST_URL}",
            "referer": f"{HOST_URL}/intel",
            "user-agent": USER_AGENT,
        }

        try:
            response = self.session.get(f"{HOST_URL}/intel", headers=self.headers, timeout=30)
            self.version = re.findall(r"gen_dashboard_(\w*)\.js", response.text)[0]
            self.headers["x-csrftoken"] = response.cookies.get("csrftoken")
            self.headers["cookie"] = f"sessionid={sessionid}; csrftoken={self.headers['x-csrftoken']};"
        except IndexError:
            raise IngrexError("Cannot connect IntelMap. Sessionid is invalid.")
        except ConnectionError as e:
            raise IngrexError("Cannot connect IntelMap. Connection error.") from e
        except Timeout as e:
            raise IngrexError("Cannot connect IntelMap. Timeout.") from e

    def fetch(self, url: str, payload: dict) -> dict:
        """raw request with auto-retry and connection check function"""
        payload["v"] = self.version
        try:
            response = self.session.post(url, data=json.dumps(payload), headers=self.headers, timeout=30)
            if response.status_code == 400:
                raise BadRequest()
            elif response.status_code in [500, 502, ]:
                raise ServerError(response.status_code)
            elif response.status_code != 200:
                raise IngrexError(f"Fetch Status Code: {response.status_code}")
            return response.json()["result"]
        except ConnectionError as e:
            raise IngrexError("Cannot connect IntelMap. Connection error") from e
        except (KeyError, JSONDecodeError) as e:
            raise IngrexError("Cannot fetch data.") from e
        except Timeout as e:
            raise IngrexError("Cannot connect IntelMap. Timeout.") from e

    def fetch_msg(self, max_lat: float, max_lng: float, min_lat: float, min_lng: float,
                  min_ts=-1, max_ts=-1, reverse=False, tab="all", ) -> dict:
        """fetch message from Ingress COMM, tab can be 'all', 'faction', 'alerts'"""
        url = f"{HOST_URL}/r/getPlexts"
        payload = {
            "maxLatE6": int(max_lat * 1E6),
            "minLatE6": int(min_lat * 1E6),
            "maxLngE6": int(max_lng * 1E6),
            "minLngE6": int(min_lng * 1E6),
            "maxTimestampMs": max_ts,
            "minTimestampMs": min_ts,
            "tab": tab,
        }
        if reverse:
            payload["ascendingTimestampOrder"] = True
        return self.fetch(url, payload)

    def fetch_map(self, tile_keys: list) -> dict:
        """fetch game entities from Ingress map"""
        url = f"{HOST_URL}/r/getEntities"
        payload = {
            "tileKeys": tile_keys,
        }
        return self.fetch(url, payload)

    def fetch_portal(self, guid: str) -> dict:
        """fetch portal details from Ingress"""
        url = f"{HOST_URL}/r/getPortalDetails"
        payload = {
            "guid": guid,
        }
        return self.fetch(url, payload)

    def fetch_score(self) -> dict:
        """fetch the global score of RESISTANCE and ENLIGHTENED"""
        url = f"{HOST_URL}/r/getGameScore"
        payload = {}
        return self.fetch(url, payload)

    def fetch_region(self, lat: float, lng: float) -> dict:
        """fetch the region info of RESISTANCE and ENLIGHTENED"""
        url = f"{HOST_URL}/r/getRegionScoreDetails"
        payload = {
            "lngE6": int(lng * 1E6),
            "latE6": int(lat * 1E6),
        }
        return self.fetch(url, payload)

    def fetch_artifacts(self) -> dict:
        """fetch the artifacts details"""
        url = f"{HOST_URL}/r/getArtifactPortals"
        payload = {}
        return self.fetch(url, payload)

    def send_msg(self, msg: str, lat: float, lng: float, tab="all") -> dict:
        """send a message to Ingress COMM, tab can be 'all', 'faction'"""
        url = f"{HOST_URL}/r/sendPlext"
        payload = {
            "message": msg,
            "latE6": int(lat * 1E6),
            "lngE6": int(lng * 1E6),
            "tab": tab,
        }
        return self.fetch(url, payload)

    def send_invite(self, address: str) -> dict:
        """send a recruit to an email address"""
        url = f"{HOST_URL}/r/sendInviteEmail"
        payload = {
            "inviteeEmailAddress": address,
        }
        return self.fetch(url, payload)

    def redeem_code(self, passcode: str) -> dict:
        """redeem a passcode"""
        url = f"{HOST_URL}/r/redeemReward"
        payload = {
            "passcode": passcode,
        }
        return self.fetch(url, payload)
