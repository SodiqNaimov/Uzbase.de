from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from uzbase.models import db, Housing

housing_bp = Blueprint('housing', __name__)

def validate_csrf(token):
    print("SESSION CSRF:", session.get('csrf_token'))
    print("FORM CSRF:", token)
    return session.get('csrf_token') == token

@housing_bp.route('/housing', methods=['GET', 'POST'])
def housing():
    if request.method == 'POST':
        if not validate_csrf(request.form.get('csrf_token')):
            abort(400, "Invalid CSRF Token")
            
        new_house = Housing(
            title=request.form.get('title'),
            type=request.form.get('type'),
            city=request.form.get('city'),
            price=request.form.get('price'),
            size=request.form.get('size'),
            available_from=request.form.get('available_from'),
            description=request.form.get('description'),
            contact=request.form.get('contact'),
            email=request.form.get('email'),
            phone=request.form.get('phone') or None,
            author=session.get('username')
        )
        db.session.add(new_house)
        db.session.commit()
        return redirect(url_for('housing.housing'))

    city_filter = request.args.get('city', '')
    type_filter = request.args.get('type', '')
    query = request.args.get('query', '').lower()

    housing_query = Housing.query
    if city_filter:
        housing_query = housing_query.filter_by(city=city_filter)
    if type_filter:
        housing_query = housing_query.filter_by(type=type_filter)
    if query:
        housing_query = housing_query.filter(
            Housing.title.ilike(f"%{query}%") |
            Housing.description.ilike(f"%{query}%")
        )

    all_housing = housing_query.order_by(Housing.created_at.desc()).all()
    
    cities = sorted(list(set(h.city for h in Housing.query.all())))
    types = sorted(list(set(h.type for h in Housing.query.all())))

    return render_template(
        'housing.html',
        housing=all_housing,
        cities=cities,
        types=types,
        city_filter=city_filter,
        type_filter=type_filter,
        query=query
    )
