import nltk
from nltk.tokenize import word_tokenize

# Загрузка данных для русского языка
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_ru')

def get_part_of_speech(word):
    # Токенизируем слово
    tokens = word_tokenize(word, language='russian')
    # Определяем часть речи с помощью nltk.pos_tag
    pos_tags = nltk.pos_tag(tokens, lang='rus')
    # Возвращаем часть речи слова
    return pos_tags[0][1] if pos_tags else None

# Пример использования
word = "яблоко"
part_of_speech = get_part_of_speech(word)
print(f"Часть речи слова '{word}': {part_of_speech}")
