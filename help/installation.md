# 📥💻 Installation and Usage
## Recommended way
You can run QTRigdoppler as a pre-compiled binary available from the release section. The binary should work on all major linux distributions. Please report any troubles you might encounter.
To make this possible, the binary contains a full packed python environment which decreases its speed on startup.<br/>

## From source
As an alternative, you can install it yourself following the installation guides for Ubuntu or Manjaro.


### Install on Ubuntu 24.10 or higher
 1) It is assumed that you use Ubuntu 24.10 (or newer) or a derivative of it
 2) Open a terminal
 3) Update package sources by:<br/> `sudo apt update`
 5) Install required packages:<br/> `sudo apt install git python3 python3-pyside6.qtcore python3-pyside6.qtgui python3-pyside6.qtwidgets python3-pyside6.qtuitools python3-qt-material python3-ephem python3-numpy`
 6) Add your user to the dialout group to access the serial port by:<br/> `sudo adduser [username, remove brackets] dialout` e.g.: `sudo adduser dl3jop dialout`<br/>
 6.1) Restart you computer for all changes to take effect, than repeat step 2)<br/>
 7) Get the software by:<br/> `git clone https://github.com/dl3jop/QTrigdoppler.git`
 8) Enter software directory by:<br/> `cd QTrigdoppler`
 9) Start using:<br/> `python3 QTrigdoppler.py`
 10) For every startup from now on repeat step 2,7 and 8 or create a starter in the start menu


### Install on Arch or derivatives (e.g.: Manjaro)
The installation process is similar to the one on Ubuntu:<br/>
`sudo pacman -Syu`\
 `sudo pacman -S git python pyside6 python-qt-material python-ephem python-numpy`\
 `sudo usermod -aG uucp [username, remove brackets]`\
 `git clone https://github.com/dl3jop/QTrigdoppler.git`\
 `python3 QTrigdoppler.py`
 
### Install on systems using pip
For system using pip as a python package management you need to install the dependencies using the provided requirements.txt in the repo after cloning it:
`pip install -r /path/to/requirements.txt`
 
# After installtion steps:
After installation/download you need to adjust the configuration in the `Settings` Tab to suit your needs. If you have a US configured IC-910 you need to change the rig type from `EU` to `US` otherwise TSQL or TONE won't work
You might also need to change the serial port of your CI-V to serial adapter. The easiest solution is to run `sudo dmesg -wH` in a terminal and plugging in your serial adpter to get the serial port name.
Port names might be `/dev/ttyUSB0`, `/dev/ttyUSB1` .... or `/dev/tty/ACM0` ...
For additional information, please have a look in the corresponding readme files
