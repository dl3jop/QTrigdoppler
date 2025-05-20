# QTRigdoppler


<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/dl3jop/QTrigdoppler/blob/main/images/mainWindow.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/dl3jop/QTrigdoppler/blob/main/images/mainWindow.png">
 <img alt="Shows QTRigDoppler GUI." src="https://github.com/dl3jop/QTrigdoppler/blob/main/images/mainWindow.png">
</picture> 

## 📌 QTRigdoppler features doppler shift control for ICOM radios

Based on K8DP Doug Papay rigdoppler (@K8DP_Doug)  
Adapted by EA4HCF Pedro Cabrera (@PCabreraCamara)  
Extended and modified by DL3JOP Joshua Petry (@dl3jop)
Contributions in this repo by:
Joshua, DL3JOP
Peter, 2M0SQL
 
## 🧠 What QTRigdoppler does

QTRigdoppler keeps track of satellites and their transponders. It handles mutliple tasks: <br/>
 1) Tracking satellites and calculating the doppler shifts of their used frequencies.<br/>
 2) Update VFOs of a connected ICOM IC-910 (and IC-9700) for fully automatic frequency tracking.<br/>
 3) Depending on the transpoder type: FM/SSB Voice or FM/SSB Data, the software determines the best tracking approch.<br/>
 4) Rotators can be connected to sync their postion with the current satellite.<br/>
 5) A websocket option enable integration into software like [Zenith](https://github.com/magicbug/Zenith).<br/>
 6) There is an optional map you can use to plot the satellites position<br/>
 
## 📥💻 Installation and Usage

You can run QTRigdoppler as a pre-compiled binary available from the release section. The binary should work on all major Linux dsitributions. Please report any troubles you might encounter.
To make this possible, the binary conatins a full packed python environment which decreases its speed on startup.<br/>

As an alternative, you can install it yourself follwing the installation guides for Ubuntu or Manjaro.

After installation/download you need to adjust the configuration inthe `Settings` Tab to suit your needs. If you have a US configured IC-910 you need to change the rig type from `EU` to `US` otherwise TSL or TONE won't work
You might also need to change the serial port of your CI-V to serial adapter. The easiest solution is to run `sudo dmesg -wH` in a terminal and plugging in your serial adpter to get the serial port name.
Portnames might be `/dev/ttyUSB0`, `/dev/ttyUSB1` .... or `/dev/tty/ACM0` ...
If you like, you can also edit the `config.ini` to access developer or more advanced options.

### Install on Ubuntu 24.10 or higher
 1) It is assumed that you use Ubuntu 24.10 (or newer) or a derivative of it
 2) Open a terminal
 3) Update package sources by:<br/> `sudo apt update`
 5) Install required packages:<br/> `sudo apt install git python3 python3-pyqt5 python3-qt-material python3-ephem python3-numpy`
 6) Add your user to the dialout group to access the serial port by:<br/> `sudo adduser [username, remove brackets] dialout` e.g.: `sudo adduser dl3jop dialout`<br/>
 6.1) Restart you computer for all changes to take effect, than repeat step 2)<br/>
 7) Get the software by:<br/> `git clone https://github.com/dl3jop/QTrigdoppler.git`
 8) Enter software directory by:<br/> `cd QTrigdoppler`
 9) Start using:<br/> `python3 QTrigdoppler.py`
 10) For every startup from now on repeat step 2,7 and 8 or create a starter in the start menu

 TLDR:\
 `sudo apt update`\
 `sudo apt install git python3 python3-pyqt5 python3-qt-material python3-ephem python3-numpy`\
 `sudo adduser [username, remove brackets] dialout`\
 `git clone https://github.com/dl3jop/QTrigdoppler.git`\
 `python3 QTrigdoppler.py`

