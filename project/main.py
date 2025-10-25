from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length

class BigIdeaForm(FlaskForm):
    idea = StringField('big_idea', validators=[InputRequired(), Length(min=1, max=500)])

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)

@main.route('/map', methods = ['GET', 'POST'])
def map():
  
  return render_template('map.html')