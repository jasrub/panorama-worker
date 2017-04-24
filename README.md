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


## Run:

#### Extra files:
Some files are missing from that repository due to their side. You should make sure they exsist in the folder before trying to run the worker

 - `word2vec_model/GoogleNews-vectors-negative300.bin` is the Google News word2vec model. Could be downloaded from https://github.com/mmihaltz/word2vec-GoogleNews-vectors
  - `trends/stanford-ner` that includes the extracted stanford-ner model, obtained from https://nlp.stanford.edu/software/CRF-NER.shtml#Download
  
  
Then run:
```bazaar
source venv/bin/activate
source .env
python worker.py
```