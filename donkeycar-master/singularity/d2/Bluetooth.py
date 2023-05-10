import sys, time
from bluepy import btle                                 #Bluetooth LE library
from bluepy.btle import Scanner, DefaultDelegate        #Scanner library

#Bluetooth message handler
class MyDelegate(btle.DefaultDelegate):
    received = 0
    def __init__(self, datafilename):
        btle.DefaultDelegate.__init__(self)
        self.datafilename = datafilename
 
    def handleNotification(self, cHandle, data):        #On receiving from ESP32
        datafile = open(self.datafilename, "a")
        #FIXME: Format into JSON style, optional decode: .decode("utf8", "ignore")
        datatext = data.decode("utf8", "ignore")
        print(datatext, end = '', file = datafile) 			#Save to file   FIXME: datatext instead
        
        print(datatext)                                     #Show on console FIXME: datatext instead
        
        datafile.close()                                    #Close data file
        self.received += 1
        #try:
        #    dataDecoded = data.decode()
        #    self.sgn.signalRes.emit(dataDecoded)
        #except UnicodeError:
        #    print("UnicodeError: ", data)

def getNodeDataBLE(nodeID, nodeMAC):
    datafilename = "/home/singularity/d2/data/" + "ESP32-" + nodeID + "-" + str(int(time.time()))				        #FIXME: Get specific ESP32 name? Initialize in global?
    try:
        #ESP32-Hessah: ec:94:cb:6b:91:4a
        #ESP32-1: c8:f0:9e:4a:92:76
        #ESP32-2: c8:f0:9e:4f:dd:02
        p = btle.Peripheral(nodeMAC, btle.ADDR_TYPE_PUBLIC)						        #Peripherals as list?
    except btle.BTLEException:
        print("Failed connection to node " + nodeID)
        #sys.exit("Failed connection to node " + nodeID)
        return '-1'

    svc = p.getServiceByUUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
    ch_Tx = svc.getCharacteristics("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")[0]
    ch_Rx = svc.getCharacteristics("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")[0]
    d = MyDelegate(datafilename)
    p.setDelegate(d)
    
    setup_data = b"\x01\00"
    p.writeCharacteristic(ch_Rx.valHandle+1, setup_data)

    while True:
        #Wait until data recieved
        try:
            if p.waitForNotifications(1.0):
                pass
        except btle.BTLEException:
            print("Wait btle.BTLEException");
            break

        print("Waiting for " + nodeID)
        try:
            ch_Tx.write(bytes("GET", 'utf-8'), True)
        except btle.BTLEException:
            print("Write btle.BTLEException");
        
        if (d.received >= 6):
            break

    p.disconnect()				        #Quit Bluetooth
    return datafilename

if __name__ == '__main__':
    print(getNodeDataBLE(sys.argv[1], sys.argv[2]))

#Quit without exceptions? Fixed
#Autoscan with name?
#Catch btle.Peripheral exceptions? Fixed

#If not working, make sure internal BTLE is disabled with following in /boot/config.txt:
#dtoverlay=disable-bt
#dtoverlay=pi3-disable-bt
