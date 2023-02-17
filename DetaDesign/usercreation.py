from hashlib import sha256
from datetime import datetime


class User ():

    # setting all the variables to private variable so no_one can access it
    def __init__(self , username : str , password : str , creation_time : str ,private_key_gen_code : int) -> None:
        self._username = username
        self._password = password
        self._private_key_gen_code = private_key_gen_code
        self._private_key = ""
        self.public_key = ""
        self._user_creation_timestamp = creation_time
        self.address_code = ""
        self.key_pair_creation()
        self.two_address_generation()



    # getter and a setter for username    
    def set_username(self , new_username : str) -> None:
        self._username = new_username
    
    def get_username(self) : 
        return self._username
    
    # getter for password
    def get_pass(self):
        return self._password

    # getter and setter for the private_key_gen_code
    def set_private_key_gen(self , key : int) -> None:
        self._private_key_gen_code = key
    
    def get_private_key_gen(self) : 
        return self._private_key_gen_code
    


    def key_pair_creation (self) -> None: # key generation
        self._key_creation_timestamp = str(datetime.now())
        data = {
            "username" : self._username,
            "password" : self._password,
            "private_key_gen_code" : self._private_key_gen_code,
            "user_creation_time" : self._user_creation_timestamp,
            "creation_time" : self._key_creation_timestamp
        }
        
        private_key_data =str(data).encode('utf-8')
        self._private_key = sha256(private_key_data).hexdigest()
        data["private_key"] = self._private_key
        public_key_data = str(data).encode('utf-8')
        self.public_key = sha256(public_key_data).hexdigest()


    def two_address_generation(self) -> None:
        data = str({
            "username" : self._username,
            "password" : self._password,
            "private_key_gen_code" : self._private_key_gen_code,
            "public_key" : self.public_key,
            "private_key": self._private_key,
            "user_creation_time" : self._user_creation_timestamp,
            "creation_time" : self._key_creation_timestamp
        }).encode('utf-8')
        self.address_code = sha256(data).hexdigest()



    def get_key_pair(self):
        return self._private_key , self.public_key 
        

    def get_creation_time(self):
        return self._user_creation_timestamp

    def get_dictionary_data(self) -> dict:
        data = {
            "username" : self._username,
            "password" : self._password,
            "private_key_gen_code" : self._private_key_gen_code,
            "public_key" : self.public_key,
            "private_key": self._private_key,
            "user_creation_time" : self._user_creation_timestamp,
            "key_creation_time" : self._key_creation_timestamp,
            "address_code" : self.address_code
        }

        return data

    




