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

@socketio.on('get_audio')
def audio(meta_data):
    print("weird")
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