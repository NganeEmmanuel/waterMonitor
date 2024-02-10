# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QLabel, QTableWidget, \
    QTableWidgetItem
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from Service import userService
from model import user


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()

        # initialize nodes from add users tab
        self.user_table = None
        self.addUser_warning_label = None
        self.addUser_success_label = None
        self.addUser_authority_selector = None
        self.addUser_password_input = None
        self.addUser_email_input = None
        self.addUser_username_input = None
        self.addUser_name_input = None
        self.addUser_btn = None
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "dashboard.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        self.user_table = self.findChild(QTableWidget, "user_table")
        # Fill the user_table with all available users' info
        users = userService.get_all_users()  # Retrieve the list of users from the database
        self.populate_user_table(users)  # Populate the user_table with the retrieved users

        self.addUser_authority_selector = self.findChild(QComboBox, "addUser_authority_selector")


        # get nodes from add users tab
        self.addUser_btn = self.findChild(QPushButton, "addUser_btn")
        self.addUser_name_input = self.findChild(QLineEdit, "addUser_name_input")
        self.addUser_username_input = self.findChild(QLineEdit, "addUser_username_input")
        self.addUser_email_input = self.findChild(QLineEdit, "addUser_email_input")
        self.addUser_password_input = self.findChild(QLineEdit, "addUser_password_input")
        self.addUser_success_label = self.findChild(QLabel, "addUser_success_label")
        self.addUser_warning_label = self.findChild(QLabel, "addUser_warning_label")

        self.addUser_btn.clicked.connect(self.add_user_clicked)

    def populate_user_table(self, users):
        self.user_table.setRowCount(len(users))
        for row, user in enumerate(users):
            name_item = QTableWidgetItem(user.name)
            username_item = QTableWidgetItem(user.username)
            email_item = QTableWidgetItem(user.email)
            authority_item = QTableWidgetItem(user.authority)  # Assuming each user has only one authority

            self.user_table.setItem(row, 0, name_item)
            self.user_table.setItem(row, 1, username_item)
            self.user_table.setItem(row, 2, email_item)
            self.user_table.setItem(row, 3, authority_item)

    def add_user_clicked(self):
        name = self.addUser_name_input.text()
        username = self.addUser_username_input.text()
        email = self.addUser_email_input.text()
        password = self.addUser_password_input.text()
        authority = self.addUser_authority_selector.currentText()

        result = userService.add_user(name, username, email, password, authority)
        if isinstance(result, user.User):
            self.addUser_success_label.setText("User was added successfully!")
            self.clear_add_user_fields()
            self.add_user_to_table(name, username, email, authority)
        else:
            self.addUser_warning_label.setText(result)

    def clear_add_user_fields(self):
        self.addUser_name_input.clear()
        self.addUser_username_input.clear()
        self.addUser_email_input.clear()
        self.addUser_password_input.clear()
        self.addUser_authority_selector.setCurrentIndex(0)

    def add_user_to_table(self, name, username, email, authority):
        row = self.user_table.rowCount()
        self.user_table.insertRow(row)
        name_item = QTableWidgetItem(name)
        username_item = QTableWidgetItem(username)
        email_item = QTableWidgetItem(email)
        authority_item = QTableWidgetItem(authority)

        self.user_table.setItem(row, 0, name_item)
        self.user_table.setItem(row, 1, username_item)
        self.user_table.setItem(row, 2, email_item)
        self.user_table.setItem(row, 3, authority_item)



if __name__ == "__main__":
    app = QApplication([])
    widget = Login()
    widget.show()
    sys.exit(app.exec())