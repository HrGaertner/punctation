#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:35:51 2019

@author: workshop
"""

import speech_recognition as sr
import nltk
import pickle
import textblob_de

nltk.download('punkt')

class Speech2Segment():
    def __init__(self, service, language='de-DE', mic=None):
        self.r = sr.Recognizer()
        if not mic:
            self.mic = sr.Microphone(device_index=None)
        else:
            self.mic = sr.Microphone(device_index=mic)
        self.language = language
        self.service = service
    def Microphones(self):
        return sr.Microphone.list_microphone_names()
    def set_Microphone(self, mic):
        self.mic = sr.Microphone(device_index=mic)
    def listen(self):
        print('[*] Listening')
        with self.mic as source:
            #self.r.adjust_for_ambient_noise(source)
            return self.r.listen(source, timeout=10, phrase_time_limit=None)
        print('[+] Finished')
    def recognize(self, audio):
        if self.service.upper() == 'GOOGLE':
            return self.r.recognize_google(audio, language=self.language)
        elif self.service.upper() == 'SPHINX':
            return self.r.recognize_google(audio, language=self.language)
    def tokenize(self, text):
        return nltk.word_tokenize(text)
    def error(self):
        self.error()
    def tag(self, list):
        with open('../ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f:
            tagger = pickle.load(f)
            return tagger.tag(list)
    def polarity(self, sen):
        blob = textblob_de.TextBlobDE(sen)
        return blobsentence[0].sentiment.polarity
    def language(self, word):
        b = TextBlob(word)
        return b.detect_language()
    def S2S(self):
        return self.tag(self.tokenize(self.recognize(self.listen())))
        
        
    
