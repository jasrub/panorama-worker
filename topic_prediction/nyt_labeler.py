import requests
import logging

from Base import settings

log = logging.getLogger(__name__)

host = settings.get('labeller', 'host')

THRESHOLD = 0.1
def _get_url():
    return host+'/predict.json'


def get_labels(story_text):
    result = _query({'text': story_text})
    return filter_list(result['descriptors600'])


def _query(data):
    try:
        r = requests.post(_get_url(), json=data)
        # log.debug('labeller says %r', r.content)
        return r.json()
    except requests.exceptions.RequestException as e:
        log.exception(e)
    return None

def filter_list(terms):
    return [{"term": x['label'], "score": x['score']} for x in terms if x['score']>THRESHOLD]