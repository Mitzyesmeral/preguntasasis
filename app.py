from flask import Flask, request, session, redirect, url_for, render_template
from pymongo import MongoClient
import uuid
from datetime import datetime
import os
import certifi

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura' 

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://CHAT_BOT61:CHAT_BOT61@mitzy.llcmyll.mongodb.net/?appName=mitzy")
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['sistema_escolar']
coleccion_dudas = db['dudas']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4().hex

    if request.method == 'POST':
        session['perfil'] = request.form.get('perfil')
        return redirect(url_for('index'))

    dudas_usuario = []
    if session.get('perfil'):
        cursor = coleccion_dudas.find({'session_id': session['session_id']}).sort('fecha_raw', -1)
        dudas_usuario = list(cursor)
    
    return render_template('index.html', dudas=dudas_usuario)

@app.route('/registrar_duda', methods=['POST'])
def registrar_duda():
    pregunta = request.form.get('pregunta')
    perfil = session.get('perfil')
    session_id = session.get('session_id')

    if pregunta and perfil:
        nueva_duda = {
            'session_id': session_id,
            'perfil': perfil,
            'pregunta': pregunta,
            'fecha_raw': datetime.now(),
            'fecha': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        coleccion_dudas.insert_one(nueva_duda)

    return redirect(url_for('index'))

@app.route('/cambiar_perfil', methods=['POST'])
def cambiar_perfil():
    session.pop('perfil', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)