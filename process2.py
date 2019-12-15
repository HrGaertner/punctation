import nltk
import csv
import pickle

def tag(liste):
    with open('ClassifierBasedGermanTagger/germanTagger.pickle', 'rb') as f:   
        tagger = pickle.load(f)
        return tagger.tag(liste)
"""
with  open("preprocess.txt") as f:
    data = f.read()
"""

data = """0,00001% der Stimmrechte (das entspricht 14 Stimmrechten) sind der Gesellschaft gemäß § 22 Abs. 1, Satz 1, Nr. 2 in Verbindung mit Satz 2 WpHG zuzurechnen. 0,00001% der Stimmrechte (das entspricht 257 Stimmrechten) sind der Gesellschaft gemäß § 22 Abs. 1, Satz 1, Nr. 2 WpHG in Verbindung mit Satz 2 WpHG zuzurechnen. 00:00 DGAP-AFR: AGROB Immobilien AG: Bekanntmachung gemäß § 37v, 37w, 37x ff. WpHG mit dem Ziel der europaweiten Verbreitung 29.12. 00.00 - Schalten Sie das iPad ab: Eine Stunde vor der Schlafenszeit muss blaues Licht wie jenes vom iPad vermieden werden. 01.00 Uhr - Schlaf: Wenn Sie später schlafen gehen, brauchen Sie eine Notlüge, warum sie verschlafen haben. 0:0 (0:0) Tabelle Viele klare Torszenen im Sechzehner gab es nicht, beide Abwehrreihen standen recht sicher. 00:00 Uhr: Ende des Liveticker Wir beenden für heute den Liveticker zu den Geschehnissen rund um den Anschlag auf die französische Satirezeitschrift "Charlie Hebdo". 00:04 Zu sehen ist ein weinender, weiss gekleideter Prophet, der ein Plakat mit der Aufschrift «Je suis Charlie» in denb Händen hält. 00:05 Petkovic: "Rio ist mein großes Ziel" Von Rückzug keine Spur, Andrea Petkovic wird ihre Karriere fortsetzen. 00.05 Uhr: ARD-Fernsehkorrespondentin Ellis Fröder kann die Zahl von 35 Toten, die zwischenzeitlich kursieren, nicht bestätigen. 00:09 Uhr: Serbien kappt Lkw-Verkehr aus Kroatien Serbien will nach Worten von Innenminister Nebojsa Stefanovic Frachtfahrzeuge aus Kroatien und Lkws mit Gütern aus Kroatien nicht ins Land lassen. 000 In der Bergwelt schwimmen Der fantastische Pool des Hotels Cambrian in Adelboden bietet eine herrliche Rundumsicht auf die Berner Alpen. 0,00 Prozent-Coupon Der Zinscoupon, nachdem sich die Zinsüberweisungen richten, lautete erstmals auf 0,00 Prozent. 0:00 Uhr: Luis aus dem Burgenland ist der Sieger Beate Hruby, 35, Angestellte aus Klostermarienberg, brachte den kleinen Sieger exakt um Mitternacht im Krankenhaus Oberpullendorf zur Welt: Luis ist kerngesund, 3.680 Gramm schwer und 54 cm groß. 0 0 1 0 Keine Kommentare Martin Schindler Martin Schindler schreibt nicht nur über die SAPs und IBMs dieser Welt sondern hat auch eine Schwäche für etwas abseitige und unterhaltsame Themen aus der Welt der IT. 00:10: Tschechien könnte nach den Worten von Ministerpräsident Bohuslav Sobotka Tausende von Flüchtlingen aufnehmen. 00:14Neujahrsbotschaft: SPD-Chef Gabriel warnt vor Spaltung der Gesellschaft SPD-Chef Sigmar Gabriel hat in seiner Botschaft zum Jahreswechsel vor einer"""

print("Loaded")
print()
data = nltk.word_tokenize(data)
print("Tokenized")
print()
tags = tag(data)
print("Tagged")
print()
tagged = []
for i in tags:
    tagged.append(i[1])
print("Finished")
print()

with open('feature.csv', 'w', newline='') as csvfile:
    sen = []
    feature = []
    vec = []
    punctation = []
    punctation2 = []
    punc_vec = []
    event = False
    
    fieldnames = ['tagged', 'sen', 'vector']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for i in range(0, len(data)):
        if tagged[i] == "$.":
            event = True
            punctation = []
            punctation2 = []
            punc_vec = []
        else:
            sen.append(data[i])
            punctation.append(data[i])
            feature.append(tagged[i])
            punctation2.append(tagged[i])
            if event:
                vec.append(1)
                punc_vec.append(1)
            else:
                vec.append(0)
                punc_vec.append(0)
            if len(sen) == 40:
                print(sen)
                writer.writerow({'tagged': tagged, 'sen': sen, 'vector': vec})
                print(len(punctation))
                sen = punctation
                feature = punctation2
                vec = punc_vec
                punctation, punctation2, punc_vec = [], [], []
        print(len(sen))
        #print(i)
        if len(punctation) >= 39:
            punctation = []
            punctation2 = []
    while len(tagged) < 40:
        tagged.append("NULL")
        writer.writerow({'sen': sen,'tagged': sentence, 'vector': vec})
