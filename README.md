# Panorama Worker

This is a worker that runs every X hours.  
It updates the panorama database.
If any new datapoints are added, the classifiers are retrained before labling any new stories.
  
  
### Enviroment Variables:
**MEDIA_CLOUD_KEY** - api key for Media Cloud API  
**SUPERGLUE_MONGO_URL**  - url of the superglue mongo database    
**TWITTER_CONSUMER_KEY**  - Twitter API Consumer key  
**TWITTER_CONSUMER_SECRET** - Twitter aPI Consumer secret   
**DB_URL** - URL for Panorama database
