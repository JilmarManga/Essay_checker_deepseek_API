from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
#import requests
import random
import json
import re # For parsing the response from DeepSeek API


app = Flask(__name__)
CORS(app) # Enable CORS for Front-Backend communication


# Load IELTS writing task 2 prompts
with open('prompts.json', 'r') as file:
    prompts = json.load(file)


'''# Initialize DeepSeek client: API's endpoint and key for web
client = OpenAI(
    api_key='sk-ce5a90e32c5144f3bfe86ca948e1566b',
    base_url="https://api.deepseek.com"
)'''

# Connect Ollama, Local model deepseek-r1
client = OpenAI(
    api_key='ollama',
    base_url="http://localhost:11434/v1"
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
            # model="deepseek-chat",
            model="deepseek-r1",
            messages=[
                #{"role": "system", "content": "You are an expert IELTS evaluator."},
                #{"role": "user", "content": f"Evaluate this IELTS Writing Task 2 essay and provide detailed feedback, including band scores for Task Response, Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy:\n\n {essay}"},
                #{"role": "system", "content": "You are an IELTS Writing Task 2 evaluator. Provide a band score (0-9) and detailed feedback on the essay, including Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy, and Conclusion."},
                #{"role": "user", "content": f"Evaluate this IELTS Writing Task 2 essay and provide a band score and feedback:\n\n{essay}"},
                {"role": "system", "content": "You are an IELTS Writing Task 2 evaluator."},
                {"role": "user", "content": f"Provide a band score and consice constructive feedback on the essay, including Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy, and a overall Conclusion.\n\n{essay}"},
                # {"role": "user", "content": f"Evaluate this IELTS Writing Task 2 essay and provide detailed feedback in the following order: Band Score, general feedback then including band scores for Task Response, Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy each one with its feedback and finally a conclusion. all the items in a diferent paragraph\n\n {essay}"},
            ],
            temperature=0.7,
            stream=False
        )

        # Extract the evaluation from the API response
        evaluation = response.choices[0].message.content

        # Log the raw evaluation for debugging
        print("Raw evaluation Response:")
        print(evaluation)

        # Check if evaluation is None or empty
        '''if not evaluation:
            return jsonify({
                "bandScore": "N/A",
                "feedback": {
                    "taskAchievement": "No feedback available.",
                    "coherenceAndCohesion": "No feedback available.",
                    "lexicalResource": "No feedback available.",
                    "grammaticalRangeAndAccuracy": "No feedback available.",
                    "conclusion": "No feedback available."
                }
            }), 500'''


        '''# Parse the evaluation into a structured format (e.g., score and feedback)
        band_score = evaluation.split("Band Score: ")[1].split("\n")[0] if "Band Score: " in evaluation else evaluation'''
        '''feedback = evaluation.split("Feedback: ")[1] if "Feedback: " in evaluation else evaluation'''

        # Parce de band score
        band_score_match = re.search(r"Band Score: (\d+\.\d+)", evaluation)
        band_score = band_score_match.group(1) if band_score_match else 'N/A'
        '''band_score = band_score_match.group(1) if band_score_match in evaluation else evaluation'''

        # Parse feedback for each category
        feedback = {
            "taskAchievement": extract_feedback(evaluation, "Task Achievement"),
            "coherenceAndCohesion": extract_feedback(evaluation, "Coherence and Cohesion"),
            "lexicalResource": extract_feedback(evaluation, "Lexical Resource"),
            "grammaticalRangeAndAccuracy": extract_feedback(evaluation, "Grammatical Range and Accuracy"),
            "conclusion": extract_feedback(evaluation, "Overall Conclusion")
        }

        # Log the parsed feedback debugging
        print("Parsed feedback:")
        print(feedback)

        return jsonify({
            "bandScore": band_score,
            "feedback": feedback
        })

    except Exception as e:
        return jsonify(print({"error": str(e)})), 500

# Helper function to extract feedback for a specific category
def extract_feedback(evaluation, category):
    # Use regex to find the feedback for the given category
    pattern = rf"{category}: (.*?)(?=\n\n|$)"
    match = re.search(pattern, evaluation, re.DOTALL)
    if match:
        return match.group(1).strip() #Remove leading/trailing whitespace
    return f"No feedback available for this {category}"

if __name__ == '__main__':
    app.run(debug=True)
