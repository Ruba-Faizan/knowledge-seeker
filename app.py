from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)


API_KEY = os.environ.get("GEMINI_API_KEY") # ya jo bhi variable aapka naam ho
client = genai.Client(api_key=API_KEY)

@app.route("/")
def home():
    return render_template("index.en.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print(f"--- User message received: {user_message} ---")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        print("--- Calling Gemini 3.5 Flash Lite... ---")
        # Yahan model name gemini-3.5-flash-lite kar diya gaya hai
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_message,
        )
        print("--- Response received successfully! ---")
        
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"❌ ERROR OCCURRED: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)