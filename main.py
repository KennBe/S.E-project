from PyQt6.QtWidgets import QDialog, QApplication , QStackedWidget, QWidget
from PyQt6.uic import loadUi
import sys
import datetime

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

        #alarmpage
    def ToSetAnAlarm(self):

        alarmHour = int(input("Enter hour: "))
        alarmMin = int(input("Enter Minutes: "))
        alarmAm = input("am / pm")

        if alarmAm=="pm":  
            alarmHour+=12
    
        while True:
            if alarmHour==datetime.datetime.now().hour and alarmMin==datetime.datetime.now().minute:
                print("WAKE UP")
                break



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
    
    
testinggg
