import pickle
import nltk

def tag(liste):
    with open('ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f:   
        tagger = pickle.load(f)
        return tagger.tag(liste)

with  open("final_raw.pickle", "rb") as f:
    tagged = pickle.load(f)

tagged = tags
feature = []
vec = []
punctation2 = []
punc_vec = []
event = False

f_feature = []
f_vector = []

for i in range(0, len(tagged)):
    if tagged[i] == 24:
        event = True
        punctation = []
        punctation2 = []
        punc_vec = []
    else:
        feature.append(tagged[i])
        punctation2.append(tagged[i])
        if event:
            vec.append(1)
            punc_vec.append(1)
        else:
            vec.append(0)
            punc_vec.append(0)
        if len(vec) == 40:
            f_vector.append(vec)
            f_feature.append(tagged)
            feature = punctation2
            vec = punc_vec
            punctation2, punc_vec = [], []
    print(i)
    if len(punctation2) >= 39:
        punctation2 = []
while len(tagged) < 40:
    tagged.append(100)
    f_vector.append(vec)
    f_feature.append(sen)

with open('vec.pickle', 'wb') as f_vec:
    pickle.dump(f_vector, f_vec)
with open("feature.pickle", "wb") as f:
    pickle.dump(f_feature, f)
