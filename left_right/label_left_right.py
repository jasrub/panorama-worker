import json

media_cloud_left_right_tags = {}
media_sources = {}
with open('./left_right/media_cloud_left_right_tags.json', 'r') as infile:
    media_cloud_left_right_tags = json.load(infile)

with open('./left_right/media_sources.json', 'r') as infile:
    media_sources = json.load(infile)

tags_1959 = media_cloud_left_right_tags['tags_1959']
tags_1960 = media_cloud_left_right_tags['tags_1960']
def score(source_id):
    source = media_sources[source_id]
    leftRightScore = 0
    if '1959_tag' in source:
        leftRightScore = tags_1959[str(source['1959_tag'])]
    elif '1960_tag' in source:
        leftRightScore = tags_1960[str(source['1960_tag'])]
    return leftRightScore