from sklearn.model_selection import train_test_split
import numpy as np
from nltk.corpus import subjectivity
from sklearn.linear_model import SGDClassifier
from subjective import classifier_path

from sklearn.preprocessing import scale
import pickle

from Base.utils import drange
from Base.vectorize import vectorize

subj_sents = [sent for fileid in subjectivity.fileids('subj') for sent in subjectivity.sents(fileid)]
obj_sents = [sent for fileid in subjectivity.fileids('obj') for sent in subjectivity.sents(fileid)]


# #use 1 for subjective, 0 for objective
obj_y = np.full((len(obj_sents)), '-1.0')
subj_y = np.full((len(subj_sents)), '1.0')

y = np.concatenate((subj_y, obj_y))

x_train, x_test, y_train, y_test = train_test_split(np.concatenate((subj_sents, obj_sents)), y, test_size=0.1)

print "Vectorizing train set...."
train_vecs = [vectorize(z) for z in x_train]
train_vecs = scale(train_vecs)

print "Vectorizing test set...."
test_vecs = [vectorize(z) for z in x_test]
test_vecs = scale(test_vecs)

#
lr = SGDClassifier(loss='log', penalty='l1')
batch_size = 100
chunks = [(train_vecs[i:i + batch_size],y_train[i:i + batch_size] ) for i in xrange(0, len(train_vecs), batch_size)]
classes = np.array(list(drange(-1, 1, '0.1')))
print classes
for x_chunk, y_chunk in chunks:
    lr.partial_fit(x_chunk, y_chunk, classes=classes)

print 'Test Accuracy: %.2f'%lr.score(test_vecs, y_test)

save_classifier = open(classifier_path, "wb")
pickle.dump(lr, save_classifier)
save_classifier.close()