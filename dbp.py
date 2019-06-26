import sqlite3
class Account:
    """
    serialno,holder,address
    """
    def __init__(self,serialno,holder,address):
        self.serialno=serialno
        self.holder=holder
        self.address=address

    def insertDB(self):
        conn=sqlite3.connect('accountsinfo.db')
        cur=conn.cursor()
        cur.execute('INSERT INTO Account(SerialNo,AccountHolder,Address) values(?,?,?)',(self.serialno,self.holder,self.address))
        conn.commit()

    def deposit(self,amount):
        conn=sqlite3.connect('accountsinfo.db')
        cur=conn.cursor()
        cur.execute('INSERT INTO Deposits(SerialNo,Amount) values(?,?)',(self.serialno,amount))
        conn.commit()
        cur.close()

    def withdraw(self,amount):
        conn=sqlite3.connect('accountsinfo.db')
        balance=0.0
        cur=conn.cursor()
        cursor=cur.execute("SELECT sum(Amount) from Deposits where SerialNo=?",(self.serialno,))
        row = cur.fetchone()
        if row == None:
            pass
        else:
            balance=float(row[0])
        cur1=conn.cursor()
        cur1.execute("SELECT sum(Amount) from Withdrawal where SerialNo=?",(self.serialno,))
        try:
            for row1 in cur1:
                balance=balance-float(row1[0])
        except:
            pass
        if amount>balance:
            print('Not enough balance')
            return
        cur=conn.cursor()
        cur.execute('INSERT INTO Withdrawal(SerialNo,Amount) values(?,?)',(self.serialno,amount))
        conn.commit()
        cur.close()

    def __str__(self):
        conn=sqlite3.connect('accountsinfo.db')
        cur=conn.cursor()
        balance=0.0
        cursor=cur.execute("SELECT sum(Amount) from Deposits where SerialNo=?",(self.serialno,))
        row = cur.fetchone()
        if row == None:
            pass
        else:
            balance=float(row[0])
        cur1=conn.cursor()
        cur1.execute("SELECT sum(Amount) from Withdrawal where SerialNo=?",(self.serialno,))
        try:
            for row1 in cur1:
                balance=balance-float(row1[0])
        except:
            pass
                
        #else:
            #balance=balance-float(row1[0]) 
                
        return('AccountNo:'+self.serialno+',Name:'+self.holder+',Balance:'+str(balance))
        cur.close()

def displayall():
     conn=sqlite3.connect('accountsinfo.db')
     cur=conn.cursor()
     cursor=cur.execute("SELECT * from Account")
     for row in cursor:
         print(row)
     cur.close()

def displaySavingsAccount():
     conn=sqlite3.connect('accountsinfo.db')
     cur=conn.cursor()
     cursor=cur.execute("SELECT * from Account")
     for row in cursor:
         if row[0][0]=='S':
            print(row)
     cur.close()

def displayCurrentAccount():
     conn=sqlite3.connect('accountsinfo.db')
     cur=conn.cursor()
     cursor=cur.execute("SELECT * from Account")
     for row in cursor:
         if row[0][0]=='C':
            print(row)
     cur.close()

def displayAccountbyName(name):
    conn=sqlite3.connect('accountsinfo.db')
    cur=conn.cursor()
    cursor=cur.execute("SELECT * from Account")
    for row in cursor:
        if row[1]==name:
            print(row)
    cur.close()


def loadDB():
    global l
    conn=sqlite3.connect('accountsinfo.db')
    cur=conn.cursor()
    cursor=cur.execute("SELECT * from Account")
    for row in cursor:
        d=Account(row[0],row[1],row[2])
        l.append(d)
    cur.close()

def auth():
    uname=input('Enter user name')
    pwd=input('Enter password')
    if uname=="aa" and pwd=="pp":
        return True
    return False

def menu():
    global l
    loadDB()
    act=False
    while True:
        print('*****Account Operations******')
        print('1: Account Creation')
        print('2: Account Information')
        print('3: Deposit')
        print('4: Withdraw')
        print('5: Reports-All Accounts in DB')
        print('6: Reports-All SB Accounts in DB')
        print('7: Reports-All Current Accounts in DB')
        print('8: Reports-Account Info by Name')
        print('9: Exit')
        opt=int(input('Enter option'))
        if opt==1:
            act=auth()
            if(act):
                name=input('Enter Account Holder Name').strip()
                typ=input('Account Type: Savings-S, Current-C').strip()
                addr=input('Enter Holder address').strip()
                year=int(input('Year of creation'))
                init=input('Holder initials').strip()
                serialno=typ+init+str(year)
                d=Account(serialno,name,addr)
                l.append(d)
                d.insertDB()
        elif opt==2:
            serialno=input('Enter serialno for info')
            for o in l:
                if o.serialno==serialno:
                    print(o)
                    break
        
        elif opt==3:
            serialno=input('Enter serialno')
            amt=float(input('Enter amount'))
            for o in l:
                if o.serialno==serialno:
                    o.deposit(amt)
                    break
        elif opt==4:
            serialno=input('Enter serialno')
            amt=float(input('Enter amount'))
            for o in l:
                if o.serialno==serialno:
                    o.withdraw(amt)
                    break
        elif opt==5:
            displayall()

        elif opt==6:
            displaySavingsAccount()

        elif opt==7:
            displayCurrentAccount()

        elif opt==8:
            name=input('Enter account holder name')
            displayAccountbyName(name)

        elif opt==9:
            print('Thank u..')
            break
        else:
            print('invalid command')


l=list()
menu()
            
        
        
