import serial
import binascii
import time
import binascii
import random
import sys
from os import path
from sys import exit, version_info

from PIL import Image, ImageDraw, ImageFont

try:
    from smbus import SMBus
except ImportError:
    if version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo "
             "apt-get install python-smbus")
    elif version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo "
             "apt-get install python3-smbus")

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = (path.join(DIR_PATH, "Fonts/GothamLight.ttf"))

STARTBYTE     ='A8'  
ENDBYTE       ='A9'
HARD_VERSION  ='0007000100'
GET_ADDRESS   ='0001000100'
READ_DATA     ='0037000200'         
NTAG_VERSION  ='0036000100'
ECC_SIG       ='003C000100'
WRITE_DATA    ='0039000600'
CARD_UID      ='0026000100'

# Fundamental Command Table
SET_CONTRAST = 0x81
DISPLAY_ON = 0xA4
DISPLAY_INVERT = 0xA6
DISPLAY_ON = 0xAE  # Off: sleep mode
DISPLAY_OFF = 0xAF  # On: Normal Mode

# Address Settting Command Table
MEM_ADD_MODE = 0x20
COLUMN_ADD = 0x21
PAGE_ADD = 0x22

# Hardware Configuration
DISPLAY_START_LINE = 0x40
SEGMENT_REMAP = 0xA0
MUX_RATIO = 0xA8
COM_OUT_SCAN = 0xC0
COM_SCAN_REMAP = 0xC8
DISPLAY_OFFSET = 0xD3
SET_COM_PIN = 0xDA

# Timing and Driving
SET_CLK_DIV = 0xD5
SET_PRE_CHARGE = 0xD9
SET_DESELECT = 0xDB
CHARGE_PUMP = 0x8D


