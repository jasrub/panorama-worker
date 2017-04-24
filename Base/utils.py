import os
import time
import json
import mediacloud
from pymongo import MongoClient
from datetime import datetime
from nltk import compat
import numpy as np
import requests
import logging

from Base import settings
import decimal


log = logging.getLogger(__name__)

host = settings.get('labeller', 'host')

MEDIA_CLOUD_KEY = os.environ.get('MEDIA_CLOUD_KEY')
mc = mediacloud.api.AdminMediaCloud(MEDIA_CLOUD_KEY)

SUPERGLUE_MONGO_URL = os.environ.get('SUPERGLUE_MONGO_URL')
client = MongoClient(SUPERGLUE_MONGO_URL)
superglue_db = client['super-glue']
sg = superglue_db['media']

with open('./Base/media_sources.json', 'r') as infile:
    media_sources = json.load(infile)

with open('./Base/descriptors_600.json') as desc_file:
    descriptors_clean_list = json.load(desc_file)

DAY = 86400000
HOUR = 3600000
def millis():
    return int(round(time.time() * 1000))


def millis_since(num_days='2'):
    # return millis() - 86400000
    days = int(os.environ.get('TIME_FRAME_DAYS', num_days))
    #print ("using time frame days:", days)
    return millis() - days*DAY #debugging - millis week
def millis_since_hours(hours):
    return millis()-HOUR*hours

def segment_to_story(doc, seg, ind):
    return {
            "stories_id": "%s_%s" % (doc["_id"], ind),
            'media_id': doc['channel'],
            'title': doc['title'],
            'url': "%s#t=%.2f,%.2f" % (doc["media_url_no_comm"], seg["start"] / 1000, seg["end"] / 1000),
            'publish_date': datetime.fromtimestamp(doc["date_added"] / 1000),
            'media_name': media_sources[doc['channel']]['name'],
            'media_url': media_sources[doc['channel']]['url'],
             'isMediaCloud': False,
            'isSuperglue': True,
            'collect_date': datetime.fromtimestamp(doc["date_added"] / 1000),
            'descriptors': [d for d in seg['descriptors'] if d in descriptors_clean_list],
            'image': seg['thumbnail_image'],
            'story_text': seg['text']
    }


def inc_train(self, labeled_featuresets):
    """
    Train (fit) the scikit-learn estimator.

    :param labeled_featuresets: A list of ``(featureset, label)``
        where each ``featureset`` is a dict mapping strings to either
        numbers, booleans or strings.
    """

    X, y = list(compat.izip(*labeled_featuresets))
    X = self._vectorizer.fit_transform(X)
    y = self._encoder.fit_transform(y)
    print y
    self._clf.partial_fit(X, y, classes=np.array([0, 1]))

    return self

def _get_url():
    return host+'/word2vec'

def get_story_vector(text):
    try:
        r = requests.post(_get_url(), json={'text':text})
        return r.json()
    except Exception as e:
        log.exception(e)
    return None

#   vec=np.array(result)

def drange(x, y, jump):
    x = decimal.Decimal('%.1f'%x)
    while x <= y:
        yield str(x)
        x += decimal.Decimal(jump)

classes = np.array(list(drange(-1, 1, '0.1')))