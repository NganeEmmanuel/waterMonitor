# This Python file uses the following encoding: utf-8
import datetime
import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QStackedWidget, QVBoxLayout

import dashboard
from Database import dbInit, crud
from Service import loginService
from model import user, authUser


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        dbInit.create_tables()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "login.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.formWidget = loader.load(ui_file, self)
        ui_file.close()

        # Access the QPushButton using its object name
        self.loginBtn = self.findChild(QPushButton, "loginBtn")
        self.username = self.findChild(QLineEdit, "username")
        self.password = self.findChild(QLineEdit, "password")
        self.errormsg = self.findChild(QLabel, "errormsg")
        # Connect the clicked signal of the button to a function
        self.loginBtn.clicked.connect(self.login)

        self.dashboardWidget = QWidget()
        dashboardLayout = QVBoxLayout(self.dashboardWidget)
        dashboardLabel = QLabel("Welcome to the Dashboard!")
        dashboardLayout.addWidget(dashboardLabel)

        # Create a stacked widget and add the login form and dashboard window
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.formWidget)
        self.stackedWidget.addWidget(self.dashboardWidget)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.stackedWidget)

    @Slot()
    def login(self):
        username = self.username.text()
        password = self.password.text()

        # This function will be called when the button is clicked
        logged_in_user = loginService.login(username, password)
        auth_user = crud.session.query(authUser.AuthUser).filter_by(id=1).first()
        auth_user.name = logged_in_user.name
        auth_user.username = logged_in_user.username
        auth_user.email = logged_in_user.email
        auth_user.password = logged_in_user.password
        auth_user.authority = logged_in_user.authority
        if isinstance(logged_in_user, user.User):
            crud.session.commit()
            subprocess.Popen(["python", "dashboard.py"])
            self.close()
        else:
            self.errormsg.setText(logged_in_user)


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.setFixedHeight(471)
    widget.setFixedWidth(761)
    widget.show()
    sys.exit(app.exec_())
