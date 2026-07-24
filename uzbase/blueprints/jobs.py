from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from uzbase.models import db, Job

jobs_bp = Blueprint('jobs', __name__)

def validate_csrf(token):
    return session.get('csrf_token') == token

@jobs_bp.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        if not validate_csrf(request.form.get('csrf_token')):
            abort(400, "Invalid CSRF Token")
            
        new_job = Job(
            title=request.form.get('title'),
            company=request.form.get('company'),
            city=request.form.get('city'),
            salary=request.form.get('salary'),
            type=request.form.get('type', 'Full-time'),
            category=request.form.get('category'),
            description=request.form.get('description'),
            contact=request.form.get('contact'),
            email=request.form.get('email'),
            phone=request.form.get('phone') or None,
            author=session.get('username')
        )
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('jobs.jobs'))

    city_filter = request.args.get('city', '')
    cat_filter = request.args.get('category', '')
    query = request.args.get('query', '').lower()

    jobs_query = Job.query
    if city_filter:
        jobs_query = jobs_query.filter_by(city=city_filter)
    if cat_filter:
        jobs_query = jobs_query.filter_by(category=cat_filter)
    if query:
        jobs_query = jobs_query.filter(
            Job.title.ilike(f"%{query}%") |
            Job.company.ilike(f"%{query}%") |
            Job.description.ilike(f"%{query}%")
        )

    all_jobs = jobs_query.order_by(Job.created_at.desc()).all()
    
    # Extract unique values for filtering dropdowns
    cities = sorted(list(set(j.city for j in Job.query.all())))
    categories = sorted(list(set(j.category for j in Job.query.all())))

    return render_template(
        'jobs.html',
        jobs=all_jobs,
        cities=cities,
        categories=categories,
        city_filter=city_filter,
        cat_filter=cat_filter,
        query=query
    )
