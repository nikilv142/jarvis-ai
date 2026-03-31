from flask import Flask, render_template, request, Response
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    def generate():
        try:
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Respond clearly in simple points without markdown symbols."},
                    {"role": "user", "content": user_message}
                ],
                model="openai/gpt-oss-120b",
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(generate(), content_type='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
