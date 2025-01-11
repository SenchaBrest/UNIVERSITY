import tkinter as tk
from tkinter import ttk
import pymorphy3
from bs4 import BeautifulSoup


class WordViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Viewer")

        self.label = ttk.Label(root, text="Выберите слово:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.word_combobox = ttk.Combobox(root, state="readonly", width=30)
        self.word_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.word_combobox.bind("<<ComboboxSelected>>", self.display_word_info)

        self.text_info = tk.Text(root)
        self.text_info.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.search_result_text = tk.Text(root)
        self.search_result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.edit_distance_button = tk.Button(root, text="Расстояние между словами", command=self.display_edit_distance_all_forms)
        self.edit_distance_button.grid(row=4, column=0, padx=10, pady=10)

        self.edit_distance_all_forms_button = tk.Button(root, text="Расстояние между всеми формами слова", command=self.display_edit_distance_all_forms_for_selected_word)
        self.edit_distance_all_forms_button.grid(row=4, column=1, padx=10, pady=10)

        self.words = self.load_data_from_file("test.html")
        self.word_combobox["values"] = self.words

        self.morph_analyzer = pymorphy3.MorphAnalyzer()

    def load_data_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        words = self.extract_words_from_html(content)
        return words

    def extract_words_from_html(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        words = [tag.get_text() for tag in soup.find_all('p')]
        return words

    def display_word_info(self, event=None):
        selected_word = self.word_combobox.get()
        forms = self.get_word_forms(selected_word)
        self.text_info.delete(1.0, tk.END)
        self.text_info.insert(tk.END, f"Слово: {selected_word}\n")
        self.text_info.insert(tk.END, f"Формы: {', '.join(forms)}\n")
        self.search_result_text.delete(1.0, tk.END)

    def get_word_forms(self, word):
        analyzed_word = self.morph_analyzer.parse(word)[0]
        forms = [parsed_word.word for parsed_word in analyzed_word.lexeme]
        return forms
    
    def edit_distance(self, word1, word2):
        len1 = len(word1)
        len2 = len(word2)
        
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j
        
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if word1[i - 1] == word2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
        
        return dp[len1][len2]
    
    def edit_distance_all_forms(self):
        all_forms = self.words
        len_all_forms = len(all_forms)
        
        distance_dict = {}
        
        for i in range(len_all_forms):
            for j in range(i + 1, len_all_forms):
                distance = self.edit_distance(all_forms[i], all_forms[j])
                distance_dict[(all_forms[i], all_forms[j])] = distance
        
        return distance_dict
        
    def display_edit_distance_all_forms(self):
        distance_dict = self.edit_distance_all_forms()
        self.search_result_text.delete(1.0, tk.END)
        self.search_result_text.insert(tk.END, "Редакционное расстояние между всеми парами слов:\n")
        for pair, distance in distance_dict.items():
            word1, word2 = pair
            self.search_result_text.insert(tk.END, f"Между '{word1}' и '{word2}': {distance}\n")

    def display_edit_distance_all_forms_for_selected_word(self):
        selected_word = self.word_combobox.get()
        word_forms = self.get_word_forms(selected_word)
        distance_dict = {}
        
        for i in range(len(word_forms)):
            for j in range(i + 1, len(word_forms)):
                distance = self.edit_distance(word_forms[i], word_forms[j])
                distance_dict[(word_forms[i], word_forms[j])] = distance

        self.search_result_text.delete(1.0, tk.END)
        self.search_result_text.insert(tk.END, f"Редакционное расстояние между всеми формами слова '{selected_word}':\n")
        for pair, distance in distance_dict.items():
            word1, word2 = pair
            self.search_result_text.insert(tk.END, f"Между '{word1}' и '{word2}': {distance}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = WordViewerApp(root)
    root.mainloop()