class NFC:
    def __init__(self,port,baudrate):
        self.serial = serial.Serial(port='/dev/ttyS0',baudrate = baudrate,
                      parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,
                      bytesize=serial.EIGHTBITS,timeout=1)
        self.serial.flush()

    def calculate_checksum(self,data):
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum

    def calculation(self,address_r):
        address_r = str(hex(int(address_r))[2:])
        if len(address_r) < 2:
            address_r = '0' + address_r            
        rand_hex = self.random_hex()
        chksm_data = rand_hex+READ_DATA+address_r
        bin_data1 = binascii.unhexlify(chksm_data)
        chk_1 = (hex(self.calculate_checksum(bin_data1)))
        chk = chk_1[2:]
        dat = STARTBYTE+rand_hex+READ_DATA+address_r+chk+ENDBYTE
        return dat
    
    def calculation_1(self,da):           
        rand_hex_1  = self.random_hex()
        chksm_data_1  = rand_hex_1 +da
        bin_data1_1  = binascii.unhexlify(chksm_data_1 )
        chk_2 = (hex(self.calculate_checksum(bin_data1_1 )))
        chk_1  = chk_2[2:]
        dat_1  = STARTBYTE+rand_hex_1 +da+chk_1 +ENDBYTE
        return dat_1 

    def write_calculation(self,data,address_r,s):
        address_r = str(hex(int(address_r))[2:])
        if len(address_r) < 2:
            address_r = '0' + address_r            
        rand_hex = self.random_hex()
        chksm_data = rand_hex+s+address_r+data
        bin_data1 = binascii.unhexlify(chksm_data)
        chk_1 = (hex(self.calculate_checksum(bin_data1)))
        chk = chk_1[2:]
        dat = STARTBYTE+rand_hex+s+address_r+data+chk+ENDBYTE
        return dat
    
        
    def random_hex(self):
        length = 2
        random_bytes = bytearray(random.getrandbits(8) for _ in range((length + 1) // 2))
        random_hex = ''.join('{:02x}'.format(byte) for byte in random_bytes)
        return random_hex[:length]
           
    def send_command(self, Data):
        if Data is not None:
            bin_data = binascii.unhexlify(Data)
            response = self.serial.write(bin_data)
        

    def hardware_version(self):
        dat_1  = self.calculation_1(HARD_VERSION)
        self.send_command(dat_1 )
        #time.sleep(0.1)
        d = self.serial.read(19)
        s = []
        if d is not  None: 
            def split_bytes_data(data, packet_size):
                # Split the bytes object into packets of the specified size
                packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]
                return packets
            ds = split_bytes_data(d,7)
            for i in range(1,len(ds)):
                   s.append(str(ds[i],'latin-1'))
            return "".join(s)

########################## read operations ############################################
    def data_read(self,address_r):
        #self.serial.flush()
        dat = self.calculation(address_r)
        if len(dat) == 20:
            data = self.send_command(dat)
            rec_data = self.serial.readline()
            #print("##",len(rec_data))
            #print(rec_data)
            
            if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                #print(a)
                if "".join(a)[6:14] != "37000101": 
                        if  len("".join(a)[14:22]) > 7:
                            return "".join(a)[14:22]
                            
                        else:
                            return "Card not detect"
                
        
    def Ntag_version(self):
        dat = self.calculation_1(NTAG_VERSION)
        data = self.send_command(dat)
        #time.sleep(0.1)
        rec_data = self.serial.read()
        #print("rec_data = ",rec_data)
        if rec_data is not None:
            a = ['{:02x}'.format(x) for x in rec_data]
            return "".join(a)
        #read_data.flush()
        
    def ECC_signature(self):
        dat = self.calculation_1(ECC_SIG)
        if len(dat) == 18:
            data = self.send_command(dat)
            #time.sleep(0.1)
            rec_data = self.serial.read()
            #print("rec_data = ",rec_data)
            if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                f =  "".join(a)[-5:-4]
                
                if  "".join(a)[-5:-4] == '1':
                    return "Card not detect"
                else:
                    return  "".join(a)
        
    def Card_UID(self):
        dat = self.calculation_1(CARD_UID)
        if len(dat) == 18:
            data = self.send_command(dat)
            #time.sleep(0.1)
            rec_data = self.serial.read()
            if rec_data is not None and len(rec_data) > 18:
                a = ['{:02x}'.format(x) for x in rec_data]
                s = "".join(a)
                return s
        
########################## write operations ############################################
        
    def Data_write(self,data,address_r):
        dat = self.write_calculation(data,address_r,WRITE_DATA)
        if len(dat) == 28:
            data = self.send_command(dat)
            rec_data = self.serial.readline()
            #print(f"write len: {len(rec_data)}")
            if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                f =  "".join(a)[-5:-4]
            
                if  "".join(a)[-5:-4] == '0':
                    return "Card write sucessfully"
                else:
                    return "Card not detect"
                
    ########################################################## Command Mode ##########    
    def Command_Mode(self,COMMAND):
            dat  = self.calculation_1(COMMAND)
            data = self.send_command(dat)
            rec_data = self.serial.readline()            
            if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                return a

    ##################################################################################

                        
class i2c_interface:
    def __init__(self, address=0x3c):
        """
        :param address: i2c address of ssd1306
        """
        self.bus = SMBus(self.bus_id())
        self.address = address

    def __del__(self):
        self.close_i2c()

    def close_i2c(self):
        self.bus.close()

    def bus_id(self):
        """
        :return: Returns SMBUS id of Raspberry Pi
        """
        revision = [lines[12:-1] for lines in open('/proc/cpuinfo',
                                                   'r').readlines() if
                    "Revision" in lines[:8]]
        revision = (revision + ['0000'])[0]
        return 1 if int(revision, 16) >= 4 else 0

    def i2c_read(self, register=0):
        data = self.bus.read_byte_data(self.address, register)
        return data

    def i2c_write(self, register=DISPLAY_START_LINE, data=0):
        # Write a byte to address, register
        self.bus.write_byte_data(self.address, register, data)

    def i2c_write_block(self, register=DISPLAY_START_LINE, data=None):
        if data is None:
            data = [40]
        self.bus.write_i2c_block_data(self.address, register, data)


class SSD1306(i2c_interface):
    def __init__(self, width=128, height=32, address=0x3c):
        i2c_interface.__init__(self, address=address)
        self.Height = height
        self.Width = width
        self.Page = height // 8
        self.address = address
        self._Image = None
        self._Image_New = None
        self.Draw = None
        self.Image_Buf = None

        self.NewImage()
        self.InitDisplay()

    def NewImage(self):
        self._Image = Image.new('1', (self.Width, self.Height), "WHITE")
        self.Draw = ImageDraw.Draw(self._Image)

    def DirImage(self, filename, size=None, cords=(0, 0)):
        """
        :param cords: Coordinates of image on display
        :param pos: X, Y positions of paste location
        :param filename: Image file path
        :param size: The requested size in pixels, as a 2-tuple: (width,
        height)
        :return: None
        """
        self._Image_New = Image.open(filename).convert("1")
        if not size:
            size = (self.Width, self.Height)
        self._Image_New = self._Image_New.resize(size)

        self._Image.paste(self._Image_New, box=cords)
        self.Draw = ImageDraw.Draw(self._Image)

    def WriteCommand(self, cmd):  # write command
        self.i2c_write(register=0x00, data=cmd)

    def WriteData(self, data):  # write ram
        self.i2c_write(register=DISPLAY_START_LINE, data=data)

    def InitDisplay(self):
        self.WriteCommand(DISPLAY_ON)

        self.WriteCommand(DISPLAY_START_LINE)

        self.WriteCommand(0xB0)  # Page Address

        self.WriteCommand(COM_SCAN_REMAP)  # Com Output Scan

        # Contrast Setting
        self.WriteCommand(SET_CONTRAST)
        self.WriteCommand(0xFF)
        self.WriteCommand(0xA1)

        self.WriteCommand(DISPLAY_INVERT)

        self.WriteCommand(MUX_RATIO)
        self.WriteCommand(0x1F)  # Column Start Address

        self.WriteCommand(DISPLAY_OFFSET)
        self.WriteCommand(0x00)

        self.WriteCommand(SET_CLK_DIV)
        self.WriteCommand(0xF0)

        self.WriteCommand(SET_PRE_CHARGE)
        self.WriteCommand(PAGE_ADD)

        self.WriteCommand(SET_COM_PIN)
        self.WriteCommand(0x02)

        self.WriteCommand(SET_DESELECT)
        self.WriteCommand(0x49)

        self.WriteCommand(CHARGE_PUMP)
        self.WriteCommand(0x14)

        self.WriteCommand(DISPLAY_OFF)

    def NoDisplay(self):
        for i in range(0, self.Page):
            self.WriteCommand(0xb0 + i)
            self.WriteCommand(0x00)
            self.WriteCommand(0x10)
            for j in range(0, self.Width):
                self.WriteData(0x00)

    def WhiteDisplay(self):
        for i in range(0, self.Page):
            self.WriteCommand(0xb0 + i)
            self.WriteCommand(0x00)
            self.WriteCommand(0x10)
            for j in range(0, self.Width):
                self.WriteData(0xff)

    def ImgBuffer(self, image):
        buf = [0xff] * (self.Page * self.Width)
        Img_Mono = image.convert('1')
        Img_Width, Img_Height = Img_Mono.size
        pixels = Img_Mono.load()
        if Img_Width == self.Width and Img_Height == self.Height:
            #  Horizontal screen
            for y in range(Img_Height):
                for x in range(Img_Width):
                    # Set the bits for the column of pixels at the current
                    # position.
                    if pixels[x, y] == 0:
                        buf[x + (y // 8) * self.Width] &= ~(1 << (y % 8))
        elif Img_Width == self.Width and Img_Height == self.Height:
            #  Vertical screen
            for y in range(Img_Height):
                for x in range(Img_Width):
                    x_pos = y
                    y_pos = self.Height - x - 1
                    if pixels[x, y] == 0:
                        buf[(x_pos + int(y_pos / 8) * self.Width)] &= ~(
                                1 << (y % 8))
        for i in range(self.Page * self.Width):
            buf[i] = ~buf[i]
        return buf

    def ShowImage(self):
        i_buf = self.ImgBuffer(self._Image)
        for i in range(0, self.Page):
            self.WriteCommand(0xB0 + i)  # set page address
            self.WriteCommand(0x00)  # set low column address
            self.WriteCommand(0x10)  # set high column address
            # write data #
            for j in range(0, 128):  # self.Width):
                self.WriteData(i_buf[j + self.Width * i])
        self.NewImage()

    def PrintText(self, text, cords=(10, 5), Font=DefaultFont,
                  FontSize=14):
        """
        :param text: Text to print
        :param cords: Top left Corner (X, Y) cords
        :param Font: Font Type
        :param FontSize: Size of Font
        :return: None
        """
        self.Draw.text(cords, text, font=ImageFont.truetype(Font, FontSize))

    def DrawRect(self, cords=(0, 0, 127, 31)):
        """
        :param cords: X0, X1, Y0, Y1
        :return: None
        """
        self.Draw.rectangle(cords, outline=0)

    def DrawPolygon(self, cords=(1, 2, 3, 4, 5, 6)):
        """
        :param cords: Sequence of either 2-tuples like [(x, y), (x, y),
        ...] or numeric values like [x, y, x, y, ...]
        :return: None
        """
        self.Draw.polygon(cords)

    def DrawPoint(self, cords=(64, 16, 66, 18)):
        """
        :param cords: tuple of X, Y coordinates of Points
        :return: None
        """
        self.Draw.point(cords)

    def DrawLine(self, cords=(64, 16, 78, 18)):
        """
        Draws a line between the coordinates in the xy list
        :param cords: tuple of X, Y coordinates for line
        :return: None
        """
        self.Draw.line(cords)

    def DrawEllipse(self, cords=(64, 16, 78, 18)):
        """
        Draws an ellipse inside the given bounding box
        :param cords: Four points to define the bounding box
        :return: None
        """
        self.Draw.ellipse(cords)

    def DrawArc(self, cords=(10, 10, 120, 10), start=0, end=90):
        """
        Draws an arc (a portion of a circle outline) between the start and
        end angles, inside the given bounding box
        :param end: Starting angle, in degrees. Angles are measured from 3
        o’clock, increasing clockwise.
        :param start: Ending angle, in degrees.
        :param cords: Four points to define the bounding box
        :return: None
        """
        self.Draw.arc(cords, start=start, end=end)

