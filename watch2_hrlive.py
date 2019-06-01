import pexpect
from colorama import Fore, Back, Style 

# Device mac address.
DEVICE = "C7:EB:B2:97:2E:C2" 

# Run gatttool interactively.
gatt = pexpect.spawn("gatttool -i hci0 -I")
 
# Connect to the device.
gatt.sendline("connect {0}".format(DEVICE))
gatt.expect("Connection successful", timeout=10)

# Enable notifications for HR. [write request]
command = "char-write-req 0x0040 01"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10) 

# Enable HR sensor + read values (looped 99 times). [write request + listen for notification handle]
for x in range(0,99):
	command = "char-write-req 0x0035 feea10066d00"
	gatt.sendline(command)
	gatt.expect("Characteristic value was written successfully", timeout=10)
	for x in range(0, 11):
		gatt.expect("Notification handle = 0x003f value: ", timeout=30)
		gatt.expect("\r\n", timeout=10)
		print(int(gatt.before[3:5], 16))
