__author__ = 'karthi'

import time
import RPi.GPIO as GPIO
import fonts
fontWidth = 6
currentScreen = 0


class LCD_GPIO(object):
    # Timing constants
    E_PULSE = 0.000000070  # Addess setup time 140ns
    E_DELAY = 0.000000100  # Data setup time 200ns
    def __init__(self, RST,RS,RW,E1,E2,CS1,CS2, D0, D1, D2, D3, D4, D5, D6, D7):

        #GPIO number Assignment

        self.CS1=CS1
        self.CS2=CS2
        self.RST=RST
        self.E1 = E1
        self.E2 = E2
        self.RS = RS
        self.RW = RW

        self.D0 = D0
        self.D1 = D1
        self.D2 = D2
        self.D3 = D3
        self.D4 = D4
        self.D5 = D5
        self.D6 = D6
        self.D7 = D7

        GPIO.setmode(GPIO.BCM)        # Use BCM GPIO numbers

        GPIO.setup(self.E1, GPIO.OUT)  # E1
        GPIO.setup(self.E2, GPIO.OUT)  # E2
        GPIO.setup(self.RW, GPIO.OUT) # RW
        GPIO.setup(self.RS, GPIO.OUT) # RS

        GPIO.setup(self.D0, GPIO.OUT) # DB0
        GPIO.setup(self.D1, GPIO.OUT) # DB1
        GPIO.setup(self.D2, GPIO.OUT) # DB2
        GPIO.setup(self.D3, GPIO.OUT) # DB3
        GPIO.setup(self.D4, GPIO.OUT) # DB4
        GPIO.setup(self.D5, GPIO.OUT) # DB5
        GPIO.setup(self.D6, GPIO.OUT) # DB6
        GPIO.setup(self.D7, GPIO.OUT) # DB7

        GPIO.setup(self.CS1, GPIO.OUT) # CS1
        GPIO.setup(self.CS2, GPIO.OUT) # CS2

        GPIO.output(self.RS, 0)
        GPIO.output(self.RW, 0)
        GPIO.output(self.E1, 0)
        GPIO.output(self.E2, 0)
        GPIO.output(self.CS1, 0)
        GPIO.output(self.CS2, 0)
        GPIO.setup(self.RST, GPIO.OUT) # RST

        GPIO.output(self.RST, 0)
        time.sleep(0.5)
        GPIO.output(self.RST, 1)

        time.sleep(0.03)



    def useDisp1(self):
        # use Controller 1 (Display's LEFT part)
        GPIO.output(self.CS1, 1)
        GPIO.output(self.CS2, 0)

    def useDisp2(self):
        # use Controller 2 (Display's RIGHT part)
        GPIO.output(self.CS1, 0)
        GPIO.output(self.CS2, 1)


    def lcd_byte(self,value, mode):

        GPIO.output(self.RW,0)
        GPIO.output(self.RS,mode)
        if (mode == 19):
            GPIO.output(self.D0, (~(value)) & 0x01)
            GPIO.output(self.D1, (~(value)) & 0x02)
            GPIO.output(self.D2, (~(value)) & 0x04)
            GPIO.output(self.D3, (~(value)) & 0x08)
            GPIO.output(self.D4, (~(value)) & 0x10)
            GPIO.output(self.D5, (~(value)) & 0x20)
            GPIO.output(self.D6, (~(value)) & 0x40)
            GPIO.output(self.D7, (~(value)) & 0x80)
        else:
            GPIO.output(self.D0, (value) & 0x01)
            GPIO.output(self.D1, (value) & 0x02)
            GPIO.output(self.D2, (value) & 0x04)
            GPIO.output(self.D3, (value) & 0x08)
            GPIO.output(self.D4, (value) & 0x10)
            GPIO.output(self.D5, (value) & 0x20)
            GPIO.output(self.D6, (value) & 0x40)
            GPIO.output(self.D7, (value) & 0x80)

        # Toggle E
        if(currentScreen == 0):
