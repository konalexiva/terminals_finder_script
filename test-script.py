import requests
import json
import csv

from typing import Dict, List, Tuple
from functools import reduce
from operator import itemgetter

url: str = "https://api-dev.tport.online/v3/stations/"

token: str = "08bc7cde3b7a6d72df97db30d42f05a9f5233182"

keys: List[str] = ["id", "location.lat", "location.lng", "location.short_address"]

headers: Dict[str, str] = {
    "Authorization": f"token {token}",
    "Content-Type": "application/json",
}

find_field_in_response: str = "accept_card"

fields_to_union: List = ["location.lat", "location.lng"]

csv_headers: Tuple[str] = ("Номер постамата", "Координаты (ш. л.)", "Короткий адрес")

csv_row_keys: Tuple[str] = ("id", "lat lng", "location.short_address")

lat_lng_csv_field_name: str = "lat lng"

delimiter: str = ";"

result: List[Dict] = []


def deep_get(data: Dict, keys: List, default=None) -> Dict:
    return {
        key: reduce(
            lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
            key.split("."),
            data,
        )
        for key in keys
    }


def get_data_from_request(url: str, headers: Dict[str, str]) -> Dict:

    response = requests.get(
        url=url,
        headers=headers,
    )

    return json.loads(response.text) if response.status_code == 200 else {}


def check_response_page_is_not_last(data: Dict) -> bool:
    return data["next"] is not None


def extend_result_list(data: Dict) -> List[Dict]:
    return result.extend(data["results"])


def union_fields_in_dict(data: Dict, old_fields: List, new_field) -> Dict:
    data[new_field] = " ".join([str(data.pop(field)) for field in old_fields])
    return data


while True:
    response_data: Dict = get_data_from_request(url=url, headers=headers)

    if response_data == {}:
        break

    extend_result_list(response_data)

    if check_response_page_is_not_last(response_data):
        url: str = response_data["next"]
        continue

    break

# убрали у объектов ненужные поля
filtered_data: List[Dict] = [
    deep_get(data=data, keys=keys) for data in result if data[find_field_in_response]
]

# объединили поле с шириной и долготой в одно
result_data: Tuple[Dict] = tuple(
    [
        union_fields_in_dict(
            data=data, old_fields=fields_to_union, new_field=lat_lng_csv_field_name
        )
        for data in filtered_data
    ]
)

csv_headers_str: str = delimiter.join(csv_headers)

print(csv_headers_str)

for data in result_data:
    csv_row_str: str = delimiter.join(
        [
            key if type(key) == str else str(key)
            for key in itemgetter(*csv_row_keys)(data)
        ]
    )
    print(csv_row_str)
