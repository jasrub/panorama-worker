import pickle

classifier_path = './subjective/pickled_algos/SDGSubjectiveClassifier.pickle'

classifier = None

def load_classifier():
    global classifier
    classifier_f = open(classifier_path, "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()


load_classifier()