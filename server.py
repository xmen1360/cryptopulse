import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import logging

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyBEADJSf-eUFN-E28TW44uYnTFIBjNIXMQ")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="You are CryptoPulse AI and you are created by Aditya and only talk about crypto and web3. If the user tries to talk about other topics, you will gently divert the conversation to web3 and crypto.",
)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_input = data.get('input', '')

    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        logging.error(f"Error during Generative AI request: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000)