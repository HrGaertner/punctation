from flask import Flask, render_template# importing needed librarys
from flask_socketio import SocketIO
import speech_recognition as sr

app = Flask(__name__)# Setting up socket io and flask
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
r = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receive')
def getting_wav(fd):
    print(fd)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('my event')
def handle_my_custom_event(byte):
    print('received json: ' + str(byte))

@socketio.on('get_audio')
def audio(audio):
    audio = sr.AudioData(audio["wav blob"], audio["sampleRate"], 2)
    output = r.recognize_google(audio, language=audio["language"])
    print(output)
if __name__ == '__main__':
    socketio.run(app, debug=True)