import asyncio
import time
from fitness_machine_service import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import sys

import test     #This file contains the actual process. If you want to create your own process, rename test to the name of your file or change the test file


class Worker(QObject):
    """Worker class that runs the Sensor and Bluetooth parts of the program in a different thread from the GUI
    to prevent freezing the window while the program runs.
    """    

    #Signals to call functions
    finished = pyqtSignal()
    issue_message = pyqtSignal(str)
    green_screen = pyqtSignal()
    red_screen = pyqtSignal()
    color_reset = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        """Constructor for creating Worker objects. Called whenever one is created
        """     
        
        self.args = args
        self.kwargs = kwargs
        self.gui = args[0]
        self.device_name = args[1]
        self.working = True

    def run(self):
        """Sets up async event loop used for Bluetooth functions, then runs sensor_data.main() in its own thread
        """        
        loop = asyncio.new_event_loop()                                              # create async event loop
        self.issue_message.emit("Getting Device Address")
        
        device_address = loop.run_until_complete(test.find_device(self.device_name))    # run find_device function in the event loop
        self.issue_message.emit("Connecting...")

        speed = loop.run_until_complete(test.main(device_address, self))                # run sensor_data.main() in event loop
        time.sleep(2)
        self.issue_message.emit("Resetting")

        time.sleep(2)
        self.color_reset.emit()                                                         # give the signal to reset the color
        self.finished.emit()                                                            # gives signal that funciton is finished


class BTMainWindow(QMainWindow):
    """Class representing the main window of the GUI. Called whenever one is created
    """    
    #Signals:
    stopSig = pyqtSignal()

    def __init__(self):
        super(BTMainWindow, self).__init__()
        """Constructor function for setting up BTMainWindow objects.
        """        

        self.setObjectName("MainWindow")
        self.resize(425, 328)
        self.setStyleSheet("background-color: gray;")                                   # If you want to modify the looks, this sets the background color for the
        self.thread = None

        self.setupUi()
        self.stop_button.setEnabled(False)
        self.update()

    def setupUi(self):
        """Performs the setup for all the GUI widgets, layouts and inputs
        """    
#---------------------------SETUP VERTICAL LAYOUT---------------------------------------#
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)

#---------------------------TITLE LABEL-------------------------------------------------#
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setScaledContents(True)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)

#-------------------TEXT BOX AND LAYOUT---------------------------------------#
        #________________TEXT BOX________________#
        self.text_box = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_box.sizePolicy().hasHeightForWidth())

        self.text_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text_box.setFont(font)
        self.text_box.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.text_box.setText("")
        self.text_box.setFrame(True)
        self.text_box.setAlignment(QtCore.Qt.AlignCenter)
        self.text_box.setDragEnabled(False)
        self.text_box.setPlaceholderText("")
        self.text_box.setClearButtonEnabled(False)
        self.text_box.setObjectName("text_box")

        #___________________TEXTBOX LAYOUT AND SPACERS_____________________#
        self.horizontalLayout.addWidget(self.text_box)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

    #-----------------------SETUP GRID LAYOUT-----------------------------------------------#    
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName("gridLayout")

        #________________________START BUTTON_____________________________#
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 0, 0, 1, 1)

        #________________________SAVE BUTTON_____________________________#
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_button.setFont(font)
        self.save_button.setObjectName("save_button")
        self.gridLayout.addWidget(self.save_button, 1, 0, 1, 1)

        #________________________LOAD BUTTON_____________________________#
        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.load_button.setFont(font)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 1, 1, 1, 1)

        #________________________STOP BUTTON_____________________________#
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stop_button.setFont(font)
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 0, 1, 1, 1)

    #----------------------------------------OUTPUT LABELS AND SPACERS-----------------------------------------------------------------#
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.output_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.output_label.setFont(font)
        self.output_label.setText("")
        self.output_label.setAlignment(QtCore.Qt.AlignCenter)
        self.output_label.setObjectName("output_label")
        self.verticalLayout.addWidget(self.output_label)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.setCentralWidget(self.centralwidget)

        #________________________BUTTON CONNECTIONS_______________________#
        '''This is where functions are attached to each button. Everything else is just layout and style'''
        self.start_button.clicked.connect(self.thread_start)
        self.stop_button.clicked.connect(self.stop)
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)

    #------------------------------------OTHER-----------------------------#
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Opens to fit the screen
        self.showMaximized()

        # opens at the size defined in the __init__ method
        # self.show()
 
    # It's for making GUIS with multiple language (human languages, not programming languages) options, and the code cannot display text without it
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Treadmill Bluetooth"))
        self.title_label.setText(_translate("self", "Enter Treadmill Name:"))
        self.start_button.setText(_translate("self", "Start"))
        self.save_button.setText(_translate("self", "Save"))
        self.load_button.setText(_translate("self", "Load"))
        self.stop_button.setText(_translate("self", "Stop"))



