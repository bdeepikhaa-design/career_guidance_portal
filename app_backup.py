from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------
# 🏠 Home Page
# -------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -------------------------------
# 🧠 Quiz Page
# -------------------------------
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# -------------------------------
# 📖 About Page
# -------------------------------
@app.route('/about')
def about():
    return render_template('about.html')

# -------------------------------
# 🌿 Career Paths Page
# -------------------------------
@app.route('/career_paths')
def career_paths():
    return render_template('career_paths.html')

# -------------------------------
# 🏁 Result Page (Main Logic)
# -------------------------------
@app.route('/result', methods=['POST'])
def result():
    # Collect answers from form
    answers = []
    for i in range(1, 11):  # 10 questions
        ans = request.form.get(f'q{i}')
        answers.append(ans)

    # Simple scoring based on selected options
    science = answers.count("science")
    commerce = answers.count("commerce")
    arts = answers.count("arts")
    technical = answers.count("technical")
    sports = answers.count("sports")

    # Determine result
    if science >= max(commerce, arts, technical, sports):
        result_text = (
            "🔬 You seem to love Science! You can explore MPC, BiPC, or Computer Science streams. "
            "Careers: Engineering, Medicine, Data Science, and more!"
        )
    elif commerce >= max(science, arts, technical, sports):
        result_text = (
            "💰 You’re great with numbers and logic! Commerce stream could be your best path. "
            "Careers: CA, Business, Banking, Management, etc."
        )
    elif arts >= max(science, commerce, technical, sports):
        result_text = (
            "🎨 You’re creative and expressive! Arts and Humanities might suit you. "
            "Careers: Journalism, Design, Psychology, Literature, etc."
        )
    elif technical >= max(science, commerce, arts, sports):
        result_text = (
            "🛠️ You enjoy hands-on learning! ITI, Diploma, or vocational courses are great choices. "
            "Careers: Electrician, Technician, Mechanic, and more!"
        )
    else:
        result_text = (
            "⚽ You’re active and energetic! Sports or physical education might be your calling. "
            "Careers: Athlete, Trainer, Coach, or Sports Scientist!"
        )

    # Send result to HTML page
    return render_template('result.html', result=result_text)

# -------------------------------
# 🚀 Run the App
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
