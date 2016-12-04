__author__ = 'guru'
import sqlite3
import os.path
import sys

conn = sqlite3.connect('hexabeta.db')

print("Opened database successfully")


def createtables():
    conn.execute('''CREATE TABLE IF NOT EXISTS CustomerDetails
       (MobileNumber CHAR(10) PRIMARY KEY NOT NULL UNIQUE,
       AccountBalance REAL);''')
    print("CustomerDetails Table created successfully")
    conn.execute('''CREATE TABLE IF NOT EXISTS TransactionLogs
       (TransactionId INT PRIMARY KEY NOT NULL,
       MobileNumber CHAR(10) NOT NULL,
       TransactionType CHAR NOT NULL,
       DateTime TEXT NOT NULL,
       VendorId INT NOT NULL,
       Amount REAL NOT NULL);''')
    print("transaction logs Table created successfully")
    conn.execute('''CREATE TABLE IF NOT EXISTS VendorLogs
       (LogId INT PRIMARY KEY NOT NULL,
       DeviceId INT NOT NULL,
       VendorId INT NOT NULL,
       UserId INT NOT NULL,
       DateTime TEXT NOT NULL);''')
    print("vendor logs Table created successfully")
    conn.execute('''CREATE TABLE IF NOT EXISTS VendorDetails
       (VendorId INT PRIMARY KEY     NOT NULL,
       VendorName CHAR(3) NOT NULL,
       VendorBalance REAL NOT NULL);''')
    print("vendor details Table created successfully")
    conn.execute('''CREATE TABLE IF NOT EXISTS VendingUserDetails
       (UserId INT PRIMARY KEY     NOT NULL,
       VendorId INT NOT NULL,
       AccessPin INT );''')
    print("vendor User details Table created successfully")
    conn.execute('''CREATE TABLE IF NOT EXISTS FPTemplatedb
       (MobileNumber CHAR(10) PRIMARY KEY NOT NULL UNIQUE,
       template1 BLOB,
       template2 BLOB);''')
    print("FingerPrint Template Table created successfully")

def registerVendor(VendorId, VendorName = "NULL", VendorBalance = 0.00):
    conn.execute("INSERT INTO VendorDetails (VendorId, VendorName, VendorBalance) \
      VALUES (?, ?, ?)", (VendorId, VendorName, VendorBalance))
    conn.commit()
    print("Vendor created successfully")

def registerVendingUser(UserId, VendorId, AccessPin):
    conn.execute("INSERT INTO VendorDetails (UserId, VendorId, AccessPin) \
      VALUES (?, ?, ?)", (UserId, VendorId, AccessPin))
    conn.commit()
    print("Vending user created successfully")

def createVendorLog(LogId, DeviceId, VendorId, UserId, DateTime):
    conn.execute("INSERT INTO VendorDetails (LogId, DeviceId, VendorId, UserId, DateTime) \
      VALUES (?, ?, ?, ? ,?)", (LogId, DeviceId, VendorId, UserId, DateTime))
    conn.commit()
    print("Vendor log created successfully")

def registerUser (MobileNumber, VendorId, AccountBalance = 0):
    conn.execute("INSERT INTO CustomerDetails (MobileNumber,AccountBalance) \
      VALUES (?, ?)", (MobileNumber, 0))
    conn.commit()
    trans(MobileNumber, AccountBalance, '+', VendorId)
    conn.commit()
    print("Records created successfully")

def trans(MobileNumber, Amount, TransactionType, VendorId):
    if verifyMobileNumber(MobileNumber)[0] == 1:
        return 2, 0  # account not found in db
    currentBalance=getbal(MobileNumber)
    if(TransactionType == '-'):
        if(currentBalance<Amount):
            return 0, currentBalance
    if (os.path.isfile("transid.dat")):
        fo = open("transid.dat", "rb+")
        tid = fo.read()
        tid = tid.decode('utf-8')
        tid = int(tid)
        tid += 1
        fo.seek(0)
        fo.truncate()
        fo.write(bytes(str(tid), 'UTF-8'))
    else:
        fo = open("transid.dat", "ab")
        tid = 1
        fo.write(bytes(str(tid), 'UTF-8'))
    fo.close()
    DateTime = getDateTime()
    conn.execute("INSERT INTO TransactionLogs (TransactionId,MobileNumber,TransactionType, DateTime, VendorId ,Amount) \
      VALUES (?, ?, ?, ?, ?,     ? )",(tid, MobileNumber, TransactionType, DateTime, VendorId, Amount))
    if (TransactionType == '+'):
        t = currentBalance + Amount
        # s = "UPDATE CustomerDetails SET AccountBalance = %d WHERE MobileNumber = '{!s}'" .format(t, MobileNumber)
        conn.execute("UPDATE CustomerDetails SET AccountBalance = ? WHERE MobileNumber = ?",(t, MobileNumber))
    elif(TransactionType == '-'):
        t = currentBalance - Amount
        # s = "UPDATE CustomerDetails SET AccountBalance = %d WHERE MobileNumber = '{!s}'" .format(t, MobileNumber)
        conn.execute("UPDATE CustomerDetails SET AccountBalance = ? WHERE MobileNumber = ?",(t, MobileNumber))
    conn.commit()
    print("Records created successfully id = %d"%(tid))
    return 1, getbal(MobileNumber)

