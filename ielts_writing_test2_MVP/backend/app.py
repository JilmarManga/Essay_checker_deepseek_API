from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
#import requests
import random
import json


app = Flask(__name__)
CORS(app) # Enable CORS for Front-Backend communication


# Load IELTS writing task 2 prompts
with open('prompts.json', 'r') as file:
    prompts = json.load(file)


# Initialize DeepSeek client: API's endpoint and key
client = OpenAI(
    api_key='sk-ce5a90e32c5144f3bfe86ca948e1566b',
    base_url="https://api.deepseek.com"
)

# Route to get a random prompt
@app.route("/get-prompt", methods=["GET"])
def get_prompt():
    prompt = random.choice(prompts)
    return jsonify({"prompt": prompt})

#Route to evaluate an essay
@app.route("/evaluate-essay", methods=["POST"])
def evaluate_essay():
    data = request.json
    essay = data.get("essay")

    # Ensure the data is a dictionary
    if not isinstance(data, dict):
        return jsonify(print({"error": "Invalid JSON format: Expected a dictionary"})), 400

    # Access the essay field using .get() ensuring the essay was provided
    if not essay:
        return jsonify({"error": "No essay provided"}), 400

    # Call DeepSeek API for evaluation
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert IELTS evaluator."},
                {"role": "user", "content": f"Evaluate this IELTS Writing Task 2 essay and provide detailed feedback, including band scores for Task Response, Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy:\n\n {essay}"},
            ],
            stream=False
        )

        # Extract the evaluation from the API response
        evaluation = response.choices[0].message.content

        # Parse the evaluation into a structured format (e.g., score and feedback)

        band_score = evaluation.split("Band Score: ")[1].split("\n")[0] if "Band Score: " in evaluation else "N/A"
        feedback = evaluation.split("Feedback: ")[1] if "Feedback: " in evaluation else evaluation

        return jsonify({
            "band_score": band_score,
            "feedback": feedback
        })

    except Exception as e:
        return jsonify(print({"error": str(e)})), 500

if __name__ == '__main__':
    app.run(debug=True)




'''@app.route('/evaluate-essay', methods=['POST'])
def evaluate_essay():
    try:
        # Parse JSON data from the request body
        data = request.json

        # Ensure the data is a dictionary
        if not isinstance(data, dict):
            return jsonify(print({"error": "Invalid JSON format: Expected a dictionary"})), 400

        # Access the essay field using .get()
        essay = data.get("essay")
        if not essay:
            return jsonify({"error": "Missing 'essay' field"}), 400

        # Process the essay (e.g., evaluate it)
        # Replace this with your actual logic
        evaluation_result = {"score": 7, "feedback": "Good essay!"}

        return jsonify(evaluation_result)
    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
'''