import pexpect
from colorama import Fore, Back, Style 

# Device mac address.
DEVICE = "A4:C1:C2:F6:82:06"

# Run gatttool interactively.
gatt = pexpect.spawn("gatttool -i hci1 -I")
 
# Connect to the device.
gatt.sendline("connect {0}".format(DEVICE))
gatt.expect("Connection successful", timeout=15)

# Notifications enabled by default on 0x001e

# Enable HR sensor + read values (looped 99 times). [write request + listen for notification handle]
for x in range(0,99):
	command = "char-write-req 0x0025 0a01"
	gatt.sendline(command)
	gatt.expect("Characteristic value was written successfully", timeout=10)
	gatt.expect("Notification handle = 0x001f value: ", timeout=50)
	gatt.expect("\r\n", timeout=10)
	print(int(gatt.before[30:32], 16))
