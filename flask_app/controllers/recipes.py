from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def index