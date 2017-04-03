# worker work flow.

# check if any labels were input.
# retrain sentiment analysis model
# retrain subjectivity model
# extract entities from stories labeled as trending
# get new trending topics with time stamp
#---------------------------------------------------#

import os
import mediacloud
from datetime import datetime, timedelta, date
# import numpy as np
# from time import time
# import random
# from nltk.tokenize import word_tokenize
# import json
# import uuid
from pymongo import MongoClient, TEXT

from topic_prediction import nyt_labeler
from left_right import label_left_right
from trends import trend_score
from sentiment import sentiment_predict
from subjective import subjective_predict


MEDIA_CLOUD_KEY = os.environ.get('MEDIA_CLOUD_KEY')
SUPERGLUE_MONGO_URL = os.environ.get('SUPERGLUE_MONGO_URL')
DB_URL = os.environ.get('DB_URL')

# connect to media cloud
mc = mediacloud.api.AdminMediaCloud(MEDIA_CLOUD_KEY)

#connect to superglue
client = MongoClient(SUPERGLUE_MONGO_URL)
db = client.get_default_database()
collection = db['media']

# get all stories from past X hours. if already in DB, pop from array.

#get media cloud stories
timeframe = 3
end = datetime.now()
start = (end - timedelta(days=7))

print start

story_count = mc.storyCount('*',['tags_id_media: (8875027)','(language:en)', mc.publish_date_query(start,end)])['count']
print "got %d stories"%story_count

all_stories = []

# get media cloud stories
max_id = 0
num_rows = 1000
while len(all_stories)<10:#story_count:
    # get a page
    stories = mc.storyList('*',['tags_id_media: (8875027)','(language:en)', mc.publish_date_query(start,end)],
                           last_processed_stories_id=max_id,text=True)
    max_id = stories[-1]["processed_stories_id"]#find max processed_stories_id on page
    all_stories += stories
    if len(all_stories)%1000==0:
        print len(all_stories)

for story in all_stories:
    # check if story exists in db, if so, delete from all_stories
    story['is_media_cloud'] = True
    story['is_super_glue'] = False

# get super glue stories

for story in all_stories:
    story['descriptors'] = nyt_labeler.get_labels(story['story_text'])
    story['leftRight'] = label_left_right.score(str(story['media_id']))
    story['trend'] = trend_score.score(story['story_text'], datetime.strptime(story['publish_date'], '%Y-%m-%d %H:%M:%S'))
    story['posNeg'] = sentiment_predict.calssify_text(story['story_text'])
    story['objective'] = subjective_predict.calssify_text(story['story_text'])

print "done"
for s in all_stories:
    print s['descriptors']