#            print("cs0")
            time.sleep(self.E_DELAY)
            GPIO.output(self.E1, True)
            time.sleep(self.E_PULSE)
            GPIO.output(self.E1, False)
            time.sleep(self.E_DELAY)
        elif(currentScreen == 1):
            time.sleep(self.E_DELAY)
            GPIO.output(self.E2, True)
            time.sleep(self.E_PULSE)
            GPIO.output(self.E2, False)
            time.sleep(self.E_DELAY)


        # Waiting write operation complete by listening BUSY singal

#        GPIO.setup(self.D7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#        GPIO.output(self.RW,1)
#        GPIO.output(self.RS,0)

#        time.sleep(self.E_DELAY)
#        GPIO.output(self.E, True)
#        time.sleep(self.E_PULSE)
#        GPIO.output(self.E, False)
#        time.sleep(self.E_DELAY)

        #Wait until BUSY(D7) is off
#        while GPIO.input(self.D7):
#          pass

#        GPIO.setup(self.D7, GPIO.OUT) # set D7 back to Output


class LCD12864(object):
    def __init__(self, driver):
        self.driver = driver
        self.lcd_init()

    def setPage(self, value):
        # set y=value * 8
        self.driver.lcd_byte(0xB8|(value&0x07),0)

    def setAddress(self, value):
        # set x=value
        self.driver.lcd_byte(0x40|(value&0x3F),0)

    def lcd_cls(self):
        # clear screen by write 0x00 to all display memory
        self.driver.useDisp1()

        for y in range(8):
          self.setPage(y)
          self.setAddress(0)
          for i in range(64):
             self.driver.lcd_byte(0x00,1)

        self.driver.useDisp2()

        for y in range(8):
          self.setPage(y)
          self.setAddress(0)
          for i in range(64):
             self.driver.lcd_byte(0x00,1)

    def lcd_init(self):
        self.driver.useDisp1()
        currentScreen = 0
        self.driver.lcd_byte(0x3F,0)
        currentScreen = 1
        self.driver.lcd_byte(0x3F,0)
        self.driver.useDisp2()
        currentScreen = 0
        self.driver.lcd_byte(0x3F,0)
        currentScreen = 1
        self.driver.lcd_byte(0x3F,0)

driver = LCD_GPIO(RS=4,RW=17,E1=27,E2=7,D0=22,D1=10,D2=9,D3=11,D4=5,D5=6,D6=13,D7=19,CS1=26,CS2=21,RST=20)
lcd = LCD12864(driver=driver)

def getHexCode(string):
    for ch in string:
        for i in range(fontWidth):
            yield fonts.font6x7[(ord(ch)-32)*fontWidth+i]


def displayText(string, lineNumber, byteNumber, screen):
    global currentScreen
    currentScreen = screen
    byteStream = getHexCode(string)
    byteStreamLength = len(string)*fontWidth
    if (byteStreamLength>127-byteNumber+1):
        byteStreamLength=(127-byteNumber+1)
    if (byteNumber < 64):
        lcd.driver.useDisp1()
        lcd.setPage(lineNumber)
        lcd.setAddress(byteNumber)
        if(byteStreamLength > 64 - byteNumber):
            for i in range(0,64-byteNumber):
                lcd.driver.lcd_byte(next(byteStream),1)
            lcd.driver.useDisp2()
            lcd.setPage(lineNumber)
            lcd.setAddress(0)
            for i in range(64-byteNumber,byteStreamLength-1):
                lcd.driver.lcd_byte(next(byteStream),1)
            return
        else:
            for i in range(0,byteStreamLength-1):
                lcd.driver.lcd_byte(next(byteStream),1)
            return
    else:
        lcd.driver.useDisp2()
        lcd.setPage(lineNumber)
        lcd.setAddress(byteNumber-64)
        for i in range (0,byteStreamLength-1):
            lcd.driver.lcd_byte(next(byteStream),1)


def clearDisplay(screen):
    global currentScreen
    currentScreen = screen
    lcd.lcd_cls()

if __name__ == "__main__":
    clearDisplay(0)
    print("hi")
    displayText("{:^21}".format("Project Hexa"),3,1,0)
    displayText("{:^21}".format(" Welcomes You!! "),4,1,0)
    clearDisplay(1)
    displayText("{:^21}".format("Project Hexa"),3,1,1)
    displayText("{:^21}".format(" Welcomes You!! "),4,1,1)

#    GPIO.cleanup()

