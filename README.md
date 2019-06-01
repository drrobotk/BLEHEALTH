# BLEHEALTH
Reading Heart Rate (bpm), Systolic/Diastolic Blood Pressure (mmHg) and SpO2 Blood Oxygen (%) from BLE smart watches in Python. 

Live plot of real-time HR readings using gnuplot.

Tested on a laptop running Ubuntu 18.04.2 LTS and a Rapberry Pi 3 B+ running Raspbian.

## Requirements

* Python 2.7
* [pexpect](https://pypi.org/project/pexpect/)
* [bluez](http://www.bluez.org/) (for gatttool)
* [gnuplot](http://www.gnuplot.info/)
* a Bluetooth Low Energy (BLE 4.0) USB dongle

I personally used the following two watches as a starting point, but the code can be adapted to most BLE devices with the same features after you identify the handles in which to enable notifications and activate the particular sensor. 

Watch 1 (£9.99): https://www.ebay.co.uk/itm/Bluetooth-Smart-Fit-bit-watch-Heart-Rate-Blood-Pressure-Monitor-Fitness-Tracker/392261520327?ssPageName=STRK%3AMEBIDX%3AIT&var=661217069201&_trksid=p2060353.m2749.l2649

![w1](https://user-images.githubusercontent.com/51001263/58653932-bde20d80-830e-11e9-922f-e3bbbe0c7906.jpg)

Watch 2 (£23.57): https://www.ebay.co.uk/itm/M19-Plus-Sport-Waterproof-Smart-Bluetooth-Bracelet-Calorie-Step-Counter-AC1768/163542991010?epid=21029075228&hash=item2613ec00a2:g:PowAAOSwR2ZcZULc

![w2](https://user-images.githubusercontent.com/51001263/58653933-bde20d80-830e-11e9-9e61-6fc9e54615db.jpg)

## Install
```
sudo apt-get -y install bluez gnuplot
sudo pip install pexpect
git clone https://github.com/drrobotk/BLEHEALTH
cd BLEHEALTH
sudo chmod +x liveplot.sh
sudo chmod +x health.sh
```
## Usage
***Display health stats***:
```
./health.sh w
```
***Display HR live plot***:
```
./liveplot.sh w
```
where w (=1,2) is the watch number.
## Examples

You will need 2 bluetooth dongles to run the code with two BLE watches concurrently. 

### Showing health stats (watch 1 & 2):

![code1](https://user-images.githubusercontent.com/51001263/58371825-de742700-7f0c-11e9-9d3f-d7789c5fcf6d.PNG)

### Showing a live HR plot (watch 2) and health stats (watch 1):

![code2](https://user-images.githubusercontent.com/51001263/58371826-de742700-7f0c-11e9-8afb-7fe72b3d45cc.PNG)
