from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length

class BigToSmallForm(FlaskForm):
    big_idea = StringField('Main Idea', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Generate Subtopics')

class SmallToSourceForm(FlaskForm):
    subtopic = StringField('Subtopic', validators=[InputRequired(), Length(min=1, max=500)])
    subtopic_index = HiddenField()  # To track which subtopic this is (0, 1, or 2)
    submit = SubmitField('Generate Sources')

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/map', methods=['GET', 'POST'])
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
            # TODO: Generate 3 subtopics from main_idea
            # For now, placeholder subtopics
            subtopics = [
                f"Subtopic 1 of {main_idea}",
                f"Subtopic 2 of {main_idea}",  
                f"Subtopic 3 of {main_idea}"
            ]
        
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
                # TODO: Generate 3 sources for this subtopic
                # For now, placeholder sources
                sources[subtopic_index] = [
                    f"Source 1 for {subtopic}",
                    f"Source 2 for {subtopic}",
                    f"Source 3 for {subtopic}"
                ]
                
                # Update the subtopic in case user modified it
                if subtopic_index < len(subtopics):
                    subtopics[subtopic_index] = subtopic
    
    # Always re-populate the forms with current subtopics (whether from generation or preservation)
    for i, subtopic in enumerate(subtopics):
        if i < len(small_to_source_forms):
            small_to_source_forms[i].subtopic.data = subtopic
            small_to_source_forms[i].subtopic_index.data = str(i)
    
    return render_template('map.html', 
                         big_to_small_form=big_to_small_form,
                         small_to_source_forms=small_to_source_forms,
                         main_idea=main_idea,
                         subtopics=subtopics,
                         sources=sources)

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)


