import pexpect
import json
from colorama import Fore, Style

class BLEHealthDevice:
    def __init__(self, device_mac, config_file):
        self.device_mac = device_mac
        self.gatt = pexpect.spawn("gatttool -i hci1 -I")
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

    def enable_sensor_and_read_values(self, params):
        print(Style.RESET_ALL + f'Reading {params["label"]}...')
        command = f"char-write-req {params['write_handle']} {params['write_value']}"
        self.gatt.sendline(command)
        try:
            self.gatt.expect("Characteristic value was written successfully", timeout=10)
            self.gatt.expect(f"Notification handle = {params['read_handle']} value: ", timeout=40)
            self.gatt.expect("\r\n", timeout=10)
            print(Fore.RED + params['label'] + ':', int(self.gatt.before[params['value_start']:params['value_end']], 16), params['unit'])
        except pexpect.TIMEOUT:
            print("Failed to read value!")

    def run(self):
        self.connect()

        for metric in self.config['metrics']:
            self.enable_sensor_and_read_values(metric)

        self.disconnect()

if __name__ == "__main__":
    device = BLEHealthDevice("A4:C1:C2:F6:82:06", 'config.json')
    device.run()
