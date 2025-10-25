from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class BigIdeaForm(FlaskForm):
    topic = StringField('Topic', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Generate Mind Map')

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/map', methods=['GET', 'POST'])
def map_page():
    form = BigIdeaForm()
    
    if form.validate_on_submit():
        topic = form.topic.data
        # TODO: generate or process mind map for `topic`
        return render_template('map.html', form=form, topic=topic)
    
    return render_template('map.html', form=form)

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)


