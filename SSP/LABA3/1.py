import tkinter as tk
from tkinter import messagebox


class MultipleChoiceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Multiple Choice App")

        self.available_items = [f"Item {i}" for i in range(1, 20)]
        self.selected_items = []

        self.available_listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE)
        for item in self.available_items:
            self.available_listbox.insert(tk.END, item)
        self.available_listbox.pack(pady=10)

        select_button = tk.Button(self.master, text="Select", command=self.select_items)
        select_button.pack(pady=5)

        self.selected_listbox = tk.Listbox(self.master)
        self.selected_listbox.pack(pady=10)

    def select_items(self):
        selected_indices = self.available_listbox.curselection()
        selected_items = [self.available_items[i] for i in selected_indices]

        selected_text = ', '.join(selected_items)

        if len(selected_text) > 100:
            messagebox.showinfo("Warning", "Selected text exceeds 100 characters.")
        else:
            self.selected_listbox.delete(0, tk.END)
            self.selected_listbox.insert(tk.END, selected_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultipleChoiceApp(root)
    root.mainloop()
