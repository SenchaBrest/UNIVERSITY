from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QGridLayout


class SimpleAddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Address Book")
        self.resize(582, 295)

        self.gridLayout = QGridLayout(self)

        self.label_name = QLabel("Name:")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)

        self.lineEdit_name = QLineEdit()
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 2)
        self.lineEdit_name.textChanged.connect(self.text_changed)

        self.label_address = QLabel("Address:")
        self.gridLayout.addWidget(self.label_address, 1, 0, 1, 1)

        self.textEdit_address = QTextEdit()
        self.gridLayout.addWidget(self.textEdit_address, 1, 1, 6, 2)
        self.textEdit_address.textChanged.connect(lambda: self.text_changed(self.lineEdit_name.text()))

        self.toggle_input_fields(False)

        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_entry)
        self.gridLayout.addWidget(self.previous_button, 8, 1, 1, 1)
        self.previous_button.setEnabled(False)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_entry)
        self.gridLayout.addWidget(self.next_button, 8, 2, 1, 1)
        self.next_button.setEnabled(False)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_entry)
        self.gridLayout.addWidget(self.add_button, 0, 3, 1, 2)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_entry)
        self.gridLayout.addWidget(self.edit_button, 1, 3, 1, 2)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_entry)
        self.gridLayout.addWidget(self.remove_button, 2, 3, 1, 2)

        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.find_entry)
        self.gridLayout.addWidget(self.find_button, 3, 3, 1, 2)

        self.load_button = QPushButton("Load...")
        self.load_button.clicked.connect(self.load_data)
        self.gridLayout.addWidget(self.load_button, 4, 3, 1, 2)

        self.save_button = QPushButton("Save...")
        self.save_button.clicked.connect(self.save_data)
        self.gridLayout.addWidget(self.save_button, 5, 3, 1, 2)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_data)
        self.gridLayout.addWidget(self.export_button, 6, 3, 1, 2)

        self.current_name = self.lineEdit_name.text()
        self.current_address = self.textEdit_address.toPlainText()
        self.data = {}
        self.data_keys = []
        self.current_index = -1  # индекс текущей записи
        self.doing_now = None

    def update_current_name_and_address(self):
        self.current_name = self.lineEdit_name.text()
        self.current_address = self.textEdit_address.toPlainText()

    def len_changed(self, i):
        if i > 1:
            self.previous_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)

    def show_tick_and_cross_buttons(self, pos):
        self.active_button.hide()

        self.tick_button = QPushButton("✓")
        self.tick_button.setStyleSheet("""
            background-color: #66BB6A;
            border: 2px solid #388E3C;
            border-radius: 10px;
            padding: 5px;
        """)
        self.tick_button.clicked.connect(self.confirm)
        self.gridLayout.addWidget(self.tick_button, pos, 3, 1, 1)

        self.cross_button = QPushButton("✗")
        self.cross_button.setStyleSheet("""
            background-color: #EF5350;
            border: 2px solid #B71C1C;
            border-radius: 10px;
            padding: 5px;
        """)
        self.cross_button.clicked.connect(self.cancel)
        self.gridLayout.addWidget(self.cross_button, pos, 4, 1, 1)

    def toggle_buttons_state(self, state):
        buttons = [self.previous_button, self.next_button, self.add_button,
                   self.edit_button, self.remove_button, self.find_button,
                   self.load_button, self.save_button, self.export_button]
        for button in buttons:
            button.setEnabled(state)

    def toggle_input_fields(self, state):
        self.lineEdit_name.setEnabled(state)
        self.textEdit_address.setEnabled(state)

    def confirm(self):
        name = self.lineEdit_name.text()
        address = self.textEdit_address.toPlainText()
        if self.doing_now == "add":
            self.data[name] = address
        elif self.doing_now == "edit":
            del self.data[self.current_name]
            self.data[name] = address
        elif self.doing_now == "remove":
            delete_index = self.data_keys.index(self.current_name)
            del self.data[self.current_name]

        self.tick_button.deleteLater()
        self.cross_button.deleteLater()
        self.active_button.show()
        self.toggle_buttons_state(True)
        self.toggle_input_fields(False)
        self.doing_now = None

        self.data_keys = list(self.data.keys())
        if self.data_keys:
            self.len_changed(len(self.data_keys))
            self.data_keys = sorted(self.data_keys)
            self.update_current_name_and_address()
            try:
                self.current_index = self.data_keys.index(self.current_name)
                self.display_entry(self.current_name)
            except ValueError:
                self.current_index = delete_index
                self.display_entry(self.data_keys[self.current_index % len(self.data_keys)])
        else:
            self.len_changed(-1)
            self.current_index = -1
            self.display_entry()
        print("confirm")

    def cancel(self):
        self.tick_button.deleteLater()
        self.cross_button.deleteLater()
        self.active_button.show()
        self.toggle_buttons_state(True)
        self.toggle_input_fields(False)
        self.doing_now = None

        self.lineEdit_name.setText(self.current_name)
        self.textEdit_address.setText(self.current_address)

        print("cancel")

    def text_changed(self, name):
        print("text_changed")
        address = self.textEdit_address.toPlainText()

        if self.doing_now == "add":
            if name.strip() != '' and address.strip() != '':
                if name not in self.data:
                    self.tick_button.setEnabled(True)
                else:
                    self.tick_button.setEnabled(False)
            else:
                self.tick_button.setEnabled(False)
        elif self.doing_now == "edit":
            if name.strip() != '' and address.strip() != '':
                if name == self.current_name and address != self.current_address \
                        or name != self.current_name and name not in self.data:
                    self.tick_button.setEnabled(True)
                else:
                    self.tick_button.setEnabled(False)
            else:
                self.tick_button.setEnabled(False)

    def previous_entry(self):
        if self.current_index != -1:
            self.current_index -= 1
            self.current_index %= len(self.data_keys)
            self.display_entry(self.data_keys[self.current_index])
            print(self.current_index)
        else:
            self.display_entry()

    def next_entry(self):
        if self.current_index != -1:
            self.current_index += 1
            self.current_index %= len(self.data_keys)
            self.display_entry(self.data_keys[self.current_index])
            print(self.current_index)
        else:
            self.display_entry()

    def display_entry(self, key=''):
        if self.current_index != -1:
            self.lineEdit_name.setText(key)
            self.textEdit_address.setPlainText(self.data[key])
        else:
            self.lineEdit_name.setText('')
            self.textEdit_address.setPlainText('')

    def add_entry(self):
        self.update_current_name_and_address()
        self.toggle_buttons_state(False)
        self.toggle_input_fields(True)
        self.active_button = self.add_button
        self.show_tick_and_cross_buttons(0)
        self.tick_button.setEnabled(False)
        self.doing_now = "add"
        print("Add button clicked")

    def edit_entry(self):
        self.update_current_name_and_address()
        self.toggle_buttons_state(False)
        self.toggle_input_fields(True)
        self.active_button = self.edit_button
        self.show_tick_and_cross_buttons(1)
        self.tick_button.setEnabled(False)
        self.doing_now = "edit"
        print("Edit button clicked")

    def remove_entry(self):
        self.update_current_name_and_address()
        self.toggle_buttons_state(False)
        self.active_button = self.remove_button
        self.show_tick_and_cross_buttons(2)
        if self.current_name == '':
            self.tick_button.setEnabled(False)
        self.doing_now = "remove"
        self.data_keys = list(self.data.keys())
        print("Remove button clicked")

    def find_entry(self):
        print("Find button clicked")

    def load_data(self):
        print("Load button clicked")

    def save_data(self):
        print("Save button clicked")

    def export_data(self):
        print("Export button clicked")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = SimpleAddressBook()
    window.show()
    sys.exit(app.exec_())
