from flask import Flask, request, jsonify
import pyttsx3
import wikipedia

app = Flask(__name__)

def speak(text):
    """Convert text to speech."""
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()

def fetch_wikipedia(query):
    """Fetch summary from Wikipedia."""
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple results for your query. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "I couldn't find any results on Wikipedia."

@app.route('/voice-command', methods=['POST'])
def voice_command():
    data = request.json
    command = data.get('command', '').lower()
    response = "I didn't understand that."

    if 'wikipedia' in command:
        query = command.replace('wikipedia', '').strip()
        response = fetch_wikipedia(query)
    elif 'exit' in command or 'bye' in command:
        response = "Goodbye!"
    else:
        response = "I'm not sure how to help with that."

    speak(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
