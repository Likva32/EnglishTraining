import pytesseract
from googletrans import Translator
from spellchecker import SpellChecker
import re
import time
import pprint
import os
import pickle


def normalize_text(text):
    spell = SpellChecker()
    units = {}
    lines = text.split('\n')
    current_unit = None
    current_category = None

    for line in lines:
        line = line.strip()
        unit_match = re.search(r'[Uu]nit (\d+)', line)
        if unit_match:
            current_unit = int(unit_match.group(1))
            if units.get(current_unit) is None:
                units[current_unit] = {}
            print(f'penis   {units}')
            print(f'penis   {current_unit}')
        elif line:
            category_match = re.search(r'\b(basic|medium|extreme)\b', line, re.IGNORECASE)
            if category_match:
                current_category = category_match.group(1).lower()
                if current_unit is not None:
                    units[current_unit][current_category] = []
            else:
                match = re.search(r'\b(\w+)\b', line)
                if match and current_unit is not None and current_category is not None:
                    word = match.group(1)
                    if len(word) > 2:
                        corrected_word = spell.correction(word)
                        if corrected_word == word and corrected_word in spell and corrected_word in spell.known(
                                spell.candidates(word)):
                            units[current_unit][current_category].append(word)
    return units


def write_image_list_to_file(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            images.append(filename)
    images.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    with open('images.txt', 'w') as file:
        for image in images:
            file.write(r'images//' + image + '\n')


def translate_words(units):
    translator = Translator()
    cache = {}

    for unit, categories in units.items():
        translated_unit = {}
        for category, words in categories.items():
            translated_category_ru = cache.get((category, 'ru'))
            translated_category_he = cache.get((category, 'he'))
            if not translated_category_ru:
                translated_category_ru = translator.translate(category, dest='ru').text
                cache[(category, 'ru')] = translated_category_ru
            if not translated_category_he:
                translated_category_he = translator.translate(category, dest='he').text
                cache[(category, 'he')] = translated_category_he

            translated_words = {}
            for word in words:
                translated_word_ru = cache.get((word, 'ru'))
                translated_word_he = cache.get((word, 'he'))
                if not translated_word_ru:
                    try:
                        translated_word_ru = translator.translate(word, dest='ru').text
                        cache[(word, 'ru')] = translated_word_ru
                    except:
                        translated_word_ru = "Translation not available"
                if not translated_word_he:
                    try:
                        translated_word_he = translator.translate(word, dest='he').text
                        cache[(word, 'he')] = translated_word_he
                    except:
                        translated_word_he = "Translation not available"

                translated_words[word] = {
                    'ru': translated_word_ru,
                    'he': translated_word_he
                }

            translated_category = {
                category: translated_words
            }
            translated_unit.update(translated_category)

        units[unit] = translated_unit
        time.sleep(0.1)

    return units


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
write_image_list_to_file(r'C:\Users\artur\Desktop\projects\EnglishTraining\images')
text = pytesseract.image_to_string('images.txt')

normalized_words = normalize_text(text)
pprint.pprint(normalized_words)

# translate words
# translated_words = translate_words(normalized_words)
# pprint.pprint(translated_words)

# # safe translated_words
# with open('translated_words.pickle', 'wb') as f:
#     pickle.dump(translated_words, f)

# load translated_words
with open('data.pickle', 'rb') as f:
    data = pickle.load(f)
print(data[1]['basic'])

keys = list(data[1]['basic'].keys())[:10]
print(keys)