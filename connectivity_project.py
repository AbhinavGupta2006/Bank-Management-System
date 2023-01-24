import mysql.connector as mc
Pass=input('Enter MySQL password: ')
con=mc.connect(host='localhost',user='root',password=Pass)
cur=con.cursor()
cur.execute('create database if not exists bank')
cur.execute('use bank')
#creating tables
cur.execute('create table if not exists Customer_info(Cust_id int(5) primary key,Name varchar(50),DOB date,Gender char(1),Mobile char(10),Customer_since date);')
cur.execute('create table if not exists Account_info(Account_number bigint(12),Account_type varchar(16),Cust_id int(5),Balance_cr int(10),Balance_dr int(10),\
                   PRIMARY KEY (Account_number),FOREIGN KEY (Cust_id) REFERENCES Customer_info(Cust_id) ON DELETE CASCADE ON UPDATE CASCADE);')
cur.execute('create table if not exists Emp(Emp_id int(5) primary key,Name varchar(50),Post varchar(25),Mobile char(10),Qualification varchar(20),DOJ date,\
                   Leave_entitled int,Leave_availed int,Leave_balance int as(Leave_entitled-Leave_availed));')
cur.execute('create table if not exists Emp_details(Emp_id int(5),Mother varchar(40),Father varchar(40),Gender char(1),Marital_status varchar(2),Spouse varchar(40),\
                   FOREIGN KEY (Emp_id) REFERENCES Emp(Emp_id) ON DELETE CASCADE ON UPDATE CASCADE);')


#VIEWING CUSTOMER INFO
def C_View():
    cur.execute('select *,DATE_FORMAT(DOB,"%d-%m-%Y") as DOB,DATE_FORMAT(Customer_since,"%d-%m-%Y") as Customer_since from Customer_info,Account_info where Customer_info.Cust_id=Account_info.Cust_id;')
    result=cur.fetchall()
    for i in result:
        print('\nCust_ID: ',i[0],'\nName: ',i[1],'\nDOB: ',i[-2],'\nGender: ',i[3],'\nMobile: ',i[4],'\nCustomer since: ',i[-1],'\nAccount number: ',i[6],'\nAccount type: ',i[7],'\nCredit balance: ',i[9],'\nDebit balance: ',i[10])


#INSERTING CUSTOMER INFO
def C_inserting():
    print('==============================INSERT CUSTOMER INFO==============================')
    n=int(input('Enter Number of Records: '))
    for i in range(n):

        cid=int(input('\nEnter Customer ID: '))
        name=input('Enter Customer Name: ')
        dob=input('Date of birth(dd-mm-yyyy): ')
        gen=input('Enter Customer Gender(M/F): ')
        mob=input('Enter Mobile: ')
        C_since=input('Customer Since(dd-mm-yyyy): ')
        t=cid,name,dob,gen,mob,C_since

        acc_no=input('Enter Account Number(11-digits): ')
        acc_type=input('Enter Account Type(sb for saving account, ca for current account, cc, od, la for loan account): ')
        bal_Cr=int(input('Enter Credit Balance: '))
        bal_Dr=int(input('Enter Debit Balance: '))
        t1=acc_no,acc_type,cid,bal_Cr,bal_Dr

        cur.execute('insert into Customer_info values(%s,%s,STR_TO_DATE(%s,"%d-%m-%Y"),%s,%s,STR_TO_DATE(%s,"%d-%m-%Y"))',t)
        cur.execute('insert into Account_info values(%s,%s,%s,%s,%s)',t1)
        cur.execute('commit')
    print('INFO INSERTED SUCCESSFULLY!')


