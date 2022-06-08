from commons import (
    safe_write_to_file,
    safe_read_json_as_obj_from_file,
    safe_write_obj_as_json_to_file
)

import requests


RAW = 'data/fortune_500/raw.json'
CONVERTED = 'data/fortune_500/converted.json'
TECH_FILTERED = 'data/fortune_500/tech_filtered.json'
T25_MGMGT_CONSULTING = 'data/managementconsulted/top-25.json'


def run_scraper():
    # The token and URL may need to be recreated
    token = 'Zm9ydHVuZTpCcHNyZmtNZCN5SndjWkkhNHFqMndEOTM='
    url = f'https://fortune.com/wp-json/irving/v1/data/franchise-search-results?list_id=3287962&token={token}'
    response = requests.get(url)
    json_obj = response.text
    safe_write_to_file(RAW, json_obj)


def run_obj_conversion():
    obj = safe_read_json_as_obj_from_file(RAW, [])
    obj = obj[1]
    objs = obj['items']
    new_objs = []

    for o in objs:
        fields = o['fields']
        new_obj = {}
        for field in fields:
            k, v = field['key'], field['value']
            new_obj[k] = v
        new_objs.append(new_obj)

    safe_write_obj_as_json_to_file(CONVERTED, new_objs)


def run_filter():
    data = safe_read_json_as_obj_from_file(CONVERTED, [])
    data = [x for x in data if x['sector'] == 'Technology']
    data.sort(key=lambda x: int(x['rank']))
    safe_write_obj_as_json_to_file(TECH_FILTERED, data)


def get_top_tech_from_f500():
    data = safe_read_json_as_obj_from_file(TECH_FILTERED)
    return [d['name'] for d in data]


def get_top_25_consulting():
    return safe_read_json_as_obj_from_file(T25_MGMGT_CONSULTING)