### Install on Arch or derivatives (e.g.: Manjaro)
The installation process is similar to the one on Ubuntu:<br/>
`sudo pacman -Syu`\
 `sudo pacman -S git python python-pyqt5 python-qt-material python-ephem python-numpy`\
 `sudo usermod -aG uucp [username, remove brackets]`\
 `git clone https://github.com/dl3jop/QTrigdoppler.git`\
 `python3 QTrigdoppler.py`

#### 🗺️ Requirements for using the map:  
Currently, using the map is not advised due to bad perfomance. If you choose to try it, you'll need these additional python packages:<br/>
`matplotlib`<br/>
`cartopy`<br/>
`pyproj`<br/>

# 📋🔄⏳ Changelog
DL3JOP modifications: <br/>
    1) Removed hamlib<br/>
    2) support for IC-910H by direct serial communication, IC-9700 should work as well (not yet tested)<br/>
    3) Implemented transponder selection<br/>
    4) Implemented correct switch between Split mode for V/V & U/U packet and satmode for V/U,U/V<br/>
    5) Implemented doppler correction threshold<br/>
    6) Added SubTone control<br/>
    7) Various smaller changes and additions<br/>
    8) Added binaries

2M0SQL Modifications:<br>
    1) Changed to PySide<br/>
    2) Implemented Websocket features using Flask and SocketIO<br/>
    3) Added Cloudlog/Wavelog integration: automatic logging of frequency and satellite info via Cloudlog API, configurable in config.ini.<br/>
    4) Added ability to automatically record satellite passes to .wav files.
    5) Added support to use USB / Serial GPS units to get location position.
    
    
# 🎯 Roadmap
  - Adding support for IC-9700 (should be easy as it uses nearly the same comands as the IC-910H)
  - Adding support for FT-8xx radios. Same approch: serial driver, although that will add additonal reworks in the doppler tracking loop to account for two radios
  - Building a much nicer GUI
  - Separate GUI and tracking class
  - Refactor tracking loop:
    - no global F0/I0 variables, more abstracted methods to allow eaier implementation of other radios
    
# 🛠️ Advanced information
    
## Remote Server Configuration

QTrigdoppler includes a remote server component built with Node.js that enables remote control and integration with other applications. Here's how to set it up:

### Prerequisites

