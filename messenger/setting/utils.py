import json
import logging

from ..utils import load_result_json_text


def check_result(text, *args):
    try:
        raw_json = load_result_json_text(text)
    except json.decoder.JSONDecodeError as msg:
        logging.error(msg, text)
    else:
        if 'error' in raw_json:
            msg = ', '.join([raw_json.get('errorSummary'),
                             raw_json.get('errorDescription'),
                             *args])
            logging.error(msg)
        else:
            return True
