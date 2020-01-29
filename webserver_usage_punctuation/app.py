from flask import Flask, render_template# importing needed librarys
from flask_socketio import SocketIO
import speech_recognition as sr
from punctation_lib.knn_use import punctate
from punctation_lib import process

app = Flask(__name__)# Setting up socket io and flask
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
r = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/en')
def index_en():
    return render_template('index_en.html')

@app.route('/cookies')
def cookies():
    return '<h1>This Website has just two cookies one which indentifys you so we can give the text which belongs to you send to you and one which handles that you do not get anyoed with cookie requests<h1><h2>Diese Webseite hat nur zwei Cookies eines um sie zu indentifizieren, damit ihre Daten zu ihnen zurückkommen und eines um dafür zu sorgen das sie nicht die ganze Zeit diese "Wir nutzen Cookies" pop-ups bekokmen. Wir bitten um ihr Verständnis<h2><a href=https://de.wikipedia.org/wiki/HTTP-Cookie>Hier eine genauere Erläuterung</a>'

@app.route('/privacy_policy')
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route('/datenschutzerklaerung')
def datenschutzerklaerung():
    return render_template("datenschutz.html")

@app.route('/impressum')
def impressum():
    return render_template("impressum.html")

@app.route('/im_print')
def im_print():
    return render_template("im_print.html")

@app.route('/ueber')
def ueber():
    return "<h1>Das ist ein Jugend-Forscht Projekt in dem wir hinter eine Spracherkennung eine automatische Zeichensetzung bauen wollen</h1>"

@app.route('/about')
def about():
    return "<h1>This is a Jugend-Forscht project in which we aim to make an automatic punctation software behind a speech recognition</h1>"

@socketio.on('get_audio')
def audio(meta_data):
    audio = sr.AudioData(meta_data["wav blob"], meta_data["sampleRate"], 2)
    text = r.recognize_sphinx(audio, language=meta_data["language"])
    if text:
        text = punctate(text)
        text = text[0].upper() + text[1:]
    socketio.emit("textarea_text", text)

@socketio.on('punctate')
def text_punctation(text):
    if text:
        text = punctate(text)
        text = text[0].upper() + text[1:]
    print(text)
    socketio.emit("textarea_text", text)

@socketio.on("add_to_training")
def make_training(data):
    process(data)
    #socketio.emit("textarea_text", data)

if __name__ == '__main__':
    socketio.run(app, debug=True)