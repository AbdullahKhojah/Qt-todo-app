import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from database import Database


class DetailedTask(QMainWindow):
    def __init__(self, user_id):
        super(DetailedTask, self).__init__()
        loadUi("detailedtask.ui", self)
        self.user_id = user_id
        self.db = Database()

        #  for task cards
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setSpacing(8)
        self.task_layout.setContentsMargins(10, 10, 10, 10)
        self.task_layout.setAlignment(Qt.AlignTop)

        self.addTaskButton.clicked.connect(self.add_task)
        self.backButton.clicked.connect(self.back_to_home)

        self.load_tasks()


    def load_tasks(self):
        for i in reversed(range(self.task_layout.count())):
            widget = self.task_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        tasks = self.db.get_tasks(self.user_id, "detailed")
        for task in tasks:
            task_id, title, time, effort, done, task_type, user_id, created_at = task
            self.add_task_ui(task_id, title, time, effort, done)

    def add_task(self):
        """Add a new detailed task"""
        title = self.taskInput.text().strip()
        time = self.timeInput.text().strip()
        effort = self.effortCombo.currentText()

        if not title or not time or effort == "":
            self.show_message("Please fill in all fields.")
            return

        self.db.add_task(title, "detailed", self.user_id, time, effort)
        self.taskInput.clear()
        self.timeInput.clear()
        self.effortCombo.setCurrentIndex(0)
        self.load_tasks()
        self.show_message("Detailed task added successfully!")

    def add_task_ui(self, task_id, title, time, effort, done):
        card = QWidget()
        card.setFixedHeight(80)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        card.setStyleSheet("""
            QWidget {
                background-color: #F8FAFF;
                border: 1px solid #DADADA;
                border-radius: 10px;
            }
        """)

        title_label = QLabel(f" {title}")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")

        time_label = QLabel(f"⏰ {time}")
        time_label.setStyleSheet("font-size: 13px; color: #555;")

        effort_label = QLabel(f" {effort}")
        effort_label.setStyleSheet("font-size: 13px; color: #555;")

        done_checkbox = QCheckBox("Done")
        done_checkbox.setChecked(bool(done))
        done_checkbox.stateChanged.connect(
            lambda state, tid=task_id: self.toggle_task_done(tid, state, title_label)
        )

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
        delete_button.clicked.connect(lambda _, tid=task_id, cont=card: self.delete_task(tid, cont))

        layout.addWidget(title_label)
        layout.addWidget(time_label)
        layout.addWidget(effort_label)
        layout.addStretch()
        layout.addWidget(done_checkbox)
        layout.addWidget(delete_button)

        self.task_layout.addWidget(card)

        if done:
            title_label.setStyleSheet("font-size: 14px; color: gray; text-decoration: line-through;")

    def toggle_task_done(self, task_id, state, label):
        if state == Qt.Checked:
            self.db.mark_task_done(task_id)
            label.setStyleSheet("font-size: 14px; color: gray; text-decoration: line-through;")
        else:
            label.setStyleSheet("font-size: 14px; color: #333;")

    def delete_task(self, task_id, container):
        """Delete a task"""
        self.db.delete_task(task_id)
        container.deleteLater()
        self.show_message("Task deleted successfully!")

    def show_message(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec_()

    def back_to_home(self):
        from HomeF import Home
        self.home = Home(self.user_id)
        self.home.show()
        self.close()



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DetailedTask(user_id=1)
#     window.show()
#     sys.exit(app.exec_())