#SEARCHING CUSTOMER INFO
def C_searching():
    print('==============================SEARCH CUSTOMER INFO==============================')
    print('What do want to search with?\n[C]ust_id,[N]ame,[M]obile: ')
    ser=input()
    if ser.upper()=='C':
        take_cid=input('Enter the customer ID: ')
        t=(take_cid,)
        q='select *,DATE_FORMAT(DOB,"%d-%m-%Y") as DOB, DATE_FORMAT(Customer_since,"%d-%m-%Y") as Customer_since from Customer_info,Account_info where Customer_info.Cust_id=Account_info.Cust_id and Customer_info.Cust_id = %s ;'
        cur.execute(q,t)
        result=cur.fetchall()
        for i in result:
            print('Cust_ID: ',i[0],'\nName: ',i[1],'\nDOB: ',i[-2],'\nGender: ',i[3],'\nMobile: ',i[4],'\nCustomer since: ',i[-1],'\nAccount number: ',i[6],'\nAccount type: ',i[7],'\nCredit balance: ',i[9],'\nDebit balance: ',i[10])
    elif ser.upper()=='N':
        take_name=input('Enter the Name: ')
        t=(take_name+'%',)
        q='select *,DATE_FORMAT(DOB,"%d-%m-%Y") as DOB, DATE_FORMAT(Customer_since,"%d-%m-%Y") as Customer_since from Customer_info,Account_info where Customer_info.Cust_id=Account_info.Cust_id and Customer_info.Name like %s ;'
        cur.execute(q,t)
        result=cur.fetchall()
        for i in result:
            print('Cust_ID: ',i[0],'\nName: ',i[1],'\nDOB: ',i[-2],'\nGender: ',i[3],'\nMobile: ',i[4],'\nCustomer since: ',i[-1],'\nAccount number: ',i[6],'\nAccount type: ',i[7],'\nCredit balance: ',i[9],'\nDebit balance: ',i[10])
    elif ser.upper()=='M':
        take_mob=input('Enter the Mobile: ')
        t=(take_mob,)
        q='select *,DATE_FORMAT(DOB,"%d-%m-%Y") as DOB, DATE_FORMAT(Customer_since,"%d-%m-%Y") as Customer_since from Customer_info,Account_info where Customer_info.Cust_id=Account_info.Cust_id and Customer_info.Mobile = %s ;'
        cur.execute(q,t)
        result=cur.fetchall()
        for i in result:
            print('Cust_ID: ',i[0],'\nName: ',i[1],'\nDOB: ',i[-2],'\nGender: ',i[3],'\nMobile: ',i[4],'\nCustomer since: ',i[-1],'\nAccount number: ',i[6],'\nAccount type: ',i[7],'\nCredit balance: ',i[9],'\nDebit balance: ',i[10])


#UPDATING CUSTOMER INFO
def C_updating():
    print('==============================UPDATE CUSTOMER INFO==============================')
    cur.execute('select Cust_id,Name,Mobile from Customer_info;')
    result=cur.fetchall()
    for i in result:
        print(i)
    upd_id=input('Enter Customer ID to update: ')
    updfield=int(input('What do you want to update(\n1.Name\n2.DOB\n3.Gender\n4.Mobile\n5.Customer Since\n6.Account Number\n7.Account Type\n8.Balance Credit\n9.Balance Debit\n '))
    if updfield==1:
        CName=input('Enter Updated Name: ')
        t=CName,upd_id
        q='update Customer_info set Name=%s where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==2:
        CDOB=input('Enter Updated DOB(dd-mm-yyyy): ')
        t=CDOB,upd_id
        q='update Customer_info set DOB=STR_TO_DATE(%s,"%d-%m-%Y") where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==3:
        CG=input('Enter Updated Gender(M/F): ')
        t=CG,upd_id
        q='update Customer_info set Gender=%s where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==4:
        CMobile=input('Enter Updated Mobile: ')
        t=CMobile,upd_id
        q='update Customer_info set Mobile=%s where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==5:
        CCS=input('Enter Customer Since Date(dd-mm-yyyy): ')
        t=CCS,upd_id
        q='update Customer_info set Customer_since=STR_TO_DATE(%s,"%d-%m-%Y") where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==6:
        CAN=input('Enter Updated Account Number(11-digits): ')
        t=CAN,upd_id
        q='update Account_info set Account_number=%s where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==7:
        CAT=input('Enter Updated Account Type(s for saving account, c for current account, cc, od, l for loan account): ')
        t=CAT,upd_id
        q='update Account_info set Account_type=%s where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==8:
        CBC=input('Enter Updated Credit Balance: ')
        t=CBC,upd_id
        q='update Account_info set Balance_cr=%s where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==9:
        CBD=input('Enter Updated Debit Balance: ')
        t=CBD,upd_id
        q='update Account_info set Balance_dr=%s where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    print('\nINFO UPDATED SUCCESSFULLY!')


