import RPi.GPIO as GPIO
import database
import fpsDriver as fps
import idleScreen as ids
import miniStatementScreen as mss
import rechargeScreen as rs
import paymentScreen as ps
import userRegistrationScreen as urs
#import kbh
import messageScreen as ms
import time
import binascii
import evdev


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
        if kb.kbhit() or GPIO.input(GIO_fps) == 0 or GPIO.input(GIO_back) == 0 or GPIO.input(GIO_pay) == 0 or GPIO.input(GIO_rech) == 0 or GPIO.input(GIO_reg) == 0:
            break
        else:
            GPIO.output(8,True)
            GPIO.output(11,True)

            if time.time()-flagtime > 0.25:

                GPIO.output(8,False)
                GPIO.output(11,False)
                flagtime = time.time()

kptime = 0
def kbhit():
    global key
    global kptime
    try:
        # keypress = 1
        for event in device.read():
            if event.type == evdev.ecodes.EV_KEY:
                # keypress = 0
                if event.code != 69:
                    key = event.code
                    kptime = event.timestamp()
    except BlockingIOError:
        return time.time() - kptime < 0.05

state = 0
key = 0
try:
    global state
    device = evdev.InputDevice('/dev/input/event0')
    GIO_reg = 23
    GIO_rech = 24
    GIO_pay = 25
    GIO_back = 8
    GIO_fps = 18
    GIO_green = 12
    GIO_red = 16
    keyclock = 0
    keypress = 0
    fps.autoIdentifyStop()
    fps.autoIdentifyStart()
    mobileNumber = ""
    amount = ""
    fingerRegistrationGo = 0
    screenTime = 0
    flagtime = 0
    # state 0 - idle_Screen mode
    # state 1 - registration mode
    # state 2 - recharge mode
    # state 3 - payment mode
    # state 4 - ministatement mode
    # state 5 - screen waiting
    kptime = time.time()-5
    kcode = {
        82:'0',
        79:'1',
        80:'2',
        81:'3',
        75:'4',
        76:'5',
        77:'6',
        71:'7',
        72:'8',
        73:'9',
        83:'.',
        96:chr(13),
        #96:'2',
        14:chr(127),
        78:'+',
        74:'-',
        55:'*',
        98:'/'
        }

    #kb = kbh.KBHit()


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GIO_reg, GPIO.IN, pull_up_down = GPIO.PUD_UP) # register
    GPIO.setup(GIO_rech, GPIO.IN, pull_up_down = GPIO.PUD_UP) # recharge
    GPIO.setup(GIO_pay, GPIO.IN, pull_up_down = GPIO.PUD_UP) # payment
    GPIO.setup(GIO_back, GPIO.IN, pull_up_down = GPIO.PUD_UP) # back
    GPIO.setup(GIO_fps, GPIO.IN, pull_up_down = GPIO.PUD_UP) # FPS Interrupt
    GPIO.setup(GIO_green,GPIO.OUT) #buzzer # now green
    GPIO.setup(GIO_red,GPIO.OUT) #red

    ids.state10()


    while True:
        global state
        if GPIO.input(GIO_fps) == 0:
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
                    if GPIO.input(GIO_fps) == 1:
                        break
                ids.state10()
                state = 0
                mss.currentState = 0
                amount = ""
                mobileNumber = ""

        if kbhit():
            x = kcode[key]
            print(key,ord(x),keypress)
            if keypress == 0:    
                keypress = 1
                keyclock = time.time()
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
                        elif kcode[key] == "-":
                            ids.state10()
                            state = 5
                            ps.currentState = 0
                            amount = ""
                            mobileNumber = ""
                            screenTime = time.time() + 5
                        elif ord(x) == 13 or ord(x) == 10:
                            ps.state20(amount)
                            fps.autoIdentifyStart()
                            while True:
                                if GPIO.input(GIO_fps) == 0:
                                    print("fps interrupt in payment mode")
                                    ps.state30()
                                    fres = fps.identify()
                                    if fres[0] == 1:
                                        fps.autoIdentifyStop()
                                        transr = database.trans(fres[1], int(amount), '-', 1001)
                                        if transr[0] == 1:
                                            ps.state40(str(amount),str(fres[1]))
                                        elif transr[0] == 2:
                                            ps.state31(str(amount))
                                            while True:
                                                if GPIO.input(GIO_fps) == 1:
                                                    break
                                            fps.autoIdentifyStart()
                                        else:
                                            ps.state32(str(transr[1]))
                                        break
                                    else:
                                        ps.state31(str(amount))
                                        while True:
                                            if GPIO.input(GIO_fps) == 1:
                                                break
                                elif GPIO.input(GIO_back) == 0:
                                    ids.state10()
                                    break
                                elif kbhit():
                                    if ord(kcode[key]) == 127:  # backspace
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
                        elif kcode[key] == "-":
                            ids.state10()
                            state = 5
                            rs.currentState = 0
                            amount = ""
                            mobileNumber = ""
                            screenTime = time.time() + 5
                        elif ord(x) == 13 or ord(x) == 10:
                            rs.state20(amount)
                            fps.autoIdentifyStart()
                            while True:
                                if GPIO.input(GIO_fps) == 0:
                                    print("fps interrupt in recharge mode")
                                    rs.state30()
                                    fres = fps.identify()
                                    print("fres >>", fres)
                                    if fres[0] == 1:
                                        fps.autoIdentifyStop()
                                        transr = database.trans(fres[1], int(amount), '+', 1001)
                                        print ("transr >>", transr)
                                        if transr[0] == 1:
                                            rs.state40(str(amount), str(transr[1]),str(fres[1]))
                                            break
                                        else:
                                            rs.state31(amount) # "fatal" exeption to be handled
                                            while True:
                                                if GPIO.input(GIO_fps) == 1:
                                                    break
                                            fps.autoIdentifyStart()
                                    else:
                                        rs.state31(amount)
                                        while True:
                                            if GPIO.input(GIO_fps) == 1:
                                                break
                                elif GPIO.input(GIO_back) == 0:
                                    ids.state10()
                                    break
                                elif kbhit():
                                    if ord(kcode[key]) == 127:  # backspace
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
                        elif ord(kcode[key]) == 127: # backspace
                            print("backspace start>>", len(mobileNumber))
                            mlen = len(mobileNumber)
                            mobileNumber = mobileNumber[0:mlen-1]
                            print("backspace end>>", len(mobileNumber))
                            urs.state40(mobileNumber)
                        elif kcode[key] == "-":
                            ids.state10()
                            state = 0
                            urs.currentState = 0
                            amount = ""
                            mobileNumber = ""

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
                                        if GPIO.input(GIO_fps) == 0:
                                            if fps.identify()[0] == 0:
                                                fps.autoIdentifyStop()
                                                if True: # fps.doubleRegistration()[0] == 1:
                                                    if fps.initiateRegistration(mobileNumber)[0] == 1:
                                                        urs.state101()
                                                        while True:
                                                            if GPIO.input(GIO_fps) == 1:
                                                                break
                                                        while True:
                                                            if GPIO.input(GIO_fps) == 0:
                                                                break
                                                            # elif kbhit():
                                                            #     if ord(x) == 127:  # backspace
                                                            #         ids.state10()
                                                                    
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
                                        elif GPIO.input(GIO_back) == 0 or (kcode[key] == "-" and kbhit()):
                                            ids.state10()
                                            state = 0
                                            urs.currentState = 0
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
                        elif ord(kcode[key]) == 127:  # backspace
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



        elif GPIO.input(GIO_reg) == 0:
            if state == 0 or state == 5:
                registermode()


        elif GPIO.input(GIO_rech) == 0:
            if state == 0 or state == 5:
                rechargemode()


        elif GPIO.input(GIO_pay) == 0:
            if state == 0 or state == 5:
                paymentmode()


        elif GPIO.input(GIO_back) == 0:
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
            pass
        if (time.time() - keyclock > 0.30) and keyclock != 0 and keypress == 1:
            keypress = 0
            keyclock = 0
            print('is now zero')


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
    ms.msg('Exited Program!!!')
    database.conn.close()
    #database.cursor.close()
    GPIO.cleanup()
    fps.serialport.close()
