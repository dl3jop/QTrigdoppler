# Frequency Control Guide

Complete guide to frequency management and doppler correction in QTRigdoppler.

## 📡 Overview

QTRigdoppler provides sophisticated frequency control features to handle doppler shift correction for satellite communications. This includes automatic tracking, manual control options, and advanced predictive algorithms.

### Supported Features
- **Automatic Doppler Correction**: Real-time frequency adjustment for satellite movement
- **Manual Frequency Control**: Pause automatic updates while maintaining rotator tracking
- **Predictive Doppler**: Advanced algorithms for smooth tracking around TCA
- **Geographic Optimization**: Settings optimized for different latitudes
- **Mode-Specific Handling**: Different strategies for FM vs SSB/Linear satellites

## ⚙️ Configuration

### Basic Frequency Settings

Edit your `config.ini` file and locate the `[satellite]` section:

```ini
[satellite]
doppler_threshold_fm = 200           # FM mode threshold in Hz
doppler_threshold_linear = 50        # Linear transponder threshold in Hz  
predictive_doppler = True            # Enable predictive algorithms
```

### Doppler Thresholds

| Satellite Type | Default Threshold | Purpose |
|---------------|-------------------|---------|
| **FM** | 200 Hz | Larger threshold for less frequent updates |
| **Linear** (SSB/CW) | 50 Hz | Smaller threshold for precise tracking |
| **Data** | 0 Hz | Update on every change |

### Predictive Doppler

The adaptive prediction algorithm is now recommended for most users, as it improves tracking accuracy during periods of rapid doppler shift changes, which are common for LEO satellites. It is particularly effective for high-latitude locations.

To enable it, set the following in your `config.ini`:
```ini
predictive_doppler = True
```

## 🎛️ Manual Frequency Control

For newer satellites that require manual frequency tuning, you can pause automatic frequency updates while keeping rotator tracking active.

### Requirements
- Rotator system must be enabled
- Currently tracking a satellite
- Available in both desktop and web interfaces

### How to Use

1. **Start Normal Tracking**: Begin tracking as usual with both frequency and rotator control
2. **Pause Frequency Updates**: Click the frequency toggle button or press **F**
3. **Manual Tuning**: Manually adjust your radio frequency as needed
4. **Rotator Continues**: The rotator continues to track the satellite automatically
5. **Resume When Needed**: Press **F** or click the toggle button again to return to automatic frequency control

### Controls

| Method | Action | Notes |
|--------|--------|-------|
| **Desktop Button** | Click "Pause/Resume Frequency Updates" | Button text changes based on current state |
| **Keyboard Shortcut** | Press **F** | Toggles between pause/resume |
| **Web Interface** | Click frequency toggle button | Available in remote control interface |

## 📊 RX Offset Control

QTRigdoppler provides a built-in **RX Offset** control in the main GUI for fine-tuning receive frequencies.

### Using RX Offset

The RX Offset feature allows you to add a fixed frequency offset to the calculated doppler-corrected frequency:

1. **Location**: RX Offset control is in the main window interface
2. **Range**: Configurable offset in Hz (positive or negative)
3. **Real-time**: Changes apply immediately to the receive frequency
4. **Independent**: Works with both automatic and manual frequency control modes

### Common Use Cases

- **Fine-tuning for voice quality** on SSB satellites
- **Compensating for transponder frequency errors** 
- **Adjusting for local oscillator drift** in your radio
- **Optimizing for weak signal conditions**
- **Correcting for antenna/feedline frequency response**

### RX Offset vs Manual Control

| Feature | RX Offset | Manual Frequency Control |
|---------|-----------|-------------------------|
| **Purpose** | Fine-tune calculated frequency | Complete manual frequency control |
| **Scope** | Adds fixed offset to automatic calculation | Pauses all automatic updates |
| **Rotator** | Continues automatic tracking | Continues automatic tracking |
| **Use Case** | Small corrections to doppler calculation | Complete manual operation |
| **Range** | Limited offset range (configurable) | Full manual radio control |

### Best Practices

