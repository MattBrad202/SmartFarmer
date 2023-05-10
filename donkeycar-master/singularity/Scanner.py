from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(5.0)

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if (desc == "Complete Local Name" and (value == "Pixel 3a" or value == "Eagles ESP32 1" or value == "Eagles ESP32 2")):
            print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print("  %s = %s" % (desc, value))
		
    #print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    #for (adtype, desc, value) in dev.getScanData():
	#	
    #    print("  %s = %s" % (desc, value))
