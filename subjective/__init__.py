import pickle

classifier_path = './subjective/pickled_algos/naivebayes.pickle'
word_features_path = './subjective/pickled_algos/word_features.pickle'

classifier_f = open(classifier_path, "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

word_features_f = open(word_features_path, "rb")
word_features = pickle.load(word_features_f)
word_features_f.close()