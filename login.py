import sys
import sqlite3
import bcrypt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from HomeF import Home


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.loginBut.clicked.connect(self.login_function)
        self.goToSignup.mousePressEvent = self.goto_signup_event

    def msg_box(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()

    def login_function(self):
        email = self.emailF_login.text()
        password = self.passwordF_login.text()

        if not email or not password:
            self.msg_box("Please input all fields.")
            return

        try:
            with sqlite3.connect(r"C:\Users\bobok\PycharmProjects\PythonProject5\AuthDB.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, password FROM Auth WHERE email = ?", (email,))
                result = cur.fetchone()

                if result:
                    user_id, stored_hash = result
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        self.msg_box("Login successful!")
                        self.goto_Home(user_id)
                    else:
                        self.msg_box("Invalid password.")
                else:
                    self.msg_box("Email not found.")

        except Exception as error:
            self.msg_box(str(error))

    def goto_signup_event(self, event):
        self.goto_signup()

    def goto_signup(self):
        from signup import CreateAccount
        self.signup = CreateAccount()
        self.signup.show()
        self.close()

    def goto_Home(self, user_id):
        self.Home = Home(user_id)
        self.Home.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec_())
