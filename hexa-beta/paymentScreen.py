__author__ = 'guru'
#state 10 = payment amount
#state 20 = Ask's user to place their finger on FPS
#state 30 = Scanning ur finger now
#state 31 = account not found
#state 32 = no enough balance
#state 40 = payment successful

#screen = 0 vendor,screen = 1 customer.

import GLCD as g

currentState = 0
fontWidth = 6
lineLength = 21


def state10(paymentAmount = " "):
    global currentState
    if currentState == 10:
        num(paymentAmount)
        return
    currentState = 10
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Payment Amount")
    g.displayText(string,2,0,0)
    string = ("{:<%d}" % lineLength).format("Rs.")
    g.displayText(string,3,0,0)
    string = "{:<4}".format(paymentAmount)
    g.displayText(string,3,(3*fontWidth-1),0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Payment Amount")
    g.displayText(string,2,0,1)
    string = ("{:<%d}" % lineLength).format("Rs.")
    g.displayText(string,3,0,1)
    string = "{:<4}".format(paymentAmount)
    g.displayText(string,3,(3*fontWidth-1),1)


def num (paymentAmount):
    # vendor Screen
    string = "{:<4}".format(paymentAmount)
    g.displayText(string,3,(3*fontWidth-1),0)
    # User Screen
    string = "{:<4}".format(paymentAmount)
    g.displayText(string,3,(3*fontWidth-1),1)


def state20(amount = "0"):
    global currentState
    currentState = 20
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:<%d}" % lineLength).format(" Pay Rs. ")
    g.displayText(string, 1, 0, 0)
    g.displayText(amount + " ?", 1, (9 * fontWidth - 1), 0)
    string = ("{:^%d}" % lineLength).format("Waiting For Finger")
    g.displayText(string,3,0,0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:<%d}" % lineLength).format(" Pay Rs. ")
    g.displayText(string, 1, 0, 1)
    g.displayText(amount + " ?", 1, (9 * fontWidth - 1), 1)
    string = ("{:^%d}" % lineLength).format("Place Ur Finger")
    g.displayText(string,3,0,1)




def state30():
    global currentState
    currentState = 30
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Scanning User's")
    g.displayText(string,2,0,0)
    string = ("{:^%d}" % lineLength).format("Finger...")
    g.displayText(string,3,0,0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Scanning your")
    g.displayText(string,2,0,1)
    string = ("{:^%d}" % lineLength).format("Finger...")
    g.displayText(string,3,0,1)

def state31(amount):
    global currentState
    currentState = 31
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Account Not Found")
    g.displayText(string,0,0,0)
    string = ("{:^%d}" % lineLength).format("Try again")
    g.displayText(string,1,0,0)
    string = ("{:<%d}" % lineLength).format(" Pay Rs. ")
    g.displayText(string, 3, 0, 0)
    g.displayText(amount + " ?", 3, (9 * fontWidth - 1), 0)
    string = ("{:^%d}" % lineLength).format("Waiting For Finger")
    g.displayText(string,4,0,0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Oops! Account Not Found!")
    g.displayText(string,0,0,1)
    string = ("{:^%d}" % lineLength).format("Try again")
    g.displayText(string,1,0,1)
    string = ("{:<%d}" % lineLength).format(" Pay Rs. ")
    g.displayText(string, 3, 0, 1)
    g.displayText(amount + " ?", 3, (9 * fontWidth - 1), 1)
    string = ("{:^%d}" % lineLength).format("Waiting For Finger")
    g.displayText(string,4,0,1)



def state32(currentBalance = " "):
    global currentState
    currentState = 32
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Insufficient Balance")
    g.displayText(string,3,0,0)
    string = ("{:<%d}" % lineLength).format("Balance Rs.")
    g.displayText(string,4,0,0)
    g.displayText(currentBalance,4,(11*fontWidth-1),0)

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Insufficient BALANCE")
    g.displayText(string, 3, 0, 1)
   # string = ("{:^%d}" % lineLength).format("We've all been there!")
   # g.displayText(string,5,0,1)
    string = ("{:<%d}" % lineLength).format("Balance Rs.")
    g.displayText(string,5,0,1)
    g.displayText(currentBalance,5,(11*fontWidth-1),1)




def state40(paymentAmount = " ",mobileNumber = " "):
    global currentState
    currentState = 40
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format("Payment Successful")
    g.displayText(string,0,0,0)
    string = ("{:<%d}" % lineLength).format("Rs.")
    g.displayText(string,1,0,0)
    g.displayText(paymentAmount,1,(3*fontWidth-1),0)
    string = ("{:^%d}" % lineLength).format("Mobile Number:")
    g.displayText(string,2,0,0)
    g.displayText(mobileNumber,3,0,0)


    #user Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format("Payment Successful")
    g.displayText(string,0,0,1)
    string = ("{:<%d}" % lineLength).format("Rs.")
    g.displayText(string,1,0,1)
    g.displayText(paymentAmount,1,(3*fontWidth-1),1)
    string = ("{:^%d}" % lineLength).format("Mobile Number:")
    g.displayText(string,2,0,1)
    g.displayText(mobileNumber,3,0,1)

