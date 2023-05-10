import sys
import time
 
import requests
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow,  QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    )
 
from bluepy import btle
 
class WorkerSignals(QObject):
    signalMsg = pyqtSignal(str)
    signalRes = pyqtSignal(str)
    
class MyDelegate(btle.DefaultDelegate):
    
    def __init__(self, sgn):
        btle.DefaultDelegate.__init__(self)
        self.sgn = sgn
 
    def handleNotification(self, cHandle, data):
        datafile = open(datafilename, "a")
        print(data, file = datafile) 												#Save to file, optional decode: .decode("utf8", "ignore")
        datafile.close()
        
        try:
            dataDecoded = data.decode()
            self.sgn.signalRes.emit(dataDecoded)
        except UnicodeError:
            print("UnicodeError: ", data)
 
class WorkerBLE(QRunnable):
    
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.rqsToSend = False
        
    @pyqtSlot()
    def run(self):
        global running
        global p
        self.signals.signalMsg.emit("WorkerBLE start")
        
        #---------------------------------------------
        try:
			#ESP32-1: ec:94:cb:6b:91:4a
			#ESP32-2: c8:f0:9e:4a:92:76
            p = btle.Peripheral("c8:f0:9e:4a:92:76" , btle.ADDR_TYPE_PUBLIC) #b8:27:eb:41:62:6b 3c:71:bf:0d:dd:6a b8:27:eb:14:37:3e, btle.ADDR_TYPE_RANDOM
        except btle.BTLEException:
            print("Peripheral could not be connected to")
            return
            
        p.setDelegate( MyDelegate(self.signals) )
 
        #svc = p.getServiceByUUID("0000aaa0-0000-1000-8000-aabbccddeeff")
        #self.ch_Tx = svc.getCharacteristics("0000aaa2-0000-1000-8000-aabbccddeeff")[0]
        #ch_Rx = svc.getCharacteristics("0000aaa1-0000-1000-8000-aabbccddeeff")[0]
        
        svc = p.getServiceByUUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        self.ch_Tx = svc.getCharacteristics("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")[0]
        ch_Rx = svc.getCharacteristics("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")[0]
        
        setup_data = b"\x01\00"
        p.writeCharacteristic(ch_Rx.valHandle+1, setup_data)
 
        # BLE loop --------
        print("Peripheral connected")
        while running:
            """
            if p.waitForNotifications(1.0):
                # handleNotification() was called
                continue
 
            print("Waiting...")
            """
            
            try:
                p.waitForNotifications(1.0)
            except btle.BTLEException:
                break
            
            if self.rqsToSend:
                self.rqsToSend = False
 
                try:
                    self.ch_Tx.write(self.bytestosend, True)
                except btle.BTLEException:
                    print("btle.BTLEException");
            
        #---------------------------------------------hellohello
        p.disconnect()																	#Quit Bluetooth
        self.signals.signalMsg.emit("WorkerBLE end")
        
    def toSendBLE(self, tosend):
        self.bytestosend = bytes(tosend, 'utf-8')
        self.rqsToSend = True
        """
        try:
            self.ch_Tx.write(bytestosend, True)
        except BTLEException:
            print("BTLEException");
        """
            
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        
        buttonStartBLE = QPushButton("Start BLE")
        buttonStartBLE.pressed.connect(self.startBLE)
        
        buttonQuit = QPushButton("Quit")
        buttonQuit.pressed.connect(self.quit)
        
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        
        self.outconsole = QPlainTextEdit()
        
        buttonSendBLE = QPushButton("Send message")
        buttonSendBLE.pressed.connect(self.sendBLE)
 
        layout.addLayout(top_layout)
        top_layout.addWidget(buttonStartBLE)
        top_layout.addWidget(buttonQuit)
        layout.addWidget(self.console)
        layout.addWidget(self.outconsole)
        layout.addWidget(buttonSendBLE)
        
        w = QWidget()
        w.setLayout(layout)
        
        self.setCentralWidget(w)
        
        self.show()
        self.threadpool = QThreadPool()
        print(
            "Multithreading with Maximum %d threads" % self.threadpool.maxThreadCount())
            
    def startBLE(self):
        self.workerBLE = WorkerBLE()
        self.workerBLE.signals.signalMsg.connect(self.slotMsg)
        self.workerBLE.signals.signalRes.connect(self.slotRes)
        self.threadpool.start(self.workerBLE)
        
    def quit(self):
        global running
        global p

        running = False
        time.sleep(1.0)
        self.close()
        
    def sendBLE(self):
        strToSend = self.outconsole.toPlainText()
        self.workerBLE.toSendBLE(strToSend)
        
    def slotMsg(self, msg):
        print(msg)
        
    def slotRes(self, res):
        self.console.appendPlainText(res)
        

datafilename = "./data/" + "ESP32-" + str(int(time.time()))						#FIXME: Get specific ESP32 name? Initialize in global?
p = btle.Peripheral()															#Peripherals as list?
running = True

app = QApplication(sys.argv)
window = MainWindow()
app.exec()

#Quit without exceptions? Fixed
#Autoscan with name?
#Catch btle.Peripheral exceptions? Fixed
