from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QGridLayout, QMessageBox, \
    QFileDialog
from sql import AddressBookDatabase
import os

class SimpleAddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Address Book")
        self.setFixedSize(582, 295)

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
        self.textEdit_address.textChanged.connect(self.text_changed)

        self.toggle_input_fields_state(False)

        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_entry)
        self.gridLayout.addWidget(self.previous_button, 8, 1, 1, 1)
        self.previous_button.setEnabled(False)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_entry)
        self.gridLayout.addWidget(self.next_button, 8, 2, 1, 1)
        self.next_button.setEnabled(False)

        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.make_new_file)
        self.gridLayout.addWidget(self.new_button, 0, 3, 1, 1)

        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_file)
        self.gridLayout.addWidget(self.open_button, 0, 4, 1, 1)

        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.import_data)
        self.gridLayout.addWidget(self.import_button, 1, 3, 1, 1)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_data)
        self.gridLayout.addWidget(self.export_button, 1, 4, 1, 1)
        self.export_button.setEnabled(False)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_entry)
        self.gridLayout.addWidget(self.add_button, 2, 3, 1, 2)
        self.add_button.setEnabled(False)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_entry)
        self.gridLayout.addWidget(self.edit_button, 3, 3, 1, 2)
        self.edit_button.setEnabled(False)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_entry)
        self.gridLayout.addWidget(self.remove_button, 4, 3, 1, 2)
        self.remove_button.setEnabled(False)

        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.find_entry)
        self.gridLayout.addWidget(self.find_button, 5, 3, 1, 2)
        self.find_button.setEnabled(False)

        self.sort_button = QPushButton("Sort")
        self.sort_button.clicked.connect(self.sort_data)
        self.gridLayout.addWidget(self.sort_button, 6, 3, 1, 2)
        self.sort_button.setEnabled(False)

        self.destroyed.connect(lambda: self.database.close() if self.database else None)

        self.current_name = self.lineEdit_name.text()
        self.current_address = self.textEdit_address.toPlainText()

        self.current_index = None
        self.sort = None
        self.len = 0
        self.file_name = None
        self.database = None

    def text_changed(self):
        if self.lineEdit_name.isEnabled():
            name, address = self.get_current_name_and_address()
            if name.strip() != '' and address.strip() != '' and self.textEdit_address.isEnabled() \
                    or name.strip() != '' and not self.textEdit_address.isEnabled():
                if self.current_index is not None:
                    _name, _address = self.get_name_and_address_by_index()
                    if name != _name or address != _address:
                        self.left_button.setEnabled(True)
                    else:
                        self.left_button.setEnabled(False)
                else:
                    self.left_button.setEnabled(True)
            else:
                self.left_button.setEnabled(False)

    def previous_entry(self):
        if self.current_index is not None:
            self.current_index -= 1
            self.current_index %= self.len
        self.display_entry()

    def next_entry(self):
        if self.current_index is not None:
            self.current_index += 1
            self.current_index %= self.len
        self.display_entry()

    def display_entry(self):
        if self.current_index is not None:
            _name, _address = self.get_name_and_address_by_index()
            self.lineEdit_name.setText(_name)
            self.textEdit_address.setPlainText(_address)
        else:
            self.lineEdit_name.setText('')
            self.textEdit_address.setPlainText('')

    def make_new_file(self):
        if self.file_name:
            self.database.close()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_name, _ = QFileDialog.getSaveFileName(self, "New file", "", "", options=options)
        if self.file_name:
            try:
                os.remove(self.file_name)
            except OSError:
                pass
            self.setWindowTitle(f"Simple Address Book: {self.file_name}")
            self.database = AddressBookDatabase(self.file_name)
            self.database.create_table()
            self.add_button.setEnabled(True)
            self.len = 0
            self.sort = None

    def open_file(self):
        if self.file_name:
            self.database.close()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", options=options)
        if self.file_name:
            self.setWindowTitle(f"Simple Address Book: {self.file_name}")
            self.database = AddressBookDatabase(self.file_name)
            self.database.create_table()
            self.add_button.setEnabled(True)
            self.len = self.database.get_table_size()
            self.sort = None

            if self.len:
                self.current_index = self.len - 1
                self.display_entry()
                self.toggle_length_dependent_buttons()

    def import_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file for import", "", options=options)
        if file_name:
            if self.file_name:
                self.database.close()
            self.file_name, _ = QFileDialog.getSaveFileName(self, "Make new file to save", "", "", options=options)
            if self.file_name:
                try:
                    os.remove(self.file_name)
                except OSError:
                    pass
                self.setWindowTitle(f"Simple Address Book: {self.file_name}")
                self.database = AddressBookDatabase(self.file_name)
                self.database.create_table()

                if self.database.import_from_vcf(file_name):
                    self.show_message_box("Data written successfully.", "success", "Everything is ok!")
                else:
                    self.show_message_box("Something went wrong.", "error", "Caution!")

                self.add_button.setEnabled(True)
                self.len = self.database.get_table_size()
                self.sort = None

                if self.len:
                    self.current_index = self.len - 1
                    self.display_entry()
                    self.toggle_length_dependent_buttons()

    def export_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Make new file to export", "", "", options=options)
        if self.database.export_to_vcf(file_name):
            self.show_message_box("Exporting data ended successfully.", "success", "Everything is ok!")
        else:
            self.show_message_box("Something went wrong.", "error", "Caution!")

    def add_entry(self):
        self.lineEdit_name.clear()
        self.textEdit_address.clear()
        self.actions_before_confirm_or_cancel(self.add_button, False, True)

        def confirm():
            name, address = self.get_current_name_and_address()
            if not self.database.add_contact(name, address):
                self.show_message_box("The entry is already in the book.", "error", "Caution!")
                return
            else:
                # self.show_message_box("Data written successfully.", "success", "Everything is ok!")
                pass

            self.actions_after_confirm_or_cancel(self.add_button)

            self.current_index = self.database.get_index_by_name(name, self.sort)
            self.toggle_length_dependent_buttons()
            self.display_entry()

        def cancel():
            self.actions_after_confirm_or_cancel(self.add_button)
            self.toggle_length_dependent_buttons()
            self.display_entry()

        self.show_new_buttons(2, confirm, cancel)
        self.left_button.setEnabled(False)

    def edit_entry(self):
        self.actions_before_confirm_or_cancel(self.edit_button, False, True)
        old_name, _ = self.get_current_name_and_address()

        def confirm():
            new_name, new_address = self.get_current_name_and_address()
            if not self.database.edit_contact(old_name, new_name, new_address):
                self.show_message_box("The entry is already in the book.", "error", "Caution!")
                return
            else:
                # self.show_message_box("Data updated successfully.", "success", "Everything is ok!")
                pass

            self.actions_after_confirm_or_cancel(self.edit_button)

            self.current_index = self.database.get_index_by_name(new_name, self.sort)
            self.toggle_length_dependent_buttons()
            self.display_entry()

        def cancel():
            self.actions_after_confirm_or_cancel(self.edit_button)
            self.toggle_length_dependent_buttons()
            self.display_entry()

        self.show_new_buttons(3, confirm, cancel)
        self.left_button.setEnabled(False)

    def remove_entry(self):
        self.actions_before_confirm_or_cancel(self.remove_button, False, False)

        def confirm():
            name, address = self.get_current_name_and_address()
            index = self.database.get_index_by_name(name, self.sort)
            if not self.database.delete_contact(name):
                self.show_message_box("Something went wrong.", "error", "Caution!")
                return
            else:
                # self.show_message_box("Entry deleted successfully.", "success", "Everything is ok!")
                pass

            self.actions_after_confirm_or_cancel(self.remove_button)

            self.len = self.database.get_table_size()
            if self.len:
                self.current_index = index - 1
                self.current_index %= self.len
            else:
                self.current_index = None
            self.toggle_length_dependent_buttons()
            self.display_entry()

        def cancel():
            self.actions_after_confirm_or_cancel(self.remove_button)
            self.toggle_length_dependent_buttons()
            self.display_entry()

        self.show_new_buttons(4, confirm, cancel)

    def find_entry(self):
        self.lineEdit_name.clear()
        self.textEdit_address.clear()
        self.label_name.setText("Find by name:")
        self.label_address.setText("")
        self.actions_before_confirm_or_cancel(self.find_button, False, True)
        self.textEdit_address.setEnabled(False)

        def confirm():
            name, _ = self.get_current_name_and_address()
            if (index := self.database.get_index_by_name(name, self.sort)) is None:
                self.show_message_box("The entry was not found in the book.", "error", "Caution!")
                return
            else:
                # self.show_message_box(f"Contact found successfully.", "success", "Everything is ok!")
                self.current_index = index

            self.actions_after_confirm_or_cancel(self.find_button)

            self.toggle_length_dependent_buttons()

            self.label_name.setText("Name:")
            self.label_address.setText("Address:")

            self.display_entry()

        def cancel():
            self.actions_after_confirm_or_cancel(self.find_button)
            self.toggle_length_dependent_buttons()

            self.label_name.setText("Name:")
            self.label_address.setText("Address:")

            self.display_entry()

        self.show_new_buttons(5, confirm, cancel)
        self.left_button.setEnabled(False)

    def sort_data(self):
        self.actions_before_confirm_or_cancel(self.sort_button, False, False)

        def asc_sort():
            self.actions_after_confirm_or_cancel(self.sort_button)
            self.current_index = 0
            self.toggle_length_dependent_buttons()
            self.sort = "asc"
            self.display_entry()

        def desc_sort():
            self.actions_after_confirm_or_cancel(self.sort_button)
            self.current_index = 0
            self.toggle_length_dependent_buttons()
            self.sort = "desc"
            self.display_entry()

        self.show_new_buttons(6,
                              asc_sort, desc_sort,
                              left_label="↑", right_label="↓",
                              left_background_color="#F5F5DC", right_background_color="#F5F5DC",
                              left_border_color="#D2B48C", right_border_color="#D2B48C"
                              )

    def show_new_buttons(self, pos,
                         left_f, right_f,
                         left_label="✓", right_label="✗",
                         left_background_color="#66BB6A", right_background_color="#EF5350",
                         left_border_color="#388E3C", right_border_color="#B71C1C"):
        self.left_button = QPushButton(left_label)
        self.left_button.setStyleSheet(f"""
            background-color: {left_background_color};
            border: 2px solid {left_border_color};
            border-radius: 10px;
            padding: 5px;
        """)
        self.left_button.clicked.connect(left_f)
        self.gridLayout.addWidget(self.left_button, pos, 3, 1, 1)

        self.right_button = QPushButton(right_label)
        self.right_button.setStyleSheet(f"""
            background-color: {right_background_color};
            border: 2px solid {right_border_color};
            border-radius: 10px;
            padding: 5px;
        """)
        self.right_button.clicked.connect(right_f)
        self.gridLayout.addWidget(self.right_button, pos, 4, 1, 1)

    def actions_before_confirm_or_cancel(self, button, button_state, input_fields_state):
        button.hide()
        self.toggle_buttons_state(button_state)
        self.toggle_input_fields_state(input_fields_state)

    def actions_after_confirm_or_cancel(self, button):
        self.left_button.deleteLater()
        self.right_button.deleteLater()
        button.show()
        self.toggle_buttons_state(True)
        self.toggle_input_fields_state(False)

    def toggle_buttons_state(self, state):
        buttons = [self.previous_button, self.next_button,
                   self.new_button, self.open_button, self.import_button, self.export_button,
                   self.add_button, self.edit_button, self.remove_button, self.find_button, self.sort_button]
        for button in buttons:
            button.setEnabled(state)

    def toggle_input_fields_state(self, state):
        self.lineEdit_name.setEnabled(state)
        self.textEdit_address.setEnabled(state)

        background_color = "#FFFFFF" if state else "#F9F9F9"

        self.lineEdit_name.setStyleSheet("background-color: {};".format(background_color))
        self.textEdit_address.setStyleSheet("background-color: {};".format(background_color))

    def toggle_length_dependent_buttons(self):
        self.len = self.database.get_table_size()
        if self.len > 1:
            self.previous_button.setEnabled(True)
            self.next_button.setEnabled(True)
        else:
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)

        if self.current_index is not None:
            for button in [self.export_button, self.edit_button, self.remove_button, self.find_button,
                           self.sort_button]:
                button.setEnabled(True)
        else:
            for button in [self.export_button, self.edit_button, self.remove_button, self.find_button,
                           self.sort_button]:
                button.setEnabled(False)

    def get_name_and_address_by_index(self):
        return self.database.get_contact_by_index(self.current_index, self.sort)

    def get_current_name_and_address(self):
        return self.lineEdit_name.text(), self.textEdit_address.toPlainText()

    def show_message_box(self, text, message_type, title):
        message_box = QMessageBox()
        message_box.setText(text)

        if message_type == "success":
            message_box.setIcon(QMessageBox.Information)
        elif message_type == "error":
            message_box.setIcon(QMessageBox.Critical)
        else:
            message_box.setIcon(QMessageBox.Warning)

        message_box.setWindowTitle(title)

        main_window_geometry = self.geometry()
        message_box.move(main_window_geometry.x() + 50, main_window_geometry.y() + 50)
        message_box.exec_()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = SimpleAddressBook()
    window.show()
    sys.exit(app.exec_())
