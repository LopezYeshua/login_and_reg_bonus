import re
from flask import flash


from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = "login_and_reg"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(DATABASE).query_db( query, data)

    # READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL(DATABASE).query_db( query )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        result = results[0]
        return result
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("first name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("last name must be at least 2 characters.", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        if len(user['password']) < 8:
            flash("password too short.", 'password')
            is_valid = False
        if user['password'] != user['password_confirmation']:
            flash("Passwords do not match.", 'password_confirmation')
            is_valid = False
        if user['password'].isalpha() and user['password'].isdigit() == False:
            flash("Password must have: 1 uppercase letter, 1 number.", 'password')
            is_valid = False
        return is_valid