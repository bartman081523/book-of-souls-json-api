import logging
logger = logging.getLogger(__name__)

import inflect
from datetime import datetime
from deep_translator import GoogleTranslator

# Custom function to convert number to ordinal words
def number_to_ordinal_word(number):
    ordinal_dict = {
        1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
        6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
        11: "eleventh", 12: "twelfth", 13: "thirteenth", 14: "fourteenth",
        15: "fifteenth", 16: "sixteenth", 17: "seventeenth", 18: "eighteenth",
        19: "nineteenth", 20: "twentieth", 21: "twentyfirst", 22: "twentysecond",
        23: "twentythird", 24: "twentyfourth", 25: "twentyfifth",
        26: "twentysixth", 27: "twentyseventh", 28: "twentyeighth",
        29: "twentyninth", 30: "thirtieth", 31: "thirtyfirst"
    }
    return ordinal_dict.get(number, "")

def custom_normalize(text):
    mappings = {
        'ü': 'ue', 'ö': 'oe', 'ä': 'ae', 'ß': 'ss', 'Ü': 'Ue', 'Ö': 'Oe', 'Ä': 'Ae',
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'å': 'aa', 'ā': 'a', 'ă': 'a', 'ą': 'a',
        'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'Å': 'Aa', 'Ā': 'A', 'Ă': 'A', 'Ą': 'A',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'ē': 'e', 'ĕ': 'e', 'ė': 'e', 'ę': 'e', 'ě': 'e',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E', 'Ē': 'E', 'Ĕ': 'E', 'Ė': 'E', 'Ę': 'E', 'Ě': 'E',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'ī': 'i', 'ĭ': 'i', 'į': 'i', 'ı': 'i',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I', 'Ī': 'I', 'Ĭ': 'I', 'Į': 'I', 'I': 'I',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ø': 'oe', 'ō': 'o', 'ŏ': 'o', 'ő': 'o',
        'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Õ': 'O', 'Ø': 'Oe', 'Ō': 'O', 'Ŏ': 'O', 'Ő': 'O',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ū': 'u', 'ŭ': 'u', 'ů': 'u', 'ű': 'u', 'ų': 'u',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'Ue', 'Ū': 'U', 'Ŭ': 'U', 'Ů': 'U', 'Ű': 'U', 'Ų': 'U',
        'ç': 'c', 'ć': 'c', 'ĉ': 'c', 'ċ': 'c', 'č': 'c',
        'Ç': 'C', 'Ć': 'C', 'Ĉ': 'C', 'Ċ': 'C', 'Č': 'C',
        'ñ': 'n', 'ń': 'n', 'ņ': 'n', 'ň': 'n', 'ŋ': 'n',
        'Ñ': 'N', 'Ń': 'N', 'Ņ': 'N', 'Ň': 'N', 'Ŋ': 'N',
        'ý': 'y', 'ÿ': 'y', 'ŷ': 'y',
        'Ý': 'Y', 'Ÿ': 'Y', 'Ŷ': 'Y',
        'ž': 'zh', 'ź': 'z', 'ż': 'z',
        'Ž': 'Zh', 'Ź': 'Z', 'Ż': 'Z',
        'ð': 'd', 'Ð': 'D', 'þ': 'th', 'Þ': 'Th', 'ł': 'l', 'Ł': 'L', 'đ': 'd', 'Đ': 'D',
        'æ': 'ae', 'Æ': 'Ae', 'œ': 'oe', 'Œ': 'Oe',
        'ś': 's', 'ŝ': 's', 'ş': 's', 'š': 's',
        'Ś': 'S', 'Ŝ': 'S', 'Ş': 'S', 'Š': 'S',
        'ť': 't', 'ţ': 't', 'ŧ': 't', 'Ť': 'T', 'Ţ': 'T', 'Ŧ': 'T',
        'ŕ': 'r', 'ř': 'r', 'Ŕ': 'R', 'Ř': 'R',
        'ľ': 'l', 'ĺ': 'l', 'ļ': 'l', 'ŀ': 'l',
        'Ľ': 'L', 'Ĺ': 'L', 'Ļ': 'L', 'Ŀ': 'L',
        'ē': 'e', 'Ē': 'E',
        'ň': 'n', 'Ň': 'N',
        'ğ': 'g', 'Ğ': 'G',
        'ġ': 'g', 'Ġ': 'G',
        'ħ': 'h', 'Ħ': 'H',
        'ı': 'i', 'İ': 'I',
        'ĵ': 'j', 'Ĵ': 'J',
        'ķ': 'k', 'Ķ': 'K',
        'ļ': 'l', 'Ļ': 'L',
        'ņ': 'n', 'Ņ': 'N',
        'ŧ': 't', 'Ŧ': 'T',
        'ŭ': 'u', 'Ŭ': 'U'
    }
    for key, value in mappings.items():
        text = text.replace(key, value)
    return text




# Convert a numerical date to words with an ordinal day
def date_to_words(date_string):
    # Create an inflect engine
    inf_engine = inflect.engine()

    date_obj = datetime.strptime(date_string, "%Y-%m-%d")

    # Get year in the desired format
    year = date_obj.year
    if 1900 <= year <= 1999:
        year_words = f"{inf_engine.number_to_words(year // 100, andword='') } hundred"
        if year % 100 != 0:
            year_words += f" {inf_engine.number_to_words(year % 100, andword='')}"
    else:
        year_words = inf_engine.number_to_words(year, andword='')
    year_formatted = year_words.replace(',', '')  # Remove commas

    month = date_obj.strftime("%B")  # Full month name
    day = date_obj.day
    day_ordinal = number_to_ordinal_word(day)  # Get ordinal word for the day

    output_text = f"{day_ordinal} {month} {year_formatted}"

    return output_text



def translate_date_to_words(date, lang='en'):
    """Converts a date to words in the specified language."""
    if date is None:
        return "No date selected"
    
    date_string = date.strftime("%Y-%m-%d")
    logger.info(f"Date string: {date_string}")
    
    date_in_words = date_to_words(date_string)
    logger.info(f"Date in words: {date_in_words}")
    
    translator = GoogleTranslator(source='auto', target=lang)
    translated_date_words = translator.translate(date_in_words)
    logger.info(f"Translated date words: {translated_date_words}")
    
    # Normalize the text if it contains any special characters
    translated_date_words = custom_normalize(translated_date_words)
    logger.info(f"Normalized date words: {translated_date_words}")
    
    return translated_date_words