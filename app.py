from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Serverul Flask + Twilio este online.'

@app.route('/call', methods=['POST'])
def call():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/handle-key', method='POST', timeout=5)
    gather.say("Bun venit! Pentru a face o rezervare, apasa 1. Pentru informatii, apasa 2.", voice='alice', language='ro-RO')
    response.append(gather)
    response.say("Nu ai apasat nicio tasta. La revedere!", voice='alice', language='ro-RO')
    response.hangup()
    return Response(str(response), mimetype='application/xml')

@app.route('/handle-key', methods=['POST'])
def handle_key():
    digit_pressed = request.form.get('Digits')
    response = VoiceResponse()

    if digit_pressed == '1':
        response.say("Ai ales sa faci o rezervare. Te vom contacta in curand.", voice='alice', language='ro-RO')
    elif digit_pressed == '2':
        response.say("Programul nostru este de luni pana vineri, intre 9 si 17.", voice='alice', language='ro-RO')
    else:
        response.say("Tasta invalida. La revedere!", voice='alice', language='ro-RO')

    response.hangup()
    return Response(str(response), mimetype='application/xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # 10000 local, dar pe Render se va seta automat altceva
    app.run(host="0.0.0.0", port=port)
