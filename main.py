import pytesseract
from spellchecker import SpellChecker
import re


def normalize_text(text):
    spell = SpellChecker()
    normalized_words = []
    lines = text.split('\n')
    for line in lines:
        match = re.match(r'^([^\s-]+)', line)
        if match:
            word = match.group(1)
            if len(word) > 2:  # Проверка на длину слова (минимум 3 символа)
                corrected_word = spell.correction(word)
                if corrected_word == word and corrected_word in spell and corrected_word in spell.known(spell.candidates(word)):
                    normalized_words.append(word)
    return normalized_words


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string('images.txt')
print(text)
normalized_words = normalize_text(text)
for word in normalized_words:
    print(word)
