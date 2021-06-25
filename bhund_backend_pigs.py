import mysql.connector
from bhund_backend_class import user, credentials, sessions, pigs, populate_session_with_json, populate_pigs_with_json

import time
import random
connection = mysql.connector.connect(host='localhost',
                                     database='bhund',
                                     user='root',
                                     passwd="Jay@10125",
                                     auth_plugin='mysql_native_password')

def authorise_with_email(credential):
    connection.commit()
    cursor1 = connection.cursor(buffered= True)
    cursor1.execute("SELECT * FROM sessions WHERE sessions.user_email = '"+credential.email_id+"';")
    if cursor1.rowcount == 1:
        cursor1.close()
        cursor2 = connection.cursor(buffered=True)
        cursor2.execute("SELECT * FROM users WHERE users.email_id = '"+credential.email_id+"' AND users.password = '"+credential.password+"';")
        if cursor2.rowcount == 1:
            cursor2.close()
            return 1
        else:
            cursor2.close()
            return 0
    else:
        return 0


def authorise_with_session_id(session_id):
    connection.commit()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * from bhund.sessions WHERE sessions.session_id = " + session_id+ ";")
    if cursor.rowcount == 1:
        cursor.close()
        connection.commit()
        return 1
    else:
        cursor.close()
        connection.commit()
        return 0

def getall_pigs():
    connection.commit()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM bhund.pigs")
    pigs_sql = cursor.fetchall()
    pigs_list = []
    pigs_dict = {}
    for entry in pigs_sql:
        each_pig = pigs(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
        pigs_list.append(each_pig.__dict__)
    connection.commit()
    cursor.close()
    pigs_dict['records'] = pigs_list
    return pigs_dict


def get_pig_by_id(id):
    connection.commit()
    cursor = connection.cursor(buffered=True)
    ##checking for the entry:
    cursor.execute("SELECT * FROM pigs WHERE id = "+ id +";")
    if cursor.rowcount == 0:
        cursor.close()
        connection.commit()
        return "No such entry found, check id"
    else:
        entry = cursor.next()
        pig = pigs(entry[0],entry[1], entry[2], entry[3], entry[4], entry[5])
        cursor.close()
        connection.commit()
        return pig.__dict__

def delete_pig(id):
    connection.commit()
    cursor = connection.cursor(buffered=True)
    ##checking for the entry:
    cursor.execute("SELECT * FROM pigs WHERE id = " + id + ";")
    if cursor.rowcount == 0:
        cursor.close()
        connection.commit()
        return "No such entry found, check id"
    else:
        cursor.close()
        cursor2 = connection.cursor(buffered=True)
        cursor2.execute("DELETE FROM pigs WHERE id = '" +id+"';")
        connection.commit()
        cursor2.close()
        return "Delete Successful"

def modify(pig):
    connection.commit()
    cursor =  connection.cursor(buffered= True)
    cursor.execute("SELECT * FROM pigs WHERE id = " + str(pig.id) + ";")
    if cursor.rowcount == 0:
        cursor.close()
        connection.commit()
        return "No such entry found, check id"
    else:
        cursor.close()
        cursor1 = connection.cursor(buffered=True)
        pig_dict = pig.__dict__
        string = ""
        count_null = 0
        for key in pig_dict:
            if pig_dict[key] == None:
                count_null+=1
        total_keys = len(pig_dict.keys())-count_null
        count = 0
        for key in pig_dict:
            if pig_dict[key] != None:
                count+=1
                if str(key) == "id" or str(key) == "prize" or str(key) == "spouse":
                    string += str(key) + '=' + str(pig_dict[key])
                else:
                    string+= str(key) +'=' + "'"+ str(pig_dict[key]) +"'"
                if count < total_keys:
                    string += ","
        cursor1.execute("UPDATE pigs SET "+ string + " WHERE id = "+pig.id+";")
        connection.commit()
        cursor1.close()
        return "Pig updated"


def insert_pig(pig):
    connection.commit()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT * FROM pigs WHERE id = " + str(pig.id) + ";")
    if cursor.rowcount == 1:
        cursor.close()
        connection.commit()
        return "Data with given id already exist"
    else:
        cursor1 = connection.cursor(buffered=True)
        pig_dict = pig.__dict__
        columns = ""
        values = ""
        count_null = 0
        for key in pig_dict:
            if pig_dict[key] == None:
                count_null += 1
        total_keys = len(pig_dict.keys()) - count_null
        count = 0
        for key in pig_dict:
            if pig_dict[key] != None:
                count += 1
                columns += str(key)
                if str(key) == "id" or str(key) == "prize" or str(key) == "spouse":
                    values += str(pig_dict[key])
                else:
                    values += "'"+str(pig_dict[key]) + "'"
                if count < total_keys:
                    columns += ","
                    values += ","
        cursor1.execute("INSERT INTO pigs (" + columns + ") VALUES (" + values + ");")
        connection.commit()
        cursor1.close()
        return "user added"

if __name__ == "__main__":
    print("hello")