# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QLabel, QTableWidget, \
    QTableWidgetItem, QTextEdit
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from Service import userService, sourceService, qualityService, exportService, emailService, complaintService, \
    loginUser, authUserService
from model import user, source, authUser


class Dashboard(QWidget):
    def __init__(self):
        super(Dashboard, self).__init__()

        authUserService.set_auth_user()
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

        # Initialize dashboard nodes
        self.source_table = None
        self.export_data_btn = None
        self.email_btn = None
        self.complaint_details = None

        # initialize complaint nodes
        self.source_selector = None
        self.complaint_success_message = None
        self.complaint_error_message = None
        self.submit_complaint_btn = None
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

        self.source_table = self.findChild(QTableWidget, "source_table")
        sources = sourceService.get_all_sources()
        self.populate_source_table(sources)

        # Fill the moderator selectors in the add source section
        self.moderator_selector = self.findChild(QComboBox, "moderator_selector")
        self.moderator_selector_2 = self.findChild(QComboBox, "moderator_selector_2")
        self.moderator_selector_3 = self.findChild(QComboBox, "moderator_selector_3")
        self.populate_moderator_selectors(users)

        # Fill the source_selector with all available users' info
        self.source_selector = self.findChild(QComboBox, "source_selector")
        sources = sourceService.get_all_sources()  # Retrieve the list of users from the database
        self.populate_source_selector(sources)  # Populate the user_table with the retrieved users

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

        self.export_data_btn = self.findChild(QPushButton, "export_data")
        self.export_data_btn.clicked.connect(self.export_to_spreadsheet)

        self.email_btn = self.findChild(QPushButton, "email_btn")
        self.email_btn.clicked.connect(self.send_email)

        self.complaint_details = self.findChild(QTextEdit, "complaint_details")
        self.complaint_success_message = self.findChild(QLabel, "complaint_success_message")
        self.complaint_error_message = self.findChild(QLabel, "complaint_error_message")
        self.submit_complaint_btn = self.findChild(QPushButton, "submit_complaint_btn")
        self.submit_complaint_btn.clicked.connect(self.submit_complaint)

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

    def populate_source_table(self, sources):
        self.source_table.setRowCount(len(sources))
        for row, table_source in enumerate(sources):
            # get quality reading for each water source
            quality_readings = qualityService.get_quality_by_id(table_source.quality_id)

            # get approved moderators for each water sources
            approved_moderators = userService.find_users_by_string_ids(table_source.approvers)
            name_item = QTableWidgetItem(table_source.name)
            location_item = QTableWidgetItem(table_source.location)
            type_item = QTableWidgetItem(table_source.type)
            capacity_item = QTableWidgetItem(str(table_source.capacity))
            status_item = QTableWidgetItem(table_source.status)
            water_leve_item = QTableWidgetItem(str(table_source.water_level))
            approvers_item = QTableWidgetItem(approved_moderators)
            chlorine_item = QTableWidgetItem(
                str(quality_readings.chlorine_residual) if quality_readings.chlorine_residual is not None else "NA")
            ph_item = QTableWidgetItem(
                str(quality_readings.ph_level) if quality_readings.ph_level is not None else "NA")
            temp_item = QTableWidgetItem(
                str(quality_readings.temperature) if quality_readings.temperature is not None else "NA")
            turb_item = QTableWidgetItem(
                str(quality_readings.turbidity) if quality_readings.turbidity is not None else "NA")
            do_item = QTableWidgetItem(
                str(quality_readings.dissolved_0xygen) if quality_readings.dissolved_0xygen is not None else "NA")
            conductivity_item = QTableWidgetItem(
                str(quality_readings.conductivity) if quality_readings.conductivity is not None else "NA")
            tds_item = QTableWidgetItem(
                str(quality_readings.total_dissolved_solids) if quality_readings.total_dissolved_solids is not None else "NA")
            bod_item = QTableWidgetItem(
                str(quality_readings.biochemical_oxygen_demand) if quality_readings.biochemical_oxygen_demand is not None else "NA")
            cod_item = QTableWidgetItem(
                str(quality_readings.chemical_oxygen_demand) if quality_readings.chemical_oxygen_demand is not None else "NA")
            tss_item = QTableWidgetItem(
                str(quality_readings.total_suspended_solids) if quality_readings.total_suspended_solids is not None else "NA")

            self.source_table.setItem(row, 0, name_item)
            self.source_table.setItem(row, 1, location_item)
            self.source_table.setItem(row, 2, type_item)
            self.source_table.setItem(row, 3, capacity_item)
            self.source_table.setItem(row, 4, status_item)
            self.source_table.setItem(row, 5, water_leve_item)
            self.source_table.setItem(row, 6, approvers_item)
            self.source_table.setItem(row, 7, chlorine_item)
            self.source_table.setItem(row, 8, ph_item)
            self.source_table.setItem(row, 9, temp_item)
            self.source_table.setItem(row, 10, turb_item)
            self.source_table.setItem(row, 11, do_item)
            self.source_table.setItem(row, 12, conductivity_item)
            self.source_table.setItem(row, 13, tds_item)
            self.source_table.setItem(row, 14, bod_item)
            self.source_table.setItem(row, 15, cod_item)
            self.source_table.setItem(row, 16, tss_item)

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
            approvers = s_moderator1 + "," + s_moderator2 + "," + s_moderator3
            self.add_source_to_table(s_name, s_location, s_type, s_capacity, s_status, s_water_level, approvers,
                                     s_chlorine, s_ph_level, s_temperature, s_turbidity, s_do, s_conductivity, s_tds,
                                     s_bod, s_cod, s_tss)
            self.addSource_success_message.setText("source added successfully")
            self.clear_add_source_fields()
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

    def add_source_to_table(self, name, location, s_type, capacity, status, water_level, approvers, chlorine, ph, temp,
                            turb, do, conductivity, tds, bod, cod, tss):
        row = self.source_table.rowCount()
        self.source_table.insertRow(row)

        name_item = QTableWidgetItem(name)
        location_item = QTableWidgetItem(location)
        type_item = QTableWidgetItem(s_type)
        capacity_item = QTableWidgetItem(capacity)
        status_item = QTableWidgetItem(status)
        water_leve_item = QTableWidgetItem(water_level)
        approvers_item = QTableWidgetItem(approvers)
        chlorine_item = QTableWidgetItem(
            chlorine if chlorine != "" and not chlorine.isspace() else "NA")
        ph_item = QTableWidgetItem(ph if ph != "" and not ph.isspace() else "NA")
        temp_item = QTableWidgetItem(temp if temp != "" and not temp.isspace() else "NA")
        turb_item = QTableWidgetItem(turb if turb != "" and not turb.isspace() else "NA")
        do_item = QTableWidgetItem(do if do != "" and not do.isspace() else "NA")
        conductivity_item = QTableWidgetItem(
            conductivity if conductivity != "" and not conductivity.isspace() else "NA")
        tds_item = QTableWidgetItem(tds if tds != "" and not tds.isspace() else "NA")
        bod_item = QTableWidgetItem(bod if bod != "" and not bod.isspace() else "NA")
        cod_item = QTableWidgetItem(cod if cod != "" and not cod.isspace() else "NA")
        tss_item = QTableWidgetItem(tss if tss != "" and not tss.isspace() else "NA")

        self.source_table.setItem(row, 0, name_item)
        self.source_table.setItem(row, 1, location_item)
        self.source_table.setItem(row, 2, type_item)
        self.source_table.setItem(row, 3, capacity_item)
        self.source_table.setItem(row, 4, status_item)
        self.source_table.setItem(row, 5, water_leve_item)
        self.source_table.setItem(row, 6, approvers_item)
        self.source_table.setItem(row, 7, chlorine_item)
        self.source_table.setItem(row, 8, ph_item)
        self.source_table.setItem(row, 9, temp_item)
        self.source_table.setItem(row, 10, turb_item)
        self.source_table.setItem(row, 11, do_item)
        self.source_table.setItem(row, 12, conductivity_item)
        self.source_table.setItem(row, 13, tds_item)
        self.source_table.setItem(row, 14, bod_item)
        self.source_table.setItem(row, 15, cod_item)
        self.source_table.setItem(row, 16, tss_item)

    def populate_moderator_selectors(self, users):
        self.clear_moderator_selectors()  # Clear existing items in the QComboBoxes
        for moderator in users:
            # Assuming the 'type' attribute of the Authority object is the one to be displayed
            user_name = moderator.name
            self.add_items_to_moderator_selectors(user_name)

    def populate_source_selector(self, sources):
        for water_source in sources:
            # Assuming the 'type' attribute of the Authority object is the one to be displayed
            source_name = water_source.name
            self.add_items_to_source_selectors(source_name)

    def export_to_spreadsheet(self):
        # Get selected row from self.source_table (using QTableWidget) and its column data
        selected_row = self.source_table.currentRow()
        column_data = []
        for column in range(self.source_table.columnCount()):
            item = self.source_table.item(selected_row, column)
            column_data.append(item.text())

        # Call a function that takes the column data as arguments
        exportService.export_data_to_spreadsheet(*column_data)

    def send_email(self):
        selected_row = self.source_table.currentRow()
        source_name = self.source_table.item(selected_row, 0).text()

        # Get the source with the name equal to the column data
        email_source = sourceService.get_source_by_name(source_name)

        # Prepare email content
        subject = "[Warning message for water source]"
        body = f"Source Information:\n\n" \
               f"Name: {email_source.name}\n" \
               f"Location: {email_source.location}\n" \
               f"Type: {email_source.type}\n" \
               f"Capacity: {email_source.capacity}\n" \
               f"Status: {email_source.status}\n" \
               f"Water Level: {email_source.water_level}\n" \
               f"Approvers: {email_source.approvers}\n"

        # Send email
        emailService.send_email_to_recipient("emmanuelngane06@gmail.com", subject, body)

    def clear_moderator_selectors(self):
        self.moderator_selector.clear()
        self.moderator_selector_2.clear()
        self.moderator_selector_3.clear()

    def clear_add_source_fields(self):
        self.sourceName_input.setText("")
        self.sourceLocation_input.setText("")
        self.sourceCapacity_input.setText("")
        self.waterLevel_input.setText("")
        self.chlorine_input.setText("")
        self.phLevel_input.setText("")
        self.temperature_input.setText("")
        self.turbidity_input.setText("")
        self.dissolvedOxygen_input.setText("")
        self.conductivity_input.setText("")
        self.tds_input.setText("")
        self.bod_input.setText("")
        self.cod_input.setText("")
        self.tss_input.setText("")

    def add_items_to_moderator_selectors(self, item):
        self.moderator_selector.addItem(item)
        self.moderator_selector_2.addItem(item)
        self.moderator_selector_3.addItem(item)

    def add_items_to_source_selectors(self, item):
        self.source_selector.addItem(item)

    def submit_complaint(self):
        result = complaintService.submit_complaint(self.source_selector.currentText(),
                                                   self.complaint_details.toPlainText())
        if result == "success":
            self.complaint_success_message.setText("Complaint submitted successfully")
            self.complaint_details.setText("")
        else:
            self.complaint_error_message.setText(result)


if __name__ == "__main__":
    app = QApplication([])
    widget = Dashboard()
    widget.show()
    sys.exit(app.exec())
