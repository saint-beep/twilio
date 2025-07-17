from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai
import os

# Configurare OpenAI
openai.api_key = os.getenv("OPEN_API_KEY")

app = Flask(__name__)

# Sesiuni pe baza CallSid (fiecare apel separat)
sessions = {}

@app.route("/voice", methods=["POST"])
def voice():
    call_sid = request.form.get("CallSid")
    speech_result = request.form.get("SpeechResult", "")
    session = sessions.get(call_sid, {"step": 1})

    response = VoiceResponse()

    # Prima dată: întreabă
    if session["step"] == 1:
        gather = Gather(input="speech", action="/voice", method="POST")
        gather.say("Salut! Pentru ce zi doriți o rezervare?")
        response.append(gather)
        session["step"] = 2

    # După ce a vorbit clientul
    elif session["step"] == 2 and speech_result:
        prompt = f"Clientul a spus: {speech_result}. Răspunde frumos și întreabă pentru ce oră dorește rezervarea."

        # trimitem la GPT
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = gpt_response.choices[0].message.content
        gather = Gather(input="speech", action="/voice", method="POST")
        gather.say(reply)
        response.append(gather)
        session["step"] = 3

    # Confirmare finală
    elif session["step"] == 3 and speech_result:
        reply = f"Am înregistrat răspunsul dumneavoastră: {speech_result}. Vă mulțumim pentru apel!"
        response.say(reply)
        sessions.pop(call_sid, None)

    else:
        response.say("Nu am înțeles. Încercați din nou mai târziu.")

    sessions[call_sid] = session
    return str(response)

if __name__ == "__main__":
    app.run(port=5000)
