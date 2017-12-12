import requests
import time


def get(url, params="", json=""):
    api_limit.inc()
    return requests.get(url, params=params, json=json)


def post(url, params="", json=""):
    api_limit.inc()
    return requests.post(url, params=params, json=json)


class ApiLimit:
    counter = 0
    api_limit = 35

    def __init__(self):
        self.counter = 0

    def inc(self):
        self.counter += 1
        if self.counter >= self.api_limit:
            self.sleep()

    def sleep(self):
        self.counter = 0
        print("Sleeping for 15 seconds so we don't go over API limit!")
        time.sleep(15)
        print("Continuing..")


api_limit = ApiLimit()
