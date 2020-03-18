import pickle
import nltk
import numpy as np
import time

def read_pdf(file):
    pass


def tag(liste):
    with open('ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f:
        tagger = pickle.load(f)
        tagged = tagger.tag(liste)
        tags = []
        for i in tagged:
            tags.append(i[1])
        return tags

def process(data, tagged=None):
    global tag
    if tagged is None:
        tagged = tag(nltk.word_tokenize(data, language="german"))

    tag_set = ['PPER', 'APPRART', 'PWS', 'NE', 'PRELS', 'KOKOM', 'PIAT', 'CARD', 'VMINF', 'PIS', 'XY', 'PTKANT',
               'PTKNEG', 'APPR', 'ADV', 'KON', 'VMFIN', 'APZR', 'ADJD', 'PDS', 'VVFIN', 'PRF', 'VAINF', 'ADJA', '$.',
               'TRUNC', 'VVPP', 'PDAT', 'ART', 'NN', 'PPOSAT', 'VVINF', '$(', 'VAPP', '$,', 'PWAV', 'KOUS', 'KOUI',
               'FM', 'VVIZU', 'VVIMP', 'VAFIN', 'PTKZU', 'PTKVZ', 'PROAV', 'VAIMP', 'NNE', 'PWAT', 'APPO', 'ITJ',
               'PRELAT', 'VMPP', 'PPOSS', 'PTKA', 'NULL']

    tags = []

    for tag_part in tagged:
        if tag_part in tag_set:
            tags.append(tag_set.index(tag_part))
        else:
            print(tag_part)
            raise (Exception)

    tagged = tags

    feature = []
    vec = []
    punctation = []
    punc_vec = []
    event = False

    f_feature = []
    f_vector = []

    for i in range(0, len(tagged)):
        if tagged[i] == 24:
            event = True
            punctation = []
            punc_vec = []
        elif tagged[i] == 34:
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
            if len(vec) == 20:
                f_vector.append(vec)
                f_feature.append(feature)
                feature = punctation
                vec = punc_vec
                punctation, punc_vec = [], []
        if len(punctation) >= 19:
            punctation = []
            punc_vec = []

    if len(feature) != 20:
        vec.append(1)
        feature.append(54)
        for i in range(len(vec), 20):
            feature.append(54)
            vec.append(0)
        f_feature.append(feature)
        f_vector.append(vec)

    print(tags)
    with open('output/vec.pickle'+ str(time.time()), 'wb') as f_vec:
        pickle.dump(np.array(f_vector), f_vec)
    with open("output/feature.pickle"+ str(time.time()), "wb") as f:
        pickle.dump(np.array(f_feature), f)
#Change Null