#DELETING CUSTOMER INFO
def C_deleting():
    print('==============================DELETE CUSTOMER INFO==============================')
    del_ask=input('Enter [C]ust_id or [N]ame to delete: ')
    if del_ask.upper()=='C':
        del_id=input('Enter Customer ID to delete: ')
        t=(del_id,)
        q='delete from Customer_info where Cust_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif del_ask.upper()=='N':
        del_name=input('Enter Name to delete: ')
        t=(del_name+'%',)
        q='delete from Customer_info where Name like %s;'
        cur.execute(q,t)
        cur.execute('commit')
    print('\nINFO DELETED SUCCESSFULLY')


#MENU FOR CUSTOMER        
def Customer_menu():
    while 1:
        print('\n==============================CUSTOMER MENU==============================')
        print('\n[V]iew, [I]nsert, [S]earch, [U]pdate, [D]elete, [E]xit')
        ask=input()
        if ask.upper()=='V':
            C_View()
        elif ask.upper()=='I':
            C_inserting()
        elif ask.upper()=='S':
            C_searching()
        elif ask.upper()=='U':
            C_updating()
        elif ask.upper()=='D':
            C_deleting()
        elif ask.upper()=='E':
            break


#VIEWING EMPLOYEE INFO
def E_View():
    cur.execute('select *,DATE_FORMAT(DOJ,"%d-%m-%Y") as DOJ from Emp,Emp_details where Emp.Emp_id=Emp_details.Emp_id;')
    result=cur.fetchall()
    for i in result:
        print('\nEmp_ID: ',i[0],'\nName: ',i[1],'\nPost: ',i[2],'\nMobile: ',i[3],'\nQualification: ',i[4],'\nDOJ: ',i[-1],'\nLeaves Entitled: ',i[6],'\nLeaves Availed: ',i[7],'\nLeaves Balance: ',i[8],'\nMother:',i[10],'\nFather: ',i[11],'\nGender: ',i[12],'\nMarital Status: ',i[13],'\nSpouse: ',i[14])


#INSERTING EMPLOYEE INFO
def E_inserting():
    print('==============================INSERT EMPLOYEE INFO==============================')
    n=int(input('Enter Number of Records: '))
    for i in range(n):

        eid=int(input('\nEnter Employee ID: '))
        ename=input('Enter Employee Name: ')
        post=input('Enter Post of Employee: ')
        emob=input('Enter Mobile: ')
        qual=input('Enter Employee Qualification: ')
        edoj=input('Date of Joining(dd-mm-yyyy): ')
        LE=input('No. of Leaves Entitled: ')
        LA=input('No. of Leaves Availed: ')
        t=eid,ename,post,emob,qual,edoj,LE,LA
        cur.execute('insert into Emp (Emp_id,Name,Post,Mobile,Qualification,DOJ,Leave_entitled,Leave_availed) values(%s,%s,%s,%s,%s,STR_TO_DATE(%s,"%d-%m-%Y"),%s,%s)',t)
        cur.execute('commit')
        
        mother=input('Employee Mother Name: ')
        father=input('Employee Father Name: ')
        gen=input('Gender(M/F): ')
        maritalStat=input('Marital Status(M/UM): ')
        if maritalStat=='M':
            spouse=input('Spouse Name: ')
        elif maritalStat=='UM':
            spouse='NA'
        t1=eid,mother,father,gen,maritalStat,spouse
        cur.execute('insert into Emp_details values(%s,%s,%s,%s,%s,%s)',t1)
        cur.execute('commit')
    print('INFO INSERTED SUCCESSFULLY!')


