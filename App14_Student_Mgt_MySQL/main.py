import os
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
)

load_dotenv()
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Base path for app resources.
BASE_DIR = Path(__file__).resolve().parent


class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password=None, database="school"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }
        self.connection = None

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        return self.connection

    def __exit__(self, exception_type, exception_value, traceback):
        if self.connection is None:
            return
        if exception_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Main window setup.
        self.setWindowTitle("Student Management System")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        # Build the app menus.
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        add_student_action = QAction(
            QIcon(str(BASE_DIR / "icons/add.png")), "Add Student", self
        )
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)
        search_action = QAction(
            QIcon(str(BASE_DIR / "icons/search.png")), "Search", self
        )
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        # Display student records in a table.
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        # Toolbar shortcuts for common actions.
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)
        # Create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        # Show edit/delete buttons in status bar whenever a table row is selected.
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        # Read all student rows from the database and refresh the table.
        with DatabaseConnection(password=MYSQL_PASSWORD) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, course, mobile FROM students ORDER BY id")
            rows = cursor.fetchall()

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(rows):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )

    def insert(self):
        # Open the add-student form.
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        # Open the search form.
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        # Open edit form for the selected record.
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        # Open delete confirmation for the selected record.
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        # Open the about form.
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """This app was created during the course "The Python Mega Course". Feel free to modify and reuse the app."""
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Form used to edit a new student record.
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        index = window.table.currentRow()

        if index < 0:
            self.close()
            return

        self.student_id = window.table.item(index, 0).text()
        student_name = window.table.item(index, 1).text()
        course_name = window.table.item(index, 2).text()
        student_mobile = window.table.item(index, 3).text()
        # Student name input.
        self.student_name = QLineEdit(student_name)
        layout.addWidget(self.student_name)
        # Course selection dropdown.
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)
        # Mobile number input.
        self.student_mobile = QLineEdit(student_mobile)
        layout.addWidget(self.student_mobile)
        # Save the new student to the database.
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)
        self.setLayout(layout)

    def update_student(self):
        with DatabaseConnection(password=MYSQL_PASSWORD) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s",
                (
                    self.student_name.text(),
                    self.course_name.currentText(),
                    self.student_mobile.text(),
                    self.student_id,
                ),
            )
        window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        layout = QGridLayout()

        confimration = QLabel("Are you sure you want to delete?")
        layout.addWidget(confimration, 0, 0, 1, 2)
        yes = QPushButton("Yes")
        layout.addWidget(yes, 1, 0)
        no = QPushButton("No")
        layout.addWidget(no, 1, 1)

        yes.clicked.connect(lambda: self.delete_student(True))
        no.clicked.connect(lambda: self.delete_student(False))

        self.setLayout(layout)

    def delete_student(self, confirmed):
        if confirmed:
            # Get selected row index and student id
            index = window.table.currentRow()
            if index < 0:
                self.close()
                return

            student_id = window.table.item(index, 0).text()
            with DatabaseConnection(password=MYSQL_PASSWORD) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            window.load_data()
            self.close()
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Success")
            confirmation_widget.setText("The record was deleted successfully")
            confirmation_widget.exec()
        else:
            self.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Form used to add a new student record.
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        # Student name input.
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        # Course selection dropdown.
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        # Mobile number input.
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)
        # Save the new student to the database.
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        self.setLayout(layout)

    def add_student(self):
        # Collect form values and insert them into the students table.
        name = self.student_name.text().strip()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.student_mobile.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation", "Name cannot be empty.")
            return

        with DatabaseConnection(password=MYSQL_PASSWORD) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)",
                (name, course, mobile),
            )
        window.load_data()
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Form for searching students by name.
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        # Search input field.
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Search by name...")
        layout.addWidget(self.search_name)
        # Run the database search when pressed.
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)
        self.setLayout(layout)

    def search_student(self):
        # Find matching names and highlight the results in the table.
        name = self.search_name.text().strip()
        if not name:
            return

        with DatabaseConnection(password=MYSQL_PASSWORD) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name, course, mobile FROM students WHERE name LIKE %s",
                (f"%{name}%",),
            )
            rows = cursor.fetchall()

        window.table.clearSelection()
        if not rows:
            QMessageBox.information(self, "Search", "No matching student found.")
            return

        for row in rows:
            matched_name = row[1]
            items = window.table.findItems(matched_name, Qt.MatchFlag.MatchContains)
            for item in items:
                if item.column() == 1:
                    window.table.setCurrentCell(item.row(), 1)
                    break

        self.close()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())
