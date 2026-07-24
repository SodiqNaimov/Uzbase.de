from flask import Blueprint, render_template, request, session, abort, redirect, url_for
from uzbase.models import db, User, Job, Housing, ForumTopic, WikiCategory, WikiItem, PageVisit

admin_bp = Blueprint('admin', __name__)

def validate_csrf(token):
    return session.get('csrf_token') == token

def check_admin_auth():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if not user or not user.is_admin:
        abort(404) # Hide the route completely

@admin_bp.route('/admin_uzbase_portal_sec_779', methods=['GET', 'POST'])
def admin_panel():
    check_admin_auth()

    if request.method == 'POST':
        if not validate_csrf(request.form.get('csrf_token')):
            abort(400, "Invalid CSRF Token")

        action = request.form.get('action')
        target_id = request.form.get('id')
        target_username = request.form.get('username')

        # Core Entities Deletion
        if action == 'delete_user' and target_username:
            if target_username != session['username']:
                user = User.query.filter_by(username=target_username).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
        elif action == 'delete_job' and target_id:
            job = Job.query.get(target_id)
            if job:
                db.session.delete(job)
                db.session.commit()
        elif action == 'delete_housing' and target_id:
            house = Housing.query.get(target_id)
            if house:
                db.session.delete(house)
                db.session.commit()
        elif action == 'delete_topic' and target_id:
            topic = ForumTopic.query.get(target_id)
            if topic:
                db.session.delete(topic)
                db.session.commit()

        # Wiki Categories CRUD
        elif action == 'add_category':
            name_uz = request.form.get('name_uz', '').strip()
            name_de = request.form.get('name_de', '').strip()
            name_ru = request.form.get('name_ru', '').strip()
            if name_uz and name_de and name_ru:
                new_cat = WikiCategory(name_uz=name_uz, name_de=name_de, name_ru=name_ru)
                db.session.add(new_cat)
                db.session.commit()
        elif action == 'edit_category' and target_id:
            name_uz = request.form.get('name_uz', '').strip()
            name_de = request.form.get('name_de', '').strip()
            name_ru = request.form.get('name_ru', '').strip()
            cat = WikiCategory.query.get(target_id)
            if cat and name_uz and name_de and name_ru:
                cat.name_uz = name_uz
                cat.name_de = name_de
                cat.name_ru = name_ru
                db.session.commit()
        elif action == 'delete_category' and target_id:
            cat = WikiCategory.query.get(target_id)
            if cat:
                db.session.delete(cat)
                db.session.commit()

        # Wiki Guides CRUD
        elif action == 'add_wiki':
            title_uz = request.form.get('title_uz', '').strip()
            title_de = request.form.get('title_de', '').strip()
            title_ru = request.form.get('title_ru', '').strip()
            category_id = request.form.get('category_id')
            content_uz = request.form.get('content_uz', '').strip()
            content_de = request.form.get('content_de', '').strip()
            content_ru = request.form.get('content_ru', '').strip()
            if title_uz and title_de and title_ru and category_id and content_uz and content_de and content_ru:
                new_item = WikiItem(
                    title_uz=title_uz, title_de=title_de, title_ru=title_ru,
                    category_id=category_id,
                    content_uz=content_uz, content_de=content_de, content_ru=content_ru
                )
                db.session.add(new_item)
                db.session.commit()
        elif action == 'edit_wiki' and target_id:
            title_uz = request.form.get('title_uz', '').strip()
            title_de = request.form.get('title_de', '').strip()
            title_ru = request.form.get('title_ru', '').strip()
            category_id = request.form.get('category_id')
            content_uz = request.form.get('content_uz', '').strip()
            content_de = request.form.get('content_de', '').strip()
            content_ru = request.form.get('content_ru', '').strip()
            item = WikiItem.query.get(target_id)
            if item and title_uz and title_de and title_ru and category_id and content_uz and content_de and content_ru:
                item.title_uz = title_uz
                item.title_de = title_de
                item.title_ru = title_ru
                item.category_id = category_id
                item.content_uz = content_uz
                item.content_de = content_de
                item.content_ru = content_ru
                db.session.commit()
        elif action == 'delete_wiki' and target_id:
            item = WikiItem.query.get(target_id)
            if item:
                db.session.delete(item)
                db.session.commit()

        active_tab = request.form.get('active_tab', 'dashboard')
        return redirect(url_for('admin.admin_panel', tab=active_tab))

    tab = request.args.get('tab', 'dashboard')
    users = User.query.all()
    user_count = len(users)
    jobs = Job.query.all()
    housing = Housing.query.all()
    topics = ForumTopic.query.all()
    categories = WikiCategory.query.all()
    wiki_items = WikiItem.query.all()
    page_visits = PageVisit.query.order_by(PageVisit.count.desc()).all()

    return render_template(
        'admin.html',
        users=users,
        user_count=user_count,
        jobs=jobs,
        housing=housing,
        topics=topics,
        categories=categories,
        wiki_items=wiki_items,
        page_visits=page_visits,
        tab=tab
    )