#SEARCHING EMPLOYEE INFO
def E_searching():
    print('==============================SEARCH EMPLOYEE INFO==============================')
    print('What do want to search with?\n[E]mp_id,[N]ame,[M]obile: ')
    ser=input()
    if ser.upper()=='E':
        take_eid=input('Enter Employee ID: ')
        t=(take_eid+'%',)
        q='select *,DATE_FORMAT(DOJ,"%d-%m-%Y") as DOJ from Emp,Emp_details where Emp.Emp_id=Emp_details.Emp_id and Emp.Emp_id = %s;'
        cur.execute(q,t)
        result=cur.fetchall()
        for i in result:
            print('Emp_ID: ',i[0],'\nName: ',i[1],'\nPost: ',i[2],'\nMobile: ',i[3],'\nQualification: ',i[4],'\nDOJ: ',i[-1],'\nLeaves Entitled: ',i[6],'\nLeaves Availed: ',i[7],'\nLeaves Balance: ',i[8],'\nMother:',i[10],'\nFather: ',i[11],'\nGender: ',i[12],'\nMarital Status: ',i[13],'\nSpouse: ',i[14])
    elif ser.upper()=='N':
        take_name=input('Enter Name: ')
        t=(take_name+'%',)
        q='select *,DATE_FORMAT(DOJ,"%d-%m-%Y") as DOJ from Emp,Emp_details where Emp.Emp_id=Emp_details.Emp_id and Emp.Name like %s;'
        cur.execute(q,t)
        result=cur.fetchall()
        for i in result:
            print('Emp_ID: ',i[0],'\nName: ',i[1],'\nPost: ',i[2],'\nMobile: ',i[3],'\nQualification: ',i[4],'\nDOJ: ',i[-1],'\nLeaves Entitled: ',i[6],'\nLeaves Availed: ',i[7],'\nLeaves Balance: ',i[8],'\nMother:',i[10],'\nFather: ',i[11],'\nGender: ',i[12],'\nMarital Status: ',i[13],'\nSpouse: ',i[14])
    elif ser.upper()=='M':
        take_mob=input('Enter Mobile: ')
        t=(take_mob,)
        q='select *,DATE_FORMAT(DOJ,"%d-%m-%Y") as DOJ from Emp,Emp_details where Emp.Emp_id=Emp_details.Emp_id and Emp.Mobile = %s;'
        cur.execute(q,t)
        result=cur.fetchall()
        for i in result:
            print('Emp_ID: ',i[0],'\nName: ',i[1],'\nPost: ',i[2],'\nMobile: ',i[3],'\nQualification: ',i[4],'\nDOJ: ',i[-1],'\nLeaves Entitled: ',i[6],'\nLeaves Availed: ',i[7],'\nLeaves Balance: ',i[8],'\nMother:',i[10],'\nFather: ',i[11],'\nGender: ',i[12],'\nMarital Status: ',i[13],'\nSpouse: ',i[14])


