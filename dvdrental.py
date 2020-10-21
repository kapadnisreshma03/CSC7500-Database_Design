import mysql.connector
from userauthentication import userAuthentication
from datetime import date, datetime, timedelta

global cnx
global cursor
global userid


def adddvd():
    dvdname=input("Enter the DVD name: ")
    dvdgenre=input("Enter the DVD Genre: ")
    rent=int(input("Enter the rental price: "))
    querystr="insert into dvd(dvd_name,dvd_genre,rent_price,dvd_owner_id) values('%s','%s',%d, %d)" %(dvdname,dvdgenre,rent,userid)
    query=(querystr)
    cursor.execute(query)
    dvdid=cursor.lastrowid
    cnx.commit()
    print("DVD Added successfully !!\n\n")
    exit()

def searchdvd():
    dvdgenre=input("Enter the DVD Genre to search: ")
    query="select dvd_id,dvd_name,rent_price from dvd where dvd_genre='"+ dvdgenre +"' "
    cursor.execute(query)
    print('{:^10}' '{:20}' '{:10}'.format('DVD ID','DVD Name','Rent Price'))
   
    for(dvd_id,dvd_name,rent_price)in cursor:
        print('{:^10}' '{:20}' '{:10}'.format(dvd_id,dvd_name,str(rent_price)))
    exit()
       
#if dvd_id is not the dvd table and dvd status is 0 then cannot borrow dvd
#if the above check passes then we are ready to borrow the dvd.
# check_dvd_status function returns bool.
# True - check passed
# False - check failed 
def check_dvd_status(dvdid):
    query="select dvd_name,dvd_status,dvd_owner_id from dvd where dvd_id="+ str(dvdid) 
    cursor.execute(query)
    if(cursor.rowcount==0):
        print("DVD ID doesn't exists")
        return False
    """
    row = cursor.fetchone()
    dvd_status = row[0]
    """
    
    for(dvd_name,dvd_status,dvd_owner_id) in cursor:
        if dvd_status == 0:
            print("DVD not available for rent")
            return False

        if userid == dvd_owner_id:
            print("You are not allowed to borrow your own DVD")
            return False

    return True


def borrowdvd():
    dvdid=int(input("Enter the DVD Id to rent :"))
    days=int(input("Enter the number of days to rent the DVD:"))
    #if dvd_id is not the dvd table and dvd status is 0 then cannot borrow dvd
    #if the above check passes then we are ready to borrow the dvd.

    status = check_dvd_status(dvdid)
    if(status == False):
        return

    # To successfully borrow the dvd we have to do the following 2 things:
    # 1. Add a new record to the rental table and
    # 2. Update the dvd table record to change the dvd_status to 0
    query="select rent_price from dvd where dvd_id="+ str(dvdid)
    cursor.execute(query)
    row = cursor.fetchone()
    rent_price = row[0]
    
    total_rent_price=rent_price*days
    currentDate = "curdate()"
    dueDate=datetime.now().date() + timedelta(days)
    dueDate = dueDate.isoformat()

   

    querystr="insert into rental(borrower_id,issue_date,dvd_id,due_date,Total_Rent_price) values('%d',%s,'%d','%s','%d')" %(userid, currentDate,dvdid, dueDate,total_rent_price)
    cursor.execute(querystr)

    querystr="update dvd set dvd_status=0 where dvd_id="+str(dvdid)
    cursor.execute(querystr)

    cnx.commit()
    print("DVD rented sucessfully !! Please don't forgot to return the DVD on time.")
    exit()

def check_status(dvdid1):
    query="select dvd_name,dvd_status,dvd_owner_id from dvd where dvd_id="+ str(dvdid1) 
    cursor.execute(query)
    if(cursor.rowcount==0):
        print("DVD ID doesn't exists")
        return False
    """
    row = cursor.fetchone()
    dvd_status = row[0]
    """
    for(dvd_name,dvd_status, dvd_owner_id) in cursor:
        if dvd_owner_id != userid:
            print("DVD cannot be deleted as you are not the owner of the DVD.")
            return False
        elif dvd_status == 0:
            print("DVD cannot be deleted as it is rented to someone")
            return False

    return True

