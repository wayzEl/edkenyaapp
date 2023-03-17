from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import openai
import os
from datetime import datetime

app = Flask(__name__)
run_with_ngrok(app)

api_call_counter = 0
api_key_usage = {}

def ask_ai(query, api_key):
    # Here, you should use the provided API key to communicate with OpenAI API
    # and get the response from the GPT model based on the query.
    # For now, we'll return a dummy response.
    response = f"Response for query: {query}"
    return response

@app.route('/ask', methods=['POST'])
def ask_endpoint():
    global api_call_counter, api_key_usage
    api_call_counter += 1

    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'error': 'No API key provided'}), 400

    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Update the API key usage
    current_month = datetime.now().strftime('%Y-%m')
    if api_key not in api_key_usage:
        api_key_usage[api_key] = {current_month: 0}
    elif current_month not in api_key_usage[api_key]:
        api_key_usage[api_key][current_month] = 0

    api_key_usage[api_key][current_month] += 1

    response = ask_ai(query, api_key)
    return jsonify({'response': response})

@app.route('/api_key_usage', methods=['GET'])
def api_key_usage_endpoint():
    api_key = request.args.get('api_key')
    if not api_key:
        return jsonify({'error': 'No API key provided'}), 400

    if api_key not in api_key_usage:
        return jsonify({'error': 'API key not found'}), 404

    return jsonify(api_key_usage[api_key])

@app.route('/call_count', methods=['GET'])
def call_count_endpoint():
    global api_call_counter
    return jsonify({'call_count': api_call_counter})

app.run()
