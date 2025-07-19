from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/learning_progress'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Helper function: handle file path
def get_file_url(file_path):
    if not file_path:
        return None

    if file_path.startswith('static/uploads/'):
        return url_for('static', filename=file_path.replace('static/', ''))
    
    return None

# Add helper function to template global variables
@app.context_processor
def inject_utilities():
    return dict(get_file_url=get_file_url)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    progresses = db.relationship('Progress', backref='user', lazy=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(200), nullable=True)
    total_units = db.Column(db.Integer, nullable=False)
    current_unit = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Float, default=0)  # Total time spent (hours)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes and view functions
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get all learning progress for the user
    progresses = Progress.query.filter_by(user_id=session['user_id']).all()
    
    # Calculate statistics
    progress_count = len(progresses)
    completed_count = 0
    
    for progress in progresses:
        if progress.current_unit >= progress.total_units:
            completed_count += 1
    
    # Calculate completion rate
    completion_rate = f"{int((completed_count / progress_count) * 100)}%" if progress_count > 0 else "0%"
    
    return render_template('index.html', 
                          progress_count=progress_count, 
                          completed_count=completed_count, 
                          completion_rate=completion_rate)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Plain text password storage and comparison
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', 'danger')
            return render_template('register.html')
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email is already registered!', 'danger')
            return render_template('register.html')
        
        # Create new user (plain text password storage)
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful, please login!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/progress')
def progress_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    progresses = Progress.query.filter_by(user_id=session['user_id']).all()
    return render_template('progress_list.html', progresses=progresses)

@app.route('/progress/add', methods=['GET', 'POST'])
def add_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        total_units = request.form.get('total_units')
        time_spent = request.form.get('time_spent', 0)
        
        # Handle file upload
        file_path = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                # Use original filename without secure_filename processing
                original_filename = file.filename
                # Add timestamp to avoid filename conflicts
                import time
                timestamp = str(int(time.time()))
                filename = timestamp + '_' + original_filename
                # Save file
                file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_save_path)
                # Store only relative path for URL generation
                file_path = 'static/uploads/' + filename
        
        new_progress = Progress(
            title=title,
            description=description,
            file_path=file_path,
            total_units=total_units,
            current_unit=0,
            time_spent=time_spent,
            user_id=session['user_id']
        )
        
        db.session.add(new_progress)
        db.session.commit()
        
        flash('Learning progress added successfully!', 'success')
        return redirect(url_for('progress_list'))
    
    return render_template('add_progress.html')

@app.route('/progress/update/<int:id>', methods=['POST'])
def update_progress(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    progress = Progress.query.get_or_404(id)
    
    # Ensure user can only update their own progress
    if progress.user_id != session['user_id']:
        flash('You are not authorized to update this progress!', 'danger')
        return redirect(url_for('progress_list'))
    
    current_unit = request.form.get('current_unit')
    time_spent = request.form.get('time_spent')
    
    if current_unit is not None:
        progress.current_unit = current_unit
    
    if time_spent is not None:
        progress.time_spent = time_spent
    
    db.session.commit()
    
    flash('Progress updated successfully!', 'success')
    return redirect(url_for('progress_list'))

@app.route('/progress/delete/<int:id>')
def delete_progress(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    progress = Progress.query.get_or_404(id)
    
    # Ensure user can only delete their own progress
    if progress.user_id != session['user_id']:
        flash('You are not authorized to delete this progress!', 'danger')
        return redirect(url_for('progress_list'))
    
    db.session.delete(progress)
    db.session.commit()
    
    flash('Progress deleted successfully!', 'success')
    return redirect(url_for('progress_list'))

@app.route('/visualization')
def visualization():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    progresses = Progress.query.filter_by(user_id=session['user_id']).all()
    progress_data = []
    
    for progress in progresses:
        percentage = int((progress.current_unit / progress.total_units) * 100) if progress.total_units > 0 else 0
        progress_data.append({
            'title': progress.title,
            'percentage': percentage,
            'current_unit': progress.current_unit,
            'total_units': progress.total_units,
            'time_spent': progress.time_spent
        })
    
    return render_template('visualization.html', progress_data=progress_data)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password
        if user.password != current_password:
            flash('Current password is incorrect!', 'danger')
            return redirect(url_for('profile'))
        
        # Verify new password
        if new_password != confirm_password:
            flash('New passwords do not match!', 'danger')
            return redirect(url_for('profile'))
        
        # Update password
        user.password = new_password  # Plain text password storage
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
