import unicodedata
import logging

logger = logging.getLogger(__name__)

def strip_diacritics(text):
    """
    Entfernt Diakritika von Unicode-Zeichen, um den Basisbuchstaben zu erhalten, und gibt Warnungen
    für tatsächlich unbekannte Zeichen aus.
    """
    stripped_text = ''
    for char in unicodedata.normalize('NFD', text):
        if unicodedata.category(char) not in ['Mn', 'Cf']:
            stripped_text += char
        else:
            logger.info(f"Info: Diakritisches Zeichen '{char}' wird ignoriert.")
    return stripped_text

def letter_to_value(letter):
    """
    Konvertiert einen einzelnen Buchstaben in seinen Gematria-Wert, ignoriert Leerzeichen
    und Nicht-Buchstaben-Zeichen.
    """
    # Dein vorhandenes Wörterbuch bleibt unverändert
    values = {
    # Lateinische Buchstaben
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 600,
    'k': 10, 'l': 20, 'm': 30, 'n': 40, 'o': 50, 'p': 60, 'q': 70, 'r': 80, 's': 90,
    't': 100, 'u': 200, 'v': 700, 'w': 900, 'x': 300, 'y': 400, 'z': 500,

    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 600,
    'K': 10, 'L': 20, 'M': 30, 'N': 40, 'O': 50, 'P': 60, 'Q': 70, 'R': 80, 'S': 90,
    'T': 100, 'U': 200, 'V': 700, 'W': 900, 'X': 300, 'Y': 400, 'Z': 500,

    # Basisbuchstaben und einige bereits genannte Varianten
    'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ى': 10, 'ك': 20, 'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
    'ٱ': 1, # Alif Wasla
    'ـ': 0, # Tatweel

    # Zusätzliche Varianten und Sonderzeichen
    'ة': 400, # Taa Marbuta
    'ؤ': 6,  # Waw mit Hamza darüber
    'ئ': 10, # Ya mit Hamza darüber
    'ء': 1,  # Hamza
    'ى': 10, # Alif Maqsurah
    'ٹ': 400, # Taa' marbuta goal
    'پ': 2,  # Pe (Persisch/Urdu)
    'چ': 3,  # Che (Persisch/Urdu)
    'ژ': 7,  # Zhe (Persisch/Urdu)
    'گ': 20, # Gaf (Persisch/Urdu)
    'ڭ': 20, # Ngaf (Kazakh, Uyghur, Uzbek, and in some Arabic dialects)
    'ں': 50, # Noon Ghunna (Persisch/Urdu)
    'ۀ': 5,  # Heh with Yeh above (Persisch/Urdu)
    'ے': 10, # Barree Yeh (Persisch/Urdu)
    '؋': 0,  # Afghani Sign (wird als Währungssymbol verwendet, nicht für Gematria relevant, aber hier zur Vollständigkeit aufgeführt)

    # Anmerkung: Das Währungssymbol und ähnliche Zeichen sind in einem Gematria-Kontext normalerweise nicht relevant,
    # werden aber der Vollständigkeit halber aufgeführt. Es gibt noch viele weitere spezifische Zeichen in erweiterten
    # arabischen Schriftsystemen (z.B. für andere Sprachen wie Persisch, Urdu, Pashto usw.), die hier nicht vollständig
    # abgedeckt sind.

    # Grund- und Schlussformen hebräischer Buchstaben

    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'כ': 20, 'ך': 500, 'ל': 30, 'מ': 40, 'ם': 600, 'נ': 50, 'ן': 700, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 800,
    'צ': 90, 'ץ': 900, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,

    # Griechische Buchstaben
    'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ϝ': 6, 'ζ': 7, 'η': 8, 'θ': 9, 'ι': 10,
    'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70, 'π': 80, 'ϟ': 90, 'ρ': 100,
    'σ': 200, 'τ': 300, 'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800, 'ϡ': 900,

        # Griechische Großbuchstaben
    'Α': 1, 'Β': 2, 'Γ': 3, 'Δ': 4, 'Ε': 5, 'Ϝ': 6, 'Ζ': 7, 'Η': 8, 'Θ': 9, 'Ι': 10,
    'Κ': 20, 'Λ': 30, 'Μ': 40, 'Ν': 50, 'Ξ': 60, 'Ο': 70, 'Π': 80, 'Ϟ': 90, 'Ρ': 100,
    'Σ': 200, 'Τ': 300, 'Υ': 400, 'Φ': 500, 'Χ': 600, 'Ψ': 700, 'Ω': 800, 'Ϡ': 900,
    'σ': 200,  # Sigma
    'ς': 200,  # Final Sigma
    }

    # Stelle sicher, dass Diakritika entfernt werden, bevor auf das Wörterbuch zugegriffen wird
    letter_no_diacritics = strip_diacritics(letter)

    if letter_no_diacritics in values:
        return values[letter_no_diacritics.lower()]
    elif letter.strip() == "":  # Ignoriere Leerzeichen und leere Zeilen
        return 0
    else:
        # Gib eine spezifische Warnung aus, wenn das Zeichen unbekannt ist
        logger.info(f"Warnung: Unbekanntes Zeichen '{letter}' ignoriert.")
        return 0


def calculate_gematria(text):
    """Calculate the Gematria value of a given Hebrew text, ignoring spaces and non-Hebrew characters."""
    return sum(letter_to_value(letter) for letter in text if letter.strip() != "")
