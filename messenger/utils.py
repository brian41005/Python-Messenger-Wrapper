import json
import logging
import math
import random
import re


def clean_json(text):
    return text.replace('for (;;);', '')


def clean_graphql(text):
    return re.sub(r'{\n   "successful_results"([\S\s]*)}', '', text)


def gen_msg_id():
    return math.floor(random.random() * 9007199254740991)


def load_result_json_text(text):
    raw_text = clean_json(text)
    raw_json = json.loads(raw_text)
    return raw_json


class Payload:
    DYN = '5V8WXBzamaUmgDxKS5k2m3miWGey8jrWo466EeAq2i5U4e2\
CEaUgxebkwy6UnGiidz9XDG4XzEa8iyA14zorx64oK9CDxi5UC4bz8gxO1typ8cUhxGbw-xqqUn\
yk6EvwvEG2Z0OwspUhCK6pE9GBy8pxO12wRyUa8lUoyU4e4e6efxu8Cx6789E-bQ6eicwKhUC5o\
cUSmiaxOmUpzUryK68Oq7U'

    JAZOEST = '265817079668881808166521065865817012265120120101122849050'
