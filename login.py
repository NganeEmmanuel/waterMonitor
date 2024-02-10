# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QLabel, QTableWidget, \
    QTableWidgetItem
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from Service import userService, sourceService
from model import user, source


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

        # Initialize nodes from add source
        self.moderator_selector = None
        self.moderator_selector_2 = None
        self.moderator_selector_3 = None
        self.sourceName_input = None
        self.sourceLocation_input = None
        self.sourceType_selector = None
        self.sourceStatus_input = None
        self.sourceCapacity_input = None
        self.waterLevel_input = None
        self.chlorine_input = None
        self.phLevel_input = None
        self.temperature_input = None
        self.turbidity_input = None
        self.dissolvedOxygen_input = None
        self.conductivity_input = None
        self.tds_input = None
        self.bod_input = None
        self.cod_input = None
        self.tss_input = None
        self.addSource_success_message = None
        self.addSource_error_message = None
        self.addSource_btn = None
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "dashboard.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        # Fill the user_table with all available users' info
        self.user_table = self.findChild(QTableWidget, "user_table")
        users = userService.get_all_users()  # Retrieve the list of users from the database
        self.populate_user_table(users)  # Populate the user_table with the retrieved users

        # Fill the moderator selectors in the add source section
        self.moderator_selector = self.findChild(QComboBox, "moderator_selector")
        self.moderator_selector_2 = self.findChild(QComboBox, "moderator_selector_2")
        self.moderator_selector_3 = self.findChild(QComboBox, "moderator_selector_3")
        self.populate_moderator_selectors(users)

        # get nodes from add users tab
        self.addUser_btn = self.findChild(QPushButton, "addUser_btn")
        self.addUser_btn.clicked.connect(self.add_user_clicked)  # call function to add user on click of button
        self.addUser_name_input = self.findChild(QLineEdit, "addUser_name_input")
        self.addUser_username_input = self.findChild(QLineEdit, "addUser_username_input")
        self.addUser_email_input = self.findChild(QLineEdit, "addUser_email_input")
        self.addUser_password_input = self.findChild(QLineEdit, "addUser_password_input")
        self.addUser_authority_selector = self.findChild(QComboBox, "addUser_authority_selector")
        self.addUser_success_label = self.findChild(QLabel, "addUser_success_label")
        self.addUser_warning_label = self.findChild(QLabel, "addUser_warning_label")

        # get nodes from add source tab
        self.sourceName_input = self.findChild(QLineEdit, "sourceName_input")
        self.sourceLocation_input = self.findChild(QLineEdit, "sourceLocation_input")
        self.sourceType_selector = self.findChild(QComboBox, "sourceType_selector")
        self.sourceStatus_input = self.findChild(QComboBox, "sourceStatus_input")
        self.sourceCapacity_input = self.findChild(QLineEdit, "sourceCapacity_input")
        self.waterLevel_input = self.findChild(QLineEdit, "waterLevel_input")
        self.chlorine_input = self.findChild(QLineEdit, "chlorine_input")
        self.phLevel_input = self.findChild(QLineEdit, "phLevel_input")
        self.temperature_input = self.findChild(QLineEdit, "temperature_input")
        self.turbidity_input = self.findChild(QLineEdit, "turbidity_input")
        self.dissolvedOxygen_input = self.findChild(QLineEdit, "dissolvedOxygen_input")
        self.conductivity_input = self.findChild(QLineEdit, "conductivity_input")
        self.tds_input = self.findChild(QLineEdit, "tds_input")
        self.bod_input = self.findChild(QLineEdit, "bod_input")
        self.cod_input = self.findChild(QLineEdit, "cod_input")
        self.tss_input = self.findChild(QLineEdit, "tss_input")
        self.addSource_success_message = self.findChild(QLabel, "addSource_success_message")
        self.addSource_error_message = self.findChild(QLabel, "addSource_error_message")
        self.addSource_btn = self.findChild(QPushButton, "addSource_btn")
        self.addSource_btn.clicked.connect(self.add_source_clicked)  # Call function to add source on button clicked

    def populate_user_table(self, users):
        self.user_table.setRowCount(len(users))
        for row, table_user in enumerate(users):
            name_item = QTableWidgetItem(table_user.name)
            username_item = QTableWidgetItem(table_user.username)
            email_item = QTableWidgetItem(table_user.email)
            authority_item = QTableWidgetItem(table_user.authority)  # Assuming each user has only one authority

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

    def add_source_clicked(self):
        s_name = self.sourceName_input.text()
        s_location = self.sourceLocation_input.text()
        s_type = self.sourceType_selector.currentText()
        s_capacity = self.sourceCapacity_input.text()
        s_status = self.sourceStatus_input.currentText()
        s_water_level = self.waterLevel_input.text()
        s_moderator1 = self.moderator_selector.currentText()
        s_moderator2 = self.moderator_selector_2.currentText()
        s_moderator3 = self.moderator_selector_3.currentText()
        s_chlorine = self.chlorine_input.text()
        s_ph_level = self.phLevel_input.text()
        s_temperature = self.temperature_input.text()
        s_turbidity = self.turbidity_input.text()
        s_do = self.dissolvedOxygen_input.text()
        s_conductivity = self.conductivity_input.text()
        s_tds = self.tds_input.text()
        s_bod = self.bod_input.text()
        s_cod = self.cod_input.text()
        s_tss = self.tss_input.text()
        result = sourceService.add_source(s_name, s_location, s_type, s_capacity, s_status, s_water_level, s_moderator1,
                                          s_moderator2, s_moderator3, s_chlorine, s_ph_level, s_temperature,
                                          s_turbidity, s_do, s_conductivity, s_tds, s_bod, s_cod, s_tss)

        if isinstance(result, source.Source):
            self.addSource_success_message.setText("source added successfully")
        else:
            self.addSource_error_message.setText(result)
        # check if a source object is being returned if so, i will hanlde it, else disaplay the warning messaged in
        # self.addSource_error_message

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

    def populate_moderator_selectors(self, users):
        self.clear_moderator_selectors()  # Clear existing items in the QComboBoxes
        for moderator in users:
            # Assuming the 'type' attribute of the Authority object is the one to be displayed
            user_name = moderator.name
            self.add_items_to_moderator_selectors(user_name)

    def clear_moderator_selectors(self):
        self.moderator_selector.clear()
        self.moderator_selector_2.clear()
        self.moderator_selector_3.clear()

    def add_items_to_moderator_selectors(self, item):
        self.moderator_selector.addItem(item)
        self.moderator_selector_2.addItem(item)
        self.moderator_selector_3.addItem(item)


if __name__ == "__main__":
    app = QApplication([])
    widget = Login()
    widget.show()
    sys.exit(app.exec())
