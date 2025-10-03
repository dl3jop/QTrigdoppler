# Radio Configuration - ICOM IC-910H and IC-9700

This guide covers the complete setup and configuration of the ICOM IC-910H and IC-9700 transceivers with QTrigdoppler for satellite operations.

## 📡 Overview

QTrigdoppler supports the **ICOM IC-910H** and **ICOM IC-9700** exclusively for radio control via CI-V (Computer Interface V) protocol. The software provides automatic frequency tracking with doppler correction, mode switching, and VFO management for satellite operations.

## 🔧 Hardware Requirements

### Required Equipment
- **ICOM IC-910H** or **ICOM IC-9700** transceiver
- **CI-V Interface Cable** or **USB-to-Serial adapter** or **USB-A to USB-B cable**(for IC9700)
- **Computer** running QTrigdoppler

### Connection Options
1. **Direct CI-V Connection**: Use ICOM's CI-V cable to connect directly to the radio's CI-V port
2. **USB Interface**: Use a CI-V to USB adapter (recommended for modern computers)
3. **Serial Interface**: Traditional RS-232 serial connection (older computers)

## ⚙️ Radio Setup

### 1. Radio Configuration

#### CI-V Settings on Radio
1. **Access Menu**: Press `[MENU]` on your IC-910H
2. **Navigate to CI-V Settings**:
   - Find CI-V address setting (usually in the "Others" or "Interface" menu)
   - Set CI-V address to **`60`** (hex) - this is the default for IC-910H
   - Enable CI-V transceive mode for automatic frequency updates

#### Required Radio Settings
| Setting | Value | Purpose |
|---------|-------|---------|
| CI-V Address | `60` (hex) | Communication address for computer control |
| CI-V Transceive | ON | Enables bidirectional communication |
| CI-V Baud Rate | 9600 | Standard communication speed |

#### Satellite Mode Configuration
- **Enable Satellite Mode**: Press `[SAT]` button on IC-910H
- **VFO Configuration**: 
  - Main VFO (VFO-A): Downlink frequency
  - Sub VFO (VFO-B): Uplink frequency
- **Split Operation**: Automatic when in satellite mode

ToDo: describe the same proceudre for the IC-9700

### 2. Computer Interface Setup

#### Windows Setup
1. **Install Drivers**: Install appropriate drivers for your CI-V adapter
2. **Identify COM Port**: 
   - Open Device Manager
   - Look under "Ports (COM & LPT)"
   - Note the COM port number (e.g., COM1, COM3, etc.)

#### Linux Setup
1. **Check Device**: Connect adapter and run:
   ```bash
   sudo dmesg -wH
   ```
2. **Identify Port**: Look for entries like `/dev/ttyUSB0`, `/dev/ttyUSB1`, or `/dev/ttyACM0`
3. **Set Permissions**: Add your user to the dialout group:
   ```bash
   sudo usermod -a -G dialout $USER
   ```
4. **Logout/Login**: Required for permissions to take effect

## 🛠️ QTrigdoppler Configuration

### GUI Settings Interface

QTrigdoppler provides a user-friendly Settings interface accessible through the application:

1. **Open Settings Tab**: Click the `Settings` tab in the QTrigdoppler main window
2. **Locate Radio Settings**: Find the radio/ICOM configuration section within the Settings tab
3. **Configure Parameters**: Set the following values:

| Setting | GUI Label | Value | Description |
|---------|-----------|-------|-------------|
| **Radio Model** | Radio | `910` | Select IC-910H or IC-9700 from dropdown |
| **CI-V Address** | CVI Address (hex) | `60` | Enter the CI-V address (must match radio) |
| **Serial Port** | Serial Port | `COM1` (Windows) or `/dev/ttyUSB0` (Linux) | Select from dropdown or enter manually |
| **Rig Type** | Rig Type | `EU`/`US` | Select your regional variant |

4. **Apply Settings**: Click `Apply` or `Save` to store the configuration
5. **Test Connection**: The status should show radio connection status

**Note**: Changes made in the GUI Settings interface are automatically saved to the `config.ini` file.

### Configuration File Settings

Alternatively, you can directly edit your `config.ini` file in the `[icom]` section:

```ini
[icom]
# Radio configuration for Icom transceivers
radio = 910                     # ICOM IC-910H model number
cviaddress = 60                 # CI-V address (hex) - must match radio setting
fullmode = False                # Enable full mode control (recommended: False)
serialport = COM1               # Serial port (Windows: COM1, Linux: /dev/ttyUSB0)
rig_type = EU                   # Frequency range (EU/US/JP)
```

