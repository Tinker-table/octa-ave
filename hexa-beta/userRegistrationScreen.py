__author__ = 'guru'


#state 40 = enter the phone number
#state 61 = phone number already exist try new number
#state 100 = Ask's user to place their 1st finger on FPS
#state 101 = Ask's user to place their 2st finger on FPS
#state 20 = Scanning ur finger now
#state 30 = remove ur finger and place it again
#state 41 = sorry user fingerprint already exists
#state 50 = processing please wait
#state 60 = initial deposit info
#state 70 = Full info

#screen = 0 vendor,screen = 1 customer.

import GLCD as g

currentState = 0
fontWidth = 6
lineLength = 21


def state40(phoneNumber = ' '):
    if currentState == 40:
        num(phoneNumber)
        return
    global currentState
    currentState = 40
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Please Enter The")
    g.displayText(string,2,0,0)
    string = ("{:^%d}" % lineLength).format("Mobile Number")
    g.displayText(string,3,0,0)
    string = ("{:<%d}" % lineLength).format("Mob.No:")
    g.displayText(string,4,0,0)
    string = "{:<10}".format(phoneNumber)
    g.displayText(string,4,(7*fontWidth-1),0)
    #user Screen
    g.clearDisplay(1)
    string = ("{:<%d}" % lineLength).format("Mob.No:")
    g.displayText(string,4,0,1)
    string = "{:<10}".format(phoneNumber)
    g.displayText(string,4,(7*fontWidth-1),1)

def num(phoneNumber = " "):
    string = "{:<10}".format(phoneNumber)
    g.displayText(string,4,(7*fontWidth-1),0)

    string = "{:<10}".format(phoneNumber)
    g.displayText(string,4,(7*fontWidth-1),1)

def state61():
    global currentState
    currentState = 61
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Mobile Number is")
    g.displayText(string,3,0,0)
    string = ("{:^%d}" % lineLength).format("Already Regd.")
    g.displayText(string,4,0,0)


    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("No. Already Exists!")
    g.displayText(string,3,0,1)
    string = ("{:^%d}" % lineLength).format("Pls Try a New No.")
    g.displayText(string,4,0,1)

def state100():
    global currentState
    currentState = 100
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Registering")
    g.displayText(string,0,0,0)
    string = ("{:^%d}" % lineLength).format("Waiting For 1st Finger")
    g.displayText(string,3,0,0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Registering")
    g.displayText(string,0,0,1)
    string = ("{:^%d}" % lineLength).format("Place Ur 1st Finger")
    g.displayText(string,3,0,1)



def state101():
    global currentState
    currentState = 101
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Registering")
    g.displayText(string,0,0,0)
    string = ("{:^%d}" % lineLength).format("Waiting for ")
    g.displayText(string,3,0,0)
    string = ("{:^%d}" % lineLength).format("2nd Finger")
    g.displayText(string, 6, 0, 0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Registering")
    g.displayText(string,0,0,1)
    string = ("{:^%d}" % lineLength).format("Pls Remove ur Finger")
    g.displayText(string,3,0,1)
    string = ("{:^%d}" % lineLength).format("And Place 2nd Finger")
    g.displayText(string,5,0,1)


def state20():
    global currentState
    currentState = 20
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Scanning User's")
    g.displayText(string,2,0,0)
    string = ("{:^%d}" % lineLength).format("Finger...")
    g.displayText(string,3,0,0)
    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Scanning Your")
    g.displayText(string,2,0,1)
    string = ("{:^%d}" % lineLength).format("Finger...")
    g.displayText(string,3,0,1)


def state30():
    global currentState
    currentState = 30
    #vendor Screen

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Remove ur Finger")
    g.displayText(string,2,0,1)
    string = ("{:^%d}" % lineLength).format("And")
    g.displayText(string,3,0,1)
    string = ("{:^%d}" % lineLength).format("Place It Again")
    g.displayText(string,4,0,1)


def state41():
    global currentState
    currentState = 41
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Finger Print")
    g.displayText(string,3,0,0)
    string = ("{:^%d}" % lineLength).format("Already Exists")
    g.displayText(string,4,0,0)
    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Sorry! :(")
    g.displayText(string,2,0,1)
    string = ("{:^%d}" % lineLength).format("Finger Print")
    g.displayText(string,3,0,1)
    string = ("{:^%d}" % lineLength).format("Already Exists")
    g.displayText(string,4,0,1)


def state50():
    global currentState
    currentState = 50
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Processing...")
    g.displayText(string,2,0,1)
    string = ("{:^%d}" % lineLength).format("Please Wait")
    g.displayText(string,3,0,1)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Processing...")
    g.displayText(string,2,0,1)
    string = ("{:^%d}" % lineLength).format("Please Wait")
    g.displayText(string,3,0,1)


def state60(accountBalance = " "):
    if currentState == 60:
        s60num(accountBalance)
        return
    global currentState
    currentState = 60
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Deposit Amount")
    g.displayText(string,2,0,0)
    string = ("{:<%d}" % lineLength).format("Rs.")
    g.displayText(string,4,0,0)
    string = "{:<4}".format(accountBalance)
    g.displayText(string,5,(3*fontWidth-1),0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("How Much do You Like")
    g.displayText(string,3,0,1)
    string = ("{:<%d}" % lineLength).format("To Deposit Rs.")
    g.displayText(string,4,0,1)
    string = "{:<4}".format(accountBalance)
    g.displayText(string,5,(14*fontWidth-1),1)


def s60num(accountBalance):
    # vendor Screen
    string = "{:<4}".format(accountBalance)
    g.displayText(string, 5, (3 * fontWidth - 1), 0)

    # User Screen
    string = "{:<4}".format(accountBalance)
    g.displayText(string, 5, (14 * fontWidth - 1), 1)



def state70(phoneNumber = "0000000000", accountBalance = "000.00"):
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Registration")
    g.displayText(string,1,0,0)
    string = ("{:^%d}" % lineLength).format("Successful")
    g.displayText(string, 2, 0, 0)
    string = ("{:<%d}" % lineLength).format("Mob.No:")
    g.displayText(string,4,0,0)
    g.displayText(phoneNumber,4,(7*fontWidth-1),0)
    string = ("{:<%d}" % lineLength).format("Balance:Rs.")
    g.displayText(string,5,0,0)
    g.displayText(accountBalance,5,(11*fontWidth-1),0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Successfully Regd.")
    g.displayText(string,0,0,1)
    string = ("{:<%d}" % lineLength).format("Mob.No:")
    g.displayText(string,4,0,1)
    g.displayText(phoneNumber,4,(7*fontWidth-1),1)
    string = ("{:<%d}" % lineLength).format("Balance:Rs.")
    g.displayText(string,5,0,1)
    g.displayText(accountBalance,5,(11*fontWidth-1),1)
    string = ("{:^%d}" % lineLength).format("THANK YOU!")
    g.displayText(string,7,0,1)
