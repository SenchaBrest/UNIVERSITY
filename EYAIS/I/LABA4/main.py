import tkinter as tk
from tkinter import filedialog
from docx import Document
import spacy

class TextAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Анализатор текста")
        master.geometry("600x600")

        self.sentences_listbox = tk.Listbox(master, width=50)
        self.sentences_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.sentences_listbox.bind("<<ListboxSelect>>", self.show_syntax_analysis)

        self.syntax_listbox = tk.Listbox(master, width=50)
        self.syntax_listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.syntax_listbox.bind("<Button-1>", lambda event: "break")

        self.load_button = tk.Button(master, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(side=tk.BOTTOM)


    def load_file(self):
            file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
            if file_path:
                doc = Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                self.analyze_text(text)

    def analyze_text(self, text):
        self.sentences_listbox.delete(0, tk.END)
        self.syntax_listbox.delete(0, tk.END)

        nlp = spacy.load('ru_core_news_sm')
        doc = nlp(text)
        for sentence in doc.sents:
            self.sentences_listbox.insert(tk.END, sentence.text)

    def show_syntax_analysis(self, event):
        selected_sentence_index = self.sentences_listbox.curselection()[0]
        selected_sentence = self.sentences_listbox.get(selected_sentence_index)
        nlp = spacy.load('ru_core_news_sm')
        doc = nlp(selected_sentence)
        self.syntax_listbox.delete(0, tk.END)
        for token in doc:
            self.syntax_listbox.insert(tk.END, f"{token.text} - {token.pos_}")

def main():
    root = tk.Tk()
    app = TextAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
