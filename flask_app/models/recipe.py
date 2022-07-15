from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    db = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (user_id, name, under, description, instructions, date_made) VALUES (%(user_id)s, %(name)s, %(under)s, %(description)s, %(instructions)s, %(date_made)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
            #might need to join users to recipes to get username

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, under = %(under)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results




    @staticmethod
    def new_recipe_validation(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Name must be 3 or more characters')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be 3 or more characters')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Instructions must be 3 or more characters')
            is_valid = False
        if len(data['date_made']) < 8:
            flash('Please enter date cooked or made')
            is_valid = False
        # if len(data['under']) < 2:
        #     flash('Is it over/under 30 minutes?')
        #     is_valid = False
        return is_valid