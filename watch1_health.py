import pexpect
from colorama import Fore, Back, Style 

# Device mac address.
DEVICE = "A4:C1:C2:F6:82:06" 

# Run gatttool interactively.
gatt = pexpect.spawn("gatttool -i hci1 -I")
 
# Connect to the device.
print(Style.RESET_ALL + 'Connecting to'),
print(DEVICE)
gatt.sendline("connect {0}".format(DEVICE))
gatt.expect("Connection successful", timeout=15)
print("Connected!")

# Notifications enabled by default on 0x001e

# Enable BP sensor + read values. [write request + listen for notification handle]
print(Style.RESET_ALL + 'Reading BP...')
command = "char-write-req 0x0025 f1031401"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10)
gatt.expect("Notification handle = 0x001f value: ", timeout=40)
gatt.expect("\r\n", timeout=10)
print(Fore.RED + 'Systolic/Diastolic Blood Pressure:')
print(int(gatt.before[6:8], 16)),
print("/"),
print(int(gatt.before[9:11], 16)),
print("mmHg")

# Enable HR sensor + read values. [write request + listen for notification handle]
print(Style.RESET_ALL + 'Reading HR...')
command = "char-write-req 0x0025 0a01"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10)
gatt.expect("Notification handle = 0x001f value: ", timeout=40)
gatt.expect("\r\n", timeout=10)
print(Fore.RED + "Heart Rate:")
print(int(gatt.before[30:32], 16)),
print("bpm")
