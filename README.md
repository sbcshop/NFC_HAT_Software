# NFC_HAT_Software

<img src="https://github.com/sbcshop/NFC_HAT_Software/blob/main/images/nfc%20hat.png">

Pi NFC HAT 13.56 MHz frequency-based NFC Reader/Writer. 
This Github provides a getting started guide and other working details for the NFC Expansion.

### Features:
- Onboard 13.56MHz NFC read/write Module
- 0.91 inch OLED
- Drag- and- drop programming using mass storage over USB
- Type C Power/UART
- Multifunction GPIO breakout supporting general I/O, UART, I2C, SPI, ADC & PWM function.
- Multi-tune Buzzer to add audio alert into the project
- Status LED for board power, and Tag Scan indication 
- Multi-platform support like MicroPython, CircuitPython, and Arduino IDE.
  
### Specifications:
- Operating voltage supply 5V
- Operating Frequency: 13.56MHz
- Operating current: 50mA
- Reading Distance: >50mm(The effective distance is related to the IC card and the use environment)
- Integrated Antenna
- Support Protocols: ISO14443A, ISO14443B, Sony, ISO15693, ISO18092
- Contactless cards: NTAG213, Mifare one S50, Mifare one S70, ultralight, FM11RF08
- Operating Temperature: -15°C~+55°C

## Getting Started with NFC HAT
### Hardware Overview
#### Pinout
<img src="https://github.com/sbcshop/NFC_HAT_Software/blob/main/images/img3.png">

### Interfacing Details
- Raspberry Pi and RFID module interfacing
  
  | Raspberry Pi | NFC Module Pin | Function |
  |---|---|---|
  |UART0 TX | RX | Serial UART connection |
  |UART0 RX | TX  | Serial UART connection |


- Buzzer and OLED Interfacing
  
  | Raspberry Pi | Buttons | Function |
  |---|---|---|
  |GPIO2 | SDA |OLED Pin|
  |GPIO3 | SCL |OLED Pin|
  |GPIO17  | Buzzer | Buzzer positive |
 
- Breakout Pins of NFC
  | NFC HAT | Function |
  |---|---|
  |BEEP | NFC buzzer Pin |
  |NFC_RX | NFC Pin |
  |NFC_TX | NFC Pin |
  |GND    | NFC Pins|
  |VCC    | NFC Pins|


