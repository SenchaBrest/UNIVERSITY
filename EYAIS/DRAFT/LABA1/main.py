import tkinter as tk
from tkinter import ttk
import PyPDF2
import tkinter.messagebox

import pymorphy3
import grammemes
from grammemes import *


class Morphius:
    def __init__(self):
        self.morph = pymorphy3.MorphAnalyzer()
        self.w = None

    def parse(self, word):
        self.w = self.morph.parse(word)[0]

    def get_info(self):
        queries = [
            'POS',
            'animacy',
            'aspect',
            'case',
            'gender',
            'mood',
            'number',
            'person',
            'tense',
            'transitivity',
            'voice'
        ]

        result = ''
        for query in queries:
            buf = getattr(grammemes, query).get(getattr(self.w.tag, query), '')
            result += buf + ', ' if buf != '' else ''
        if result.endswith(', '):
            result = result[:-2]

        return result

    def inflect(self, form: set[str]):
        return self.w.inflect(form)


class WordViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Viewer")

        self.label = ttk.Label(root, text="Выберите слово:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.word_combobox = ttk.Combobox(root, state="readonly", width=40)
        self.word_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.word_combobox.bind("<<ComboboxSelected>>", self.display_word_info)

        self.text_info = tk.Text(root, height=15, width=50)
        self.text_info.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.grid(row=0, column=2, padx=10, pady=10)

        self.search_button = tk.Button(root, text="Найти", command=self.search_word_info)
        self.search_button.grid(row=0, column=3, padx=10, pady=10)

        self.search_result_text = tk.Text(root, height=15, width=50)
        self.search_result_text.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        self.words = self.load_data_from_file('test.pdf')
        self.word_combobox["values"] = sorted(self.words)

        self.morph_analyzer = pymorphy3.MorphAnalyzer()
        self.analyzer = Morphius()

    def load_data_from_file(self, filename):
        words = []
        with open(filename, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                words.extend(text.split())
        return words

    def display_word_info(self):
        selected_word = self.word_combobox.get()
        lexemes = self.get_lexemes(selected_word)
        self.text_info.delete(1.0, tk.END)
        self.text_info.insert(tk.END, f"Слово: {selected_word}\n")
        self.text_info.insert(tk.END, f"Лексемы: {lexemes}\n")

    def get_lexemes(self, word):
        self.analyzer.parse(word)
        lexemes = self.analyzer.get_info()
        return lexemes

    def search_word_info(self):
        query = self.search_entry.get()
        selected_word = self.word_combobox.get()

        query_parts = query.split(',')
        forms = set()

        def process_query_part(query_part):
            query_mapping = {
                # Части речи
                **{value: key for key, value in POS.items()},
                # Одушевленность
                **{value: key for key, value in animacy.items()},
                # Вид
                **{value: key for key, value in aspect.items()},
                # Падеж
                **{value: key for key, value in case.items()},
                # Род
                **{value: key for key, value in gender.items()},
                # Наклонение
                **{value: key for key, value in mood.items()},
                # Число
                **{value: key for key, value in number.items()},
                # Лицо
                **{value: key for key, value in person.items()},
                # Время
                **{value: key for key, value in tense.items()},
                # Переходность
                **{value: key for key, value in transitivity.items()},
                # Залог
                **{value: key for key, value in voice.items()}
            }
            return query_mapping.get(query_part, None)

        for query_part in query_parts:
            query_part = query_part.strip().lower()
            forms.add(process_query_part(query_part))
            print(query_part)
            print(forms)

        try:
            result = self.analyzer.inflect(form=forms)
            if result is not None:
                self.search_result_text.delete(1.0, tk.END)
                self.search_result_text.insert(tk.END, f"Форма слова {selected_word} по критерию '{query}':\n")
                self.search_result_text.insert(tk.END, result.word)
        except:
            tk.messagebox.showerror("Ошибка", "Неправильный формат запроса!")


if __name__ == "__main__":
    root = tk.Tk()
    app = WordViewerApp(root)
    root.mainloop()
