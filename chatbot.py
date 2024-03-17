import google.generativeai.types.generation_types as gen_types
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
    
genai.configure(api_key='AIzaSyCitAX1XE_qmi59IiF0EC0-hbgoHyN_zQI')
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

@app.route("/chatbot/", methods=["POST"])
def chatbot():
    data = request.json
    text = data["text"]
    response_text = ""
    try:
        for chunk in get_gemini_response(text):
            response_text += chunk.text
    except gen_types.BrokenResponseError as e:
        print("Broken response error:", e)
        last_send, last_received = chat.rewind()
        response_text = "Sorry, I couldn't process your request. Can you please try again?"

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True, port=5000)



