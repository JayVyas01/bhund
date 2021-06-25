import json


class user:
    name , email_id , password , phone_no = None, None, None, None
    def __init__(self, name = None, email_id = None, password = None, phone_no = None):
        self.name = name
        self.email_id = email_id
        self.password = password
        self.phone_no = phone_no


class credentials:
    def __init__(self, email_id= None, password= None) :
        self.email_id = email_id
        self.password = password


class sessions:
    def __init__(self, session_id = None, time= None, email_id = None):
        self.session_id = session_id
        self.login_time = time
        self.user_email = email_id


class pigs:
    def __init__(self,id= None, name= None, spouse= None, image_link= None, quantity= None, prize= None):
        self.id = id
        self.name = name
        self.spouse = spouse
        self.photo = image_link
        self.quantity = quantity
        self.prize = prize


def populate_pigs_with_json(incoming_json):
    string = str(incoming_json)
    string = string.replace("\'", "\"")
    j = json.loads(string)
    pig1 = pigs(**j)
    return pig1

def populate_user_with_json(incoming_json):
    string = str(incoming_json)
    string = string.replace("\'", "\"")
    j = json.loads(string)
    user1 = user(**j)
    return user1

def populate_credential_with_json(incoming_json):
    string = str(incoming_json)
    string = string.replace("\'", "\"")
    j = json.loads(string)
    credential1 = credentials(**j)
    return credential1

def populate_session_with_json(incoming_json):
    string = str(incoming_json)
    string = string.replace("\'", "\"")
    j = json.loads(string)
    session1 = sessions(**j)
    return session1

if __name__ == "__main__":
    dict = {"email_id" : "kjshd", "password" : "1230", "phone_no":"123456"}
    string = str(dict)
    string = string.replace("\'", "\"")
    # user1.name = "jay"
    # user1.email_id = "fdsa"
    # user1.password = "123"
    # user1.phone_no = "8866"
    user1 = populate_user_with_json(string)
    print(user1.__dict__)