1. Install Node.js from [https://nodejs.org/](https://nodejs.org/) or using your system's package manager
2. Verify the installation by running:
   ```bash
   node --version
   ```

### Installation

1. Navigate to the QTrigdoppler directory
2. Install the required Node.js dependencies:
   ```bash
   npm install express socket.io ini
   ```

### Configuration

The remote server can be configured through the `config.ini` file under the `[remote_server]` section:

```ini
[remote_server]
enable = True
url = http://localhost:5001
port = 5001
debug = False
```

- `enable`: Set to `True` to enable the remote server
- `url`: The URL where the server will be accessible
- `port`: The port number for the server (default: 5001)
- `debug`: Set to `True` for additional debug logging

### Starting the Server

To start the remote server:
```bash
node remote_server.js
```

The server will start on the configured port (default: 5001) and be ready to accept connections from QTrigdoppler clients.

### Features

The remote server provides:
- WebSocket interface for real-time updates
- Cross-origin resource sharing (CORS) support
- Integration capabilities with other applications
- Tracking of satellite and transponder data
- Real-time doppler shift information
- Rotator control support (when enabled)

### Integration

Other applications can connect to the remote server using WebSocket or HTTP protocols. The server exposes various endpoints and events for satellite tracking, frequency control, and rotator management.

## Web API and WebSocket Usage
### Configuration
The web API can be configured in the `config.ini` file under the `[web_api]` section:

```ini
[web_api]
enabled = True
port = 5000
debug = False
```

- `enabled`: Set to `True` to enable the web API, or `False` to disable it
- `port`: The TCP port the web server will listen on (default: 5000)
- `debug`: Set to `True` to enable debug output, or `False` for normal operation

### Usage
When enabled, the web API server starts automatically with QTrigdoppler. You can access the web interface by opening a web browser and navigating to:

```
http://localhost:5000/
```

(Replace `localhost` with the IP address of the computer running QTrigdoppler if accessing from another device)

The web interface allows you to:
- Start/stop satellite tracking
- Select different satellites and transponders
- Set subtones
- Adjust RX offset

## WebSocket API (for Developers)

The web API uses Flask-SocketIO for real-time communication. You can integrate it with your own applications by connecting to the Socket.IO endpoints. All events are real-time and changes are reflected immediately in the desktop app and all connected clients.

### Connecting to the Server
- By default, the server runs on port 5000.
- To connect from another device on your local network, use:
  
  `http://<your-computer-ip>:5000`
  
  (e.g., `http://192.168.1.100:5000`)

### Available WebSocket Events

| Event                | Parameters                        | Description                                 |
|----------------------|------------------------------------|---------------------------------------------|
| `get_status`         | none                               | Request current status and settings         |
| `get_satellite_list` | none                               | Request list of available satellites        |
| `select_satellite`   | `{ satellite: <name> }`            | Select a satellite by name                  |
| `get_transponder_list` | `{ satellite: <name> }`          | Get transponders for a satellite            |
| `select_transponder` | `{ transponder: <name> }`          | Select a transponder by name                |
| `set_subtone`        | `{ subtone: <value> }`             | Set the radio subtone (e.g., 'None', '67 Hz') |
| `set_rx_offset`      | `{ offset: <integer> }`            | Set RX frequency offset in Hz               |
| `start_tracking`     | none                               | Start satellite tracking                    |
| `stop_tracking`      | none                               | Stop satellite tracking                     |
| `debug_main_window`  | none                               | Get debug info about the main window        |

#### Server → Client Events

| Event                | Data Example                      | Description                                 |
|----------------------|------------------------------------|---------------------------------------------|
| `status`             | `{ tracking, satellite, ... }`     | Current status and settings                 |
| `satellite_list`     | `{ satellites: [...], current }`   | List of satellites and current selection    |
| `transponder_list`   | `{ transponders: [...], current }` | List of transponders and current selection  |
| `debug_info`         | `{ attributes, ... }`              | Debug information about the main window     |

### Example Usage (JavaScript)

```js
const socket = io('http://192.168.1.100:5000');

// Request current status
socket.emit('get_status');

// Select a satellite
socket.emit('select_satellite', { satellite: 'ISS' });

// Set RX offset
socket.emit('set_rx_offset', { offset: 100 });

// Listen for status updates
socket.on('status', (data) => {
    console.log('Status:', data);
});
```

- The web client (`web_api_client.html`) demonstrates all available features and can be used as a reference.
- The server must be running and accessible from your network for remote clients to connect.

For more advanced integration, see the code in `web_api_client.html` or contact the project maintainers.


## Cloudlog/Wavelog Integration
QTrigdoppler can automatically send frequency and satellite information to [Cloudlog](https://cloudlog.co.uk/) or [Wavelog](https://www.wavelog.org/)  via its API.

### Configuration

Add or update the `[Cloudlog]` section in your `config.ini`:

```ini
[Cloudlog]
enabled = True
api_key = YOUR_API_KEY
url = https://your.cloudlog.site
```

- `enabled`: Set to `True` to enable Cloudlog/Wavelog logging, or `False` to disable it.
- `api_key`: Your Cloudlog/Wavelog API key.
- `url`: The base URL of your Cloudlog7Wavelog installation (e.g., `https://your.cloudlog.site`). The API endpoint used is `/index.php/api/radio`.

### How it Works

- When you select a new transponder, QTrigdoppler will send the current TX and RX frequencies, modes, and satellite name to Cloudlog.
- If the mode is `FMN`, it will be sent as `FM` to Cloudlog/Wavelog.
- All Cloudlog/wavelog API activity and errors are logged to the console.

## 🛠️ Compile using pyinstaller

`pyinstaller --onefile QTrigdoppler.py --exclude PyQt6 --splash images/splash.jpg`