import threading
import sounddevice as sd
import numpy as np
import os
import configparser
from datetime import datetime
import wave
import logging  # Add import for logging
import time

class PassRecorder:
    def __init__(self, config):
        self.load_config(config)
        self.recording = False
        self.thread = None
        self._stop_event = threading.Event()
        self.current_satname = None
        self.tracking_active = False  # Track if satellite tracking is active
        self.current_filepath = None  # Track the current recording file path
        self.audio_buffer = None  # Buffer to hold audio data
        self.buffer_lock = threading.Lock()
        self.device_info = None  # Store info about the selected device
        
        # Check at startup if any audio devices are available
        try:
            devices = sd.query_devices()
            input_devices = [dev for dev in devices if dev.get('max_input_channels', 0) > 0]
            logging.info(f"Pass recorder initialized: Found {len(input_devices)} audio input devices")
            if len(input_devices) == 0:
                logging.warning("No audio input devices detected. Recording will not work.")
                
            # Print available devices for troubleshooting
            for i, dev in enumerate(devices):
                input_channels = dev.get('max_input_channels', 0)
                if input_channels > 0:
                    logging.info(f"Audio input device {i}: {dev['name']} | {input_channels} channels")
                    
        except Exception as e:
            logging.error(f"Error checking audio devices at startup: {e}")

    def load_config(self, config):
        self.enabled = config.getboolean('passrecording', 'enabled', fallback=False)
        self.soundcard = config.get('passrecording', 'soundcard', fallback='default')
        self.save_dir = config.get('passrecording', 'save_dir', fallback='./recordings')
        self.min_elevation = config.getfloat('passrecording', 'min_elevation', fallback=20.0)
        self.sample_rate = config.getint('passrecording', 'sample_rate', fallback=44100)
        self.channels = config.getint('passrecording', 'channels', fallback=1)
        self.bit_depth = config.getint('passrecording', 'bit_depth', fallback=16)

    def update_config(self, config):
        self.load_config(config)
        
    def set_tracking_active(self, active):
        """Set whether satellite tracking is active"""
        self.tracking_active = active
        # If tracking is stopped, stop recording
        if not active and self.recording:
            self.stop_recording()

    def update_elevation(self, elevation, satname):
        # Remove excessive logging, only log when recording state changes
        if not self.enabled or not self.tracking_active:
            # Don't record if not enabled or tracking is not active
            if self.recording:
                self.stop_recording()
            return
            
        if elevation >= self.min_elevation:
            if not self.recording:
                logging.info(f"Starting recording for {satname} at elevation {elevation}")
                self.start_recording(satname)
        else:
            if self.recording:
                logging.info(f"Stopping recording for {satname} at elevation {elevation}")
                self.stop_recording()

    def find_audio_device(self):
        """Find the appropriate audio input device"""
        try:
            device = None
            device_name = None
            device_info = None
            
            # Get all available devices
            devices = sd.query_devices()
            logging.info(f"Available audio devices: {len(devices)}")
            
            # List all devices with detailed information to help troubleshoot
            for i, dev in enumerate(devices):
                input_channels = dev.get('max_input_channels', 0)
                hostapi_name = "unknown"
                try:
                    hostapi_name = sd.query_hostapis(dev.get('hostapi', 0)).get('name', 'unknown')
                except:
                    pass
                
                logging.info(f"Device {i}: {dev['name']} | API: {hostapi_name} | Inputs: {input_channels}")
            
            # Try to use the configured device
            if self.soundcard != 'default':
                # First try to find by exact name
                for i, dev in enumerate(devices):
                    if dev['name'] == self.soundcard and dev.get('max_input_channels', 0) > 0:
                        # Before selecting, test if device is available
                        try:
                            # Quick test with a small stream
                            with sd.InputStream(device=i, channels=1, samplerate=44100, blocksize=8192, callback=lambda *args: None):
                                pass  # Just test if it works
                            device = i
                            device_name = dev['name']
                            device_info = dev
                            logging.info(f"Selected working device '{dev['name']}' (index {i})")
                            break
                        except Exception as e:
                            logging.warning(f"Device {i} ({dev['name']}) not available: {e}")
                
                # If not found or not working, try partial name matches
                if device is None:
                    for i, dev in enumerate(devices):
                        if (self.soundcard in dev['name'] or dev['name'] in self.soundcard) and dev.get('max_input_channels', 0) > 0:
                            try:
                                # Quick test
                                with sd.InputStream(device=i, channels=1, samplerate=44100, blocksize=8192, callback=lambda *args: None):
                                    pass
                                device = i
                                device_name = dev['name']
                                device_info = dev
                                logging.info(f"Selected similar working device '{dev['name']}' (index {i})")
                                break
                            except Exception as e:
                                logging.warning(f"Similar device {i} ({dev['name']}) not available: {e}")
                
                # If still not found, try as an index
                if device is None:
                    try:
                        index = int(self.soundcard)
                        if 0 <= index < len(devices) and devices[index].get('max_input_channels', 0) > 0:
                            try:
                                # Quick test
                                with sd.InputStream(device=index, channels=1, samplerate=44100, blocksize=8192, callback=lambda *args: None):
                                    pass
                                device = index
                                device_name = devices[index]['name']
                                device_info = devices[index]
                                logging.info(f"Selected working device by index {index} ({device_name})")
                            except Exception as e:
                                logging.warning(f"Indexed device {index} not available: {e}")
                    except ValueError:
                        pass
            
            # If no device found yet, try the default device
            if device is None:
                try:
                    default_device = sd.default.device[0]
                    if default_device is not None and 0 <= default_device < len(devices):
                        try:
                            # Quick test
                            with sd.InputStream(device=default_device, channels=1, samplerate=44100, blocksize=8192, callback=lambda *args: None):
                                pass
                            device = default_device
                            device_name = devices[default_device]['name']
                            device_info = devices[default_device]
                            logging.info(f"Selected default working device {device_name} (index {device})")
                        except Exception as e:
                            logging.warning(f"Default device not available: {e}")
                except Exception as e:
                    logging.warning(f"Error getting default device: {e}")
            
            # Last resort: try every device until one works
            if device is None:
                logging.info("Trying all devices sequentially to find a working one")
                for i, dev in enumerate(devices):
                    if dev.get('max_input_channels', 0) > 0:
                        try:
                            # Quick test
                            with sd.InputStream(device=i, channels=1, samplerate=44100, blocksize=8192, callback=lambda *args: None):
                                pass
                            device = i
                            device_name = dev['name']
                            device_info = dev
                            logging.info(f"Found working device: {device_name} (index {i})")
                            break
                        except Exception as e:
                            logging.debug(f"Device {i} ({dev['name']}) not available: {e}")
            
            # If STILL no device, try with 'default' keyword explicitly (works on some systems)
            if device is None:
                try:
                    with sd.InputStream(device='default', channels=1, samplerate=44100, blocksize=8192, callback=lambda *args: None):
                        pass
                    device = 'default'
                    device_name = 'system default'
                    logging.info("Using explicit 'default' device specifier")
                except Exception as e:
                    logging.warning(f"'default' device specifier not working: {e}")
            
            # Give up if no device works
            if device is None:
                logging.error("No working audio input device found on this system")
                return None, None
                
            self.device_info = device_info
            return device, device_name
            
        except Exception as e:
            logging.error(f"Error finding audio device: {e}", exc_info=True)
            return None, None

    def start_recording(self, satname):
        if self.recording or not self.tracking_active:
            return
        
        # Initialize the buffer
        with self.buffer_lock:
            self.audio_buffer = []
            
        self.recording = True
        self.current_satname = satname
        self._stop_event.clear()
        self.thread = threading.Thread(target=self._record_worker, args=(satname,))
        self.thread.start()

    def stop_recording(self):
        if not self.recording:
            return
            
        filepath = self.current_filepath  # Save the filepath before it gets reset
        self._stop_event.set()
        
        if self.thread:
            self.thread.join()
            
        self.recording = False
        self.current_satname = None
        
        # Log the recording stop with the filepath
        if filepath:
            logging.info(f"Recording stopped: {os.path.basename(filepath)}")
            self.current_filepath = None

    def is_recording(self):
        return self.recording

    def _record_worker(self, satname):
        # Ensure save directory exists
        os.makedirs(self.save_dir, exist_ok=True)
        
        # File name: satname-YYYYMMDD-HHMMSS.wav (using UTC time for amateur radio standard)
        start_time = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        safe_satname = ''.join(c for c in satname if c.isalnum() or c in ('-_')).rstrip()
        filename = f"{safe_satname}-{start_time}.wav"
        filepath = os.path.join(self.save_dir, filename)
        self.current_filepath = filepath
        
        # Log recording start
        logging.info(f"Recording started: {filename}")
        
        # Choose WAV file parameters based on bit depth
        if self.bit_depth == 16:
            sampwidth = 2
            dtype = np.int16
            scale_factor = 32767
        elif self.bit_depth == 24:
            sampwidth = 3
            dtype = np.int32
            scale_factor = 8388607
        elif self.bit_depth == 32:
            sampwidth = 4
            dtype = np.int32
            scale_factor = 2147483647
        else:
            sampwidth = 2
            dtype = np.int16
            scale_factor = 32767
        
        # Find the appropriate audio device
        device, device_name = self.find_audio_device()
        if device is None:
            logging.error("Failed to find a suitable audio device for recording")
            self.recording = False
            # Create a short empty file to indicate the attempt
            try:
                with wave.open(filepath, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(44100)
                    # Write a brief note (silence)
                    wf.writeframes(np.zeros(4410, dtype=np.int16).tobytes())
                logging.warning(f"Created empty WAV file as no input device was available: {filepath}")
            except Exception as e:
                logging.error(f"Error creating placeholder file: {e}")
            return
        
        # Try a direct recording approach
        total_frames = 0
        
        try:
            # Define callback that stores data in our buffer
            def audio_callback(indata, frames, time, status):
                nonlocal total_frames
                
                # Only log errors other than overflow
                if status and status.input_overflow:
                    # Skip logging for input overflow as it's too verbose
                    pass
                elif status:
                    logging.warning(f"Audio status in callback: {status}")
                
                try:
                    # Get the RMS level to check if we're recording anything
                    level = np.linalg.norm(indata)
                    total_frames += frames
                    
                    # Log audio level every second to verify we're getting input
                    if total_frames % 10000 < frames:
                        logging.info(f"Audio level: {level:.4f}, total frames: {total_frames}")
                    
                    # Apply gain to make sure the audio is audible
                    gain = 2.0  # Reduced from 5.0 to 2.0 to prevent over-amplification
                    amplified_data = indata * gain
                    
                    # Clip to valid range for float (-1.0 to 1.0)
                    amplified_data = np.clip(amplified_data, -1.0, 1.0)
                    
                    # Convert to integer format
                    audio_data = (amplified_data * scale_factor).astype(dtype)
                    
                    # Store in buffer
                    with self.buffer_lock:
                        self.audio_buffer.append(audio_data.copy())
                        
                except Exception as e:
                    # Catch any errors in the callback to prevent audio stream from crashing
                    logging.error(f"Error in audio processing callback: {e}")
                    # Still increment frames to avoid hitting the logging condition too often
                    total_frames += frames
            
            # Create audio stream with careful error handling
            try:
                logging.info(f"Starting audio stream from device {device} ({device_name})")
                stream = sd.InputStream(
                    device=device,
                    channels=self.channels,
                    samplerate=self.sample_rate,
                    dtype='float32',
                    callback=audio_callback,
                    blocksize=8192  # Increased block size from 4096 to 8192 for better stability
                )
            except Exception as e:
                logging.error(f"Error creating audio stream: {e}", exc_info=True)
                # Try one more time with default device
                logging.info("Trying with 'default' device specifier as fallback")
                try:
                    stream = sd.InputStream(
                        device='default',
                        channels=self.channels,
                        samplerate=self.sample_rate,
                        dtype='float32',
                        callback=audio_callback,
                        blocksize=8192  # Increased block size for better stability
                    )
                except Exception as e2:
                    logging.error(f"Fallback also failed: {e2}")
                    raise  # Re-raise to be caught by outer exception handler
            
            # Start the stream
            stream.start()
            
            # Wait for stop event
            while not self._stop_event.is_set():
                time.sleep(0.2)
            
            # Stop the stream
            stream.stop()
            stream.close()
            
            # Write the recorded data to the WAV file
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(sampwidth)
                wf.setframerate(self.sample_rate)
                
                # Write buffer to file
                with self.buffer_lock:
                    if self.audio_buffer:
                        logging.info(f"Writing {len(self.audio_buffer)} audio chunks to file")
                        for chunk in self.audio_buffer:
                            wf.writeframes(chunk.tobytes())
                    else:
                        logging.warning("No audio data captured during recording")
            
            # File size verification
            file_size = os.path.getsize(filepath)
            logging.info(f"Saved WAV file: {filepath} (size: {file_size} bytes)")
            
            if file_size < 1000:
                logging.warning("Warning: Recorded file is very small, may not contain usable audio")
                
        except Exception as e:
            logging.error(f"Error in audio recording: {e}", exc_info=True)
        finally:
            # Clean up
            self.recording = False
            with self.buffer_lock:
                self.audio_buffer = None 