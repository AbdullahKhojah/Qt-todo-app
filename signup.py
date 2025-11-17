import sys
import sqlite3
import bcrypt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication


class CreateAccount(QDialog):
    def __init__(self):
        super(CreateAccount, self).__init__()
        loadUi("singup.ui", self)

        self.pushButton.clicked.connect(self.signup_function)
        self.goToLogin.mousePressEvent = self.goto_login_event

    def msg_box(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec_()

    def hash_fun(self, plain_text):
        plain_text = plain_text.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_text, salt)
        return hashed

    def signup_function(self):
        user = self.userNameF.text()
        email = self.emailF.text()
        password = self.passwordF.text()
        confirm_password = self.ConfirmpasswordF.text()

        if not user or not email or not password or not confirm_password:
            self.msg_box("Please fill in all inputs.")
            return

        if len(password) < 6:
            self.msg_box("Password must be at least 6 characters long.")
            return

        if password != confirm_password:
            self.msg_box("Passwords do not match.")
            return

        try:
            with sqlite3.connect(r"C:\Users\bobok\PycharmProjects\PythonProject5\AuthDB.db") as conn:
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS Auth (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        email TEXT UNIQUE,
                        password BLOB
                    )
                """)

                hashed_password = self.hash_fun(password)

                cur.execute(
                    'INSERT INTO Auth (username, email, password) VALUES (?, ?, ?)',
                    (user, email, hashed_password)
                )
                conn.commit()

                self.msg_box("User inserted successfully!")
                self.goto_login()

        except sqlite3.IntegrityError:
            self.msg_box("Email already exists.")
        except Exception as error:
            self.msg_box(str(error))

    def goto_login_event(self, event):
        self.goto_login()

    def goto_login(self):
        from login import LoginScreen
        self.login = LoginScreen()
        self.login.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateAccount()
    window.show()
    sys.exit(app.exec_())
