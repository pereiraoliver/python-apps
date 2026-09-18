import sqlite3
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
)

# Base path for app resources and the SQLite database.
BASE_DIR = Path(__file__).resolve().parent


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
        connection = sqlite3.connect(BASE_DIR / "database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        connection.close()

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


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Form used to edit a new student record.
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        index = window.table.currentRow()
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
        connection = sqlite3.connect(BASE_DIR / "database.db")
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
            (
                self.student_name.text(),
                self.course_name.currentText(),
                self.student_mobile.text(),
                self.student_id,
            ),
        )
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        self.accept()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        index = window.table.currentRow()
        st_id = window.table.item(index, 0).text()
        self.student_id = QLineEdit(st_id)
        self.student_id.setReadOnly(True)
        layout.addWidget(self.student_id)
        st_name = window.table.item(index, 1).text()
        self.student_name = QLineEdit(st_name)
        self.student_name.setReadOnly(True)
        layout.addWidget(self.student_name)
        st_course = window.table.item(index, 2).text()
        self.student_course = QComboBox()
        self.student_course = QLineEdit(st_course)
        self.student_course.setReadOnly(True)
        layout.addWidget(self.student_course)
        st_mobile = window.table.item(index, 3).text()
        self.student_mobile = QComboBox()
        self.student_mobile = QLineEdit(st_mobile)
        self.student_mobile.setReadOnly(True)
        layout.addWidget(self.student_mobile)
        self.student_label = QLabel(
            f"Are you sure you want to delete the record of {st_name}?"
        )
        layout.addWidget(self.student_label)
        button = QPushButton("Delete")
        button.clicked.connect(self.delete_student)
        layout.addWidget(button)
        self.setLayout(layout)

    def delete_student(self):
        connection = sqlite3.connect(BASE_DIR / "database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE Id = ?", (self.student_id.text(),))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        self.accept()


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
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.student_mobile.text()
        connection = sqlite3.connect(BASE_DIR / "database.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, mobile),
        )
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        self.accept()


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
        name = self.search_name.text()
        connection = sqlite3.connect(BASE_DIR / "database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",)
        )
        rows = list(result)
        print(rows)
        items = window.table.findItems(name, Qt.MatchFlag.MatchContains)
        for item in items:
            print(item)
            window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()
        # self.accept()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())
