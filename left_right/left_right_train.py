import json

media_cloud_left_right_tags = {}
media_sources = {}
with open('./left_right/media_cloud_left_right_tags.json', 'r') as infile:
    media_cloud_left_right_tags = json.load(infile)

with open('./left_right/media_sources.json', 'r') as infile:
    media_sources = json.load(infile)

def retrain(labels):
    #todo! retraind this somehow
    return 0