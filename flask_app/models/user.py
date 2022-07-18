from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?=.*[\$|\?\!])[A-Za-z\d$!&]$')

class User:
    db = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            #we get a list with a dictionary, need the zero to just grab the dictionary
            return cls(results[0])


    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])


    @classmethod
    def check_if_email_in_system(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        # if the query returns nothing, it is false.
        if not results:
            return False
        else:
            return True
        

    @staticmethod
    def new_user_validation(data):
        is_valid = True
        if not EMAIL_REGEX.match(data["email"]):
            flash('Invalid Email', 'register')
            is_valid = False
        if len(data['first_name']) < 2:
            flash('First name must be more than 2 characters', 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be more than 2 characters', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be 8 or more characters', 'register')
            is_valid = False
        #below is just for checking if email is in system already

        # if not PASSWORD_REGEX.match(data['password']):
        #     flash('Password must contain 1 uppercase letter, 1 lowercase letter, 1 number, 1 special character')
        #     is_valid = False
        return is_valid
