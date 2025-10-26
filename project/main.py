from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length
import requests, json
from time import sleep
import os
from dotenv import load_dotenv
from flask_optional_routes import OptionalRoutes

load_dotenv()

def isUserConfirmed(func):
    if current_user.isConfirmed is False:
        flash("Please confirm your account!", "warning")
        return redirect(url_for("main.inactive"))
    return func

class BigToSmallForm(FlaskForm):
    big_idea = StringField('Main Idea', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Generate Subtopics')

class SmallToSourceForm(FlaskForm):
    subtopic = StringField('Subtopic', validators=[InputRequired(), Length(min=1, max=500)])
    subtopic_index = HiddenField()  # To track which subtopic this is (0, 1, or 2)
    submit = SubmitField('Generate Sources')

main = Blueprint('main', __name__)

optional = OptionalRoutes(main)

API_KEY = os.getenv("API_KEY")

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/map', methods=['GET', 'POST'])
@login_required
def map_page():
    big_to_small_form = BigToSmallForm()
    
    # Create 3 SmallToSourceForms for each potential subtopic
    small_to_source_forms = [SmallToSourceForm() for _ in range(3)]
    
    # Initialize some variables for the template
    main_idea = None
    subtopics = []
    sources = {}  # Dictionary to store sources for each subtopic index
    
    if request.method == 'POST':
        # Check if it's the big-to-small form submission
        if 'big_idea' in request.form and big_to_small_form.validate_on_submit():
            main_idea = big_to_small_form.big_idea.data

            POST_URL = "https://api.agent.ai/v1/agent/kh2fyfmqponb9vhm/webhook/7dbe8317/async"
            GET_URL = "https://api.agent.ai/v1/agent/kh2fyfmqponb9vhm/webhook/7dbe8317/status"

            post_response = requests.post(POST_URL, json={"big_idea": main_idea, "num_small": 3}, headers={"x-api-key": API_KEY, "Content-Type": "application/json"})
            run_id = post_response.json().get("run_id")

            subtopics = {}
            get_response = requests.get(f"{GET_URL}/{run_id}", headers={"x-api-key": API_KEY, "Content-Type": "application/json"})
            timeout = 0
            while (get_response.status_code == 204) and (timeout < 60):
                timeout += 5
                sleep(5)
                get_response = requests.get(f"{GET_URL}/{run_id}", headers={"x-api-key": API_KEY, "Content-Type": "application/json"})
            if get_response.status_code == 200:
                subtopics = get_response.json().get("response")
            else:
                subtopics = ["Error Subtopic 1", "Error Subtopic 2", "Error Subtopic 3"]

            subtopics = subtopics['subtopics']

        
        # Check if any of the small-to-source forms were submitted
        elif 'subtopic' in request.form:
            # Try to get preserved data from form
            main_idea = request.form.get('main_idea_hidden', '')
            subtopics_data = request.form.get('subtopics_hidden', '')
            subtopics = subtopics_data.split('|||') if subtopics_data else []
            
            # Get existing sources from form data
            sources_data = request.form.get('sources_hidden', '')
            if sources_data and sources_data.strip():
                # Parse existing sources (format: "0:source1,source2,source3|||1:source1,source2")
                for source_entry in sources_data.split('|||'):
                    if ':' in source_entry and source_entry.strip():
                        idx_str, sources_str = source_entry.split(':', 1)
                        if sources_str.strip():
                            sources[int(idx_str)] = sources_str.split(',')
            
            # Get which subtopic was submitted
            subtopic_index = int(request.form.get('subtopic_index', 0))
            subtopic = request.form.get('subtopic', '')
            
            if subtopic:

                POST_URL = "https://api.agent.ai/v1/agent/n1mcu1mwrricwrfk/webhook/0476b719/async"
                GET_URL = "https://api.agent.ai/v1/agent/n1mcu1mwrricwrfk/webhook/0476b719/status"

                post_response = requests.post(POST_URL, json={"subtopic": subtopic, "num_sources": 3}, headers={"x-api-key": API_KEY, "Content-Type": "application/json"})
                run_id = post_response.json().get("run_id")

                get_response = requests.get(f"{GET_URL}/{run_id}", headers={"x-api-key": API_KEY, "Content-Type": "application/json"})
                timeout = 0
                while (get_response.status_code == 204) and (timeout < 60):
                    timeout += 5
                    sleep(5)
                    get_response = requests.get(f"{GET_URL}/{run_id}", headers={"x-api-key": API_KEY, "Content-Type": "application/json"})
                if get_response.status_code == 200:
                    generated_sources = get_response.json().get("response")
                    sources_list = generated_sources.get('sources', [])
                    sources_list = list(map(lambda x: x["mla_citation"], sources_list))
                    sources[subtopic_index] = sources_list
                else:
                    sources[subtopic_index] = ["Error Source 1", "Error Source 2", "Error Source 3"]
                

                
                # Update the subtopic in case user modified it
                if subtopic_index < len(subtopics):
                    subtopics[subtopic_index] = subtopic
    
    # Always re-populate the forms with current subtopics (whether from generation or preservation)
    for i, subtopic in enumerate(subtopics):
        if i < len(small_to_source_forms):
            small_to_source_forms[i].subtopic.data = subtopic
            small_to_source_forms[i].subtopic_index.data = str(i)
    
    ret = render_template('map.html', 
                         big_to_small_form=big_to_small_form,
                         small_to_source_forms=small_to_source_forms,
                         main_idea=main_idea,
                         subtopics=subtopics,
                         sources=sources)
    return isUserConfirmed(ret)

@main.route('/profile/')
@main.route('/profile/<int:user_id>/')
@login_required
def profile(user_id=None):
    if user_id is not None:
      user = User.query.get(user_id)
      ret = render_template('profile.html', 
        id=user.id,
        name=user.name,
        email=user.email)
      return isUserConfirmed(ret)
    ret = render_template('profile.html', 
        id=current_user.id,
        name=current_user.name,
        email=current_user.email)
    return isUserConfirmed(ret)


@main.route("/inactive")
@login_required
def inactive():
    if current_user.isConfirmed:
        return redirect(url_for("main.profile"))
    return render_template("inactive.html")