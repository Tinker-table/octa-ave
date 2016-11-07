import RPi.GPIO as GPIO
import database
import fpsDriver as fps
import idleScreen as ids
import miniStatementScreen as mss
import rechargeScreen as rs
import paymentScreen as ps
import userRegistrationScreen as urs
import kbh
import time
import binascii


def registermode():
    global state
    state = 1
    urs.currentState = 0
    fps.autoIdentifyStop()
    urs.state40()

def rechargemode():
    global state
    state = 2
    rs.currentState = 0
    fps.autoIdentifyStop()
    rs.state10('0')


def paymentmode():
    global state
    state = 3
    fps.autoIdentifyStop()
    ps.currentState = 0
    ps.state10('0')



def miniStatementmode():
    global state
    mss.currentState = 0
    state = 4



def blink():
    global flagtime
    flagtime = time.time()
    while True:
        if kb.kbhit() or GPIO.input(4) == 0 or GPIO.input(9) == 0 or GPIO.input(27) == 0 or GPIO.input(10) == 0 or GPIO.input(17) == 0:
            break
        else:
            GPIO.output(8,True)
            GPIO.output(11,True)

            if time.time()-flagtime > 0.25:

                GPIO.output(8,False)
                GPIO.output(11,False)
                flagtime = time.time()

