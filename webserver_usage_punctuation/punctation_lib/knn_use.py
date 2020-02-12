from tensorflow.keras.models import load_model#Importing needed Modules
import pickle
import nltk
import numpy as np

model = load_model("./lstm_sigmoid_punctator")
model.load_weights("./lstm_sigmoid_punctator.h5")


def tag(tokenized):#tagging and converting to digits
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
    #model = load_model("punctation_lib/lstm_sigmoid_punctator")
    #model.load_weights("punctation_lib/lstm_sigmoid_punctator.h5")

    sen = nltk.word_tokenize(data, "german")
    data = tag(sen)
    punctation = 0
    nulls = 0
    while len(data) % 40 != 0:  # You can divide through 40 so everything goes through the ANN
        data.append(54)
        nulls += 1
    i = 0
    while i <= len(data):
        if i == 0:
            i += 40
            continue
        data = data[:len(data)-nulls]
        nulls = 0
        while len(data) % 40 != 0:  # You can divide through 40 so everything goes through the ANN
            data.append(54)
            nulls += 1
        model_prepared = np.array([data[i - 40:i], data[i - 40:i]])
        vec = model.predict(model_prepared)[0]# Get the answer of the ANN
        vec_list = vec.tolist()# Convert to list for .index()
        vec_list[0] = 0.0# A sentence needs at least to words
        vec_list[1] = 0.0
        print(vec)
        for iter in range(0, len(vec_list)):
            if vec[iter] >= 0.47:
                print(True)
                try:
                    sen[iter + i - 40] = sen[iter + i - 40] + "."
                    sen[iter + i - 40 + 1] = sen[iter + i - 40 + 1][0].upper() + sen[iter + i - 40 + 1][1:]
                    punctation = 40 - iter
                except:
                    sen[-1] = sen[-1] + "."
                    punctation = 40
        i += 40 - punctation # NULL
    sen = ' '.join(sen)
    return sen

if __name__ == "__main__":
    data = input("Was soll punktiert werden?")
    sen = punctate(data)
    print(sen)