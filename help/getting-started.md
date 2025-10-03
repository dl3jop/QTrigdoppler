# Getting Started with QTrigdoppler

Welcome to QTrigdoppler! This comprehensive guide will take you from installation to your first successful satellite contact.

## 🎯 What is QTrigdoppler?

QTrigdoppler is a powerful satellite tracking application that automates frequency control for your ICOM IC-910H or IC-9700 radio during satellite passes. It handles doppler shift correction, transponder selection, and can control antenna rotators for a complete automated satellite station.

### Key Features
- **Automatic Doppler Correction**: Real-time frequency tracking during satellite passes
- **Transponder Management**: Smart selection of satellite transponders
- **Rotator Control**: Automated antenna pointing
- **Remote Operation**: Web-based control from anywhere
- **Pass Recording**: Automatic audio recording of satellite contacts
- **GPS Integration**: Automatic location determination
- **Cloudlog/Wavelog Integration**: Automatic logging to your online logbook

## 📦 Installation

### Option 1: Pre-compiled Binary (Recommended for Most Users)

1. **Download**: Get the latest release from the [GitHub releases page](https://github.com/dl3jop/QTrigdoppler/releases)
2. **Extract**: Unzip the downloaded file to your desired location
3. **Run**: Execute `QTrigdoppler.exe` (Windows) or the binary file (Linux)

**Note**: The binary includes a complete Python environment, so startup may be slower than a manual installation.

### Option 2: Manual Installation (Ubuntu/Debian)

```bash
# Update package sources
sudo apt update

# Install required packages
sudo apt install git python3 python3-pyside6.qtcore python3-pyside6.qtgui python3-pyside6.qtwidgets python3-pyside6.qtuitools python3-qt-material python3-ephem python3-numpy

# Add user to dialout group for serial port access
sudo adduser $USER dialout

# Clone the repository
git clone https://github.com/dl3jop/QTrigdoppler.git
cd QTrigdoppler

# Start the application
python3 QTrigdoppler.py
```

**Important**: Log out and back in after adding yourself to the dialout group.

### Option 3: Manual Installation (Arch/Manjaro)

```bash
# Update system
sudo pacman -Syu

# Install required packages
sudo pacman -S git python python-pyqt5 python-qt-material python-ephem python-numpy

# Add user to uucp group for serial port access
sudo usermod -aG uucp $USER

# Clone and run
git clone https://github.com/dl3jop/QTrigdoppler.git
cd QTrigdoppler
python3 QTrigdoppler.py
```
### Note: Install on systems using pip
For system using pip as a python package management you need to install the dependencies using the provided requirements.txt in the repository after cloning it:
`pip install -r /path/to/requirements.txt`

## 🔧 Initial Setup

### Step 1: First Launch

1. **Start QTrigdoppler**: Launch the application
2. **Initial Screen**: You'll see the main interface with empty satellite lists
3. **Settings Tab**: Click on the **Settings** tab for configuration

### Step 2: Configure Your Location (QTH)

Your location is essential for accurate satellite tracking calculations.

1. **Open Settings Tab**: Click **Settings** in the main window
2. **Find Location Settings**: Locate the QTH (location) section
3. **Enter Coordinates**:
   - **Latitude**: Your latitude in decimal degrees (e.g., `40.7128`)
   - **Longitude**: Your longitude in decimal degrees (e.g., `-74.0060`) 
   - **Altitude**: Your elevation in meters above sea level (e.g., `100`)

**Finding Your Coordinates**:
- Use Google Maps: Right-click your location and select coordinates
- Use GPS device or smartphone GPS app
- Use online coordinate conversion tools for gridsquare to decimal degrees

### Step 3: Configure Your Radio (IC-910H)

#### Hardware Setup
1. **Connect CI-V Interface**: Connect your CI-V cable or USB adapter
2. **Power On Radio**: Ensure your IC-910H is powered and functioning
3. **Set Radio CI-V Address**: 
   - Press `[MENU]` on IC-910H
   - Set CI-V address to `60` (hex) - this is the default
   - Enable CI-V transceive mode

#### Software Configuration
1. **In Settings Tab**: Find the radio/ICOM configuration section
2. **Configure Parameters**:
   - **Radio**: Set to `910` (IC-910H)
   - **CVI Address (hex)**: Set to `60` (must match radio setting)
   - **Serial Port**: Select your CI-V port (e.g., `COM1`, `/dev/ttyUSB0`)
   - **Rig Type**: Choose `EU`, `US`, or `JP` based on your radio variant
   - **Full Mode Control**: Leave unchecked for most users

3. **Test Connection**: Save settings and check the status bar for "Connected" indicator

**US Users**: If you have a US-configured IC-910H, you MUST set Rig Type to `US` for proper TSQL/TONE operation.

### Step 4: Update Satellite Data

Fresh satellite data is crucial for accurate tracking.

1. **Update TLE Data**: 
   - Click **"Update Satellite Database"** button in Settings
   - This downloads current Two-Line Element (TLE) data
   - Wait for the update to complete

2. **Update Frequency Data**:
   - Click **"Update doppler.sqf"** to get latest transponder frequencies
   - Choose **Merge** to add new satellites or **Replace** to completely refresh

3. **Verify Data**: Check that satellites appear in the main satellite list

## 🛰️ Your First Satellite Pass

### Step 1: Select a Satellite

1. **Main Window**: Return to the main tracking view
2. **Choose Satellite**: Select an active satellite from the list
   - **Beginner Tip**: Start with FM satellites like `SO-50` or `PO-101`
   - **Look for High Passes**: Choose satellites with maximum elevation >20°

3. **Select Transponder**: Choose the appropriate transponder for your intended operation

### Step 2: Prepare for the Pass

1. **Radio Setup**:
   - Verify radio is connected (check status bar)
   - Ensure appropriate antennas are connected
   - Set your radio to the correct power level

2. **Monitor Tracking**:
   - Watch the frequency displays for downlink/uplink
   - Observe the doppler correction values
   - Check the satellite elevation and azimuth

### Step 3: During the Pass

1. **Automatic Operation**:
   - QTrigdoppler automatically adjusts frequencies for doppler shift
   - Rotator (if configured) automatically points antenna
   - Focus on making contacts!

2. **Manual Adjustments**:
   - Use the frequency offset controls for fine-tuning
   - Adjust power as needed for the pass
   - Monitor for other stations

### Step 4: After the Pass

1. **Logging**: If Cloudlog/Wavelog integration is enabled, contacts are automatically logged
2. **Recordings**: If pass recording is enabled, audio files are automatically saved
3. **Next Pass**: Select the next satellite for tracking

## 🔍 Essential Features Overview

### Frequency Control
- **Automatic Doppler Correction**: Tracks satellite movement in real-time
- **Manual Override**: Pause automatic updates for manual tuning
- **Offset Controls**: Fine-tune frequencies during passes
- **Mode Selection**: Automatic USB/LSB/FM mode switching

### Transponder Selection
- **Automatic Selection**: Choose optimal transponder based on current time and satellite position
- **Manual Override**: Select specific transponders for targeted operation
- **Mode Awareness**: Different tracking strategies for FM vs Linear transponders

### Interface Themes
- **Multiple Themes**: Choose from various color schemes and styles
- **Dark/Light Modes**: Optimize for your operating environment
- **Customization**: Adjust interface to your preferences

## 🎛️ Essential Settings

### Doppler Thresholds
Control how sensitive frequency tracking is:
- **FM Satellites**: 200 Hz threshold (less frequent updates)
- **Linear Transponders**: 50 Hz threshold (more precise tracking)

### Auto-Updates
- **TLE Updates**: Automatically refresh satellite orbital data
- **Frequency Updates**: Keep transponder information current
- **Startup Updates**: Update data when application starts

### Feature Enablement
- **GPS Integration**: Automatic location determination
- **Remote Access**: Web-based control interface
- **Pass Recording**: Automatic audio recording
- **Cloudlog/Wavelog Integration**: Automatic contact logging

## 🚨 Troubleshooting Common Issues

### Radio Not Connecting
**Symptoms**: "Rig not connected, switching to dummy mode"

**Solutions**:
1. Check physical CI-V cable connections
2. Verify correct serial port in settings
3. Confirm CI-V address matches radio (typically 60 hex)
4. Ensure radio is powered on and CI-V is enabled

### No Satellites Showing
**Symptoms**: Empty satellite list

**Solutions**:
1. Update satellite database using the "Update Satellite Database" button
2. Check internet connection for TLE downloads
3. Verify location settings are correct
4. Restart application after updates

### TSQL/Tone Not Working (US Users)
**Symptoms**: Tone settings not functioning on US IC-910H

**Solution**: Set `Rig Type` to `US` in radio settings

### Frequencies Not Updating
**Symptoms**: Radio frequency remains static during passes

**Solutions**:
1. Verify radio connection status
2. Check that CI-V transceive is enabled on radio
3. Ensure correct transponder is selected
4. Verify satellite is actually above horizon

### Poor Tracking Performance
**Symptoms**: Inaccurate frequency tracking or jumpy behavior

**Solutions**:
1. Verify location coordinates are accurate
2. Update satellite TLE data
3. Check system clock accuracy
4. Consider enabling predictive doppler correction

## 📚 Next Steps

### Essential Documentation
Once you have the basics working, explore these guides for enhanced functionality:

- **[Radio Configuration](radio-configuration.md)** - Detailed IC-910H setup and advanced features
- **[Frequency Control](frequency-control.md)** - Advanced doppler correction and manual control
- **[Rotator Setup](rotator-setup.md)** - Automated antenna pointing
- **[Remote Operation](remote-operation.md)** - Control your station from anywhere
- **[Pass Recording](pass-recording.md)** - Automatic audio recording setup
- **[GPS Integration](gps-integration.md)** - Automatic location determination
- **[Cloudlog/Wavelog Integration](cloudlog-integration.md)** - Automatic logging to online logbooks
- **[Keyboard Shortcuts](keyboard-shortcuts.md)** - Efficient operation tips

### Advanced Features
As you become comfortable with basic operation, consider exploring:

1. **Rotator Control**: Automate antenna pointing for improved signal strength
2. **Remote Operation**: Access your station from anywhere via web interface
3. **Pass Recording**: Automatically record interesting passes for later analysis
4. **GPS Integration**: Perfect for portable/mobile operations
5. **Multi-Transponder Operation**: Advanced strategies for busy satellites

### Best Practices
- **Regular Updates**: Keep TLE and frequency data current
- **Backup Configuration**: Save your `config.ini` file settings
- **Monitor Performance**: Watch for changes in tracking accuracy
- **Community Engagement**: Join amateur radio satellite forums for tips and assistance

## 🆘 Getting Help

### Built-in Resources
- **Application Logs**: Check `logs/qtrigdoppler.log` for detailed system information
- **Status Indicators**: Monitor connection and tracking status in the interface
- **Help Documentation**: Complete guides available in the help/ directory

### Community Support
- **Amateur Radio Forums**: Participate in satellite operation discussions
- **QTrigdoppler Issues**: Report bugs or request features on GitHub
- **Local Clubs**: Connect with other satellite operators in your area

### Technical Support
- **Log Files**: Always check application logs first for error details
- **Configuration**: Review settings against working examples
- **Hardware**: Verify all physical connections and settings

---

**Welcome to the exciting world of amateur radio satellite communications!** 

QTrigdoppler automates the technical complexity so you can focus on making contacts and enjoying the hobby. Start with simple FM satellites, master the basics, then gradually explore more advanced features and satellite modes.

**Document Version**: 1.1  
**Last Updated**: October 2025  
**Supported Hardware**: ICOM IC-910H, IC-9700H
