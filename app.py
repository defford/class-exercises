from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Class, Exercise, Solution
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db.init_app(app)

with app.app_context():
    db.create_all() 

@app.route('/')
def home():
    classes = Class.query.all()
    return render_template('index.html', classes=classes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect to the login page after registration
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Create a session for the logged in user
            flash('You have successfully logged in.')
            return redirect(url_for('home'))  # Redirect to the home page after login
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/classes')
def classes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)

@app.route('/class/<int:class_id>')
def class_page(class_id):
    exercises = Exercise.query.filter_by(class_id=class_id).all()
    return render_template('class.html', exercises=exercises)

@app.route('/exercise/<int:exercise_id>', methods=['GET', 'POST'])
def exercise_page(exercise_id):
    if request.method == 'POST':
        content = request.form['content']
        new_solution = Solution(exercise_id=exercise_id, user_id=session['user_id'], content=content)
        db.session.add(new_solution)
        db.session.commit()
    solutions = Solution.query.filter_by(exercise_id=exercise_id).all()
    return render_template('exercise.html', solutions=solutions)

@app.route('/class/<int:class_id>')
def class_details(class_id):
    class_ = Class.query.get_or_404(class_id)  # Fetch the class or return 404 if not found
    return render_template('class_details.html', class_=class_)


if __name__ == '__main__':
    app.run(debug=True)
