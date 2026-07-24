from flask import Blueprint, render_template, request, session, redirect, url_for
from uzbase.models import Job, Housing, ForumTopic

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch latest 3 items from database for dashboard previews
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(3).all()
    recent_housing = Housing.query.order_by(Housing.created_at.desc()).limit(3).all()
    recent_forum = ForumTopic.query.order_by(ForumTopic.created_at.desc()).limit(3).all()
    return render_template(
        'index.html',
        recent_jobs=recent_jobs,
        recent_housing=recent_housing,
        recent_forum=recent_forum
    )

@main_bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['uz', 'de', 'ru']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))
