from nltk.tokenize import word_tokenize
import pickle
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
classifier_f = open("./sentiment/pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

word_features5k_f = open("./sentiment/pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


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