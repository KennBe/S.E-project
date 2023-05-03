from asyncio import TimerHandle
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QApplication, QLCDNumber
from PyQt6.uic import loadUi
import sys
from PyQt6.QtCore import QTimer, QTime
from datetime import datetime




class Window(QDialog):           
    def __init__(self):
        super(Window, self).__init__()
        loadUi("main.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)  
               
        #Buttons
        self.stackedWidget.setCurrentWidget(self.main)
        self.addToDoBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ToDoPage))
        self.addNoteBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.NotesPage))
        self.addAlarmBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.AlarmPage))
        self.addReminderBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ReminderPage))

        
        #ToDoList
    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)

        
        #alarmpage/lcdclock
    def __lcdclock__(self):
        super(Window, self).__init__()

		 # Load the ui file
        uic.loadUi("main.ui", self)

		    # Define our widgets
        self.lcd = self.findChild(QLCDNumber, "lcdNumber")	

		    # Create A Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.lcd_number)

		    # Start the timer and update every second
        self.timer.start(1000)

		    # Call the lcd function
        self.lcd_number()

    def lcd_number(self):
		    # Get the time
        time = datetime.now()
        formatted_time = time.strftime("%I:%M:%S %p ")

		    # Set number of LCD Digits
        self.lcd.setDigitCount(12)

		    # Display The Time
        self.lcd.display(formatted_time)
       


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec()) 
