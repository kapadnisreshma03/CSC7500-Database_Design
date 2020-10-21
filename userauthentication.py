import mysql.connector

def userAuthentication(cursor):
    #cnx = mysql.connector.connect(user='arnika',password='rasquare1306', host='127.0.0.1', database='dvdrental')
    #cursor = cnx.cursor(buffered=True)

    while True:
        username = input("Enter the Username: ")
        password = input("Enter the Password: ")
        queryStr = "select user_name,id from userinfo where user_name='"+ username +"' and password='"+password+"'"
        query = (queryStr)
        cursor.execute(query)
        if(cursor.rowcount == 0):
            print("Authentication Failed. Cannot Verify username and/or password.\n\n")
        else:
            print("Authentication Successfull.\n\n")
            for(username, id) in cursor:
                return id

    #cursor.close()
    #cnx.close()
