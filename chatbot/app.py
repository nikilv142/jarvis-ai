from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# 🔑 Replace with your Groq API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_ai_response(message):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": message}
            ],
            model="openai/gpt-oss-120b"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    reply = get_ai_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
