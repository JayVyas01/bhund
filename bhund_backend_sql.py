import mysql.connector
from bhund_backend_class import user, credentials, sessions

import time
import random
connection = mysql.connector.connect(host='localhost',
                                     database='bhund',
                                     user='root',
                                     passwd="Jay@10125",
                                     auth_plugin='mysql_native_password')

def getall_users():
    connection.commit()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM bhund.users")
    users_sql = cursor.fetchall()
    user_list = []
    user_dict = {}
    for entry in users_sql:
        each_user = user(entry[1],entry[2],entry[3],entry[4])
        user_list.append(each_user.__dict__)
    connection.commit()
    cursor.close()
    user_dict['records'] = user_list
    return user_dict


def delete_user(email):
    connection.commit()
    cursor = connection.cursor(buffered=True)
    ##checking for the entry:
    cursor.execute("SELECT * FROM bhund.users WHERE email_id = '" + email + "';")
    if cursor.rowcount == 0:
        cursor.close()
        return "User not found"
    else:
        cursor = connection.cursor(buffered=True)
        cursor.execute("DELETE FROM bhund.users WHERE email_id = '" + email + "';")
        connection.commit()
        cursor.close()
        return "User Deleted"

def patch_user(user1):
    connection.commit()
    cursor1 = connection.cursor(buffered=True)
    cursor1.execute("SELECT * FROM bhund.users WHERE email_id = '" + user1.email_id + "';")
    if cursor1.rowcount != 1:
        cursor1.close()
        return "User not found"
    else:
        cursor1 = connection.cursor(buffered=True)
        string = "UPDATE bhund.users SET "
        keys = user1.__dict__.keys()
        count_null = 0
        for key in keys:
            if user1.__dict__[key] == None:
                count_null +=1
        total_keys = len(keys) - count_null
        count = 0
        for key in keys:
            if user1.__dict__[key] != None:
                count+=1
                if count < total_keys:
                    string = string + str(key) + ' = ' + "'" + str(user1.__dict__[key]) + "',"
                else:
                    string = string + str(key) + ' = ' + "'" + str(user1.__dict__[key]) + "'"
        string = string + " WHERE email_id  = '"+ user1.email_id + "';"
        print(string)
        cursor1.execute(string)
        connection.commit()
        cursor1.close()
        return "user added"

    connection.commit()
    cursor.close()



def get_user_by_email(email):
    connection.commit()
    ## check if email id exists:
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM bhund.users WHERE email_id = '" + email + "';")
    if cursor.rowcount == 0:
        connection.commit()
        cursor.close()
        return "No User Found"
    else:
        user_sql = cursor.next()
        get_user = user(user_sql[1], user_sql[2],user_sql[3], user_sql[4])
        connection.commit()
        cursor.close()
        return(get_user.__dict__)



def set_user(user1):
    connection.commit()
    ##check for duplicate email
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM bhund.users WHERE email_id = '"+ user1.email_id + "';")
    if cursor.rowcount>0:
        cursor.close()
        return "user registered"
    else:
        cursor = connection.cursor(buffered=True)
        user_dict = user1.__dict__
        column_name = ""
        values = ""
        total_keys = len(user_dict.keys())
        count = 0
        for key in user_dict:
            count+=1
            if count != total_keys:
                column_name = column_name + str(key) + ","
                values = values + "'" +str(user_dict[key]) + "'" +","
            else:
                column_name = column_name = column_name + str(key)
                values = values + "'" + str(user_dict[key]) + "'"
        cursor.execute("INSERT INTO bhund.users (" + column_name + ") VALUES (" + values + ");")
        connection.commit()
        cursor.close()
        return "user added"


def add_session(email):
    login_time = time.time()
    session_id = random.randint(10000,100000)
    connection.commit()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM bhund.sessions WHERE session_id = '" + str(session_id) + "';")
    while (cursor.rowcount > 0):
        session_id = random.randint(10000, 100000)
        cursor.execute("SELECT * FROM bhund.sessions WHERE session_id = '" + str(session_id) + "';")
    cursor.close()
    cursor2 = connection.cursor(buffered=True)
    waiting_time = 2592000000
    cursor2.execute("SELECT * FROM bhund.sessions WHERE user_email = '" + email + "';")
    if cursor2.rowcount >= 1:
            session = cursor2.fetchall()[-1]
            time1 = session[1]
            session_id1 = session[0]
            if login_time - time1 < waiting_time:
                cursor2.close()
                session_dict = { "case": 1,
                                 "status" : "Already login"}
                return session_dict
    else:
        session = sessions(session_id,login_time,email)
        session_dict = session.__dict__
        column_name = ""
        values = ""
        total_keys = len(session_dict.keys())
        count = 0
        for key in session_dict:
            count += 1
            if count != total_keys:
                column_name = column_name + str(key) + ","
                values = values + "'" + str(session_dict[key]) + "'" + ","
            else:
                column_name = column_name = column_name + str(key)
                values = values + "'" + str(session_dict[key]) + "'"
        cursor3 = connection.cursor(buffered=True)
        cursor3.execute("INSERT INTO bhund.sessions (" + column_name + ") VALUES (" + values + ");")
        connection.commit()
        cursor3.close()
        session_dict["case"] = 2
        session_dict["status"] = "Login Successful"
        return session_dict

def login(credential1):
    connection.commit()
    cursor1 = connection.cursor(buffered=True)
    cursor1.execute("SELECT * FROM bhund.users where email_id = '"+ credential1.email_id + "';")
    if cursor1.rowcount == 1:
        cursor2 = connection.cursor(buffered = True)
        cursor2.execute("SELECT * FROM bhund.users where email_id = '"+ credential1.email_id + "' AND password = '"+ credential1.password +"';")
        if cursor2.rowcount == 1:
            session = add_session(credential1.email_id)
            print(session)
            status1 = session["status"]
            if session["case"] == 1:
                json = {"status" : status1}
            else:
                session_id1 = session["session_id"]
                json = {"session_id": session_id1, "status" : status1}
            return json
        else:
            return "Wrong password for the given email id"
        cursor2.close()
    else:
        return "No user registered with this email_id"
    connection.commit()
    cursor1.close()


def logout_user(session_id):
    connection.commit()
    cursor = connection.cursor(buffered= True)
    cursor.execute("DELETE FROM bhund.sessions WHERE session_id = '"+ session_id +"';")
    connection.commit()
    cursor.close()
    return "Logout successful"




if __name__ == "__main__":
    user1 = user("jay","8401003885","jayvyas@gmail.com", "12345678").__dict__
    # print(set_user(user1))
    # cred1 = credentials("jayvyas1@gmail.com","1234568")
    # print(login(cred1))
    #print(get_user_by_email("jayvyas@gmail.com"))
    connection.commit
    # cursor = connection.cursor(buffered= True)
    # cursor.execute("SELECT * FROM bhund.users")
    print(add_session(email= "jayvyas@gmail.com"))
    # dict = {"name": "jay"}
    # user1["age"] = 24
    # print(user1)
    # print(user1.__dict__)