### Example Codes
   Save whatever example code file you want to try as **main.py** in **Pico W** as shown above [step 3](https://github.com/sbcshop/ReadPi_NFC_Software/tree/main#3-how-to-move-your-script-on-pico-w-of-readpi), also add related lib files with the default name.
   In [example](https://github.com/sbcshop/Pico_NFC_Expansion_Software/tree/main/examples) folder you will find demo example script code to test onboard components of Expansion like 
   - [NFC module demo](https://github.com/sbcshop/Pico_NFC_Expansion_Software/blob/main/examples/main.py): testing onboard NFC module, buzzer and display unit of the shield. For this demo code to test you will have to add lib [nfc. py](https://github.com/sbcshop/Pico_NFC_Expansion_Software/blob/main/examples/nfc.py)

### Working Without Pico (Via USB)
<img src="https://github.com/sbcshop/NFC_HAT_Software/blob/main/images/nfc%20hat%20with%20usb.png">

You can also configure, read/write, etc using the NFC Module using Windows Software 
for this, you need to connect a USB to the Expansion board download the window software, install the software 
   
   **Find more details in [UART/USB](https://github.com/sbcshop/NFC_Module)**
   
  #### Working Description with NFC module:
   
  - Basic Communication Protocol: Data Format

    <img src="https://github.com/sbcshop/ReadPi_NFC_Software/blob/main/images/NFC_Communication_protocol.png">
   
  - Description of bytes in the data packet: 

     | Field | Length| Description | Remark |
     |---|---|---|---|
     |STX | 1  | 0xa8 - ‘Start Byte’ – Standard control bytes. Indicates the start of a data packet  | |
     |SEQ1 | 1  | Random Code  | Address bits are reserved for handling device addresses over 255.|
     |DADD | 1  | Device address is used for multiple machine communication, only address matching can be used for data communication, 0x00 and 0xFF addresses are broadcast addresses  |  |
     |CMD | 1  | Command Code One byte of the command sent by the upper unit to the lower unit  | |
     |DATA LENGTH | 2  | Data length includes TIME/STATUS + DATA field  | The high byte comes first, the low byte comes second |
     |STATUS | 1  | Lower computer return status, one byte | 00 means the command is executed correctly and the others are error codes |
     |TIME | 1  | Used for specific command time control, timeout processing, and other commands (most) the parameter is 0  | |
     |DATA  [0-N] | 2000  | Command Code One byte of the command sent by the upper unit to the lower unit  | It is used as command parameters when sent by the upper computer and as return data when sent by the lower computer with variable length. The maximum length is 512, and it will not be processed when it is out of range. It will reply directly/show that the command is too long and wait for the next command. |
     |BCC | 1  | Xor check bit, which verifies data but does not contain STX and ETX |  |
     |ETX | 1  | 0xa9 - ‘Terminating byte’ – Standard control byte. Indicates the end of a data packet| |
    
    SYSTEM COMMANDS examples:

    CMD_GetAddress (0x01)
    ```
    Description: Get the device communication address
    Sending data：0x01
    Return Data：
    STATUS     0x00 - OK
    DATA[0]    Device Address

    ```
    CMD_SetBaudRate ( 0x03 )
    ```
    Description: Set the serial port baud rate
    Sending data：0x03
      DATA[0]
        0x00 – 9600 bps
        0x01 – 19200 bps
        0x02 – 38400 bps
        0x03 – 57600 bps
        0x04 – 76800 bps
        0x05 – 115200 bps
    Return Data：
        STATUS 0x00 - OK
    ```

   Checkout [Manual](https://github.com/sbcshop/Pico_NFC_Expansion_Software/blob/main/documents/NFC%20Module%20command%20Manual.pdf) for a detailed understanding of System and Working Commands to send module from Host and corresponding response getting from NFC Module. 

   #### Basic Memory Structure of NFC Tags 
   The EEPROM memory is organized into pages with 4 bytes per page. The NTAG213 variant has 45 pages, the NTAG215 variant has 135 pages and the NTAG216 variant has 231 pages in total. The functionality of the different memory sections is shown below for NTAG213. 

   <img src="https://github.com/sbcshop/Pico_NFC_Expansion_Software/blob/main/images/memory%20organization%20NTAG213.png">
   
  Find more details in [NTAG Datasheet](https://github.com/sbcshop/Pico_NFC_Expansion_Software/blob/main/documents/NTAG213_215_216.pdf)

   
## Resources
  * [Schematic](https://github.com/sbcshop/Pico_NFC_Expansion_Hardware/blob/main/Design%20Data/SCH.pdf)
  * [Hardware Files](https://github.com/sbcshop/Pico_NFC_Expansion_Hardware)
  * [Step File](https://github.com/sbcshop/Pico_NFC_Expansion_Hardware/blob/main/Mechanical%20Data/NFC%20EXPANSION.step)
  * [MicroPython getting started for RPi Pico/Pico W](https://docs.micropython.org/en/latest/rp2/quickref.html)
  * [Pico W Getting Started](https://projects.raspberrypi.org/en/projects/get-started-pico-w)
  * [RP2040 Datasheet](https://github.com/sbcshop/HackyPi-Hardware/blob/main/Documents/rp2040-datasheet.pdf)
  * [NFC Module Command Manual](https://github.com/sbcshop/Pico_NFC_Expansion_Software/blob/main/documents/NFC%20Module%20command%20Manual.pdf)
  * [NTAG213/215/216 Datasheet](https://github.com/sbcshop/Pico_NFC_Expansion_Software/blob/main/documents/NTAG213_215_216.pdf)


## Related Products
   * [Pinco NFC Expansion RFID](https://shop.sb-components.co.uk/products/readpi-an-rfid-nfc-reader-powered-with-raspberry-pi-pico-w?variant=40478483054675) - Pico NFC Expansion with 125KHz RFID powered by Raspberry Pi Pico W
   * [Raspberry Pi Pico RFID expansion](https://shop.sb-components.co.uk/products/raspberry-pi-pico-rfid-expansion) - RFID expansion board with support to incorporate Pico/Pico W 
   * [RFID_Breakout](https://shop.sb-components.co.uk/products/rfid-breakout?_pos=5&_sid=fac219786&_ss=r) - RFID breakout for standalone testing and freedom to choose microcontroller as per requirement.

## Product License

This is ***open source*** product. Kindly check the LICENSE.md file for more information.

Please contact support@sb-components.co.uk for technical support.
<p align="center">
  <img width="360" height="100" src="https://cdn.shopify.com/s/files/1/1217/2104/files/Logo_sb_component_3.png?v=1666086771&width=300">
</p>
