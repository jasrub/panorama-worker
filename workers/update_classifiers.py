from trends import get_trends
from sentiment import sentiment_train
from subjective import subjective_train
from left_right import left_right_train
import database_connection.db
from Base.utils import mc, sg, segment_to_story
from bson.objectid import ObjectId

def run():
    labels = get_labels_with_stories()
    # retrain all classifiers
    if len(labels)>0:
        sentiment_train.retrain(labels)
        subjective_train.retrain(labels)
        get_trends.retrain(labels)
        left_right_train.retrain(labels)

        for label in labels:
            database_connection.db.label_used(label['id'])
    print "retrained classifiers"
    print "updating trends list"
    get_trends.update_trends_list()
    print "finished classifiers update"



def get_labels_with_stories():
    labels = database_connection.db.get_new_labels()
    for label in labels:
        label['story'] = get_story(label['storyId'], label['isMediaCloud'])
    return labels

def get_story(storyId, isMediaCloud):
    if isMediaCloud:
        story = mc.story(int(storyId), text=True)
    else:
        id, seg_ind = storyId.split('_')
        video = sg.find_one({"_id":ObjectId(id)})
        seg = video['story_segments'][int(seg_ind)]
        story = segment_to_story(video, seg, seg_ind)
    return story

if __name__ == "__main__":
    run()
