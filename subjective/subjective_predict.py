from subjective import classifier

def classify_text(vec):
    score = classifier.predict([vec])[0]
    return float(score)

