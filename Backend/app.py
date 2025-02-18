from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Load translations dataset
data = pd.read_csv('translations.csv')

# Helper function to translate text
def translate_text(text, input_lang, output_lang):
    # Define column mapping
    lang_map = {
        'english': 'source',
        'hindi': 'target',
        'native': 'native'
    }

    # Ensure valid languages are provided
    if input_lang not in lang_map:
        return f"Invalid input language: {input_lang}. Supported languages: english, hindi, native."
    if output_lang not in lang_map:
        return f"Invalid output language: {output_lang}. Supported languages: english, hindi, native."

    input_column = lang_map[input_lang]
    output_column = lang_map[output_lang]

    # Find the translation row
    row = data[data[input_column].str.strip().str.lower() == text.strip().lower()]

    if not row.empty:
        return row.iloc[0][output_column]
    else:
        return "Translation not found."

# Define the API route for translation
@app.route('/translate', methods=['POST'])
def translate():
    try:
        # Parse JSON request
        request_data = request.get_json()

        input_lang = request_data.get('inputLanguage')
        output_lang = request_data.get('outputLanguage')
        text = request_data.get('text')

        # Validate input
        if not input_lang or not output_lang or not text:
            return jsonify({"error": "Missing required fields: inputLanguage, outputLanguage, or text."}), 400

        # Translate text
        translation = translate_text(text, input_lang.lower(), output_lang.lower())

        return jsonify({"translation": translation}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
