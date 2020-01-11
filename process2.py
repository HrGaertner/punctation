import pickle
import nltk

def tag(liste):
    with open('ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f:   
        tagger = pickle.load(f)
        return tagger.tag(liste)

with  open("tokenized.pickle", "rb") as f:
    tagged = pickle.load(f)

print("Loaded")
print()

feature = []
vec = []
punctation = []
punc_vec = []
event = False

f_feature = []
f_vector = []

for i in range(0, len(tagged)):
    if tagged[i] == "$.":
        event = True
        punctation = []
        punc_vec = []
    elif tagged[i] == "$,":
        pass
    else:
        feature.append(tagged[i])
        punctation.append(tagged[i])
        if event:
            vec.append(1)
            punc_vec.append(1)
            event = False
        else:
            vec.append(0)
            punc_vec.append(0)
        if len(vec) == 40:
            f_vector.append(vec)
            f_feature.append(feature)
            feature = punctation
            vec = punc_vec
            punctation, punc_vec = [], []
    print(i)
    if len(punctation) >= 39:
        punctation = []
        punc_vec = []

"""while len(tagged) < 40:
    tagged.append("NULL")
    f_vector.append(vec)
    f_feature.append(sentence)"""
    
if feature != 40:
    vec.append(1)
    feature.append("NULL")
    for i in range(len(vec), 40):
        feature.append("NULL")
        vec.append(0)
    f_feature.append(feature)
    f_vector.append(vec)

with open('vec.pickle', 'wb') as f_vec:
    pickle.dump(f_vector, f_vec)
with open("feature.pickle", "wb") as f:
    pickle.dump(f_feature, f)
