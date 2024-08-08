import logging
import json
from utils import translate_date_to_words
from gematria import calculate_gematria, strip_diacritics
import torah
from flask import Flask, request, jsonify
from datetime import datetime

# Set logging level to WARNING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Use Flask API endpoint
@app.route('/els_search', methods=['POST'])
def els_search_api():
    data = request.get_json()
    date = data.get('date')
    name_or_topic = data.get('name_or_topic')

    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."})

    date_words = translate_date_to_words(date_obj)
    gematria_sum = calculate_gematria_sum(name_or_topic, date_words)

    # Default ELS search parameters
    start = 1
    end = 39
    step = gematria_sum
    rounds = "1,-1"
    length = 0
    strip_spaces = True
    strip_in_braces = True
    strip_diacritics_chk = True

    results = perform_els_search(start, end, step, rounds, length, strip_spaces, strip_in_braces, strip_diacritics_chk)
    search_phrase = f"{date_words} {name_or_topic}"

    json_output = generate_json_dump(start, end, step, rounds, length, strip_spaces, strip_in_braces, strip_diacritics_chk, search_phrase, results)

    return jsonify(json.loads(json_output))

# Helper functions
def calculate_gematria_sum(text, date_words):
    combined_input = f"{text} {date_words}"
    sum_value = calculate_gematria(strip_diacritics(combined_input))
    logger.info(f"journal phrase: {combined_input}")
    logger.infp(f"journal gematria sum: {sum_value}")
    return sum_value

def perform_els_search(start, end, step, rounds, length, strip_spaces, strip_in_braces, strip_diacritics_chk):
    results = torah.process_json_files(start, end, step, rounds, length, 'en', strip_spaces, strip_in_braces, strip_diacritics_chk)
    return results

def generate_json_dump(start, end, step, rounds, length, strip_spaces, strip_in_braces, strip_diacritics_chk, search_phrase, results):
    config = {
        "Start Book": start,
        "End Book": end,
        "Step": step,
        "Rounds": rounds,
        "Length": length,
        "Target Language": 'en',
        "Strip Spaces": strip_spaces,
        "Strip Text in Braces": strip_in_braces,
        "Strip Diacritics": strip_diacritics_chk,
        "Search Phrase": search_phrase
    }
    result = {
        "Configuration": config,
        "Results": results
    }
    return json.dumps(result, indent=4, ensure_ascii=False)

# You can remove the following line if you don't need it for local testing:
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=7860)