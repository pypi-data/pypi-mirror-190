import requests


def get_client_ip():
    requests.get("https://httpbin.com/ip")
    print("afsdfa")


import time


start = time.time()
chat_list = []
chat_data = []
jobseekers = []
for chat in chat_list:
    new_chat = chat
    new_chat["jobseeker"] = next(
        (x for x in jobseekers if x["id"] == new_chat["jobseeker_id"]), None
    )

    chat_data.append(new_chat)

print(time.time() - start)
print(chat_data)