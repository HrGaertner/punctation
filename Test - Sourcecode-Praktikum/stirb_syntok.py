import S2S
import syntok.segmenter as segmenter
import random
#s2s = S2S.Speech2Segment('Sphinx')
#document  = s2s.recognize(s2s.listen())

with open('sentence.txt') as f:
    expected = []
    while len(expected) < 10:
        sentence = f.readline()
        sentence = sentence.split('\t')[1]
        sentence = sentence.split('\n')[0]
        sentence = sentence.split('.')
        sen = ''
        for i in sentence:
            sen += i
        sentence = sen
        sentence = sentence.split('!')
        sen = ''
        for i in sentence:
            sen += i
        sentence = sen
        sentence = sentence.split('?')
        sen = ''
        for i in sentence:
            sen += i
        sentence = sen
        sentence = sentence.split(',')
        sen = ''
        for i in sentence:
            sen += i
        sentence = sen
        sentence += ' '
        expected.append(sentence)
print(expected)
print()
document = ''
random.shuffle(expected)
for phrase in expected:
	document += phrase

for paragraph in segmenter.analyze(document):
    for sentence in paragraph:
        for token in sentence:
            # exactly reproduce the input
            # and do not remove "imperfections"
            print(token.spacing, token.value, sep='', end='')
    print()
    print("\n")  # reinsert paragraph separators
