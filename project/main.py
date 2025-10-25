from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from flask import request, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/map', methods=['GET', 'POST'])
def map_page():
  if request.method == 'POST':
    # simple handling: get submitted topic and (placeholder) redirect back to map
    topic = request.form.get('topic')
    if not topic:
      flash('Please enter a topic', 'warning')
      return redirect(url_for('main.map_page'))
    # TODO: generate or process mind map for `topic`; for now re-render map with topic
    return render_template('map.html', topic=topic)

  return render_template('map.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)


