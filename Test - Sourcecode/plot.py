#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:52:06 2019

@author: workshop
"""

import matplotlib.pyplot as plt
import random
import pickle
import nltk

sentences = []
with open('sentence.txt') as f:
	for s in range(0, 5):
		f.readline()
	for i in range(0, 10):
    		sentences.append(f.readline())
fin_phrase = []
for sentence in sentences:
	sentence = sentence.split('\t')[1]
	fin_phrase.append(sentence.split('\n')[0] + ' ')
text = ''
random.shuffle(fin_phrase)
for phrase in fin_phrase:
	text += phrase

print(text)
print() 
print()

liste = nltk.word_tokenize(text)
with open('germanTagger.pickle', 'rb') as f:
	tagger = pickle.load(f)
	tagged = tagger.tag(liste)
print(tagged)
print()
print(tagged[23])
tags = []
i = 0
point = []
p = []
verbs = []
v = []
verbs_kon = []
vk = []
cnt = 0
for word in tagged:
	print(i)
	if word[1] == 'VAFIN' or word[1] == 'VVAFIN':
		print('verb_kon')
		verbs_kon.append(i)
	elif word[1][1] == 'V':
		verbs.append(i)
		print('verb')
	elif  word[0] == '.' or word[0] == '!' or word[0] == '?' and not tagged[i-1][1] == 'XY' and not tagged[i-1][1][0] == 'K':
		point.append(i)
		print(tagged[i-1][1])
		print('Point')
	i += 1
for pi in point:
	p.append(4)
for ve in verbs:
	v.append(1)
for vko in verbs_kon:
	vk.append(3)

print(p, v, vk)	
plt.plot(verbs, v, '*', point, p, 'ro', verbs_kon, vk, 'bs')
plt.title('Verb Point relation')
plt.axis([0, len(liste), 0, 5])
plt.show()

