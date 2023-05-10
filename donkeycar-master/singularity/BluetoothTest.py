from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate
import sys, time

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        #print("\n- handleNotification -\n")
        print(data)
        # ... perhaps check cHandle
        # ... process 'data'
        
        print(data, file = datafile) 										#Save to file, optional decode: .decode("utf8", "ignore")
        
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            #print("Discovered device", dev.addr)							#Identify here?
            pass
        elif isNewData:
            #print("Received new data from", dev.addr)
            pass

# Find Pixel 3a
scanner = Scanner().withDelegate(ScanDelegate())
print("Scanning...")
devices = scanner.scan(5.0)
found = False
btle_mac = "ec:94:cb:6b:91:4a"	#Default to known ESP32?
btle_type = btle.ADDR_TYPE_RANDOM
uuid_string = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"	#Defaults to ESP32 UART Characteristics
tx_string = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
rx_string = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if (desc == "Complete Local Name" and value[:13] == "Eagles ESP32 " and value[13:] == "1"):	#FIXME: Handle multiple devices? "Pixel 3a" "Eagle's ESP32"
            btle_mac = dev.addr
            btle_type = dev.addrType
            uuid_string = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"	#Defaults to ESP32 UART Characteristics
            tx_string = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
            rx_string = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
            found = True
            print("Found ESP32 %s" % dev.addr)
            break
        if (desc == "Complete Local Name" and value == "Pixel 3a"):
            btle_mac = dev.addr
            btle_type = dev.addrType
            uuid_string = "0000aaa0-0000-1000-8000-aabbccddeeff"
            tx_string = "0000aaa2-0000-1000-8000-aabbccddeeff"
            rx_string = "0000aaa1-0000-1000-8000-aabbccddeeff"
            found = True
            print("Found Pixel %s" % dev.addr)
            break
    if (found):
	    break

if (not found):
	print("Nothing Found")
	sys.exit("Exiting")

# Initialisation  -------

p = btle.Peripheral(btle_mac, btle_type)				#Pixel 3a, change as needed (btle.ADDR_TYPE_RANDOM)
#p = btle.Peripheral("3c:71:bf:0d:dd:6a")   #NodeMCU-32S
#p = btle.Peripheral("24:0a:c4:e8:0f:9a")   #ESP32-DevKitC V4

# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID(uuid_string)			#ESP32: 6E400001-B5A3-F393-E0A9-E50E24DCCA9E, 
ch_Tx = svc.getCharacteristics(tx_string)[0]	#ESP32: 6E400002-B5A3-F393-E0A9-E50E24DCCA9E, 
ch_Rx = svc.getCharacteristics(rx_string)[0]	#ESP32: 6E400003-B5A3-F393-E0A9-E50E24DCCA9E, 

p.setDelegate( MyDelegate())

setup_data = b"\x01\00"
p.writeCharacteristic(ch_Rx.valHandle+1, setup_data)

lasttime = time.localtime()

datafilename = "./data/" + "ESP32-" + str(int(time.time()))					#FIXME: Get specific ESP32 name?
datafile = open(datafilename, "a")

while True:
    """
    if p.waitForNotifications(1.0):
        pass  #continue

    print("Waiting...")
    """
    
    nowtime = time.localtime()
    if(nowtime > lasttime):
        lasttime = nowtime
        stringtime = time.strftime("%H:%M:%S", nowtime)
        btime = bytes(stringtime, 'utf-8')
        try:
            ch_Tx.write(btime, True)
        except btle.BTLEException:
            print("btle.BTLEException");
        #print(stringtime)
        #ch_Tx.write(b'wait...', True)
        
    # Perhaps do something else here
