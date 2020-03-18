from keras.models import load_model#Importing needed Modules
import pickle
import nltk
import numpy as np
from keras.utils.generic_utils import get_custom_objects
from keras.layers import Activation
import keras.backend as tf

def unit_step_activation(x):
    return tf.sign(x)

get_custom_objects().update({'unit_step_activation': Activation(unit_step_activation)})

#try:
model = load_model("punctation_lib/unit_step-punctator")
model.load_weights("punctation_lib/unit_step-punctator.h5")
#except:
#    model = load_model("punctator")
#    model.load_weights("punctator.h5")

def tag(tokenized):#tagging and converting to digits
    try:
        with open('ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f: #Tagging
            tagger = pickle.load(f)
    except:
        with open('../ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f: #Tagging
            tagger = pickle.load(f)
    sen = tagger.tag(tokenized)
    tag_set = ['PPER', 'APPRART', 'PWS', 'NE', 'PRELS', 'KOKOM', 'PIAT', 'CARD', 'VMINF', 'PIS', 'XY', 'PTKANT',
               'PTKNEG', 'APPR', 'ADV', 'KON', 'VMFIN', 'APZR', 'ADJD', 'PDS', 'VVFIN', 'PRF', 'VAINF', 'ADJA', '$.',
               'TRUNC', 'VVPP', 'PDAT', 'ART', 'NN', 'PPOSAT', 'VVINF', '$(', 'VAPP', '$,', 'PWAV', 'KOUS', 'KOUI',
               'FM', 'VVIZU', 'VVIMP', 'VAFIN', 'PTKZU', 'PTKVZ', 'PROAV', 'VAIMP', 'NNE', 'PWAT', 'APPO', 'ITJ',
               'PRELAT', 'VMPP', 'PPOSS', 'PTKA', 'NULL']
    tag_sen = []
    for sen_tag in sen:
        if sen_tag[1] in tag_set:
            tag_sen.append(tag_set.index(sen_tag[1]))
    return tag_sen

def punctate(data):
    sen = nltk.word_tokenize(data, "german")
    data = tag(sen)
    punctation = 0
    nulls = 0
    while len(data) % 40 != 0:  # You can divide through 40 so everything goes through the ANN
        data.append(54)
        nulls += 1
    i = 40
    while i <= len(data):
        while len(data) % 40 != 0:  # You can divide through 40 so everything goes through the ANN
            data.append(54)
            nulls += 1
        model_prepared = np.array([data[i - 40:i], data[i - 40:i]])
        vec = model.predict(model_prepared)[0]# Get the answer of the ANN
        vec[0] = 0.0# A sentence needs at least to words
        vec[1] = 0.0
        nulls = 0
        for iter in range(0, len(vec)):
            if vec[iter] >= 0.5 and data[i-40 + iter] != 54: #and data[i-40 + iter] != 32 and data[i-40 + iter] != 24 and data[i-40 + iter] != 34 and data[i-40 + iter - 1] != 32 and data[i-40 + iter - 1] != 24 and data[i-40 + iter - 1] != 34:
                    sen[i - 40 + iter - 1] = sen[i - 40 + iter - 1] + "."
                    sen[i - 40 + iter] = sen[i - 40 + iter][0].upper() + sen[i - 40 + iter][1:]
                    vec[iter] = 0.0
                    try:
                        vec[iter + 1] = 0.0
                    except:
                        pass
                    break
                    punctation = 39 - iter
        i += 39 - punctation # NULL
    if sen[-1][-1] != ".":
        sen[-1] = sen[-1] + "."
    sen = ' '.join(sen)
    return sen

if __name__ == "__main__":
    data = input("Was soll punktiert werden? ")
    sen = punctate(data)
    print(sen)