try:
    keyclock = 0
    keypress = 0
    fps.autoIdentifyStop()
    fps.autoIdentifyStart()
    mobileNumber = ""
    amount = ""
    fingerRegistrationGo = 0
    screenTime = 0
    state = 0
    flagtime = 0
    # state 0 - idle_Screen mode
    # state 1 - registration mode
    # state 2 - recharge mode
    # state 3 - payment mode
    # state 4 - ministatement mode
    # state 5 - screen waiting


    kb = kbh.KBHit()


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP) # register
    GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP) # recharge
    GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP) # payment
    GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP) # back
    GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP) # FPS Interrupt
    GPIO.setup(12,GPIO.OUT) #buzzer # now green
    GPIO.setup(16,GPIO.OUT) #red

    ids.state10()


    while True:
        global state
        if GPIO.input(4) == 0:
            if state == 0 or state == 5:
                miniStatementmode()
            elif state == 4:
                data = fps.identify()
                if data[0] == 1:
                    mobileNumber = data[1]
                    mss.state30(mobileNumber)
                    dispData = database.getLastTransactions(mobileNumber,3)
                    bal = database.getbal(mobileNumber)
                    for i in range(1, dispData[0] + 1):
                        tDate = dispData[i][3][5:7]+'/'+dispData[i][3][8:10]+'/'+dispData[i][3][2:4]
                        tPoint = str(dispData[i][4])
                        mss.state30Trans(tDate, "TkS", dispData[i][2], str(dispData[i][5]), str(bal), i-1)
                else:
                    print ("FPS not found")
                    mss.state21()
                while True:
                    if GPIO.input(4) == 1:
                        break
                ids.state10()
                state = 0
                mss.currentState = 0
                amount = ""
                mobileNumber = ""
        if kb.kbhit():
            keyclock = time.time()
            x = kb.getch()
            if keypress == 0:
                keypress = 1
                print ("state > ", state)
                if state == 0 or state == 5:
                    if x == '1':
                        registermode()
                    elif x == '2':
                        rechargemode()
                    elif x == '3':
                        paymentmode()
                elif state == 3:
                    print("3")
                    if ps.currentState == 10:
                        if x.isdigit() and len(amount) < 4:
                            amount += x
                            ps.state10(amount)
                        elif ord(x) == 127:  # backspace
                            alen = len(amount)
                            amount = amount[0:alen - 1]
                            ps.state10(amount)
                        elif ord(x) == 13 or ord(x) == 10:
                            ps.state20(amount)
                            fps.autoIdentifyStart()
                            while True:
                                if GPIO.input(4) == 0:
                                    print("fps interrupt in payment mode")
                                    ps.state30()
                                    fres = fps.identify()
                                    if fres[0] == 1:
                                        fps.autoIdentifyStop()
                                        transr = database.trans(fres[1], int(amount), '-', 1001)
                                        if transr[0] == 1:
                                            ps.state40(str(amount))
                                        elif transr[0] == 2:
                                            ps.state31(str(amount))
                                            while True:
                                                if GPIO.input(4) == 1:
                                                    break
                                            fps.autoIdentifyStart()
                                        else:
                                            ps.state32(str(transr[1]))
                                        break
                                    else:
                                        ps.state31(str(amount))
                                        while True:
                                            if GPIO.input(4) == 1:
                                                break
                                elif GPIO.input(9) == 0:
                                    ids.state10()
                                    break
                            state = 5
                            ps.currentState = 0
                            amount = ""
                            mobileNumber = ""
                            screenTime = time.time()





                elif state == 2:
                    print("2")
                    if rs.currentState == 10:
                        if x.isdigit() and len(amount) < 4:
                            amount += x
                            rs.state10(amount)
                        elif ord(x) == 127:  # backspace
                            alen = len(amount)
                            amount = amount[0:alen - 1]
                            rs.state10(amount)
                        elif ord(x) == 13 or ord(x) == 10:
                            rs.state20(amount)
                            fps.autoIdentifyStart()
                            while True:
                                if GPIO.input(4) == 0:
                                    print("fps interrupt in recharge mode")
                                    rs.state30()
                                    fres = fps.identify()
                                    print("fres >>", fres)
                                    if fres[0] == 1:
                                        fps.autoIdentifyStop()
                                        transr = database.trans(fres[1], int(amount), '+', 1001)
                                        print ("transr >>", transr)
                                        if transr[0] == 1:
                                            rs.state40(str(amount), str(transr[1]))
                                            break
                                        else:
                                            rs.state31(amount) # "fatal" exeption to be handled
                                            while True:
                                                if GPIO.input(4) == 1:
                                                    break
                                            fps.autoIdentifyStart()
                                    else:
                                        rs.state31(amount)
                                        while True:
                                            if GPIO.input(4) == 1:
                                                break
                                elif GPIO.input(9) == 0:
                                    ids.state10()
                                    break
                            state = 5
                            rs.currentState = 0
                            amount = ""
                            mobileNumber = ""
                            screenTime = time.time()



                elif state == 4:
                    print("4")


                elif state == 1:
                    print("1")
                    if urs.currentState == 40:
                        if x.isdigit() and len(mobileNumber) < 10:
                            mobileNumber += x
                            print("is digit>>", len(mobileNumber))
                            urs.state40(mobileNumber)
                        elif ord(x) == 127: # backspace
                            print("backspace start>>", len(mobileNumber))
                            mlen = len(mobileNumber)
                            mobileNumber = mobileNumber[0:mlen-1]
                            print("backspace end>>", len(mobileNumber))
                            urs.state40(mobileNumber)
                        elif ord(x) == 13 or ord(x) == 10:
                            if len(mobileNumber) == 10:
                                if database.verifyMobileNumber(mobileNumber)[0] == 0:#.........number alerady exists
                                    urs.state61()
                                else: #.......not existing
                                    while True:
                                        if fps.autoid == 0:
                                            fps.autoIdentifyStart()
                                        if urs.currentState != 100:
                                            urs.state100()
                                        if GPIO.input(4) == 0:
                                            if fps.identify()[0] == 0:
                                                fps.autoIdentifyStop()
                                                if fps.doubleRegistration()[0] == 1:
                                                    if fps.initiateRegistration(mobileNumber)[0] == 1:
                                                        urs.state101()
                                                        while True:
                                                            if GPIO.input(4) == 1:
                                                                break
                                                        while True:
                                                            if GPIO.input(4) == 0:
                                                                break
                                                        if fps.terminateRegistration()[0] == 1:
                                                            urs.state50()
                                                            tempdata = fps.getTemplateGenerator(mobileNumber)
                                                            if tempdata[0] == 1:
                                                                tempOne =  binascii.unhexlify(tempdata[1])
                                                                tempTwo =  binascii.unhexlify(tempdata[2])
                                                                database.storeTemplate(mobileNumber, tempOne, tempTwo)
                                                                urs.state60()
                                                                break
                                                            else:
                                                                print ("template fetch error")
                                                        else:
                                                            print("terminate reg failed")
                                                    else:
                                                        print ("initiate reg failed")
                                                else:
                                                    print("double registration ack failed")
                                            else:
                                                print("poda panni")
                                        elif GPIO.input(9) == 0:
                                            ids.state10()
                                            state = 0
                                            mss.currentState = 0
                                            amount = ""
                                            mobileNumber = ""
                                            fps.autoIdentifyStop()
                                            break


                    if urs.currentState == 61:
                        mobileNumber = ""
                        if ord(x) == 13 or ord(x) == 10:
                            urs.state40()
                    if urs.currentState == 60:
                        if x.isdigit() and len(amount) < 4:
                            amount += x
                            urs.state60(amount)
                        elif ord(x) == 127:  # backspace
                            amount = amount[0:len(amount) - 1]
                            urs.state60(amount)
                        elif (ord(x) == 13 or ord(x) == 10) and len(amount) > 0:
                            database.registerUser (mobileNumber, 1001, int(amount)) # add money to account
                            urs.state70(mobileNumber, str(database.getbal(mobileNumber)))  # parameters should be from database
                            urs.currentState = 0
                            amount = ""
                            mobileNumber = ""
                            state = 5
                            screenTime = time.time()



        elif GPIO.input(17) == 0:
            if state == 0 or state == 5:
                registermode()


        elif GPIO.input(10) == 0:
            if state == 0 or state == 5:
                rechargemode()


        elif GPIO.input(27) == 0:
            if state == 0 or state == 5:
                paymentmode()


        elif GPIO.input(9) == 0:
            print('back')
            if state == 1:
                if urs.currentState == 40:
                    screenTime = time.time() - 5
                    state = 5
            if state == 2:
                if rs.currentState == 10:
                    screenTime = time.time() - 5  
                    state = 5
            if state == 3:
                if ps.currentState == 10:
                    screenTime = time.time() - 5  
                    state = 5
            if state == 5: 
                screenTime = time.time() - 5



        else:
            if (time.time() - keyclock > 0.1) and keyclock != 0:
                keypress = 0
                keyclock = 0


        if state == 0 or state == 5:
            if fps.autoid == 0:
                fps.autoIdentifyStart()

        if state == 5:
            if time.time() - screenTime > 5:
                screenTime = 0
                state = 0
                amount = ""
                mobileNumber = ""
                ids.state10()


#---------------------------------------------------------------------------------------------------------------------





finally:
    database.conn.close()
    database.cursor.close()
    GPIO.cleanup()
    fps.serialport.close()
