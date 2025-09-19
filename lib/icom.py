"""
Original code: https://github.com/dl7oap/gp2icom
Created: by Andreas Puschendorf, DL7OAP
Date    : 09/2020

Modified: by Alex Krist, KR1ST from original by Andreas Puschendorf, DL7OAP
Date    : 11/2020
Comments: The original script has been adapted for use with the Icom IC-9100. The IC-9100 does 
          not support CAT control for RIT. I added some code to reject the echoed frames from
          the CI-V bus when "remote" jack is used on the radio rather than the USB port.

Modified: by Andreas Puschendorf, DL7OAP
Date    : 11/2020
Comments: to bring ic9100 and ic9700 together in one class the CI-V adress has to be given
          162 - default for IC9700 (162 = hex A2)
          124 - default for IC9100 (124 = hex 7C)
          
Modified: by Joshua Petry, DL3JOP
Date    : 09/2024
Comments: changed to IC-910 support, 9700/9100 deprecated     
"""

import serial
import time
import logging


class icom:

    def __init__(self, serialDevice, serialBaud, icomTrxCivAdress):
        self.connected = False
        self.icomTrxCivAdress = icomTrxCivAdress
        self.serialDevice = serialDevice
        self.serialBaud = serialBaud
        self.ser = serial.Serial()
        self.ser.baudrate = serialBaud
        self.ser.port = serialDevice
        self.ser.setDTR(0)
        self.ser.setRTS(0)
        try:
            self.ser.open()
            self.connected = True
        except:
            self.connected = False
            print("Rig not connected, switching to dummy mode")
            self.last_set_frequency_a = 0 # per VFO
            self.last_set_frequency_b = 0
            self.current_vfo = "A"
            
    # gives a empty bytearray when data crc is not valid
    def __readFromIcom(self):
        if self.connected == True:
            time.sleep(0.05)
            b = bytearray()
            b = b + self.ser.read(1)
            while self.ser.inWaiting():
                b = b + self.ser.read(1)
            # drop all but the last frame
            while b.count(b'\xfd') > 1:
                del b[0:b.find(b'\xfd') + 1]
            if len(b) > 0:
                # valid message
                validMsg = bytes([254, 254, 0, self.icomTrxCivAdress, 251, 253])
                if b[0:5] == validMsg:
                    b = b[6:len(b)]
                    if len(b) > 0:  # read answer from icom trx
                        if b[0] == 254 and b[1] == 254 and b[-1] == 253:  # check for valid data CRC
                            return b
                        else:
                            b = bytearray()
                    else:
                        b = bytearray()
                else:
                    if b[0] == 254 and b[1] == 254 and b[-1] == 253:  # check for valid data CRC
                        b = b
                    else:
                        b = bytearray()
            #print('   * readFromIcom return value: ', b)
            return b
        else:
            return bytearray()
        
    # gives a empty bytearray when data crc is not valid
    def __writeToIcom(self, b):
        if self.connected == True:
            s = self.ser.write(bytes([254, 254, self.icomTrxCivAdress, 0]) + b + bytes([253]))
            self.ser.flushInput()
            #print('   * writeToIcom value: ', b)
            return self.__readFromIcom()
        else:
            return bytearray()

    def is_connected(self):
        return self.connected
    
    def close(self):
        self.ser.close()

    def setMode(self, mode):
        mode = mode.upper()
        if mode == 'FM':
            self.__writeToIcom(b'\x06\x04')
        if mode == 'FM':
            self.__writeToIcom(b'\x06\x05')
        if mode == 'USB':
            self.__writeToIcom(b'\x06\x01')
        if mode == 'LSB':
            self.__writeToIcom(b'\x06\x00')
        if mode == 'CW':
            self.__writeToIcom(b'\x06\x03')

    def setVFO(self, vfo):
        vfo = vfo.upper()
        if vfo == 'VFOA':
            self.current_vfo = "A"
            self.__writeToIcom(b'\x07\x00')
        if vfo == 'VFOB':
            self.current_vfo = "B"
            self.__writeToIcom(b'\x07\x01')
        if vfo == 'MAIN':
            self.current_vfo = "A"
            self.__writeToIcom(b'\x07\xd0')  # select MAIN
        if vfo == 'SUB':
            self.current_vfo = "B"
            self.__writeToIcom(b'\x07\xd1')  # select SUB

    # change main and sub
    def setExchange(self):
        if self.current_vfo == "A":
            self.current_vfo = "B"
        else:
            self.current_vfo = "A"
        self.__writeToIcom(b'\x07\xB0')

    # change main and sub
    def setSatelliteMode910(self, on):
        if on:
            self.__writeToIcom(b'\x1A\x07\x01')
        else:
            self.__writeToIcom(b'\x1A\x07\x00')
            
    def setSatelliteMode9700(self, on):
        if on:
            self.__writeToIcom(b'\x16\x5A\x01')
        else:
            self.__writeToIcom(b'\x16\x5A\x00')


    # Parameter: hertz string with 3 numbers
    def setToneHz(self, hertz):
        if int(hertz) >= 1000:
            b = b'\x1b\x00' + bytes([int('1' + hertz[1], 16), int(hertz[2] + hertz[3], 16)])
        else:
            b = b'\x1b\x00' + bytes([int('0' + hertz[0], 16), int(hertz[1] + hertz[2], 16)])
        self.__writeToIcom(b)
    def setToneSQLHz(self, hertz):
        if int(hertz) >= 1000:
            b = b'\x1b\x01' + bytes([int('1' + hertz[1], 16), int(hertz[2] + hertz[3], 16)])
        else:
            b = b'\x1b\x01' + bytes([int('0' + hertz[0], 16), int(hertz[1] + hertz[2], 16)])
        self.__writeToIcom(b)

    # Caution: RIT CI-V Command only for IC-9700, the IC-9100 has no RIT CI-V command
    # Parameter: Integer
    def setRitFrequency(self, value):
        hertz = '0000' + str(abs(value))
        if value >= 0:
            b = b'\x21\x00' + bytes([int(hertz[-2] + hertz[-1], 16),  int(hertz[-4] + hertz[-3], 16)]) + b'\x00'
        else:
            b = b'\x21\x00' + bytes([int(hertz[-2] + hertz[-1], 16),  int(hertz[-4] + hertz[-3], 16)]) + b'\x01'
        self.__writeToIcom(b)

    # Parameter as string in hertz
    def setFrequency(self, freq):
        if self.current_vfo == "A":
            self.last_set_frequency_a = freq
        else:
            self.last_set_frequency_b = freq
        freq = '0000000000' + freq
        freq = freq[-10:]
        b = bytes([5, int(freq[8:10], 16), int(freq[6:8], 16), int(freq[4:6], 16),
                   int(freq[2:4], 16), int(freq[0:2], 16)])
        returnMsg = self.__writeToIcom(b)
        back = False
        if len(returnMsg) > 0:
            if returnMsg.count(b'\xfb') > 0:
                back = True
        return back


    def setToneSquelchOn(self, on):
        if on:
            self.__writeToIcom(b'\x16\x43\x01')
        else:
            self.__writeToIcom(b'\x16\x43\x00')

    def setToneOn(self, on):
        if on:
            self.__writeToIcom(b'\x16\x42\x01')
        else:
            self.__writeToIcom(b'\x16\x42\x00')

    def setAfcOn(self, on):
        if on:
            self.__writeToIcom(b'\x16\x4A\x01')
        else:
            self.__writeToIcom(b'\x16\x4A\x00')

    # Parameter b: True = set SPLIT ON, False = set SPLIT OFF
    def setSplitOn(self, on):
        if on:
            self.__writeToIcom(b'\x0F\x01')
        else:
            self.__writeToIcom(b'\x0F\x00')

    # Parameter b: True = set RIT ON, False = set RIT OFF
    def setRitOn(self, on):
        if on:
            self.__writeToIcom(b'\x1A\x06\x01')
        else:
            self.__writeToIcom(b'\x1A\x06\x00')

    def setDuplex(self, value):
        value = value.upper()
        if value == 'OFF':
            self.__writeToIcom(b'\x0F\x10')
        if value == 'DUP-':
            self.__writeToIcom(b'\x0F\x11')
        if value == 'DUP+':
            self.__writeToIcom(b'\x0F\x12')

    def getFrequency(self):
        if self.connected == True:
            b = self.__writeToIcom(b'\x03')  # ask for used frequency
            c = ''
            if len(b) > 0:
                for a in reversed(b[5:10]):
                    c = c + '%0.2X' % a
            if len(c) > 0: 
                if c[0] == '0':
                    c = c[1:len(c)]
            return c
        else:
            if self.current_vfo == "A":
                return self.last_set_frequency_a
            else:
                return self.last_set_frequency_b

    def setFrequencyOffUnselectVFO(self, freq):
        freq = '0000000000' + freq
        freq = freq[-10:]
        b = b'\x25\x01' + bytes([int(freq[8:10], 16), int(freq[6:8], 16), int(freq[4:6], 16),
                   int(freq[2:4], 16), int(freq[0:2], 16)])
        returnMsg = self.__writeToIcom(b)
        back = False
        if len(returnMsg) > 0:
            if returnMsg.count(b'\xfb') > 0:
                back = True
        return back

    # CI-V TRANSCEIVE have to be ON
    # function extract last frequency which is send to us when a user is dailing
    def getWhatFrequencyIcomSendUs(self):
        c = ''
        b = self.__readFromIcom()
        # find last CI-V message by searching from behind
        position = b.rfind(bytearray(b'\xfe\xfe'))
        if position >= 0:
            # extract answer
            answer = b[position:len(b)]
            # proof if CI-V frequence message from icom
            if len(answer) == 11 and answer[4] == 0:
                if len(answer) > 0:
                    for a in reversed(answer[5:10]):
                        c = c + '%0.2X' % a
                if c[0] == '0':
                    c = c[1:len(c)]
        return c

    def isPttOff(self):
        ret = True
        b = self.__writeToIcom(b'\x1C\x00')  # ask for PTT status
        if len(b) < 3: ## This should be fixed.
            return ret
        #print(b)
        if b[-2] == 1:
            ret = False
        return ret
        
    def setup_vfos(self, satmode, downmode, upmode, doppler_thres_fm, doppler_thres_linear):
        doppler_thres = 100
        interactive = True
        if satmode == 1:
            self.setVFO("Main")
        else:
            self.setVFO("VFOA")
        if downmode == "FM":
            self.setMode("FM")
            doppler_thres = doppler_thres_fm
            interactive = False
        elif downmode == "FMN":
            self.setMode("FM")
            doppler_thres = doppler_thres_fm
            interactive = False
        elif downmode ==  "LSB":
            interactive = True
            self.setMode("LSB")
            doppler_thres = doppler_thres_linear
        elif downmode ==  "USB":
            interactive = True
            self.setMode("USB")
            doppler_thres = doppler_thres_linear
        elif downmode ==  "DATA-LSB":
            interactive = False
            self.setMode("LSB")
            doppler_thres = 0
        elif downmode ==  "DATA-USB":
            interactive = False
            self.setMode("USB")
            doppler_thres = 0      
        elif downmode == "CW":
            interactive = True
            self.setMode("CW") 
            doppler_thres = doppler_thres_linear
        else:
            logging.warning("*** Downlink mode not implemented yet: {bad}".format(bad=self.my_satellite.downmode))
            sys.exit()
        
        if satmode == 1:
            self.setVFO("SUB")
        else:
            self.setVFO("VFOB")
        if upmode == "FM":
            self.setMode("FM")
        elif upmode == "FMN":
            self.setMode("FM")
        elif upmode == "LSB" or downmode ==  "DATA-LSB":
            self.setMode("LSB")
        elif upmode == "USB" or downmode ==  "DATA-USB":
            self.setMode("USB")
        elif upmode == "CW":
            self.setMode("CW") 
        else:
            logging.warning("*** Uplink mode not implemented yet: {bad}".format(bad=self.my_satellite.upmode))
            sys.exit()
            
        return int(doppler_thres), interactive

