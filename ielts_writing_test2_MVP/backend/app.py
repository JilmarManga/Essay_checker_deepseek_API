from flask import Flask, request, jsonify
from flask_cors import CORS
#import requests
import json


app = Flask(__name__)
CORS(app) # Enable CORS for Front-Backend communication


#Load IELTS writing task 2 prompts
with open('prompts.py', 'r') as file:
    prompts = json.load(file)


#DeepSeek API endpoint and key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/evaluate"
API_KEY = "YOUR_DEEPSEEK_API_KEY"

#Route to get a random prompt
@app.route("/get-prompt", methods=["GET"])
def get_prompt():
    import random
    prompt = random.choice(prompts)
    return jsonify({"prompt": prompt})


#Route to evaluate an essay
@app.route("/evaluate-essay", methods=["POST"])
def evaluate_essay():
    data = request.json
    essay = data.get("essay")

    if not essay:
        return jsonify({"error": "No essay provided"}), 400

    try:
        # Call DeepSeek API for evaluation
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "essay": essay,
            "task": "IELTS Writing Test 2"
        }
        response = request.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        evaluation = response.json()

        return jsonify(evaluation)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