- **Start small**: Try ±100-500 Hz offsets first
- **Voice optimization**: Adjust offset for best voice intelligibility  
- **Save settings**: Useful offsets can be stored for specific satellites
- **Combine with manual control**: Use offset for fine-tuning during manual frequency periods

### Status Indicators

- **Button Text**: Shows next action ("Pause" or "Resume")
- **Log Messages**: Detailed status in application logs
- **Web Status**: Real-time updates across all connected clients

## 🌍 Geographic Considerations

### Latitude Effects on Doppler

**High Latitude Locations** (>55°N):
- Steeper satellite passes
- More rapid doppler changes at TCA
- **Recommended**: Enable predictive doppler
- **Higher rate limits**: Better handling of rapid changes

**Mid-to-Low Latitude Locations** (<55°N):
- Shallower satellite passes  
- Gentler doppler curves
- **Recommended**: Standard settings often sufficient
- **Standard rate limits**: Adequate for typical pass geometry

### TCA (Time of Closest Approach) Handling

Around TCA, doppler changes can be very rapid:

- **Predictive algorithms** help smooth tracking
- **Rate limiting** prevents frequency jumps
- **Voice quality** may be affected on SSB satellites near TCA
- **Manual control** allows fine-tuning during critical periods

## 🔧 Advanced Settings

### Rate Limiting

The system automatically limits rapid frequency changes:

| Satellite Type | Rate Limit | Behavior |
|---------------|------------|----------|
| **Linear** (USB/LSB/CW) | 2000 Hz/sec | Caps extreme changes, continues tracking |
| **FM** | 500 Hz/sec | Moderate limiting for stability |

### Predictive Timing

When predictive doppler is enabled, the algorithm adaptively changes the prediction time based on the rate of doppler shift change:

| Doppler Rate | Prediction Time | Use Case |
|-------------|----------------|----------|
| **> 60 Hz/s** | 500ms | Very rapid change (steep passes, near TCA) |
| **> 30 Hz/s** | 350ms | Moderate rapid change |
| **> 10 Hz/s** | 250ms | Normal rapid change |
| **< 10 Hz/s** | 150ms | Slow change |

## 🎙️ Voice Quality Optimization

### SSB Voice Satellites

For optimal voice quality on SSB satellites:

1. **Monitor around TCA**: Voice may sound off-pitch ±2-3 minutes around TCA
2. **Manual Control Option**: Use manual frequency control during TCA periods
3. **Predictive Settings**: Consider disabling predictive doppler if voice quality is critical
4. **Fine Tuning**: Manual adjustment may be needed for best voice intelligibility

### FM Voice Satellites

FM satellites typically have excellent voice quality with automatic tracking:
- Larger frequency tolerance
- Less sensitive to small doppler errors
- Automatic tracking works well throughout pass

## 🌐 Web API Integration

Remote frequency control is available via web interface and API:

### Available Commands
- `pause_frequency_updates`: Pause automatic frequency correction
- `resume_frequency_updates`: Resume automatic frequency correction
- Status updates broadcast to all connected clients

### Integration Examples
- Remote station control
- Contest/DXpedition operation
- Multi-operator setups
- Automated logging systems

## 📚 Related Documentation

- **[Rotator Setup](rotator-setup.md)** - Hardware setup (rotator required for manual frequency control)
- **[Configuration Guide](configuration.md)** - Complete configuration reference
- **[Remote Operation](remote-operation.md)** - Web-based remote control
- **[Keyboard Shortcuts](keyboard-shortcuts.md)** - Quick access keys including **F** for frequency toggle

## 🔍 Troubleshooting

### Common Issues

**Voice sounds off on SSB satellites near TCA:**
- Try disabling predictive doppler
- Use manual frequency control around TCA
- Consider geographic settings optimization

**Frequency tracking stops during rapid changes:**
- Check rate limiting settings
- Verify TLE data is current
- Review doppler threshold configuration

**Manual frequency control not available:**
- Ensure rotator system is enabled in configuration
- Verify currently tracking a satellite
- Check that tracking is active (not stopped)

### Debug Information

Enable detailed logging to troubleshoot frequency issues:
- Doppler rate information in logs
- Rate limiting events
- Predictive algorithm decisions
- Manual control state changes
