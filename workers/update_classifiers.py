from trends import get_trends
from sentiment import sentiment_train
from subjective import subjective_train
from left_right import left_right_train
from database_connection import db
from base.utils import mc, sg, segment_to_story
from bson.objectid import ObjectId

def update_pipeline():
    labels = get_labels_with_stories()
    # retrain all classifiers
    sentiment_train.retrain(labels)
    subjective_train.retrain(labels)
    get_trends.retrain(labels)
    left_right_train.retrain(labels)


    get_trends.update_trends_list()
    db.update_connections()

def get_labels_with_stories():
    labels = db.get_new_labels()
    for label in labels:
        label['story'] = get_story(label['storyId'])
    return labels

def get_story(storyId, isMediaCloud):
    if isMediaCloud:
        story = mc.story(int(storyId), text=True)
    else:
        id, seg_ind = storyId.split('_')
        video = sg.find_one({"_id":ObjectId(id)})
        seg = video['story_segments'][int(seg_ind)]
        story = segment_to_story(video, seg)
    return story

