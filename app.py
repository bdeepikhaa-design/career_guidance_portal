from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# -------------------------------------------------------------
# App Setup
# -------------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'deepikhaa_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'deepikhaa_secret_key'
db = SQLAlchemy(app)

# -------------------------------------------------------------
# Database Model
# -------------------------------------------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(150), nullable=False)

# -------------------------------------------------------------
# Login Route
# -------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        school = request.form['school']

        # Save details to session
        session['name'] = name
        session['school'] = school

        # Save to database
        new_student = Student(name=name, school=school)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('login.html')

# -------------------------------------------------------------
# Home Route
# -------------------------------------------------------------
@app.route('/home')
def home():
    name = session.get('name', 'Student')
    school = session.get('school', 'Your School')
    return render_template('home.html', name=name, school=school)

# -------------------------------------------------------------
# Default Route
# -------------------------------------------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# -------------------------------------------------------------
# Quiz Route
# -------------------------------------------------------------
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# -------------------------------------------------------------
# Career Paths Route
# -------------------------------------------------------------
@app.route('/career_paths')
def career_paths():
    return render_template('career_paths.html')

# -------------------------------------------------------------
# Career Guidance Route
# -------------------------------------------------------------
@app.route('/career_guidance')
def career_guidance():
    return render_template('career_guidance.html')

# -------------------------------------------------------------
# Result Route
# -------------------------------------------------------------
@app.route('/result', methods=['POST'])
def result():
    answers = request.form
    scores = {"science": 0, "commerce": 0, "arts": 0, "technical": 0, "sports": 0}

    for q, value in answers.items():
        if value in scores:
            scores[value] += 1  # Add +1 for whichever stream was selected

    # Find top scoring stream
    best_fit = max(scores, key=scores.get)

    # Descriptions for each stream
    results = {
        "science": "You are analytical and curious! Science stream could be your path. Careers: Doctor, Engineer, Researcher. Duration: 3–5 years. Perfect for students who love innovation.",
        "commerce": "You’re logical and business-minded! Commerce could be your choice. Careers: CA, MBA, Economist, Banker. Duration: 3–5 years. Perfect for future entrepreneurs.",
        "arts": "You’re creative and expressive! Arts stream suits you. Careers: Journalist, Designer, Writer, Psychologist. Duration: 3–5 years. Perfect for imaginative thinkers.",
        "technical": "You love hands-on learning! Technical/ITI stream could fit you. Careers: Mechanic, Electrician, Technician. Duration: 1–2 years. Perfect for practical learners.",
        "sports": "You’re active and energetic! Sports education might be your path. Careers: Athlete, Trainer, Coach. Duration: 3–4 years. Perfect for physical and teamwork skills."
    }

    result_text = results.get(best_fit, "Please answer all questions to get a result.")
    return render_template('result.html', result=result_text)

# -------------------------------------------------------------
# Run App
# -------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
