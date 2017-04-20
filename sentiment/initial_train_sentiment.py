from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import SGDClassifier
from sentiment import classifier_path

from sklearn.preprocessing import scale
import pickle

from Base.utils import drange
from Base.vectorize import vectorize

from scipy.interpolate import interp1d

import itertools

import time

m = interp1d([1, 10],[1, -1])

import csv


X = []
y = []

def stream_data_points():
    with open('./sentiment/SAR14.txt', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            yield (row[0].decode('utf-8'), '%.1f'%m(float(row[1])) )

def get_minibatch(doc_iter, size):
    """Extract a minibatch of examples, return a tuple X_text, y.

    Note: size is before excluding invalid docs with no topics assigned.

    """
    data = [doc for doc in itertools.islice(doc_iter, size)]
    if not len(data):
        return np.asarray([], dtype=int), np.asarray([], dtype=int)
    X_text, y = zip(*data)
    return X_text, y

def iter_minibatches(doc_iter, minibatch_size):
    """Generator of minibatches."""
    X_text, y = get_minibatch(doc_iter, minibatch_size)
    while len(X_text):
        yield X_text, y
        X_text, y = get_minibatch(doc_iter, minibatch_size)

data_stream = stream_data_points()
# First we hold out a number of examples to estimate accuracy
n_test_documents = 3000
x_test, y_test = get_minibatch(data_stream, n_test_documents)

get_minibatch(data_stream, n_test_documents)
# Discard test set

# We will feed the classifier with mini-batches of 1000 documents; this means
# we have at most 1000 docs in memory at any time.  The smaller the document
# batch, the bigger the relative overhead of the partial fit methods.
minibatch_size = 1000

# Create the data_stream that parses Reuters SGML files and iterates on
# documents as a stream.
minibatch_iterators = iter_minibatches(data_stream, minibatch_size)
total_vect_time = 0.0

lr = SGDClassifier(loss='log', penalty='l1')
classes = np.array(list(drange(-1, 1, '0.1')))

# Main loop : iterate on mini-batches of examples
for i, (x_train, y_train) in enumerate(minibatch_iterators):

    tick = time.time()
    train_vecs = [vectorize(z) for z in x_train]
    train_vecs = scale(train_vecs)
    total_vect_time += time.time() - tick

    tick = time.time()
    # update estimator with examples in the current mini-batch
    lr.partial_fit(train_vecs, y_train, classes=classes)

    if i % 3 == 0:
        print(i)


test_vecs = [vectorize(z) for z in x_test]
test_vecs = scale(test_vecs)

print 'Test Accuracy: %.2f'%lr.score(test_vecs, y_test)

save_classifier = open(classifier_path, "wb")
pickle.dump(lr, save_classifier)
save_classifier.close()