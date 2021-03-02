import requests
import json
import csv

url: str = "https://api-dev.tport.online/v3/stations/"

token: str = "08bc7cde3b7a6d72df97db30d42f05a9f5233182"

headers: dict = {
    "Authorization": f"token {token}",
    "Content-Type": "application/json",
}

result: list = []


def get_data_from_request(url: str, headers: dict):

    response = requests.get(
        url=url,
        headers=headers,
    )

    if response.status_code == 200:
        return json.loads(response.text)


def check_response_page_is_not_last(data):
    return data["next"] is not None


def add_results_from_dict_to_result(data: dict) -> list:
    return result.extend(data["results"])


while True:
    data = get_data_from_request(url=url, headers=headers)
    if check_response_page_is_not_last(data=data):
        add_results_from_dict_to_result(data)
        url = data["next"]
    else:
        break

filtered_dictionary = {
    key: value
    for key, value in a_dictionary.items()
    if key == "accept_card" and value is True
}


print(result.__len__())