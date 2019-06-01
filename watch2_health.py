import pexpect
from colorama import Fore, Back, Style 

# Device mac address.
DEVICE = "C7:EB:B2:97:2E:C2" 

# Run gatttool interactively.
gatt = pexpect.spawn("gatttool -i hci0 -I")
 
# Connect to the device.
print(Style.RESET_ALL + 'Connecting to'),
print(DEVICE)
gatt.sendline("connect {0}".format(DEVICE))
gatt.expect("Connection successful", timeout=15)
print("Connected!")

# Get battery level. [read handle]
gatt.sendline("char-read-hnd 0x002e")
gatt.expect("Characteristic value/descriptor: ", timeout=10)
gatt.expect("\r\n", timeout=10)
print("Battery: ")
print(int(gatt.before, 16)),
print("%")

# Enable notifications for HR, BP & SpO2. [write request]
command = "char-write-req 0x0040 01"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10) 
command = "char-write-req 0x0038 0100"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10)

# Enable BP sensor + read values. [write request + listen for notification handle]
print(Style.RESET_ALL + "Reading BP...")
command = "char-write-req 0x0035 feea100869000000"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10)
gatt.expect("Notification handle = 0x0037 value: ", timeout=50)
gatt.expect("\r\n", timeout=10)
print(Fore.RED + 'Systolic/Diastolic Blood Pressure:')
print(int(gatt.before[18:20], 16)),
print("/"),
print(int(gatt.before[21:23], 16)),
print("mmHg")

# Enable Sp02 sensor + read values [write request + listen for notification handle]
print(Style.RESET_ALL + "Reading SpO2...")
command = "char-write-req 0x0035 feea10066b00"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10)
gatt.expect("Notification handle = 0x0037 value: ", timeout=30)
gatt.expect("\r\n", timeout=10)
print(Fore.RED + 'Blood Oxygen:')
print(int(gatt.before[15:17], 16)),
print("%")

# Enable HR sensor + read values. [write request + listen for notification handle]
print(Style.RESET_ALL + "Reading HR...")
command = "char-write-req 0x0035 feea10066d00"
gatt.sendline(command)
gatt.expect("Characteristic value was written successfully", timeout=10)
print(Fore.RED + "Heart Rate:")
for x in range(0, 11):
	gatt.expect("Notification handle = 0x003f value: ", timeout=30)
	gatt.expect("\r\n", timeout=10)
	print(int(gatt.before[3:5], 16)),
	print("bpm")


