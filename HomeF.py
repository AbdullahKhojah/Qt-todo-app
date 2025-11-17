import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from quicktask import QuickTask
from detailedtask import DetailedTask




class Home(QMainWindow):
    def __init__(self,user_id):
        super(Home, self).__init__()
        loadUi("HomeF.ui", self)
        self.user_id = user_id



        self.quickButton.clicked.connect(self.goto_quick_task)
        self.detailedButton.clicked.connect(self.goto_detailed_task)
        self.signOutButton.clicked.connect(self.sign_out)


    def goto_quick_task(self):
        self.quick_page = QuickTask(self.user_id)
        self.quick_page.show()
        self.close()

    def goto_detailed_task(self):
        self.detailed_page = DetailedTask(self.user_id)
        self.detailed_page.show()
        self.close()

    def sign_out(self):
        from login import LoginScreen
        self.login = LoginScreen()
        self.login.show()
        self.close()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Home(user_id=1)
#     window.show()
#     sys.exit(app.exec_())
