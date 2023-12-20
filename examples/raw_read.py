'''
Demo program to see how to read and write NFC tag
'''
#from machine import UART,Pin,SPI,PWM, I2C
import time
from nfc import NFC

    
data = '1B233A49' # must be 4 byte, for write
baudrate = 9600 # communication buadrate between pico W and NFC module
page_no = '15'    # memory location divided into pages NTAG213/215/216 -> 4bytes per page
port='/dev/ttyS0'
nfc = NFC(port,baudrate) #create object
while 1:
        dataRec = nfc.data_read(page_no) # Read Tag data written initially
        print("Received data = ",dataRec)

        
