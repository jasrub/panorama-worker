import nltk
import random
import pickle
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize
from sentiment import word_features_path, classifier_path, classifier, word_features
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import SGDClassifier
from Base.utils import inc_train

def initial_train():
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]

    random.shuffle(documents)

    all_words = []

    for w in movie_reviews.words():
        all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)

    word_features = list(all_words.keys())[:7000]

    featuresets = [(find_features(rev, word_features), category) for (rev, category) in documents]

    cut_place = int(len(featuresets)*0.9)

    # set that we'll train our classifier with
    training_set = featuresets[:cut_place]

    # set that we'll test against.
    testing_set = featuresets[cut_place:]

    batch_size = 100
    chunks = [training_set[i:i + batch_size] for i in xrange(0, len(training_set), batch_size)]

    SklearnClassifier.inc_train = inc_train
    classifier = SklearnClassifier(SGDClassifier())
    for batch in chunks:
        classifier.inc_train(batch)
    print("SGDClassifier accuracy percent:", nltk.classify.accuracy(classifier, testing_set) * 100)

    save_classifier = open(classifier_path, "wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()

    save_word_features = open(word_features_path, "wb")
    pickle.dump(word_features, save_word_features)
    save_word_features.close()



def find_features(document, word_features=word_features):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

def save_classifier():
    save_classifier = open(classifier_path, "wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()


def retrain(labels):
    documents = []
    for label in labels:
        category = False
        if label['posNeg']>=0.2:
            category = 'pos'
        if label['posNeg']<=-0.2:
            category = 'neg'
        if category:
            documents.append((word_tokenize(label['story']['story_text'].lower()), category))
    batch = [(find_features(rev, word_features), category) for (rev, category) in documents]
    SklearnClassifier.inc_train = inc_train
    classifier.inc_train(batch)
    save_classifier()