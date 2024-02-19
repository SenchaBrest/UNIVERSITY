from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QGridLayout


class SimpleAddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Address Book")
        self.resize(429, 295)

        self.gridLayout = QGridLayout(self)

        self.label_name = QLabel("Name:")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)

        self.lineEdit_name = QLineEdit()
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 2)

        self.label_address = QLabel("Address:")
        self.gridLayout.addWidget(self.label_address, 1, 0, 1, 1)

        self.textEdit_address = QTextEdit()
        self.gridLayout.addWidget(self.textEdit_address, 1, 1, 6, 2)

        self.pushButton_add = QPushButton("Add")
        self.pushButton_add.clicked.connect(self.add_entry)
        self.gridLayout.addWidget(self.pushButton_add, 0, 3, 1, 1)

        self.pushButton_previous = QPushButton("Previous")
        self.pushButton_previous.clicked.connect(self.previous_entry)
        self.gridLayout.addWidget(self.pushButton_previous, 8, 1, 1, 1)

        self.pushButton_next = QPushButton("Next")
        self.pushButton_next.clicked.connect(self.next_entry)
        self.gridLayout.addWidget(self.pushButton_next, 8, 2, 1, 1)

        self.pushButton_edit = QPushButton("Edit")
        self.pushButton_edit.clicked.connect(self.edit_entry)
        self.gridLayout.addWidget(self.pushButton_edit, 1, 3, 1, 1)

        self.pushButton_remove = QPushButton("Remove")
        self.pushButton_remove.clicked.connect(self.remove_entry)
        self.gridLayout.addWidget(self.pushButton_remove, 2, 3, 1, 1)

        self.pushButton_find = QPushButton("Find")
        self.pushButton_find.clicked.connect(self.find_entry)
        self.gridLayout.addWidget(self.pushButton_find, 3, 3, 1, 1)

        self.pushButton_load = QPushButton("Load...")
        self.pushButton_load.clicked.connect(self.load_data)
        self.gridLayout.addWidget(self.pushButton_load, 4, 3, 1, 1)

        self.pushButton_save = QPushButton("Save...")
        self.pushButton_save.clicked.connect(self.save_data)
        self.gridLayout.addWidget(self.pushButton_save, 5, 3, 1, 1)

        self.pushButton_export = QPushButton("Export")
        self.pushButton_export.clicked.connect(self.export_data)
        self.gridLayout.addWidget(self.pushButton_export, 6, 3, 1, 1)

    def add_entry(self):
        print("Add button clicked")

    def previous_entry(self):
        print("Previous button clicked")

    def next_entry(self):
        print("Next button clicked")

    def edit_entry(self):
        print("Edit button clicked")

    def remove_entry(self):
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
