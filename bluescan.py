
from bluepy.btle import Peripheral, Scanner, DefaultDelegate, BTLEException

class BlueDelegate ( DefaultDelegate ):

    def __init__ ( self ):
        DefaultDelegate.__init__(self)

    def handleDiscovery ( self, dev, isNewDev, isNewData ):
        if isNewDev:
            print( f"Discovered Device: {dev.addr}")
        elif isNewData:
            print( f"Received new data from {dev.addr}")

class BlueScan:

    def __init__ ( self, bluetoothInterface : int = 0 ):
        self.interface = bluetoothInterface
        self.delegate = BlueDelegate()
        self.scanner = Scanner(self.interface)
        self.scanner.withDelegate(self.delegate)

    def scan ( self, seconds : int = 10 ):
        return self.scanner.scan(seconds)


if __name__ == '__main__':

    scanner = BlueScan(0)
    devices = scanner.scan(10)
    for dev in devices:
        print( f"Device {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB, connectable={dev.connectable}, updateCount={dev.updateCount}")
        for (adtype, desc, value) in dev.getScanData():
            print( f"  {desc} = {value} ({adtype})")
        if dev.connectable:
            print (f"  Attempting to connect . . .")
            peripheral = None
            try:
                peripheral = Peripheral(dev)
                print( f"  ... connected.")
                services = peripheral.getServices()
                for service in services:
                    print(f"  {str(service)}:")
                    print(f"    Service UUID = {service.uuid}")
                    for characteristic in service.getCharacteristics():
                        print(f"    {characteristic}, uuid={characteristic.uuid}, hnd={hex(characteristic.getHandle())}, supports {characteristic.propertiesToString()}")
                        if characteristic.supportsRead():
                            try:
                                print(f"      -> {repr(characteristic.read())}")
                            except BTLEException as e:
                                print(f"      -> {e}")
                print(f"Getting service by ID 0xd001")
                service = peripheral.getServiceByUUID(0xd001)
                print( f"    Service UUID = {service.uuid} FOUND" )
                peripheral.disconnect()
            except Exception as e:
                if peripheral:
                    peripheral.disconnect()
                print(f"  Connection failed with {e}")
        else:
            print( f"  not connectable, not trying")

