import requests
import os
from dotenv import load_dotenv
from datetime import date, timedelta

global MASTODON_ACCESSTOKEN
global MASTODON_BASEURL
global MASTODON_ADMIN
API_BASEURL = "https://holidays-jp.github.io"


def getHolidays():
    url = "{}/api/v1/date.json".format(API_BASEURL)
    r = requests.get(url)
    try:
        data = r.json()
        return data
    except Exception as e:
        print(e)


def errorToot(content):
    url = "{}/api/v1/statuses".format(MASTODON_BASEURL)
    text = ("{} ".format(MASTODON_ADMIN) + str(content))[:500]
    body = {
        "status": text,
        "visibility": "direct",
    }
    r = requests.post(url, headers = {
        "Authorization": "Bearer {}".format(MASTODON_ACCESSTOKEN),
        "Content-Type": "application/x-www-form-urlencoded"
    },data=body)
    if r.status_code != 200:
        raise Exception(r.text)

def toot(content):
    print(MASTODON_ACCESSTOKEN)
    url = "{}/api/v1/statuses".format(MASTODON_BASEURL)
    body = {
        "status": content,
        "visibility": "private",
    }
    r = requests.post(url, headers = {
        "Authorization": "Bearer {}".format(MASTODON_ACCESSTOKEN),
        "Content-Type": "application/x-www-form-urlencoded"
    },data=body)
    if r.status_code != 200:
        raise Exception(r.text)


if __name__ == "__main__":
    if os.getenv("MASTODON_ACCESSTOKEN") is None and os.getenv("MASTODON_BASEURL") is None and os.getenv("MASTODON_ADMIN") is None:
        load_dotenv(verbose=True)
    MASTODON_ACCESSTOKEN = os.getenv("MASTODON_ACCESSTOKEN")
    MASTODON_BASEURL = os.getenv("MASTODON_BASEURL")
    MASTODON_ADMIN = os.getenv("MASTODON_ADMIN")
    print(str(date.today()))
    print("MASTODON_ACCESSTOKEN: {}".format(MASTODON_ACCESSTOKEN))
    print("MASTODON_BASEURL: {}".format(MASTODON_BASEURL))
    print("MASTODON_ADMIN: {}".format(MASTODON_ADMIN))

    try:
        holidays = getHolidays()
        # holiday = holidays[str(date.today())]
        holiday = holidays[str(date.today())]
        print(holiday)
        toot("きょうは{}です".format(holiday))
    except KeyError:
        print("Today is not holiday")
        print("Stop")
    except Exception as e:
        print("Error occured")
        errorToot(e)
        print(e)
