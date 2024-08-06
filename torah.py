import logging
logger = logging.getLogger(__name__)

import json
import os
import re
from deep_translator import GoogleTranslator
from gematria import calculate_gematria
import math

# Hebrew gematria values for relevant characters
gematria_values = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 500, 'ל': 30, 'מ': 40, 'ם': 600, 'נ': 50, 'ן': 700,
    'ס': 60, 'ע': 70, 'פ': 80, 'ף': 800, 'צ': 90, 'ץ': 900, 'ק': 100,
    'ר': 200, 'ש': 300, 'ת': 400
}

# Reverse dictionary for converting gematria values back to Hebrew characters
reverse_gematria_values = {v: k for k, v in gematria_values.items()}

# Function to convert a Hebrew string to its gematria values
def string_to_gematria(s):
    return [gematria_values.get(char, 0) for char in s]  # Handle characters not in the dictionary

# Function to convert a single gematria value to Hebrew characters
def gematria_to_string(value):
    result = []
    for val in sorted(reverse_gematria_values.keys(), reverse=True):
        while value >= val:
            result.append(reverse_gematria_values[val])
            value -= val
    return ''.join(result)

# Function to calculate the average gematria values of corresponding characters and convert them to Hebrew characters
def average_gematria(str1, str2):
    # Convert strings to gematria values
    gematria1 = string_to_gematria(str1)
    gematria2 = string_to_gematria(str2)

    # Handle cases where strings have different lengths by padding with 0s
    max_len = max(len(gematria1), len(gematria2))
    gematria1.extend([0] * (max_len - len(gematria1)))
    gematria2.extend([0] * (max_len - len(gematria2)))

    # Calculate the average of corresponding gematria values and apply math.ceil
    average_gematria_values = [math.ceil((g1 + g2) / 2) for g1, g2 in zip(gematria1, gematria2)]

    # Convert the average gematria values back to Hebrew characters
    return ''.join(gematria_to_string(val) for val in average_gematria_values)

def process_json_files(start, end, step, rounds="1", length=0, tlang="en", strip_spaces=True, strip_in_braces=True, strip_diacritics=True, average_compile=False):
    base_path = "texts"
    translator = GoogleTranslator(source='auto', target=tlang)
    results = []

    for i in range(start, end + 1):
        file_name = f"{base_path}/{i:02}.json"
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                text_blocks = data["text"]

                full_text = ""
                for block in text_blocks:
                    full_text += ' '.join(block)

                clean_text = full_text
                if strip_in_braces:
                    clean_text = re.sub(r"\[.*?\]", "", clean_text, flags=re.DOTALL)
                if strip_diacritics:
                    clean_text = re.sub(r"[^\u05D0-\u05EA ]+", "", clean_text)
                if strip_spaces:
                    clean_text = clean_text.replace(" ", "")
                else:
                    clean_text = clean_text.replace("  ", " ")
                    clean_text = clean_text.replace("  ", " ")
                    clean_text = clean_text.replace("  ", " ")

                text_length = len(clean_text)
                
                selected_characters_per_round = {}
                for round_num in map(int, rounds.split(',')):
                    # Handle cases where no characters should be selected
                    if not (round_num == 1 and step > text_length) and not (round_num == -1 and step > text_length):
                        # Corrected logic for negative rounds and step = 1
                        if round_num > 0:
                            current_position = step - 1 
                        else:
                            current_position = text_length - 1 if step == 1 else text_length - step

                        completed_rounds = 0
                        selected_characters = ""  

                        while completed_rounds < abs(round_num):
                            selected_characters += clean_text[current_position % text_length]

                            # Update current_position based on the sign of rounds
                            current_position += step if round_num > 0 else -step

                            if (round_num > 0 and current_position >= text_length * (completed_rounds + 1)) or \
                               (round_num < 0 and current_position < 0):
                                completed_rounds += 1

                        selected_characters_per_round[round_num] = selected_characters
                
                if average_compile and len(selected_characters_per_round) > 1:
                    result_text = ""
                    keys = sorted(selected_characters_per_round.keys())
                    for i in range(len(keys) - 1):
                        result_text = average_gematria(selected_characters_per_round[keys[i]], selected_characters_per_round[keys[i+1]])
                else:
                    result_text = ''.join(selected_characters_per_round.values())

                if length != 0:
                    result_text = result_text[:length]

                translated_text = translator.translate(result_text) if result_text else ""

                if result_text:  # Only append if result_text is not empty
                    results.append({
                        "book": i,
                        "title": data["title"],
                        "els_result_text": result_text,
                        "els_result_gematria": calculate_gematria(result_text),
                        "translated_text": translated_text
                    })

        except FileNotFoundError:
            results.append({"error": f"File {file_name} not found."})
        except json.JSONDecodeError as e:
            results.append({"error": f"File {file_name} could not be read as JSON: {e}"})
        except KeyError as e:
            results.append({"error": f"Expected key 'text' is missing in {file_name}: {e}"})

    return results


# Tests
test_results = [
    (process_json_files(0, 0, 21, rounds="3", length=0), "שרק"),
    (process_json_files(0, 0, 22, rounds="1", length=0), "ת"), 
    (process_json_files(0, 0, 22, rounds="3", length=0), "תתת"),
    (process_json_files(0, 0, 23, rounds="3", length=0), "אבג"),
    (process_json_files(0, 0, 11, rounds="1", length=0), "כת"),
    (process_json_files(0, 0, 2, rounds="1", length=0), "בדוחילנעצרת"),
    (process_json_files(0, 0, 23, rounds="1", length=0), None),  # Expect None, when no results
    (process_json_files(0, 0, 23, rounds="-1", length=0), None),  # Expect None, when no results
    (process_json_files(0, 0, 22, rounds="-1", length=0), "א"),
    (process_json_files(0, 0, 22, rounds="-2", length=0), "אא"),
    (process_json_files(0, 0, 1, rounds="-1", length=0), "תשרקצפעסנמלכיטחזוהדגבא"), # Reversed Hebrew alphabet
    (process_json_files(0, 0, 1, rounds="1,-1", length=0), "אבגדהוזחטיכלמנסעפצקרשתתשרקצפעסנמלכיטחזוהדגבא"), # Combined rounds
    (process_json_files(0, 0, 22, rounds="1,-1", length=0, average_compile=True), "רא"),  # average compile test (400+1) / 2 = math.ceil(200.5)=201=200+1="רא"
]

all_tests_passed = True
for result, expected in test_results:
    if expected is None:  # Check if no result is expected
        if not result:
            logger.info(f"Test passed: Expected no results, got no results.")
        else:
            logger.error(f"Test failed: Expected no results, but got: {result}")
            all_tests_passed = False
    else:
        # Check if result is not empty before accessing elements
        if result: 
            els_result_text = result[0]['els_result_text']
            if els_result_text == expected:
                logger.info(f"Test passed: Expected '{expected}', got '{els_result_text}'")
            else:
                logger.error(f"Test failed: Expected '{expected}', but got '{els_result_text}'")
                all_tests_passed = False
        else:
            logger.error(f"Test failed: Expected '{expected}', but got no results")
            all_tests_passed = False

if all_tests_passed:
    logger.info("All round tests passed.")