# QTRigdoppler


<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/dl3jop/QTrigdoppler/blob/main/images/mainWindow.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/dl3jop/QTrigdoppler/blob/main/images/mainWindow.png">
 <img alt="Shows QTRigdoppler GUI." src="https://github.com/dl3jop/QTrigdoppler/blob/main/images/mainWindow.png">
</picture> 

## 🧠 What QTRigdoppler does

QTRigdoppler keeps track of satellites and their transponders. It handles multiple tasks: <br/>
 1) Tracking satellites and calculating the doppler shifts of their used frequencies.<br/>
 2) Update VFOs of a connected ICOM IC-910 (and IC-9700) for fully automatic frequency tracking.<br/>
 3) Depending on the transponder type: FM/SSB Voice or FM/SSB Data, the software determines the best tracking approach.<br/>
 4) Rotators can be connected to sync their position with the current satellite.<br/>
 5) A websocket option enable integration into software like [Zenith](https://github.com/magicbug/Zenith).<br/>
 6) There is an optional map you can use to plot the satellites position<br/>

## 🌓 Choose your style
QTRigdoppler now comes with many themes you can choose from. A brief selection of some themes:
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/dl3jop/QTrigdoppler/blob/main/images/themes.jpg">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/dl3jop/QTrigdoppler/blob/main/images/themes.jpg">
 <img alt="Shows different QTRigdoppler GUI themes." src="https://github.com/dl3jop/QTrigdoppler/blob/main/images/themes.jpg">
</picture>
    
# 📚 Documentation

For detailed setup and usage instructions, see the [help documentation](help/):
- **[Getting Started Guide](getting-started.md)** - Complete setup and first-use tutorial for new users
- **[Configuration Guide](help/configuration.md)** - Complete config.ini reference and setup
- **[Radio Configuration](radio-configuration.md)** - Complete guide to setup your ICOM IC-910H or IC-9700 for operation
- **[Frequency Control](help/frequency-control.md)** - Doppler correction, manual control, and advanced frequency features
- **[Remote Operation](help/remote-operation.md)** - Web-based remote control systems  
- **[Cloudlog Integration](help/cloudlog-integration.md)** - Automatic logbook integration with Cloudlog/Wavelog
- **[Pass Recording](help/pass-recording.md)** - Automatic audio recording during satellite passes
- **[GPS Integration](help/gps-integration.md)** - GPS-based automatic location determination
- **[Rotator Setup](help/rotator-setup.md)** - Antenna rotator configuration and operation
- **[Keyboard Shortcuts](help/keyboard-shortcuts.md)** - Keyboard shortcuts and accessibility features
- **[Developer Information](help/development.md)** - Notes for developers


# 📋🔄⏳ Changelog
- Based on K8DP Doug Papay rigdoppler (@K8DP_Doug)  
- Adapted by EA4HCF Pedro Cabrera (@PCabreraCamara)  
- Extended and modified by DL3JOP Joshua Petry (@dl3jop)

Contributions in this repo by:
- Joshua, DL3JOP
- Peter, 2M0SQL
 
DL3JOP modifications:
- Removed hamlib
- Support for IC-910H and IC-9700 
- Implemented transponder selection, auto switch between split mode for V/V & U/U packet and sat mode for V/U,U/V
- Implemented doppler correction threshold and subtone control
- Various smaller changes and additions
- Added binaries

2M0SQL Modifications:
- Changed to PySide
- Implemented Websocket support, Cloudlog/Wavelog integration, pass recording, gps position polling, auto TLE updates
- Added satellite database (doppler.sqf) downloading with merge or replace options from oscarwatch.org.
- Added frequency pause/resume feature: pause frequency updates while keeping rotator tracking for manual frequency control on newer satellites.
- Added help files

Feel free to report bugs or submit pull requests with your additions to the codebase!
    
    
# 🎯 Roadmap
  - Adding support for FT-8xx radios. Same approach: serial driver, although that will add additional reworks in the doppler tracking loop to account for two radios
  - Separate GUI and tracking class
  - Refactor tracking loop:
    - no global F0/I0 variables
