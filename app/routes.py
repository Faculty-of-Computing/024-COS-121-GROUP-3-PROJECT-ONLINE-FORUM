from app import app, db
from app.models import User, Topic, Reply
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# --- Main Routes ---

@app.route('/')
@app.route('/index')
def index():
    topics = Topic.query.order_by(Topic.date_posted.desc()).all()
    return render_template('index.html', title='Welcome to COS 121 Project Online Forum', topics=topics)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
        
        if email_exists:
            flash('That email is already registered. Please use a different one.', 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', title='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html', title='Log In')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        flash("Please log in to view the dashboard.", "warning")
        return redirect(url_for('login'))
        
    user = User.query.filter_by(username=session['username']).first()
    topics = user.topics.order_by(Topic.date_posted.desc()).all()
    return render_template('dashboard.html', title='User Dashboard', topics=topics)

# --- Topic Management Routes ---

@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    if 'logged_in' not in session:
        flash("You must be logged in to create a topic.", "warning")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user = User.query.filter_by(username=session['username']).first()

        if title and content:
            new_topic = Topic(title=title, content=content, author=user)
            db.session.add(new_topic)
            db.session.commit()
            flash("Topic created successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Title and content cannot be empty.", "danger")
    
    return render_template('create_topic.html', title='Create New Topic')

@app.route('/topic/<int:topic_id>')
def view_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    replies = Reply.query.filter_by(topic_id=topic_id).order_by(Reply.date_posted.asc()).all()
    return render_template('view_topic.html', title=topic.title, topic=topic, replies=replies)

@app.route('/topic/<int:topic_id>/reply', methods=['POST'])
def post_reply(topic_id):
    if 'logged_in' not in session:
        flash("You must be logged in to post a reply.", "warning")
        return redirect(url_for('login'))
    
    content = request.form.get('content')
    if content:
        user = User.query.filter_by(username=session['username']).first()
        topic = Topic.query.get_or_404(topic_id)
        
        new_reply = Reply(content=content, author=user, topic=topic)
        db.session.add(new_reply)
        db.session.commit()
        flash("Reply posted successfully!", "success")
    else:
        flash("Reply cannot be empty.", "danger")
        
    return redirect(url_for('view_topic', topic_id=topic_id))

@app.route('/delete_topic/<int:topic_id>', methods=['POST'])
def delete_topic(topic_id):
    if 'logged_in' not in session:
        flash("You must be logged in to delete a topic.", "warning")
        return redirect(url_for('login'))
    
    topic = Topic.query.get_or_404(topic_id)
    user = User.query.filter_by(username=session['username']).first()
    
    # Ensure the user is the author of the topic
    if topic.author != user:
        flash("You do not have permission to delete this topic.", "danger")
        return redirect(url_for('dashboard'))
        
    db.session.delete(topic)
    db.session.commit()
    
    flash("Topic deleted successfully!", "success")
    return redirect(url_for('dashboard'))
