import pynmea2
import serial
from PySide6.QtCore import QThread, Signal

class GPSReader(QThread):
    position_update = Signal(float, float, float)  # lat, lon, alt
    status_update = Signal(str)

    def __init__(self, port, baudrate=4800, parent=None):
        super().__init__(parent)
        self.port = port
        self.baudrate = baudrate
        self._running = False
        self._ser = None
        self._has_fix = False

    def run(self):
        self._running = True
        try:
            self._ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.status_update.emit(f"Connected to {self.port}")
            while self._running:
                try:
                    line = self._ser.readline().decode('ascii', errors='replace').strip()
                    if line.startswith('$GPGGA') or line.startswith('$GNGGA'):
                        msg = pynmea2.parse(line)
                        lat = msg.latitude
                        lon = msg.longitude
                        alt = float(msg.altitude) if msg.altitude else 0.0
                        if lat == 0.0 and lon == 0.0:
                            self.status_update.emit("No fix (waiting for GPS)")
                            self._has_fix = False
                        else:
                            self.position_update.emit(lat, lon, alt)
                            self.status_update.emit("Fix")
                            self._has_fix = True
                except pynmea2.ParseError:
                    continue
                except Exception as e:
                    self.status_update.emit(f"Error: {e}")
                    self._has_fix = False
        except Exception as e:
            self.status_update.emit(f"Connection Error: {e}")
        finally:
            if self._ser:
                self._ser.close()
            self.status_update.emit("Disconnected")

    def stop(self):
        self._running = False
        if self._ser:
            self._ser.close() 