import requests


def get_client_ip():
    requests.get("https://httpbin.com/ip")
    print("afsdfa")