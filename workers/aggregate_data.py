import json
from datetime import datetime, timedelta

from topic_prediction import nyt_labeler
from left_right import label_left_right
from trends import trend_score
from sentiment import sentiment_predict
from subjective import subjective_predict

from Base.vectorize import vectorize

from Base.utils import millis_since, mc, sg, segment_to_story
import database_connection
from database_connection.db import is_story_in_db, insert_stories, insert_descriptors, recalculate_connections

def get_media_cloud_stories():
    all_stories = []

    timeframe = 1
    end = datetime.now()
    start = (end - timedelta(days=timeframe))
    story_count = mc.storyCount('*',['tags_id_media: (8875027)','(language:en)', mc.publish_date_query(start,end)])['count']
    print "got %d stories"%story_count

    max_id = 0
    num_rows = 1000
    while story_count>0 and len(all_stories)<story_count:
        # get a page
        stories = mc.storyList('*',['tags_id_media: (8875027)','(language:en)', mc.publish_date_query(start,end)],
                               last_processed_stories_id=max_id,text=True, rows=num_rows)
        max_id = stories[-1]["processed_stories_id"]#find max processed_stories_id on page
        all_stories += stories

    all_stories_clean = [story for story in all_stories if not is_story_in_db(story['stories_id'])]
    for story in all_stories_clean:
        story['isMediaCloud'] = True
        story['isSuperglue'] = False
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
        {"date_added": {"$gt": millis_since('1')}, "descriptors": {"$exists": True}})
    print "found %d videos" % all_media_has_descriptors.count()
    all_videos = []
    for doc in all_media_has_descriptors:
        for i, seg in enumerate(doc["story_segments"]):
            if len(seg["text"]) > 30:
                vid =segment_to_story(doc, seg, i)
                all_videos.append(vid)
    videos_clean = [vid for vid in all_videos if not is_story_in_db(vid['stories_id'])]
    print "got %d new videos"%len(videos_clean)
    return videos_clean


def annotate_stories(all_stories):
    for story in all_stories:
        if 'descriptors' not in story:
            if story['story_text']:
                story['descriptors'] = nyt_labeler.get_labels(story['story_text'])
            else:
                story['descriptors'] = []
        story_vector = vectorize(story['story_text'])
        story['leftRight'] = label_left_right.score(str(story['media_id']))
        story['trend'] = trend_score.score(story['story_text'], story['publish_date'])
        story['posNeg'] = sentiment_predict.classify_text(story_vector)
        story['objective'] = subjective_predict.classify_text(story_vector)
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
         'isMediaCloud':s['isMediaCloud'],
         'isSuperglue': s['isSuperglue'],
         'leftRight': s['leftRight'],
         'posNeg': s['posNeg'],
         'trend': s['trend'],
         'objective': s['objective'],
         'image':s['image'],
         'collectDate': s['collect_date']} for s in all_stories]
    insert_stories(insert_arr)

    # push descriptors results
    descriptors = [
        {'descriptorId': d['term'],
         'storyId': s['stories_id'],
         'score': d['score']} for s in all_stories for d in s["descriptors"]]
    insert_descriptors(descriptors)

def run():
    stories = get_media_cloud_stories()
    videos = [] #get_superglue_stories() #commenting out for user testing!!
    all_stories = stories+videos
    print "got %d stories"%(len(all_stories))

    batch_size = 300
    chunks = [all_stories[i:i + batch_size] for i in xrange(0, len(all_stories), batch_size)]
    for i,chunk in enumerate(chunks):
        annotate_stories(chunk)
        push_to_db(chunk)
        print "%d stories uploaded to db"%(i*batch_size)
    print "recalculating connections"
    recalculate_connections()
    print "finished data aggregation"

if __name__ == "__main__":
    run()