import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt
from database import Database


class QuickTask(QMainWindow):
    def __init__(self, user_id):
        super(QuickTask, self).__init__()
        loadUi("quicktask.ui", self)
        self.user_id = user_id
        self.db = Database()

        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setSpacing(5)
        self.task_layout.setContentsMargins(10, 10, 10, 10)
        self.task_layout.setAlignment(Qt.AlignTop)

        self.addTaskButton.clicked.connect(self.add_task)
        self.backButton.clicked.connect(self.back)

        self.load_tasks()


    def load_tasks(self):
        for i in reversed(range(self.task_layout.count())):
            widget = self.task_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        tasks = self.db.get_tasks(self.user_id, "quick")
        for task in tasks:
            task_id, title, time, effort, done, task_type, user_id, created_at = task
            self.add_task_ui(task_id, title, done)


    def add_task(self):
        title = self.taskInput.text().strip()
        if not title:
            self.show_message("Please enter a task title.")
            return

        self.db.add_task(title, "quick", self.user_id)
        self.taskInput.clear()
        self.load_tasks()
        self.show_message("Task added successfully!")


    def add_task_ui(self, task_id, title, done):
        container = QWidget()
        container.setFixedHeight(50)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignVCenter)

        container.setStyleSheet("""
            QWidget {
                background-color: #F7F9FC;
                border: 1px solid #DADADA;
                border-radius: 8px;
            }
        """)


        checkbox = QCheckBox(title)
        checkbox.setChecked(bool(done))
        checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #333;
                padding: 3px;
            }
        """)
        checkbox.stateChanged.connect(lambda state, tid=task_id: self.toggle_task_done(tid, state, checkbox))

        delete_button = QPushButton("🗑️")
        delete_button.setFixedSize(30, 30)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                font-size: 16px;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        delete_button.clicked.connect(lambda _, tid=task_id, cont=container: self.delete_task(tid, cont))

        layout.addWidget(checkbox)
        layout.addStretch()
        layout.addWidget(delete_button)
        self.task_layout.addWidget(container)

        if done:
            checkbox.setStyleSheet("""
                QCheckBox {
                    font-size: 15px;
                    color: gray;
                    text-decoration: line-through;
                }
            """)


    def toggle_task_done(self, task_id, state, checkbox):#update
        if state == Qt.Checked:
            self.db.mark_task_done(task_id)
            checkbox.setStyleSheet("""
                QCheckBox {
                    font-size: 15px;
                    color: gray;
                    text-decoration: line-through;
                }
            """)
        else:
            checkbox.setStyleSheet("""
                QCheckBox {
                    font-size: 15px;
                    color: #333;
                }
            """)

    def delete_task(self, task_id, container):
        """حذف المهمة"""
        self.db.delete_task(task_id)
        container.deleteLater()
        self.show_message("Task deleted successfully!")

    def show_message(self, text):
        """رسالة منبثقة"""
        msg = QMessageBox()
        msg.setText(text)
        msg.exec_()

    def back(self):
        from HomeF import Home
        self.home = Home(self.user_id)
        self.home.show()
        self.close()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = QuickTask(user_id=1)
#     window.show()
#     sys.exit(app.exec_())
