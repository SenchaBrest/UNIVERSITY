import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import filedialog


class DatabaseApp:
    def __init__(self, master, connection_params):
        self.master = master
        self.connection_params = connection_params
        self.master.title("Работник ритейла")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        self.conn = sqlite3.connect(**connection_params)
        self.cursor = self.conn.cursor()

        self.table_names = self.get_table_names()

        for table_name in self.table_names:
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=table_name)
            self.create_table_view(frame, table_name)

    def get_table_names(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [row[0] for row in self.cursor.fetchall()]
        return table_names

    def create_table_view(self, frame, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        tree.pack(expand=True, fill='both')

        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(tree, table_name, c, False))
            tree.column(col, width=100, anchor='center')

        self.populate_treeview(tree, table_name)

        add_button = tk.Button(frame, text="Добавить", command=lambda: self.add_row(tree, table_name))
        add_button.pack(side=tk.LEFT, padx=10)

        delete_button = tk.Button(frame, text="Удалить", command=lambda: self.delete_row(tree, table_name))
        delete_button.pack(side=tk.LEFT, padx=10)

        edit_button = tk.Button(frame, text="Изменить", command=lambda: self.edit_row(tree, table_name))
        edit_button.pack(side=tk.LEFT, padx=10)

        refresh_button = tk.Button(frame, text="Обновить", command=lambda: self.populate_treeview(tree, table_name))
        refresh_button.pack(side=tk.LEFT, padx=10)

        search_entry = tk.Entry(frame)
        search_entry.pack(side=tk.LEFT, padx=10)

        search_button = tk.Button(frame, text="Поиск", command=lambda: self.search_treeview(tree, search_entry.get()))
        search_button.pack(side=tk.LEFT, padx=10)

        generate_receipt_button = tk.Button(frame, text="Напечатать чек", command=lambda: self.generate_receipt(tree))
        generate_receipt_button.pack(side=tk.LEFT, padx=10)

    def populate_treeview(self, tree, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name};")
        data = self.cursor.fetchall()

        tree.delete(*tree.get_children())

        for row in data:
            tree.insert('', 'end', values=row)

    def add_row(self, tree, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        add_dialog = tk.Toplevel(self.master)
        add_dialog.title("Добавить строку")

        entry_widgets = []
        for col in columns:
            label = tk.Label(add_dialog, text=col)
            label.grid(row=columns.index(col), column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(add_dialog)
            entry.grid(row=columns.index(col), column=1, padx=10, pady=5, sticky='w')
            entry_widgets.append(entry)

        def insert_row():
            values = [entry.get() for entry in entry_widgets]
            placeholders = ', '.join(['?' for _ in values])
            query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            self.cursor.execute(query, values)
            self.conn.commit()
            self.populate_treeview(tree, table_name)
            add_dialog.destroy()

        submit_button = tk.Button(add_dialog, text="Подтвердить", command=insert_row)
        submit_button.grid(row=len(columns), columnspan=2, pady=10)

    def delete_row(self, tree, table_name):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для удаления.")
            return

        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту строку?")
        if not confirm:
            return

        values = tree.item(selected_item)['values']

        where_clause = ' AND '.join([f"{column} = ?" for column in tree['columns']])

        query = f"DELETE FROM {table_name} WHERE {where_clause};"
        self.cursor.execute(query, values)
        self.conn.commit()

        self.populate_treeview(tree, table_name)

    def edit_row(self, tree, table_name):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для изменения.")
            return

        values = tree.item(selected_item)['values']

        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        edit_dialog = tk.Toplevel(self.master)
        edit_dialog.title("Изменить строку")

        entry_widgets = []
        for col, value in zip(columns, values):
            label = tk.Label(edit_dialog, text=col)
            label.grid(row=columns.index(col), column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(edit_dialog)
            entry.insert(0, value)
            entry.grid(row=columns.index(col), column=1, padx=10, pady=5, sticky='w')
            entry_widgets.append(entry)

        def update_row():
            new_values = [entry.get() for entry in entry_widgets]
            set_clause = ', '.join([f"{column} = ?" for column in columns])
            where_clause = ' AND '.join([f"{column} = ?" for column in columns])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
            self.cursor.execute(query, new_values + values)
            self.conn.commit()
            self.populate_treeview(tree, table_name)
            edit_dialog.destroy()

        submit_button = tk.Button(edit_dialog, text="Подтвердить", command=update_row)
        submit_button.grid(row=len(columns), columnspan=2, pady=10)

    def sort_treeview(self, tree, table_name, column, reverse):
        query = f"SELECT * FROM {table_name} ORDER BY {column} {'DESC' if reverse else 'ASC'};"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        tree.delete(*tree.get_children())

        for row in data:
            tree.insert('', 'end', values=row)

        tree.heading(column, command=lambda: self.sort_treeview(tree, table_name, column, not reverse))

    def search_treeview(self, tree, search_term):
        for item in tree.get_children():
            values = tree.item(item)['values']

            if any(str(search_term).lower() in str(value).lower() for value in values):
                tree.selection_add(item)
            else:
                tree.selection_remove(item)

    def generate_receipt(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для генерации чека.")
            return

        values = tree.item(selected_item)['values']

        client_id = values[0]

        self.generate_receipt_function(client_id)

    def generate_receipt_function(self, client_id):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if not file_path:
            return

        with open(file_path, 'w', encoding='utf-8') as receipt_file:
            receipt_file.write("Чек покупки\n")
            receipt_file.write("=====================\n\n")

            self.cursor.execute(f"SELECT * FROM Чек WHERE КлиентID = ?;", (client_id,))
            receipt_data = self.cursor.fetchall()

            for receipt_row in receipt_data:
                receipt_file.write(f"ЧекID: {receipt_row[0]}\n")
                receipt_file.write(f"ПродавецID: {receipt_row[1]}\n")
                receipt_file.write(f"КлиентID: {receipt_row[2]}\n")
                receipt_file.write(f"Дата и время покупки: {receipt_row[3]}\n")
                receipt_file.write(f"Сумма без скидки: {receipt_row[4]}\n")
                receipt_file.write(f"Сумма со скидкой: {receipt_row[5]}\n\n")

                self.cursor.execute(f"SELECT * FROM Покупка WHERE КлиентID = ?;", (receipt_row[2],))
                purchase_data = self.cursor.fetchall()

                receipt_file.write("Товары в чеке:\n")
                for purchase_row in purchase_data:
                    self.cursor.execute(f"SELECT Название, Цена FROM Товар WHERE ТоварID = ?;", (purchase_row[2],))
                    product_data = self.cursor.fetchone()

                    self.cursor.execute(f"SELECT Количество FROM Покупка WHERE КлиентID = ? AND ТоварID = ?;", (receipt_row[2],purchase_row[2]))
                    amount = self.cursor.fetchone()

                    receipt_file.write(
                        f"  - {product_data[0]} (Цена: {product_data[1]}; Количество: {amount[0]})\n")

                receipt_file.write("=====================\n\n")

        messagebox.showinfo("Генерация чека", "Чек успешно создан.")


if __name__ == "__main__":
    connection_params = {"database": "mydb.sqlite3"}
    try:
        root = ThemedTk(theme="kroc")
        app = DatabaseApp(root, connection_params)
        root.mainloop()

    except sqlite3.Error as err:
        print(f"Error: {err}")