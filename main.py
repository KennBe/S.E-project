from asyncio import TimerHandle
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QApplication, QLCDNumber
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer, QTime
from datetime import datetime
import sys

class Window(QDialog):           
    def __init__(self):
        super(Window, self).__init__()

        # Load the main UI file
        loadUi("main.ui", self)

        # Connect the calendar's selectionChanged signal to the calendarDateChanged slot
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)

        # Set up the button connections
        self.stackedWidget.setCurrentWidget(self.main)
        self.addToDoBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ToDoPage))
        self.addNoteBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.NotesPage))
        self.addAlarmBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.AlarmPage))
        self.addReminderBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ReminderPage))

        # Call the __lcd__ function to start the LCD clock
        self.__lcd__()

    # alarmpage
    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)

    # alarm page/LCD clock
    def __lcd__(self):
        # Find the QLCDNumber widget
        self.lcd = self.findChild(QLCDNumber, "lcdNumber")

        # Create a timer and connect it to the lcd_number slot
        self.timer = QTimer()
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
        self.lcd.setDigitCount(12)

        # Display the formatted time
        self.lcd.display(formatted_time)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
