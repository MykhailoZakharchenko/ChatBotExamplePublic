import chatbot.DBClass as mdb


class User():
    '''class aims to detect first users

    need to develop other tracktion options'''
    def __init__(self, user_id, firstName, lastName, userName, languageCode):
        self.user_id = user_id
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.languageCode = languageCode
        self.db = mdb.DBrunner()

    def check_first_user(self):
        rows = self.db.select(f'SELECT userid FROM userlogs WHERE userid = {self.user_id}')
        if len(rows) == 0:
            self.db.insert(f"INSERT INTO userlogs (userid, first_name,last_name,username,language_code) VALUES ({self.user_id}, '{self.firstName}', '{self.lastName}', '{self.userName}', '{self.languageCode}')")
            return False
        else:
            return True
