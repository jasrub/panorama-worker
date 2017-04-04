from nltk.tokenize import word_tokenize
from sentiment import classifier, word_features


def find_features(document):
    words = [w.lower() for w in word_tokenize(document)]
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

def find_features_from_wc(wc):
    features = {}
    words = [w['term'] for w in wc]
    for w in word_features:
        features[w] = (w in words)

    return features


def calssify_text(text):
	prob = classifier.prob_classify(find_features(text))
	pos = prob.prob("pos")
	neg = prob.prob("neg")
	score = -1*pos+neg
	return score

def calssify_wc(wc):
	prob = classifier.prob_classify(find_features_from_wc(wc))
	pos = prob.prob("pos")
	neg = prob.prob("neg")
	score = -1*pos+neg
	return score