def deletedvd():

    #check whether the dvd status if it is 0 then can't delete the DVD otherwise delete the dvd
    dvdid1=input("Enter the DVD ID to delete: ")

    check=check_status(dvdid1)
    if check == False:
        return
    #query to delete DVD from the table

    querystr="delete from dvd where dvd_id="+str(dvdid1)+ " and dvd_owner_id="+str(userid) 
    cursor.execute(querystr)
    count = cursor.rowcount
    cnx.commit()

    if(count > 0):
        print("DVD deleted successfully !!")

    exit()

def dvdstatus():

    #check the status od the dvd with owner deatils
    querystr="select d.dvd_id,d.dvd_name,d.dvd_genre,d.rent_price,d.dvd_status,u.user_name AS 'Owner'from dvd d inner join userinfo u ON d.dvd_owner_id=u.id;"
    cursor.execute(querystr)
    
    print('{:^6} {:20} {:15} {:^10} {:^10} {:20}'.format('DVD ID', 'DVD Name', 'Genre', 'Rent Price', 'Status', 'Owner Name'))

    for(dvd_id, dvd_name, dvd_genre, rent_price, dvd_status, user_name)in cursor:
       
        print('{:^6} {:20} {:15} {:^10} {:^10} {:20}'.format(dvd_id, dvd_name, dvd_genre, str(rent_price), str(dvd_status), user_name))
    
    exit()

def returndvd():
   
    querystr="select r.dvd_id, r.due_date,d.dvd_name from rental r inner join dvd d ON r.dvd_id=d.dvd_id where r.borrower_id="+str(userid)
    cursor.execute(querystr)

    listOfBorrowedDvds = []
    print('{:^6} {:^10}{:^20}'.format('DVD ID','DUE DATE','DVD Name'))
    for(dvd_id,due_date,dvd_name) in cursor:
        print('{:^6} {:^10} {:^20}'.format(dvd_id,str(due_date),str(dvd_name)))
        listOfBorrowedDvds.append(dvd_id)

    dvd_return=int(input("Enter the DVD ID to return :"))

    if(dvd_return in listOfBorrowedDvds):
        querystr="delete from rental where dvd_id="+str(dvd_return)
        cursor.execute(querystr)

        query="update dvd set dvd_status=1 where dvd_id="+str(dvd_return)
        cursor.execute(query)

        cnx.commit()
        print("DVD Returned sucessfully !")
    else:
        print("DVD not rented by you. Please enter the DVD Id which is rented by you.")

    exit()
    
def exit():
    
    print("Press 1 to continue")
    print("Press 2 to exit from system")

    choice = int(input("Enter 1 or 2: \n\n"))
    if choice == 1:
        showmenu()
    elif choice == 2:
        quit()
    else:
     print("invalid Input")


def showmenu():
    print("********Welcome to DVD Rental System**********\n\n\n")
    print("1. Add DVD\n")
    print("2. Search DVD\n")
    print("3. Borrow DVD\n")
    print("4. Delete DVD\n")
    print("5. Check DVD Status\n")
    print("6. Return DVD\n")
    print("7. Exit the System")
    print("\n\n\n")
    choice = int(input("Enter your choice from above to continue:\n\n"))
    if choice == 1:
        adddvd()
    elif choice == 2:
        dvd_id=searchdvd()
    elif choice==3:
        borrowdvd()
    elif choice==4:
        deletedvd()
    elif choice==5:
        dvdstatus()
    elif choice==6:
        returndvd()
    elif choice==7:
        exit()
    else:
        print("Invalid Input")

    return choice


cnx = mysql.connector.connect(user='arnika',password='rasquare1306', host='127.0.0.1', database='dvdrental')
cursor = cnx.cursor(buffered=True)
userid=userAuthentication(cursor)

choice = showmenu()

cursor.close()
cnx.close()
