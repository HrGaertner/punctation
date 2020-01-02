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

tags_set = ["PPER", "APPRART", "PWS", "NE", "PRELS", "KOKOM", "PIAT", "CARD", "VMINF", "PIS", "XY", "PTKANT", "PTKNEG", "APPR", "ADV", "KON", "VMFIN", "APZR", "ADJD", "PDS", "VVFIN", "PRF", "VAINF", "ADJA", "$.", "TRUNC", "VVPP", "PDAT", "ART", "NN", "PPOSAT", "VVINF", "$(", "VAPP", "$,", "PWAV", "KOUS", "KOUI", "FM", "VVIZU", "VVIMP", "VAFIN", "PTKZU", "PTKVZ", "PROAV"]

tags = []

for tag in tagged:
    if tag in tags_set:
        tags.append(tags_set.index(tag))
    else:
        print(tag)
        tags_set.append(tag)
        tags.append(tags_set.index(tag))
print("processed")
print()
with open("final_raw.pickle", "wb") as f:
    pickle.dump(tags, f)

print(tags_set)
print()

tagged = tags
feature = []
vec = []
punctation = []
punctation2 = []
punc_vec = []
event = False

f_feature = []
f_vector = []

for i in range(0, len(tagged)):
    if tagged[i] == "$.":
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
            punctation, punctation2, punc_vec = [], [], []
    print(i)
    if len(punctation) >= 39:
        punctation = []
        punctation2 = []
while len(tagged) < 40:
    tagged.append(100)
    f_vector.append(vec)
    f_feature.append(sentence)

with open('vec.pickle', 'wb') as f_vec:
    pickle.dump(f_vector, f_vec)
with open("feature.pickle", "wb") as f:
    pickle.dump(f_feature, f)
