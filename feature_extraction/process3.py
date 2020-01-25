import pickle
import numpy as np

with open("feature.pickle", "rb") as f:
    features = pickle.load(f)

tag_set = ['PPER', 'APPRART', 'PWS', 'NE', 'PRELS', 'KOKOM', 'PIAT', 'CARD', 'VMINF', 'PIS', 'XY', 'PTKANT', 'PTKNEG', 'APPR', 'ADV', 'KON', 'VMFIN', 'APZR', 'ADJD', 'PDS', 'VVFIN', 'PRF', 'VAINF', 'ADJA', '$.', 'TRUNC', 'VVPP', 'PDAT', 'ART', 'NN', 'PPOSAT', 'VVINF', '$(', 'VAPP', '$,', 'PWAV', 'KOUS', 'KOUI', 'FM', 'VVIZU', 'VVIMP', 'VAFIN', 'PTKZU', 'PTKVZ', 'PROAV', 'VAIMP', 'NNE', 'PWAT', 'APPO', 'ITJ', 'PRELAT', 'VMPP', 'PPOSS', 'PTKA', 'NULL']

i = 0
tags = []
for features_sen in features:
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
print("Saving")
with open("digit_feature.pickle", "wb") as f:
    pickle.dump(np.array(tags), f)
