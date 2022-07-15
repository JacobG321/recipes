
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

#login registration page
@app.route('/')
def index():
    return render_template('login_registration.html')


# For new users
@app.route('/new_account', methods=['POST'])
def process():
    data = {
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':request.form['password']
    }
    if request.form['confirm_password'] != request.form['password']:
        flash('Password does not match')
        return redirect('/')
    if User.check_if_email_in_system(data) == True:
        flash('Email already taken!')
        return redirect('/')
    if not User.new_user_validation(data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data['password'] = pw_hash
    session['user_id'] = User.save_user(data)
    return redirect('/recipes')


# For existing users
@app.route('/signing_in', methods=['POST'])
def signing_in():
    data = {
        'email':request.form['email'],
    }
    user_in_db = User.get_user_by_email(data)
    
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/recipes')


@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')



# All recipes
@app.route('/recipes')
def success():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    user_data = User.get_user_by_id(data)
    all_recipes = Recipe.get_all_recipes()
    return render_template('recipes.html', this_user = user_data, all_recipes = all_recipes)


# new recipe routes
@app.route('/recipes/new')
def recipe_new():
    if "user_id" not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/publish_new_recipe', methods=['POST'])
def publish_new_recipe():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under': request.form['under']
    }
    Recipe.save_recipe(data)
    return redirect('/recipes')



# edit routes
@app.route('/recipes/edit/<int:id>')
def edit_recipe_route(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id":id
    }
    this_recipe=Recipe.get_recipe_by_id(data)
    return render_template('edit_recipe.html', this_recipe=this_recipe)

@app.route('/publish_edit_recipe/<int:id>', methods=['POST'])
def publish_edit_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id":id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under': request.form['under']
    }
    if not Recipe.new_recipe_validation(data):
        return redirect('/recipes/edit/<int:id>')
    Recipe.edit_recipe(data)
    return redirect('/recipes')
    

# View recipe
@app.route('/recipes/view/<int:id>')
def view_recipe():
    if "user_id" not in session:
        return redirect('/')
    pass

@app.route('/recipes/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id':id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')
    


