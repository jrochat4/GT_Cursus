# app/main/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
# Import add_user, and the User model for type hinting if desired
from app.models import Questionnaire, Question, get_user_by_username, User as UserModel, add_user as model_add_user
# No longer need to import users_db or next_user_id directly from models here for users

# werkzeug.security is now used in the User model directly.

bp = Blueprint('main', __name__)

# ... (questionnaire_store setup)
questionnaires_store = {}
next_questionnaire_id = 1
Question.next_question_id = 1 # Reset for subtask consistency

# ========== AUTH ROUTES ==========
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username) # Fetches User object

        if user and user.check_password(password): # Use the method from User model
            login_user(user, remember=request.form.get('remember', type=bool)) # 'remember' was string 'y'
            flash('Logged in successfully.', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if get_user_by_username(username):
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            # Use the add_user function from app.models.user
            new_user = model_add_user(username, password)
            if new_user:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('main.login'))
            else:
                flash('An error occurred during registration.', 'error') # Should not happen with current logic unless username taken
    return render_template('register.html')

# ... (rest of the routes: index, list_questionnaires, create_questionnaire, etc. - ensure they are present)
@bp.route('/')
def index():
    return redirect(url_for('main.list_questionnaires'))

@bp.route('/questionnaires', methods=['GET'])
def list_questionnaires():
    return render_template('list_questionnaires.html', questionnaires=list(questionnaires_store.values()))

@bp.route('/questionnaires/new', methods=['GET', 'POST'])
@login_required
def create_questionnaire():
    global next_questionnaire_id
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_qnaire = Questionnaire(id=next_questionnaire_id, title=title, description=description)
        questionnaires_store[next_questionnaire_id] = new_qnaire
        next_questionnaire_id += 1
        flash(f"Questionnaire '{title}' created successfully!", "success")
        return redirect(url_for('main.manage_questionnaire_questions', questionnaire_id=new_qnaire.id))
    return render_template('create_questionnaire.html')

@bp.route('/questionnaires/<int:questionnaire_id>/questions', methods=['GET', 'POST'])
@login_required
def manage_questionnaire_questions(questionnaire_id):
    questionnaire = questionnaires_store.get(questionnaire_id)
    if not questionnaire: abort(404)
    if request.method == 'POST':
        question_text = request.form['question_text']
        question_type = request.form['question_type']
        choices_str = request.form.get('choices', '')
        choices_list = [choice.strip() for choice in choices_str.split(',') if choice.strip()] if choices_str else []
        try:
            new_question = Question(text=question_text, question_type=question_type, questionnaire_id=questionnaire.id, choices=choices_list)
            questionnaire.add_question(new_question)
            flash("Question added successfully!", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for('main.manage_questionnaire_questions', questionnaire_id=questionnaire_id))
    return render_template('manage_questions.html', questionnaire=questionnaire, question_types=Question.QUESTION_TYPES)

@bp.route('/questionnaires/<int:questionnaire_id>/fill', methods=['GET'])
def fill_questionnaire_form(questionnaire_id):
    questionnaire = questionnaires_store.get(questionnaire_id)
    if not questionnaire: abort(404)
    if not questionnaire.questions:
        flash("This questionnaire has no questions yet. Cannot be filled out.", "warning")
        return redirect(url_for('main.list_questionnaires'))
    return render_template('fill_questionnaire.html', questionnaire=questionnaire)

@bp.route('/questionnaires/<int:questionnaire_id>/submit', methods=['POST'])
def submit_questionnaire(questionnaire_id):
    questionnaire = questionnaires_store.get(questionnaire_id)
    if not questionnaire: abort(404)
    answers = {}
    for question in questionnaire.questions:
        answer_key = f'question_{question.id}'
        submitted_answer = request.form.get(answer_key)
        answers[question.id] = submitted_answer
    # print(f"Submitted answers for questionnaire {questionnaire_id}: {answers}") # Keep for debugging if needed
    flash(f"Thank you for submitting your answers for '{questionnaire.title}'!", "success")
    return redirect(url_for('main.list_questionnaires'))

@bp.route('/reports')
def reports_index():
    return render_template('reports_index.html', questionnaires=list(questionnaires_store.values()))

@bp.route('/reports/questionnaire/<int:questionnaire_id>')
def view_questionnaire_report(questionnaire_id):
    questionnaire = questionnaires_store.get(questionnaire_id)
    if not questionnaire: abort(404)
    simulated_aggregated_answers = {}
    if questionnaire.questions:
        for q_model in questionnaire.questions:
            if q_model.question_type == 'LIKERT_SCALE' or q_model.question_type == 'MULTIPLE_CHOICE':
                simulated_aggregated_answers[q_model.id] = {choice: 0 for choice in q_model.choices}
                if q_model.choices:
                    import random
                    for _ in range(random.randint(5, 50)): # Simulate 5 to 50 responses
                        choice = random.choice(q_model.choices)
                        simulated_aggregated_answers[q_model.id][choice] += 1
            elif q_model.question_type == 'TEXT':
                simulated_aggregated_answers[q_model.id] = ["Sample open-ended answer 1.", "Another insightful comment from reporting."]
    return render_template('view_report.html', questionnaire=questionnaire, aggregated_answers=simulated_aggregated_answers)
