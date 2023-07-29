import pexpect
import json
from colorama import Fore, Style

class BLEHealthDevice:
    def __init__(self, device_mac, config_file):
        self.device_mac = device_mac
        self.gatt = pexpect.spawn("gatttool -i hci0 -I")
        with open(config_file) as f:
            self.config = json.load(f)

    def connect(self):
        print(Style.RESET_ALL + 'Connecting to', self.device_mac)
        self.gatt.sendline(f"connect {self.device_mac}")
        try:
            self.gatt.expect("Connection successful", timeout=15)
            print("Connected!")
        except pexpect.TIMEOUT:
            print("Connection failed!")

    def disconnect(self):
        print(Style.RESET_ALL + 'Disconnecting from', self.device_mac)
        self.gatt.sendline("disconnect")
        print("Disconnected!")

    def read_battery_level(self):
        self.gatt.sendline("char-read-hnd 0x002e")
        try:
            self.gatt.expect("Characteristic value/descriptor: ", timeout=10)
            self.gatt.expect("\r\n", timeout=10)
            print("Battery: ", int(self.gatt.before, 16), "%")
        except pexpect.TIMEOUT:
            print("Failed to read battery level!")

    def enable_notifications(self, params):
        command = f"char-write-req {params['handle']} {params['value']}"
        self.gatt.sendline(command)
        try:
            self.gatt.expect("Characteristic value was written successfully", timeout=10)
        except pexpect.TIMEOUT:
            print("Failed to enable notifications!")

    def read_value(self, params):
        print(Style.RESET_ALL + f"Reading {params['label']}...")
        self.enable_notifications(params)
        try:
            self.gatt.expect(f"Notification handle = {params['read_handle']} value: ", timeout=50)
            self.gatt.expect("\r\n", timeout=10)
            print(Fore.RED + params['label'] + ':', int(self.gatt.before[18:20], 16), params['unit'])
        except pexpect.TIMEOUT:
            print("Failed to read value!")

    def read_heart_rate(self, params):
        print(Style.RESET_ALL + f"Reading {params['label']}...")
        self.enable_notifications(params)
        print(Fore.RED + params['label'] + ":")
        for _ in range(11):
            try:
                self.gatt.expect(f"Notification handle = {params['read_handle']} value: ", timeout=30)
                self.gatt.expect("\r\n", timeout=10)
                print(int(self.gatt.before[3:5], 16), params['unit'])
            except pexpect.TIMEOUT:
                print("Failed to read heart rate!")

    def run(self):
        self.connect()
        self.read_battery_level()

        for notification in self.config['notifications']:
            self.enable_notifications(notification)

        for metric in self.config['metrics']:
            if metric['label'] == 'Heart Rate':
                self.read_heart_rate(metric)
            else:
                self.read_value(metric)

        self.disconnect()

if __name__ == "__main__":
    device = BLEHealthDevice("C7:EB:B2:97:2E:C2", 'config.json')
    device.run()
