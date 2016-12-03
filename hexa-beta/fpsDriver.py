__author__ = 'guru'
import serial
import binascii


serialport = serial.Serial("/dev/ttyAMA0", timeout=10)
serialport.baudrate = 9600
serialport.flush()

autoid = 0




def fpsTransmitter(data):
    question =  binascii.unhexlify(data)
    print("string trans >",data)
    serialport.flush()    
    serialport.write(question)

def fpsReceiver():
    str = binascii.hexlify(serialport.read(12)).decode("utf-8")
    print("string res   >",str)
    return str

def fpsReceiverWithExtraData():
    str = binascii.hexlify(serialport.read(12)).decode("utf-8")
    if str[12:16] == "0500":
        str = str + binascii.hexlify(serialport.read(5)).decode("utf-8")
    print("string res   >",str)
    return str

def fpsTemplateReceiver():
    str = binascii.hexlify(serialport.read(12)).decode("utf-8")
    if str[12:16] == "5006":
        str = str + binascii.hexlify(serialport.read(1616)).decode("utf-8")
    print("string res   >",str)
    return str
#checksum calculator
def checkSum(dataString,write):
    totalSum = 0
    for i in range(0,22):
        if( i%2 == 0):
            totalSum += int(dataString[i:i+2],16)
    checkSum = dataString[22:24]
    tempString = hex(totalSum)[::-1]     #[::-1] reverses the string
    if((tempString[0:2][::-1] == checkSum) or (write == 1)):
        chkString = tempString[0:2][::-1]
        return (1,chkString)
    else:
        chkString = '0'
        return (0,chkString)

#adds all the chunks
def dataCompiler(channel,command,param11,param12,param21,param22,dataSize11,dataSize12,dataSize21,dataSize22,errCode):
    All = (channel+command+param11+param12+param21+param22+dataSize11+dataSize12+dataSize21+dataSize22+errCode+'00')
    temp = checkSum(All,1)
    if( temp[0] == 1):
        All = All[0:22]
        All+=temp[1]
        return All
    else:
        return 0


#0x50 command starts the registration by finger info
def initiateRegistration(mobileNumber):
    data = dataCompiler('00','50','ff','ff','00','00','05','00','00','00','00')
    fpsTransmitter(data+mobileNumber)
    str=fpsReceiver()
    chk=checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == '50' and str[4:6] == 'ff' and str[6:8] == 'ff' and str[20:22] == '00'):
            return (1,'00')
        else:
            return (0,'00')
    else:
        return (0,str[20:22])

#0x51 command ends registration
def terminateRegistration():
    data = dataCompiler('00','51','00','00','00','00','00','00','00','00','00')
    fpsTransmitter(data)
    str=fpsReceiver()
    chk=checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == '51' and str[20:22] == '00'):
            return (1,'00')
        else:
            return (0,'00')
    else:
        return (0,str[20:22])


#0x19 command for including 2nd finger --- One time allow two different fingerprints during registration
def doubleRegistration():
    data = dataCompiler('00','19','00','00','00','00','00','00','00','00','00')
    fpsTransmitter(data)
    str = fpsReceiver()
    chk = checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == '19' and str[4:6] == '00' and str[6:8] == '00' and str[20:22] == '00'):
            return (1,'00')
        else:
            return (0,'00')
    else:
        return (0,str[20:22])

#0xA3 command for getting input from finger print
def identify():
    str=fpsReceiverWithExtraData()
    if len(str) == 0:
        return 2,2
    chk = checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == 'a3' and str[4:6] == 'ff' and str[6:8] == 'ff' and str[12:14] == '05' and str[20:22] =='00'):
            return (1,str[24:34])
        else:
            return (0,'00')
    else:
        return (0,str[20:22])

#get's template of respective mobileNumber
def getTemplateGenerator(mobileNumber):
    data = dataCompiler('00','73','ff','ff','00','00','05','00','00','00','00')
    fpsTransmitter(data+mobileNumber)
    str = fpsTemplateReceiver()
    chk=checkSum(str[0:24],0)
    if (chk[0] == 1):
        if(str[2:4] == '73' and str[4:6] == 'ff' and str[6:8] == 'ff' and str[3232:3242] == mobileNumber):
            #template1 = str[32:3232]
            #template2 = str[1632:3232]

            return (1,str[32:1632],str[1632:3232])
        else:
            return (0,'00')
    else:
        return (0,str[20:22])


#def putTemplateGenerator():

#    print("function under construction")

def autoIdentifyStart():
    global autoid
    autoid = 1
    fpsTransmitter('00a1010000000000000000a2')
    str = fpsTemplateReceiver()
    chk = checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == 'a1' and str[20:22] =='00'):
            return (1,'00')
        else:
            return (0,'00')
    else:
        return (0,str[20:22])


def autoIdentifyStop():
    global autoid
    autoid = 0
    fpsTransmitter('00a2000000000000000000a2')
    str = fpsTemplateReceiver()
    chk = checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == 'a2' and str[20:22] =='00'):
            return (1,'00')
        else:
            return (0,'00')
    else:
        return (0,str[20:22])



def identifySingle():
    data = dataCompiler('00','56','00','00','00','00','00','00','00','00','00')
    fpsTransmitter(data)
    str=fpsReceiverWithExtraData()
    chk=checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == '56' and str[4:6] == 'ff' and str[6:8] == 'ff' and str[12:14] == '05' and str[20:22] =='00'):
            return (1,str[24:34])
        else:
            return (0,'00')
    else:
        return (0,str[20:22])


def makeTemplateStart():
    data = dataCompiler('00', '35', '00', '00', '00', '00', '00', '00', '00', '00', '00')
    fpsTransmitter(data)
    str = fpsReceiver()
    if checkSum(str, 0)[0]:
        if str[2:4] == '35' and str[20:22] == '00':
            return 1
        else:
            return 0
    else:
        return 0

def makeTemplateContinue():
        data = dataCompiler('00', '36', '00', '00', '00', '00', '00', '00', '00', '00', '00')
        fpsTransmitter(data)
        str = fpsReceiver()
        if checkSum(str, 0)[0]:
            if str[2:4] == '36' and str[20:22] == '00':
                return 1
            else:
                return 0
        else:
            return 0
#delete single user
def SingleUserDelete(mobileNumber):
    data = dataCompiler('00', '72', 'ff', 'ff', '00', '00', '05', '00', '00', '00', '00')
    fpsTransmitter(data + mobileNumber)
    str = fpsReceiver()
    chk = checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == '72' and str[20:22] =='00'):
            return (1,'00')
        else:
            return (0,'00')
    else:
        return (0,str[20:22])

#clears the database
def clearFullDatabase():
    data = dataCompiler('00', '76', '00', '00', '00', '00', '00', '00', '00', '00', '00')
    fpsTransmitter(data)
    str = fpsReceiver()
    chk = checkSum(str,0)
    if (chk[0] == 1):
        if(str[2:4] == '76' and str[20:22] =='00'):
            return (1,'00')
        else:
            return (0,'00')
    else:
        return (0,str[20:22])




if __name__ == "__main__":
    print("1. for normal method reg\n2. for checking template presence")
    op = input()
    if op == '1':
        print("Enter Mobile Number:")
        phn = input()
        if identifySingle()[0] == 0:
            doubleRegistration()
            if initiateRegistration(str(phn))[0]:
                print ("input any char to continue")
                input()
                if terminateRegistration()[0]:
                    print ("input any char to for 2nd finger")
                    input()
                    print("done")
                    print(getTemplateGenerator(phn))
        else:
            print("user already exist")
    elif op == '2':
        print("place your finger")

