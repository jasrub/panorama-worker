import os
import gensim
import pickle
import numpy as np
from nltk.tokenize import word_tokenize

base_path = os.path.join(os.getcwd(), 'word2vec_model')
emmbedings_file_path = os.path.join(base_path, "GoogleNews-vectors-negative300.bin")

word2vec_model = None
print("loading word2vec model")
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(emmbedings_file_path, binary=True)
print("word2vec model loaded successfully")

def load_scaler_from_disk(path_to_disk):
    """ Load a pickle from disk to memory """
    if not os.path.exists(path_to_disk):
        raise ValueError("File " + path_to_disk + " does not exist")

    return pickle.load(open(path_to_disk, 'rb'))
scaler = load_scaler_from_disk(os.path.join(base_path, 'scaler'))

def vectorize(words, sample_length=200, embedding_size=300):
    if type(words)!=list:
        words = cleanText(words)
    words = words[:sample_length]
    x_matrix = np.zeros((1, sample_length, embedding_size))

    for i, w in enumerate(words):
        if w in word2vec_model:
            word_vector = word2vec_model[w].reshape(1, -1)
            scaled_vector = scaler.transform(word_vector, copy=True)[0]
            x_matrix[0][i] = scaled_vector
    return np.array(x_matrix).flatten()

def cleanText(text):
    words = [w.lower() for w in word_tokenize(text)]
    return words
