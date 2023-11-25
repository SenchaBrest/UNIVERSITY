import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox


class DatabaseApp:
    def __init__(self, master, connection_params):
        self.master = master
        self.connection_params = connection_params
        self.master.title("СМОТРИ БД")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        # Connect to the database
        self.conn = sqlite3.connect(**connection_params)
        self.cursor = self.conn.cursor()

        # Fetch table names
        self.table_names = self.get_table_names()

        # Create a tab for each table
        for table_name in self.table_names:
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=table_name)
            self.create_table_view(frame, table_name)

    def get_table_names(self):
        # Fetch table names from the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [row[0] for row in self.cursor.fetchall()]
        return table_names

    def create_table_view(self, frame, table_name):
        # Fetch column names
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        # Create a treeview widget
        tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        tree.pack(expand=True, fill='both')

        # Add column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        # Populate treeview with data from the table
        self.populate_treeview(tree, table_name)

        # Add buttons for CRUD operations
        add_button = tk.Button(frame, text="Добавить", command=lambda: self.add_row(tree, table_name))
        add_button.pack(side=tk.LEFT, padx=10)

        delete_button = tk.Button(frame, text="Удалить", command=lambda: self.delete_row(tree, table_name))
        delete_button.pack(side=tk.LEFT, padx=10)

        edit_button = tk.Button(frame, text="Изменить", command=lambda: self.edit_row(tree, table_name))
        edit_button.pack(side=tk.LEFT, padx=10)

        refresh_button = tk.Button(frame, text="Обновить", command=lambda: self.populate_treeview(tree, table_name))
        refresh_button.pack(side=tk.LEFT, padx=10)

    def populate_treeview(self, tree, table_name):
        # Fetch data from the table
        self.cursor.execute(f"SELECT * FROM {table_name};")
        data = self.cursor.fetchall()

        # Clear existing data in treeview
        tree.delete(*tree.get_children())

        # Insert data into treeview
        for row in data:
            tree.insert('', 'end', values=row)

    def add_row(self, tree, table_name):
        # Get column names
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        # Create a dialog for adding a new row
        add_dialog = tk.Toplevel(self.master)
        add_dialog.title("Добавить строку")

        # Entry widgets for each column
        entry_widgets = []
        for col in columns:
            label = tk.Label(add_dialog, text=col)
            label.grid(row=columns.index(col), column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(add_dialog)
            entry.grid(row=columns.index(col), column=1, padx=10, pady=5, sticky='w')
            entry_widgets.append(entry)

        # Function to insert the new row into the table
        def insert_row():
            values = [entry.get() for entry in entry_widgets]
            placeholders = ', '.join(['?' for _ in values])
            query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            self.cursor.execute(query, values)
            self.conn.commit()
            self.populate_treeview(tree, table_name)
            add_dialog.destroy()

        # Button to submit the new row
        submit_button = tk.Button(add_dialog, text="Подтвердить", command=insert_row)
        submit_button.grid(row=len(columns), columnspan=2, pady=10)

    def delete_row(self, tree, table_name):
        # Get the selected item in the treeview
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для удаления.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту строку?")
        if not confirm:
            return

        # Get the values of the selected row
        values = tree.item(selected_item)['values']

        # Create a WHERE clause for deletion
        where_clause = ' AND '.join([f"{column} = ?" for column in tree['columns']])

        # Execute the DELETE query
        query = f"DELETE FROM {table_name} WHERE {where_clause};"
        self.cursor.execute(query, values)
        self.conn.commit()

        # Update the treeview
        self.populate_treeview(tree, table_name)

    def edit_row(self, tree, table_name):
        # Get the selected item in the treeview
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для изменения.")
            return

        # Get the values of the selected row
        values = tree.item(selected_item)['values']

        # Get column names
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        # Create a dialog for editing the row
        edit_dialog = tk.Toplevel(self.master)
        edit_dialog.title("Изменить строку")

        # Entry widgets for each column with current values
        entry_widgets = []
        for col, value in zip(columns, values):
            label = tk.Label(edit_dialog, text=col)
            label.grid(row=columns.index(col), column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(edit_dialog)
            entry.insert(0, value)
            entry.grid(row=columns.index(col), column=1, padx=10, pady=5, sticky='w')
            entry_widgets.append(entry)

        # Function to update the row in the table
        def update_row():
            new_values = [entry.get() for entry in entry_widgets]
            set_clause = ', '.join([f"{column} = ?" for column in columns])
            where_clause = ' AND '.join([f"{column} = ?" for column in columns])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
            self.cursor.execute(query, new_values + values)
            self.conn.commit()
            self.populate_treeview(tree, table_name)
            edit_dialog.destroy()

        # Button to submit the edited row
        submit_button = tk.Button(edit_dialog, text="Подтвердить", command=update_row)
        submit_button.grid(row=len(columns), columnspan=2, pady=10)


if __name__ == "__main__":
    connection_params = {"database": "mydb.sqlite3"}
    try:
        root = tk.Tk()
        app = DatabaseApp(root, connection_params)
        root.mainloop()

    except sqlite3.Error as err:
        print(f"Error: {err}")
