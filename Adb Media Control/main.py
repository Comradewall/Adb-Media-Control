#Programmer: Craciun Mihai
#Scope: Making an control interface for Anndroid devices usinng Adb
#Cheat sheet (play:keyevent 85, next:87, prev:88, volup: 24, voldown: 25)

import sys
import os 
import threading

from time import sleep
from subprocess import run, PIPE, Popen

from PyQt5.QtGui import QBrush, QImage, QPalette, QPixmap, QColor, QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMenu,QWidget,QLabel,QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QTimer


def InitializeAdb():
    print("Initialization...")
    Popen("adb devices", stdout=PIPE, shell=True)

def BatteryLevelFct():

    #Obtains Battery level for more info check MusicRecog()

    commands_array = ["adb","shell","dumpsys battery | grep -m1 level"]
    global BatteryLevel

    while True:
        try:
            result = run(commands_array,stdout=PIPE, stderr=PIPE,
                         check= True, universal_newlines=True)
        except Exception as e:
            print("Unable To get bettery level:")
            print(e)
        
        BatteryLevel = "Battery" + result.stdout

        sleep(2)

def MusicRecog():

    # If it works don't change it for the worse (Like its a good implementation but it's inefficient)
    # This baiscly gets the current song name from the media_session of the android device
    # -m1 parameter from grep gets only the first line of the output but this mayt lead to situations where name output is null

    commands_array = ["adb","shell","dumpsys media_session | grep -m1 description"]
    global SongName

    while True: 
        try:
            result = run(commands_array, stdout=PIPE, stderr=PIPE, 
                    check=True, universal_newlines=True)
        except Exception as e:
            print("Unable to get song name:")
            print(e)
        RawOut = result.stdout

        #Removes some metadta from the raw string
        charToRemove = 31

        Output = RawOut.replace(RawOut[:charToRemove], '', 1)

        if len(Output) >= 51 :                      #Overflow Protection
            n = len(Output) - 51
            Output = Output[:len(Output) - n]
            Output = Output + '...'

        SongName = Output

        sleep(2)   

def AdbAction(adbCommNumber):

    #This makes the magic happen by taking the thing and doinng the thing and making shit work basicly simple right?

    commands_array = ["adb","shell","input keyevent " + str(adbCommNumber)]

    try:
        run(commands_array, stdout=PIPE, stderr=PIPE,
            check=True, universal_newlines=True)
        
    except Exception as e:
        print("Ope Friend Looks like u dropped something:")
        print(e)

def ExitApplication():
    sys.exit()

#Control Panel(Main GUI Elmenets)

def ControlWindow():
    class ControlPanel(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)

            self.w = None

            print(globals()["SongName"])
            
            self.setMinimumSize(QSize(400,200))
            self.setGeometry(0,0,400,200)
            self.setWindowTitle("Music Control Panel")

            TitleFont = self.font()
            TitleFont.setPointSize(15)

            #Updates every 5s to get new song name

            def onTimeout():
                newSong = globals()["SongName"]
                self.SongLabel.setText(newSong)
                self.SongLabel.setGeometry(0,10,450,35)
            self.SongLabel = QLabel(self)
            self.SongLabel.setText("Not Loaded")
            self.SongLabel.setFont(TitleFont)
            self.Updatetimer = QTimer()
            self.Updatetimer.timeout.connect(onTimeout)
            self.Updatetimer.start(2000)

            def onTimeoutBattery():
                newBatt = globals()["BatteryLevel"]
                self.BatteryLabel.setText(newBatt)
                self.BatteryLabel.setGeometry(0,165,450,35)
            self.BatteryLabel = QLabel(self)
            self.BatteryLabel.setText("Not Loaded")
            self.BatteryLabel.setFont(TitleFont)
            self.UpdatetimerBatt = QTimer()
            self.UpdatetimerBatt.timeout.connect(onTimeoutBattery)
            self.UpdatetimerBatt.start(2000)

            self.PlayButton = QPushButton(self)
            self.PlayButton.setGeometry(175,75,45,45)
            self.PlayButton.clicked.connect(lambda: AdbAction(85))
            self.PlayButton.setIcon(QIcon('play.svg'))
            self.PlayButton.setIconSize(QtCore.QSize(25,25))

            self.PrevButton = QPushButton(self)
            self.PrevButton.setGeometry(115,75,45,45)
            self.PrevButton.clicked.connect(lambda: AdbAction(88))
            self.PrevButton.setIcon(QIcon('prev.svg'))
            self.PrevButton.setIconSize(QtCore.QSize(25,25))

            self.PrevButton = QPushButton(self)
            self.PrevButton.setGeometry(235,75,45,45)
            self.PrevButton.clicked.connect(lambda: AdbAction(87))
            self.PrevButton.setIcon(QIcon('next.svg'))
            self.PrevButton.setIconSize(QtCore.QSize(25,25))

            self.VolUpButton = QPushButton(self)
            self.VolUpButton.setGeometry(20,50,45,45)
            self.VolUpButton.clicked.connect(lambda: AdbAction(24))
            self.VolUpButton.setIcon(QIcon('volUp.svg'))
            self.VolUpButton.setIconSize(QtCore.QSize(25,25))

            self.VolDownButton = QPushButton(self)
            self.VolDownButton.setGeometry(20,95,45,45)
            self.VolDownButton.clicked.connect(lambda: AdbAction(25))
            self.VolDownButton.setIcon(QIcon('volDown.svg'))
            self.VolDownButton.setIconSize(QtCore.QSize(25,25))


    if __name__ =="__main__":
        app = QtWidgets.QApplication(sys.argv)
        mainWin = ControlPanel()
        mainWin.show()
        sys.exit(app.exec_())

def Main():
    if __name__ == "__main__":
        print("Program Started and is assigned to thread: {}".format(threading.current_thread().name))
        print("ID of main program process: {}".format(os.getpid()))

        InitializeAdb()             #Initializes Adb by starting daemon and indentf. devices

        def StartMusicRecog():      #Starts a separate th. for the music recog to run in bg and update
            MusicRecogTh = threading.Thread(target=MusicRecog, name="MusicRecogTh")
            MusicRecogTh.start()
            return MusicRecogTh

        def StartBatteryLvTh():      #Starts a separate th. for the Battery Lvl to run in bg and update
            BatteryLevelTh = threading.Thread(target=BatteryLevelFct, name="BatteryLevelTh")
            BatteryLevelTh.start()
            return BatteryLevelTh
        
        StartBatteryLvTh()

        StartMusicRecog()

        ControlWindow()

        print(globals()["SongName"])
Main()
