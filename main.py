from PyQt6.QtWidgets import QApplication, QDialog, QLCDNumber, QListWidgetItem, QMessageBox, QStackedWidget, QWidget
from PyQt6.QtCore import QTimer, QUrl, Qt
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.uic import loadUi
from PyQt6 import QtCore
from datetime import datetime
import sys
import sqlite3




class Window(QDialog):
    def __init__(self):
        super().__init__()

        # Load the main UI file
        loadUi("main.ui", self)

        # Connect the calendar's selectionChanged signal to the calendarDateChanged slot
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()

        # To Do List Page Buttons
        self.saveBtn.clicked.connect(self.saveChanges)
        self.addBtn1.clicked.connect(self.addNewTask)
        self.deleteBtn.clicked.connect(self.deleteTask)
        self.editBtn.clicked.connect(self.editTask)

        # Main Page Buttons
        self.stackedWidget.setCurrentWidget(self.main)
        self.addToDoBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ToDoPage))
        self.addNoteBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.NotesPage))
        self.addAlarmBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.AlarmPage))

        # Notes Page Buttons
        self.noteOKBtn.clicked.connect(self.addNewNote)
        self.noteDeleteBtn.clicked.connect(self.deleteNote)
        self.editNoteBtn.clicked.connect(self.editNote)

        # Call the __lcd__ function to start the LCD clock
        self.lcdclock()
       
        # Alarm Page Buttons
        self.addAlarmTimeButton.clicked.connect(self.addAlarm)
        self.removeAlarmButton.clicked.connect(self.removeAlarm)
        self.alarmList.itemDoubleClicked.connect(self.removeAlarm)

        # Create a sound effect for the alarm
        self.alarmSound = QSoundEffect(self)
        self.alarmSound.setSource(QUrl.fromLocalFile("alarm1.wav"))
        self.alarmSound.setVolume(1.0)

    # ToDoList
    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)
        self.updateTaskList(dateSelected)

    # Updates the database
    def updateTaskList(self, date):
        self.tasksWidget.clear()
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.CheckState.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.tasksWidget.addItem(item)
    
    # Saves the items in the list widget to the database
    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()
        
        for i in range(self.tasksWidget.count()):
            item = self.tasksWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        messageBox.exec()

    # Adds a new task to the list widget
    def addNewTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        newTask = str(self.taskLineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)

        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()
    
    # Deletes selected task from the list widget
    def deleteTask(self):
        for item in self.tasksWidget.selectedItems():
            self.tasksWidget.takeItem(self.tasksWidget.row(item))
    
    def editTask(self): 
        overwrite = self.editBtn.setText("Over-write")
        edit = self.editBtn.setText("Edit")

        sel_items = self.tasksWidget.selectedItems()
        clearText = ""
        newText = self.taskLineEdit.text()
        
        for item in sel_items:
            item.setText(clearText)
            if item in sel_items:
                edited = item.setText(item.text() + newText)
            else:
                clearText

    # Alarm page/LCD clock
    def lcdclock(self):
        # Find the QLCDNumber widget
        self.lcd = self.findChild(QLCDNumber, "lcdNumber")

        # Create a timer and connect it to the lcd_number slot
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.lcd_number)

        # Start the timer and update every second
        self.timer.start(1000)

        # Call the lcd_number slot
        self.lcd_number()

    # Slot for updating the LCD clock
    def lcd_number(self):
        # Get the current time and format it
        time = datetime.now()
        formatted_time = time.strftime("%I:%M:%S %p ")

        # Set the number of LCD digits
        self.lcd.setDigitCount(13)

        # Display the formatted time
        self.lcd.display(formatted_time)

        # Check if an alarm has gone off
        current_time = datetime.now().strftime("%I:%M:%S %p")
        items = [self.alarmList.item(i) for i in range(self.alarmList.count())]
        for item in items:
            if item.text() == current_time:
                # Play the alarm sound
                self.alarmSound.play()

                # Remove the alarm from the list
                self.alarmList.takeItem(self.alarmList.row(item))
                print(current_time)

    # Add an alarm to the alarm list
    def addAlarm(self):
        time = self.alarmTimeEdit.time().toString("hh:mm:ss AP")
        alarm = QListWidgetItem(time)
        self.alarmList.addItem(alarm)

        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        # Get the selected date from the calendar
        date = self.calendarWidget.selectedDate().toPyDate()

        # Insert the new alarm into the database
        query = "INSERT INTO alarm(time, date, completed) VALUES (?, ?, ?)"
        row = (time, date, "NO")  # Assuming default values for "completed"
        cursor.execute(query, row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Alarm Added.")
        messageBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        messageBox.exec()

        # Update the alarm list
        self.updateAlarmList(date)
        

    def updateAlarmList(self, time):
        self.alarmList.clear()
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "SELECT time, completed FROM alarm WHERE date = ?"
        row = (time,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            time = result[0]
            item = QListWidgetItem(time)
            self.alarmList.addItem(item)

        # Remove the selected alarm
    def removeAlarm(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        for item in self.alarmList.selectedItems():
            time = item.text()

            query = "DELETE FROM alarm WHERE time = ?"
            row = (time,)
            cursor.execute(query, row)
            db.commit()

        self.alarmList.takeItem(self.alarmList.row(item))

    
    
    # Notes
    def addNewNote(self):
        newNote = str(self.noteLineEdit.text())
        self.noteItemList.addItem(newNote)

    # Deletes selected note from the list widget
    def deleteNote(self):
        for item in self.noteItemList.selectedItems():
            self.noteItemList.takeItem(self.noteItemList.row(item))
    
    def editNote(self): 
        overwrite_a = self.editNoteBtn.setText("Over-write")
        edit_a = self.editBtn.setText("Edit")

        sel_items_a = self.noteItemList.selectedItems()
        clearText_a = ""
        newText_a = self.noteLineEdit.text()
        
        for item in sel_items_a:
            item.setText(clearText_a)
            if item in sel_items_a:
                edited_a = item.setText(item.text() + newText_a)
            else:
                clearText_a


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
