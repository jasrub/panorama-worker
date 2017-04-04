import json
from datetime import datetime, timedelta

from topic_prediction import nyt_labeler
from left_right import label_left_right
from trends import trend_score
from sentiment import sentiment_predict
from subjective import subjective_predict

from Base.utils import millis_since, mc, sg, segment_to_story
from database_connection.db import is_story_in_db, insert_stories, insert_descriptors

def get_media_cloud_stories():
    all_stories = []

    timeframe = 5
    end = datetime.now()
    start = (end - timedelta(days=timeframe))
    story_count = mc.storyCount('*',['tags_id_media: (8875027)','(language:en)', mc.publish_date_query(start,end)])['count']
    print "got %d stories"%story_count

    max_id = 0
    num_rows = 1000
    while story_count>0 and len(all_stories)<10:#story_count:
        # get a page
        stories = mc.storyList('*',['tags_id_media: (8875027)','(language:en)', mc.publish_date_query(start,end)],
                               last_processed_stories_id=max_id,text=True)
        max_id = stories[-1]["processed_stories_id"]#find max processed_stories_id on page
        all_stories += stories
        if len(all_stories)%1000==0:
            print len(all_stories)

    all_stories_clean = [story for story in all_stories if not is_story_in_db(story['stories_id'])]
    for story in enumerate(all_stories_clean):
        story['is_media_cloud'] = True
        story['is_super_glue'] = False
        story['publish_date'] = datetime.strptime(story['publish_date'], '%Y-%m-%d %H:%M:%S')
        story['image'] = ''
        try:
            timestamp = datetime.strptime(story['collect_date'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            timestamp = datetime.strptime(story['collect_date'], '%Y-%m-%d %H:%M:%S')
        story['collect_date'] = timestamp

    print "%d new stories from Media Cloud"%len(all_stories_clean)
    return all_stories_clean

def get_superglue_stories():
    # get superglue data
    all_media_has_descriptors = sg.find(
        {"date_added": {"$gt": millis_since('3')}, "descriptors": {"$exists": True}})
    print "found %d videos" % all_media_has_descriptors.count()
    all_videos = []
    for doc in all_media_has_descriptors:
        for i, seg in enumerate(doc["story_segments"]):
            if len(seg["text"]) > 30:
                vid =segment_to_story(doc, seg)
                all_videos.append(vid)
    videos_clean = [vid for vid in all_videos if not is_story_in_db(vid['stories_id'])]
    print "got %d new videos"%len(videos_clean)
    return videos_clean


def annotate_stories(all_stories):
    for story in all_stories:
        if 'descriptors' not in story:
            story['descriptors'] = nyt_labeler.get_labels(story['story_text'])
        story['leftRight'] = label_left_right.score(str(story['media_id']))
        story['trend'] = trend_score.score(story['story_text'], story['publish_date'])
        story['posNeg'] = sentiment_predict.calssify_text(story['story_text'])
        story['objective'] = subjective_predict.calssify_text(story['story_text'])
    return all_stories

def push_to_db(all_stories):
    # push stories
    insert_arr = [
        {'id': s['stories_id'],
         'mediaId': s['media_id'],
         'title': s['title'],
         'url': s['url'],
         'publishDate': s['publish_date'],
         'mediaName': s['media_name'],
         'mediaUrl': s['media_url'],
         'isMediaCloud':True,
         'isSuperglue': False,
         'leftRight': s['left_right_score'],
         'posNeg': s['posNeg'] if 'posNeg' in s else 0,
         'objective': s['objective'] if 'objective' in s else 0,
         'image':s['image'],
         'collectDate': s['collect_date']} for s in all_stories]
    insert_stories(insert_arr)

    # push descriptors results
    descriptors = [
        {'descriptorId': d['term'],
         'storyId': s['stories_id'],
         'score': d['score']} for s in all_stories for d in s["descriptors"]]
    insert_descriptors(descriptors)

def run_pipeline():
    stories = get_media_cloud_stories()
    videos = get_superglue_stories()
    all_stories = stories+videos
    annotate_stories(all_stories)
    push_to_db(all_stories)