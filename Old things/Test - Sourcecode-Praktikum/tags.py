import pickle
import nltk
 
sentences = []
with open('sentence.txt') as f:
    for i in range(0, 1000):
            sentences.append(f.readline())
text = ''
for sentence in sentences:
        text += sentence
liste = nltk.word_tokenize(text)
with open('germanTagger.pickle', 'rb') as f:
    tagger = pickle.load(f)
    tagged = tagger.tag(liste)
tags = []
for tag in tagged:
    tags.append(tag[1])
tags = list(set(tags))
with open('tags.txt', 'w') as f:
        for tag in tags:
                f.write(tag + '\n')