#-----------------------------------GUI FUNCTIONS--------------------------------------------------#

#___________________________________MAIN FUNCTIONS__________________________________________#

    def update(self):
        """Adjust the size of the text labels when the text in them changes
        """

        self.title_label.adjustSize()
        self.output_label.adjustSize()

    def update_message(self, text: str):
        """Changes the text in the output label

        Args:
            text (str): The text that you want to display on the GUI
        """
        self.output_label.setText(text)
            
    def thread_start(self):
        """
        Creates the thread and worker used to run the parts of the program that have nothing to do with the GUI, 
        ie. the Bluetooth, data collection, and most of the CSV writing stuff.
        """
        #----------------------------------------------------Thread Setup--------------------------------------------------------------#
        device_name = self.text_box.text()
        self.output_label.setText("Running main")

        #Creates the thread
        self.thread = QThread()

        # creates the worker object to enact the thread so that the GUI doesn't have to
        self.worker = Worker(self, device_name)

        # make the worker part of the thread
        self.worker.moveToThread(self.thread)

        #---------------------------------------- Connect signals and slots-----------------------------------------------------------#
        #These just tell the program what to do when it recieves a signal from a different part of the program.
        self.thread.started.connect(self.worker.run)            # call worker.run funciton when the thread is started
        self.worker.finished.connect(self.thread.quit)          # when the worker signals that it's finished, exit the thread
        self.worker.finished.connect(self.worker.deleteLater)   # delete the worker when it is safe to do so
        self.thread.finished.connect(self.thread.deleteLater)   # delete the thread when it is safe to do so
        self.thread.start()                                     # run the thread

        self.worker.issue_message.connect(self.update_message)  #lets worker/sensor program update the output message (bottom textbox in the GUI)

        #----------------------------------------Color Changing Connections and Button Enablers-----------------------------------------------------------#
        # NOTE: lambda just means that what comes after it should be treated like a function, but wasn't important enough to get a name.
        self.worker.green_screen.connect(lambda: self.setStyleSheet("background-color: green;"))            # allows for the worker/sensor program to change the color of the GUI to green (see green() function)
        self.worker.red_screen.connect(lambda: self.setStyleSheet("background-color: red;"))                # same as above but red
        self.worker.color_reset.connect(lambda: self.setStyleSheet("background-color: gray;"))  #

        # disable start button and enable stop button while prog is running after start button is pressed
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # enable start and disable stop button when prog finishes
        self.thread.finished.connect(
            lambda: self.output_label.setText("Reset Complete!")
        )
        self.thread.finished.connect(
            lambda: self.start_button.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stop_button.setEnabled(False)
        )

    
    def stop(self):
        '''Stops the program after the current loop finishes executing
        '''
        if (self.thread != None) and (self.worker != None):
            self.worker.working = False
            print("Stopping after current loop")

        else:
            self.output_label.setText("Nothing to Stop")


    def save(self):
        """Saves the contents of the input text_box to config.txt so that it can be retrieved quickly
        """        

        device_name = self.text_box.text()


        try:
            # Open config.txt for writing/create file if none exists, save the file, tell the user it's saved, and close the file
            file = open("config.txt", "w")
            file.write(device_name)
            self.output_label.setText("Device Saved!")
            self.update()
            file.close()

        #tell the user if there was an error
        except:
            self.output_label.setText("ERROR: Device Not Saved")
            self.update()

    def load(self):
        """Loads the name of the saved Bluetooth device (or whatever text was saved last) from config.txt into input text_box
        """  

        #Open config.txt for reading, read data into device_name, put in text_box, close file
        try:
            file = open("config.txt", "r")
            device_name = file.readline()
            self.text_box.setText(device_name)
            self.output_label.setText("Device Loaded!")
            self.update()
            file.close()

        #tell user if there was an error
        except:
            self.output_label.setText("No Config File Found.")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = BTMainWindow()
    sys.exit(app.exec_())