### Configuration Parameters Explained

#### `radio = 910`
- **Purpose**: Identifies the radio model
- **Value**: Always `910` for IC-910H
- **Required**: Yes

#### `cviaddress = 60`
- **Purpose**: CI-V communication address
- **Value**: Must match the address set on your IC-910H (default: 60 hex)
- **Range**: 0-255 (decimal), typically specified in hex
- **Required**: Yes

#### `serialport`
- **Windows**: `COM1`, `COM3`, `COM4`, etc.
- **Linux**: `/dev/ttyUSB0`, `/dev/ttyUSB1`, `/dev/ttyACM0`, etc.
- **Purpose**: Defines which serial port to use for CI-V communication
- **Required**: Yes

#### `rig_type = EU/US`
- **Purpose**: Sets frequency ranges and features based on regional radio variants
- **EU**: European version with TONE support
- **US**: United States version with TSQL support
- **Important**: US users must set this to `US` for proper TSQL/TONE operation

## 🎛️ Operating Modes

### Supported Modes
QTrigdoppler supports the following modes on the IC-910H and IC-9700:

| Mode | Description | Use Case |
|------|-------------|----------|
| **FM** | Frequency Modulation | FM repeater satellites, packet |
| **USB** | Upper Sideband | Linear transponder uplinks |
| **LSB** | Lower Sideband | Linear transponder downlinks |
| **CW** | Continuous Wave | CW transponder QSOs, beacon tracking |

### Automatic Mode Selection
- **FM Satellites**: Automatically selects FM mode
- **Linear Transponders**: Automatically selects USB/LSB based on frequency
- **Digital Data Modes**: Uses USB/LSB modes (IC-910H does not have separate DATA modes)

## 🔍 Troubleshooting

### Common Issues

#### "Rig not connected, switching to dummy mode"
**Causes:**
- Wrong serial port specified
- CI-V cable not connected
- Radio not powered on
- Incorrect CI-V address

**Solutions:**
1. Verify physical connections
2. Check serial port in configuration
3. Confirm CI-V address matches radio setting
4. Test with different baud rates if necessary

#### TSQL/TONE Not Working
**Cause**: Incorrect `rig_type` setting for US radios

**Solution**: 
- US users must set `rig_type = US` in configuration
- EU users should use `rig_type = EU`

#### Frequency Not Updating
**Causes:**
- CI-V transceive mode disabled on radio
- Serial communication issues
- Wrong CI-V address

**Solutions:**
1. Enable CI-V transceive on IC-910H
2. Check cable connections
3. Verify CI-V address configuration

### Testing Connection

#### Manual Test
1. Start QTrigdoppler
2. Check status bar for "Connected" indicator
3. Try changing frequency manually
4. Verify radio frequency changes accordingly

#### Log File Analysis
Check `logs/qtrigdoppler.log` for connection details:
```
INFO: Radio connected successfully
INFO: CI-V communication established
```

## 🎯 Best Practices

### Setup Recommendations
1. **Use Quality Cables**: Invest in good CI-V interface cables
2. **Stable Power**: Ensure radio has stable power supply
3. **Ground Loops**: Avoid ground loops between computer and radio
4. **Cable Length**: Keep CI-V cables as short as practical

### Operating Tips
1. **Manual Backup**: Learn manual frequency control as backup
2. **Pre-check**: Test radio communication before important passes
3. **Monitoring**: Keep radio display visible to monitor frequency changes

### Performance Optimization
1. **Doppler Thresholds**: Adjust thresholds based on your operating preferences
2. **Update Rate**: CI-V updates occur automatically during satellite passes

## 📚 Advanced Configuration

### Custom Offset Profiles
Configure satellite-specific frequency offsets in the `[offset_profiles]` section:

```ini
[offset_profiles]
satoffset1 = IO-117,Digipeater,-550,-550
satoffset2 = MESAT-1,TPX,1400,0
satoffset3 = JO-97,SSB Transponder,0,-2000
```

## 🆘 Support Resources

### Documentation Links
- **[Configuration Guide](configuration.md)** - Complete config.ini reference
- **[Frequency Control](frequency-control.md)** - Doppler correction details
- **[Main README](../README.md)** - Project overview

### Technical Support
- **Log Files**: Always check `logs/qtrigdoppler.log` for detailed error information
- **Community Forums**: Amateur radio satellite operation communities
- **Hardware Manuals**: Refer to IC-910H or IC-9700 operating manual for radio-specific questions

---

**Document Version**: 1.1  
**Last Updated**: October 2025  
**Supported Radios**: ICOM IC-910H, ICOM IC-9700 
