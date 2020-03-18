import pickle
import os
import nltk

with open('germanTagger.pickle', 'rb') as f: 
    tagger = pickle.load(f)

s = 'Seit 2010 wissen zumindest die Bürgerinitiativen gegen Fluglärm, dass da mit den alten Schallschutzgutachten und dem uralten Versprechen "Niemand wird nachts aufwachen", etwas nicht stimmen kann.'
tmp = nltk.word_tokenize(s)
print(tagger.tag(tmp))
with open('sentence.txt') as text:
    for line in text:
        tokens = nltk.word_tokenize(line)
        print(tagger.tag(tokens))
