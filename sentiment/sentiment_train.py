import pickle
from sentiment import classifier_path, classifier

from Base.vectorize import vectorize
from Base.utils import classes

def save_classifier():
    save_classifier = open(classifier_path, "wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()


def retrain(labels):
    X = []
    y = []
    for label in labels:
        category = '%.1f'%label['posNeg']
        X.append(vectorize(label['story']['story_text']))
        y.append(category)
    classifier.partial_fit(X, y, classes=classes)
    save_classifier()