import tkinter as tk
from tkinter import ttk


class ListManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление списком")

        self.create_widgets()

    def create_widgets(self):
        self.odd_var = tk.BooleanVar()
        self.odd_checkbox = tk.Checkbutton(self.root,
                                           text="Выбрать четные строки",
                                           variable=self.odd_var,
                                           command=self.update_selection)
        self.odd_checkbox.pack()

        self.even_var = tk.BooleanVar()
        self.even_checkbox = tk.Checkbutton(self.root,
                                            text="Выбрать нечетные строки",
                                            variable=self.even_var,
                                            command=self.update_selection)
        self.even_checkbox.pack()

        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        for i in range(1, 11):
            self.listbox.insert(tk.END, f"Строка {i}")
        self.listbox.pack()

        self.move_button = tk.Button(self.root,
                                     text="Перенести в список",
                                     command=self.move_selected)
        self.move_button.pack()

        self.choice_var = tk.StringVar()
        self.choice = ttk.Combobox(self.root, textvariable=self.choice_var)
        self.choice.pack()

    def update_selection(self):
        self.listbox.selection_clear(0, tk.END)
        if self.odd_var.get() and self.even_var.get():
            self.listbox.select_set(0, tk.END)
        elif self.odd_var.get():
            for i in range(1, self.listbox.size(), 2):
                self.listbox.selection_set(i)
        elif self.even_var.get():
            for i in range(0, self.listbox.size(), 2):
                self.listbox.selection_set(i)

    def move_selected(self):
        selected_indices = self.listbox.curselection()
        items_to_move = [self.listbox.get(i) for i in selected_indices]
        self.choice['values'] = items_to_move


if __name__ == "__main__":
    root = tk.Tk()
    app = ListManagementApp(root)
    root.mainloop()
