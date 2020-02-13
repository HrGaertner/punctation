import pickle
import nltk
import numpy as np

def tag(liste):
    with open('ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f:   
        tagger = pickle.load(f)
        return tagger.tag(liste)

with  open("tagged.pickle", "rb") as f:
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
        vec[-1] = 1
        punctation = []
        punc_vec = []
    elif tagged[i] == "$,":
        pass
    else:
        feature.append(tagged[i])
        punctation.append(tagged[i])
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

vec[-1] = 1

for i in range(len(vec), 40):
    feature.append("NULL")
    vec.append(0)
f_feature.append(feature)
f_vector.append(vec)

tag_set = ['PPER', 'APPRART', 'PWS', 'NE', 'PRELS', 'KOKOM', 'PIAT', 'CARD', 'VMINF', 'PIS', 'XY', 'PTKANT', 'PTKNEG', 'APPR', 'ADV', 'KON', 'VMFIN', 'APZR', 'ADJD', 'PDS', 'VVFIN', 'PRF', 'VAINF', 'ADJA', '$.', 'TRUNC', 'VVPP', 'PDAT', 'ART', 'NN', 'PPOSAT', 'VVINF', '$(', 'VAPP', '$,', 'PWAV', 'KOUS', 'KOUI', 'FM', 'VVIZU', 'VVIMP', 'VAFIN', 'PTKZU', 'PTKVZ', 'PROAV', 'VAIMP', 'NNE', 'PWAT', 'APPO', 'ITJ', 'PRELAT', 'VMPP', 'PPOSS', 'PTKA', 'NULL']

i = 0
tags = []
for features_sen in f_feature:
    tag_sen = []
    for tag in features_sen:
        if tag in tag_set:
            tag_sen.append(tag_set.index(tag))
        else:
            print(tag)
            raise(Exception)
    tags.append(tag_sen)
    print(i)
    i += 1

train_features = np.array(tags[:int(0.9*len(tags))])
test_features = np.array(tags[int(0.9*len(tags)):])

train_targets = np.array(f_vector[:int(0.9*len(f_vector))])
test_targets = np.array(f_vector[int(0.9*len(f_vector)):])

with open("../Models/dataset_bad.pickle", "wb") as f:
    pickle.dump(((train_features, train_targets), (test_features, test_targets)), f)