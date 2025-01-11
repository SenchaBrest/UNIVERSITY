import os
import PyPDF2 # type: ignore
import docx # type: ignore
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, StringVar
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def index_files(directory):
    index = {}
    texts = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                path = os.path.join(root, file)
                text = extract_text_from_pdf(path)
                index[path] = text
                texts.append(text)
            elif file.endswith('.docx'):
                path = os.path.join(root, file)
                text = extract_text_from_docx(path)
                index[path] = text
                texts.append(text)

    # Векторизация текстов
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return index, tfidf_matrix, vectorizer

def search_index(index, tfidf_matrix, vectorizer, query):
    query_words = query.split()  # Разделяем запрос на слова
    results = {}
    for word in query_words:
        query_vector = vectorizer.transform([word])
        cosine_similarities = np.dot(tfidf_matrix, query_vector.T).toarray()  # косинусное сходство
        for i, path in enumerate(index.keys()):
            if cosine_similarities[i][0] > 0:
                if path not in results:
                    results[path] = {'texts': [], 'count': 0}
                results[path]['texts'].append(index[path])
                results[path]['count'] += index[path].lower().count(word.lower())
    return results

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        indexing_label.set("Индексация...")
        root.update()
        index, tfidf_matrix, vectorizer = index_files(directory)
        indexing_label.set("Индексация завершена.")
        messagebox.showinfo("Индексация завершена", f"Найдено {len(index)} файлов.")
        return index, tfidf_matrix, vectorizer
    return {}, None, None

def update_index():
    global index, tfidf_matrix, vectorizer
    index, tfidf_matrix, vectorizer = browse_directory()

def search_files():
    query = query_entry.get()
    if not query:
        messagebox.showwarning("Предупреждение", "Введите запрос для поиска.")
        return
    results = search_index(index, tfidf_matrix, vectorizer, query)
    result_text.delete(1.0, tk.END)

    if results:
        for path, data in results.items():
            matched_texts = []
            for text in data['texts']:
                for word in query.split():
                    start_index = text.lower().find(word.lower())
                    while start_index != -1:
                        start_context = max(0, start_index - 30)  # 30 символов перед
                        end_context = min(len(text), start_index + len(word) + 30)  # 30 символов после
                        matched_text = text[start_context:end_context].replace(word, f"[{word}]")
                        matched_texts.append(matched_text)
                        start_index = text.lower().find(word.lower(), start_index + 1)
            # Выводим результаты для файла, если есть совпадения
            if matched_texts:
                result_text.insert(tk.END, f"Найдено в: {path} (Совпадений: {data['count']})\nТексты:\n")
                for matched_text in matched_texts:
                    result_text.insert(tk.END, f"{matched_text}\n")
                    result_text.insert(tk.END, "-----\n")
    else:
        result_text.insert(tk.END, "Результаты не найдены.\n")

root = tk.Tk()
root.title("Первая лаба 1")

frame = tk.Frame(root)
frame.pack(pady=10)

index = {}

indexing_label = StringVar()
indexing_label.set("")

browse_button = tk.Button(frame, text="Выбрать папку для индексации", command=lambda: update_index())
browse_button.pack(pady=5)

query_label = tk.Label(frame, text="Введите запрос для поиска:")
query_label.pack(pady=5)

query_entry = tk.Entry(frame, width=50)
query_entry.pack(pady=5)

search_button = tk.Button(frame, text="Поиск", command=search_files)
search_button.pack(pady=5)

indexing_status = tk.Label(frame, textvariable=indexing_label)
indexing_status.pack(pady=5)

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.pack(pady=10)

root.mainloop()
