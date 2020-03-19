import pickle
import nltk
import numpy as np
import time

def process(data, tagged = None):
    if tagged is None:
        def tag(liste):
            with open('ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f:
                tagger = pickle.load(f)
                return tagger.tag(liste)
        tagged = tag(nltk.word_tokenize(data, language="german"))
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
                vec.append(-1)
                punc_vec.append(-1)
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
        feature.append(("NULL", "NULL"))
        for i in range(len(vec), 20):
            feature.append(("NULL", "NULL"))
            vec.append(-1)
        f_feature.append(feature)
        f_vector.append(vec)

    features = f_feature
    tag_set = ['PPER', 'APPRART', 'PWS', 'NE', 'PRELS', 'KOKOM', 'PIAT', 'CARD', 'VMINF', 'PIS', 'XY', 'PTKANT',
               'PTKNEG', 'APPR', 'ADV', 'KON', 'VMFIN', 'APZR', 'ADJD', 'PDS', 'VVFIN', 'PRF', 'VAINF', 'ADJA', '$.',
               'TRUNC', 'VVPP', 'PDAT', 'ART', 'NN', 'PPOSAT', 'VVINF', '$(', 'VAPP', '$,', 'PWAV', 'KOUS', 'KOUI',
               'FM', 'VVIZU', 'VVIMP', 'VAFIN', 'PTKZU', 'PTKVZ', 'PROAV', 'VAIMP', 'NNE', 'PWAT', 'APPO', 'ITJ',
               'PRELAT', 'VMPP', 'PPOSS', 'PTKA', 'NULL']

    i = 0
    tags = []
    for features_sen in features:
        tag_sen = []
        for tag in features_sen:
            if tag[1] in tag_set:
                tag_sen.append(tag_set.index(tag[1]))
            else:
                print(tag)
                raise (Exception)
        tags.append(tag_sen)
        i += 1
    print(tags)
    with open('output/vec.pickle'+ str(time.time()), 'wb') as f_vec:
        pickle.dump(np.array(f_vector), f_vec)
    with open("output/feature.pickle"+ str(time.time()), "wb") as f:
        pickle.dump(np.array(tags), f)