def getDateTime():
    for row in conn.execute('SELECT datetime("now","localtime")'):
        return row[0]

def getbal(MobileNumber):
    # s = "SELECT AccountBalance from CustomerDetails WHERE MobileNumber = %s" % MobileNumber
    cursor = conn.execute("SELECT AccountBalance from CustomerDetails WHERE MobileNumber = ?", (MobileNumber,))
    for row in cursor:
        return row[0]
    return -1

def getLastTransactions(MobileNumber, count = 3):
    cursor = conn.execute("SELECT * FROM TransactionLogs  WHERE MobileNumber = ? ORDER BY DateTime DESC LIMIT ?", (MobileNumber, count,))
    a = [1]
    for row in cursor:
        a.append(row)
    a[0] = len(a) - 1
    return a


def storeTemplate(MobileNumber, template1, template2):
    conn.execute("INSERT INTO FPTemplatedb (MobileNumber,template1,template2) \
      VALUES (?, ?, ?)", (MobileNumber, template1, template2))
    conn.commit()
    return 1


def displayAllTransactionLogs():
    cursor = conn.execute("SELECT *  from TransactionLogs")
    for row in cursor:
        print("\nTransactionId = ", row[0])
        print("MobileNumber = ", row[1])
        print("TransactionType = ", row[2])
        print("DateTime = ", row[3])
        print("VendorId = ", row[4])
        print("Amount = ", row[5])
    print("Operation done successfully")

def displayAllCustomerDetails():
    cursor = conn.execute("SELECT *  from CustomerDetails")
    for row in cursor:
        print("\nMobileNumber = ", (row[0]))
        print("AccountBalance = ", (row[1]))
    print("Operation done successfully")

def getFPTemplate(mobileNumber):
    cursor = conn.execute("SELECT * from FPTemplatedb WHERE MobileNumber = ?",(mobileNumber,))
    a = [1]
    for row in cursor:
        print("hi")
        a.append(row)
    return a

def verifyMobileNumber(mobileNumber):
    try:
        cursor = conn.execute("SELECT AccountBalance from CustomerDetails WHERE MobileNumber = ? ", (mobileNumber,))
        # print ("length of cursor >>",cursor)
        for row in cursor:
            p = row[0]
        # print(p)
        return 0, "Mobile number already Exist", p
    except UnboundLocalError as e:
        if e.args[0] == "local variable 'p' referenced before assignment":  # "name 'p' is not defined":
            return 1, "Mobile number not found", e
            # print("yay",e)
        else:
            print("unexpected behavior")


def cleardb():
    print('Warning!!! this will clear all your data... \n please make a backup... \n\n \n please type "7345 DB Clear" to continue... ')
    if input() == '7345 DB Clear':
        print('clearing DB Now...')
        cursor = conn.execute("DELETE FROM CustomerDetails")
        cursor = conn.execute("DELETE FROM TransactionLogs")
        cursor = conn.execute("DELETE FROM VendorLogs")
        cursor = conn.execute("DELETE FROM VendorDetails")
        cursor = conn.execute("DELETE FROM VendingUserDetails")
        cursor = conn.execute("DELETE FROM FPTemplatedb")
        if (os.path.isfile("transid.dat")):
            fo = open("transid.dat", "rb+")
            tid = 0
            fo.truncate()
            fo.write(bytes(str(tid), 'UTF-8'))
        else:
            fo = open("transid.dat", "ab")
            tid = 0
            fo.write(bytes(str(tid), 'UTF-8'))
        fo.close()

        print('all clear...')
    else:
        print('no action taken...')
        return



#createtables()
#conn.execute('.schema LOGS')
# conn.execute('tables')
#print(trans("7790844870",102,'+',1001))
# registerUser("7790844870",500, 1001)
# registerVendor(1001,"Tuck Shop", 0)
#displayAllTransactionLogs()
#print(getbal("7790844870"))
#displayAllCustomerDetails()
#print((getLastTransactions("7790844870")))
#print(getFPTemplate("7790844870"))
# print(verifyMobileNumber("7790844870"))
