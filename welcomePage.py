import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication
from login import LoginScreen


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomePage.ui", self)

        self.getStartedB.clicked.connect(self.goto_login)
        # self.createAccountBut.clicked.connect(self.goto_create)


    def goto_login(self):
        self.login = LoginScreen()
        self.login.show()
        self.close()


    # def goto_create(self):
    #     self.create = CreateAccount()
    #     self.create.show()
    #     self.close()


