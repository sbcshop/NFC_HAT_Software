'''
Demo program to see how to read and write NFC tag
'''
import time
from nfc import NFC,SSD1306
from subprocess import check_output
from time import sleep
from datetime import datetime
from os import path
import serial
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.LOW)

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = path.join(DIR_PATH, "Fonts/GothamLight.ttf")

def info_print():
    display.DirImage(path.join(DIR_PATH, "Images/SB.png"))
    display.DrawRect()
    display.ShowImage()
    sleep(1)
    
    display.PrintText("PLACE YOUR NFC TAG", FontSize=14)
    display.DrawRect()
    display.ShowImage()
    
display = SSD1306()
info_print()

data = 'FFFFFFFF' # must be 4 byte, for write
baudrate = 9600 # communication buadrate between pico W and NFC module
page_no = '15'    # memory location divided into pages NTAG213/215/216 -> 4bytes per page
port='/dev/ttyS0'

nfc = NFC(port,baudrate) #create object

while 1:
        status = nfc.Data_write(data,page_no) # Write data to Tag
        
        if status == "Card write sucessfully":
            dataRec = nfc.data_read(page_no) # Read Tag data written initially
            print("Received data = ",dataRec)
            
            if dataRec is not None:
                    #print("size = ",sys.getsizeof(hex(dataRec)))
                    #print(type(dataRec))
                    display.PrintText("DATA : " +(dataRec), cords=(4, 8), FontSize=11)
                    display.DrawRect()
                    display.ShowImage()
                    GPIO.output(17,GPIO.HIGH)
                    sleep(0.5)
                    GPIO.output(17,GPIO.LOW)
                    display.PrintText("PLACE YOUR NFC TAG", FontSize=14)
                    display.ShowImage()
            
        else :
            print("Scan Card Please!")
            GPIO.output(17,GPIO.LOW)
        
        
        
