from PyQt6.QtWidgets import QApplication, QDialog, QLCDNumber, QListWidgetItem
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.uic import loadUi
from datetime import datetime
import sys



class Window(QDialog):
    def __init__(self):
        super().__init__()

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
        self.lcdclock()
       
        # alarm page buttons
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
        dateSelected = self.calendarWidget.selectedDate().toPython()
        print("Date selected:", dateSelected)

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

    # Remove an alarm from the alarm list
    def removeAlarm(self):
        for item in self.alarmList.selectedItems():
            self.alarmList.takeItem(self.alarmList.row(item))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())