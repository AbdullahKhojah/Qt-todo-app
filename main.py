import sys

from PyQt5.QtWidgets import QApplication

from welcomePage import WelcomeScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec_())
      