import re
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from uzbase.models import db, User

auth_bp = Blueprint('auth', __name__)

FAILED_ATTEMPTS = {}
MAX_FAILED_ATTEMPTS = 5

def validate_csrf(token):
    return session.get('csrf_token') == token

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None
    if request.method == 'POST':
        if not validate_csrf(request.form.get('csrf_token')):
            abort(400, "Invalid CSRF Token")

        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        fullname = request.form.get('fullname', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not fullname or not password:
            error = "All fields are required."
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = "Invalid email address format."
        elif len(password) < 8 or not re.search(r"[^a-zA-Z0-9]", password):
            error = "Password must be at least 8 characters long and contain at least one special character."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            # Check db
            if User.query.filter(db.func.lower(User.username) == username.lower()).first():
                error = "Username already exists."
            else:
                new_user = User(
                    username=username,
                    email=email,
                    full_name=fullname,
                    password_hash=generate_password_hash(password)
                )
                db.session.add(new_user)
                db.session.commit()
                success = "Registration successful! You can now log in."

    return render_template('register.html', error=error, success=success)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not validate_csrf(request.form.get('csrf_token')):
            abort(400, "Invalid CSRF Token")

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Normalize lookup to prevent case sensitivity issues
        username_lower = username.lower()
        if FAILED_ATTEMPTS.get(username_lower, 0) >= MAX_FAILED_ATTEMPTS:
            error = "Account temporarily locked due to too many failed attempts. Try again later."
        else:
            user = User.query.filter(db.func.lower(User.username) == username_lower).first()
            if user and check_password_hash(user.password_hash, password):
                session['username'] = user.username
                session['email'] = user.email
                session['fullname'] = user.full_name
                FAILED_ATTEMPTS[username_lower] = 0
                return redirect(url_for('auth.cabinet'))
            else:
                FAILED_ATTEMPTS[username_lower] = FAILED_ATTEMPTS.get(username_lower, 0) + 1
                attempts_left = MAX_FAILED_ATTEMPTS - FAILED_ATTEMPTS[username_lower]
                if attempts_left > 0:
                    error = f"Invalid username or password. {attempts_left} attempts remaining."
                else:
                    error = "Too many failed attempts. Account locked."

    return render_template('login.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@auth_bp.route('/cabinet', methods=['GET', 'POST'])
def cabinet():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    from uzbase.models import Job, Housing, ForumTopic
    
    username = session['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
        
    success = None
    error = None
    action = None
    active_tab = request.args.get('tab', 'profile')

    if request.method == 'POST':
        if not validate_csrf(request.form.get('csrf_token')):
            abort(400, "Invalid CSRF Token")

        action = request.form.get('action')
        active_tab = request.form.get('active_tab', 'profile')
        
        if action == 'update_profile':
            fullname = request.form.get('fullname', '').strip()
            email = request.form.get('email', '').strip()
            if fullname and email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
                user.full_name = fullname
                user.email = email
                db.session.commit()
                session['fullname'] = fullname
                session['email'] = email
                success = "Profile updated successfully!"
            else:
                error = "Invalid inputs."
        elif action == 'change_password':
            current_pass = request.form.get('current_password', '')
            new_pass = request.form.get('new_password', '')
            confirm_pass = request.form.get('confirm_new_password', '')
            
            if not check_password_hash(user.password_hash, current_pass):
                error = "Current password is incorrect."
            elif len(new_pass) < 8 or not re.search(r"[^a-zA-Z0-9]", new_pass):
                error = "New password must be at least 8 characters long and contain at least one special character."
            elif new_pass != confirm_pass:
                error = "New passwords do not match."
            else:
                user.password_hash = generate_password_hash(new_pass)
                db.session.commit()
                success = "Password changed successfully!"
        elif action == 'delete_my_job':
            target_id = request.form.get('id')
            job = Job.query.get(target_id)
            if job and job.author == username:
                db.session.delete(job)
                db.session.commit()
                success = "Job listing deleted successfully!"
            else:
                error = "Could not delete job listing."
        elif action == 'edit_my_job':
            target_id = request.form.get('id')
            job = Job.query.get(target_id)
            if job and job.author == username:
                job.title = request.form.get('title')
                job.company = request.form.get('company')
                job.city = request.form.get('city')
                job.salary = request.form.get('salary')
                job.type = request.form.get('type')
                job.category = request.form.get('category')
                job.description = request.form.get('description')
                job.contact = request.form.get('contact')
                job.email = request.form.get('email')
                job.phone = request.form.get('phone') or None
                db.session.commit()
                success = "Job listing updated successfully!"
            else:
                error = "Could not update job listing."
        elif action == 'delete_my_housing':
            target_id = request.form.get('id')
            house = Housing.query.get(target_id)
            if house and house.author == username:
                db.session.delete(house)
                db.session.commit()
                success = "Housing listing deleted successfully!"
            else:
                error = "Could not delete housing listing."
        elif action == 'edit_my_housing':
            target_id = request.form.get('id')
            house = Housing.query.get(target_id)
            if house and house.author == username:
                house.title = request.form.get('title')
                house.type = request.form.get('type')
                house.city = request.form.get('city')
                house.price = request.form.get('price')
                house.size = request.form.get('size')
                house.available_from = request.form.get('available_from')
                house.description = request.form.get('description')
                house.contact = request.form.get('contact')
                house.email = request.form.get('email')
                house.phone = request.form.get('phone') or None
                db.session.commit()
                success = "Housing listing updated successfully!"
            else:
                error = "Could not update housing listing."
        elif action == 'delete_my_topic':
            target_id = request.form.get('id')
            topic = ForumTopic.query.get(target_id)
            if topic and topic.author == username:
                db.session.delete(topic)
                db.session.commit()
                success = "Forum topic deleted successfully!"
            else:
                error = "Could not delete forum topic."
        elif action == 'edit_my_topic':
            target_id = request.form.get('id')
            topic = ForumTopic.query.get(target_id)
            if topic and topic.author == username:
                topic.title = request.form.get('title')
                topic.category = request.form.get('category')
                db.session.commit()
                success = "Forum topic updated successfully!"
            else:
                error = "Could not update forum topic."
                
    user_jobs = Job.query.filter_by(author=username).all()
    user_housing = Housing.query.filter_by(author=username).all()
    user_topics = ForumTopic.query.filter_by(author=username).all()

    return render_template(
        'cabinet.html',
        user=user,
        success=success,
        error=error,
        action=action,
        active_tab=active_tab,
        user_jobs=user_jobs,
        user_housing=user_housing,
        user_topics=user_topics
    )

@auth_bp.route('/notifications/mark-read', methods=['POST'])
def mark_read():
    if not session.get('username'):
        return jsonify({'success': False}), 401
    from uzbase.models import Notification
    try:
        Notification.query.filter_by(username=session['username'], is_read=False).update({Notification.is_read: True})
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'success': False}), 500
    return jsonify({'success': True})
