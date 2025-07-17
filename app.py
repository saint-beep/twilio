from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Serverul Flask + Twilio e online."

@app.route('/call', methods=['POST'])
def call():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/handle-key", method="POST", timeout=5)
    gather.say("Salut! Pentru rezervare, apasă 1. Pentru informații, apasă 2.", voice="alice", language="ro-RO")
    response.append(gather)
    response.say("Nu ai apăsat nicio tastă. La revedere!", voice="alice", language="ro-RO")
    response.hangup()
    return Response(str(response), mimetype='application/xml')

@app.route('/handle-key', methods=['POST'])
def handle_key():
    digit = request.form.get('Digits')
    response = VoiceResponse()

    if digit == '1':
        response.say("Perfect. Spuneți-mi la ce masă doriți să stați.", voice="alice", language="ro-RO")
        # Poți continua logica aici, ex. cu alt Gather sau webhook
    elif digit == '2':
        response.say("Programul nostru este de la 8 la 22. Vă așteptăm!", voice="alice", language="ro-RO")
    else:
        response.say("Tastă invalidă. Încercați din nou.", voice="alice", language="ro-RO")
        response.redirect('/call')

    return Response(str(response), mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)
