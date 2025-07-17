from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os

# Încarcă variabilele din .env
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Serverul Flask + Twilio e online."

@app.route("/voice", methods=["POST"])
def voice():
    """Twilio te va apela și va executa instrucțiunile de aici."""
    resp = VoiceResponse()
    
    # Spune un mesaj simplu
    resp.say("Bună! Aceasta este o rezervare automată de test.", voice='alice', language='ro-RO')
    
    # Așteaptă input de la utilizator (max 1 cifră)
    resp.gather(
        input='dtmf',
        timeout=5,
        num_digits=1,
        action='/handle-key',
        method='POST'
    )
    
    return Response(str(resp), mimetype='text/xml')

@app.route("/handle-key", methods=["POST"])
def handle_key():
    """Gestionează inputul utilizatorului în timpul apelului"""
    digit_pressed = request.form.get("Digits")
    resp = VoiceResponse()

    if digit_pressed == "1":
        resp.say("Ai ales masa de două persoane.")
    elif digit_pressed == "2":
        resp.say("Ai ales masa de patru persoane.")
    else:
        resp.say("Opțiune necunoscută. Închidem apelul.")
    
    resp.hangup()
    return Response(str(resp), mimetype='text/xml')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
