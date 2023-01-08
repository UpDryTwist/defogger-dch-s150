
from bluepy.btle import Peripheral, Scanner, DefaultDelegate

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
        print( f"Device {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB")
        for (adtype, desc, value) in dev.getScanData():
            print( f"  {desc} = {value} ({adtype})")
        print (f"    Attempting to connect . . .")
        peripheral = Peripheral(dev.addr)
        services = peripheral.getServices()
        for service in services:
            print(f"    Service UUID = {service.uuid}")
        characteristics = peripheral.getCharacteristics()
        for characteristic in characteristics:
            print(f"    Characteristic handle {characteristic.getHandle()} has properties {characteristic.propertiesToString()}")
        # service = peripheral.getServiceByUUID( 0xd001 )
        # handles = service.getCharacteristics()