#UPDATING EMPLOYEE INFO
def E_updating():
    print('==============================UPDATE EMPLOYEE INFO==============================')
    cur.execute('select Emp_id,Name,Mobile from Emp;')
    result=cur.fetchall()
    for i in result:
        print(i)
    upd_id=input('Enter Emp_id to Update: ')
    updfield=int(input('What do you want to update(\n1.Name\n2.Post\n3.Mobile\n4.Qualification\n5.DOJ\n6.Leaves Entitled\n7.Leaves Availed\n8.Mother Name\n9.Father Name\n10.Gender\n11.Marital Status\n12.Spouse Name\n'))
    if updfield==1:
        EName=input('Enter Updated Name: ')
        t=EName,upd_id
        q='update Emp set Name=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==2:
        epost=input('Enter Updated Post: ')
        t=epost,upd_id
        q='update Emp set Post=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==3:
        EMobile=input('Enter updated Mobile: ')
        t=EMobile,upd_id
        q='update Emp set Mobile=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==4:
        EQual=input('Enter Updated Qualification: ')
        t=EQual,upd_id
        q='update Emp set Qualification=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==5:
        eDOJ=input('Enter Updated DOJ(dd-mm-yyyy): ')
        t=eDOJ,upd_id
        q='update Emp set DOJ=STR_TO_DATE(%s,"%d-%m-%Y") where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==6:
        le=input('Enter Updated Leave Entitled: ')
        t=le,upd_id
        q='update Emp set Leave_entitled=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==7:
        la=input('Enter updated Leave Availed: ')
        t=la,upd_id
        q='update Emp set Leave_availed=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==8:
        MN=input('Enter Updated Mother Name: ')
        t=MN,upd_id
        q='update Emp_details set Mother=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==9:
        FN=input('Enter Updated Father Name: ')
        t=FN,upd_id
        q='update Emp_details set Father=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==10:
        ugen=input('Enter Updated Gender(M/F): ')
        t=ugen,upd_id
        q='update Emp_details set Gender=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif updfield==11:
        MS=input('Enter Updated Marital Status: ')
        if MS=='M':
            ES=input('Enter Spouse Name: ')
        t=MS,upd_id
        q='update Emp_details set Marital_status=%s where Emp_id=%s;'
        cur.execute(q,t)
        t1=ES,upd_id
        q1='update Emp_details set Spouse=%s where Emp_id=%s'
        cur.execute(q1,t1)
        cur.execute('commit')
    elif updfield==12:
        ES=input('Enter Updated Spouse Name: ')
        t=ES,upd_id
        q='update Emp_details set Spouse=%s where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    print('\nINFO UPDATED SUCCESSFULLY!')


#DELETING EMPLOYEE INFO 
def E_deleting():
    print('==============================DELETE EMPLOYEE INFO==============================')
    del_ask=input('Enter [E]mp_id or [N]ame to delete: ')
    if del_ask.upper()=='E':
        del_id=input('Enter Emp_id to Delete: ')
        t=(del_id,)
        q='delete from Emp where Emp_id=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    elif del_ask.upper()=='N':
        del_name=input('Enter Name to Delete: ')
        t=(del_name+'%',)
        q='delete from Emp where Name=%s;'
        cur.execute(q,t)
        cur.execute('commit')
    print('\nINFO DELETED SUCCESSFULLY')


#MENU FOR EMPLOYEE
def Employee_menu():
    while 1:
        print('\n==============================EMPLOYEE MENU==============================')
        print('\n[V]iew, [I]nsert, [S]earch, [U]pdate, [D]elete, [E]xit')
        ask=input()
        if ask.upper()=='V':
            E_View()
        elif ask.upper()=='I':
            E_inserting()
        elif ask.upper()=='S':
            E_searching()
        elif ask.upper()=='U':
            E_updating()
        elif ask.upper()=='D':
            E_deleting()
        elif ask.upper()=='E':
            break


#MAIN MENU
while True:
    print('\n==============================MAIN MENU==============================')
    ask=input('[C]ustomer Menu , [E]mployee Menu ,[I]nformation Analysis, [Q]uit: ')
    if ask.upper()=='C':
        Customer_menu()
    elif ask.upper()=='E':
        Employee_menu()
    elif ask.upper()=='Q':
        print('Thanks for using BANK MANAGEMENT SYSTEM.')
        print('Made by *****ABHINAV GUPTA*****')
        break
