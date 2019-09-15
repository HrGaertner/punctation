import S2S
import random


#################################Programm#################################
saetze = ["Heute esse ich Pizza", "Ich esse heute Pizza", "Morgen fliege ich zum Mond", "Du gehst morgen in das Ausland", "Ich programmiere um vierzehn Uhr", "Morgen geht die Welt unter"]
random.seed()
r = random.choice(saetze)

print("Der Satz ist:",r)

s2s = S2S.Speech2Segment('Google')
a = s2s.tokenize(r)
s2s.tag(a)

tags = []
words = []
for i in s2s.tag(a):
        tags.append(i[1])

if tags[0] == 'ADV' :
        print("Der Satz '",r,"' ist ein Hauptsatz mit Hauptsatzstruktur I.")
        print("Das erste Wort in diesem Hauptsatz ist ein Adverb.")
        print(r,".")

elif tags[0] == 'PPER' :
        print("Der Satz '",r,"' ist ein Hauptsatz mit Hauptsatzstruktur II.")
        print("Das erste Wort in diesem Hauptsatz ist ein irreflexives Personalpronomen.")
        print("Mit Punkt:")
        print(r,".")

else:
        print("ERROR")







