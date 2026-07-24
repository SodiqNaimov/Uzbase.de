from flask import Blueprint, render_template, request
from uzbase.models import Service

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
def services():
    cat_filter = request.args.get('category', '')
    query = request.args.get('query', '').lower()

    services_query = Service.query
    if cat_filter:
        services_query = services_query.filter_by(category=cat_filter)
    if query:
        services_query = services_query.filter(
            Service.name.ilike(f"%{query}%") |
            Service.role.ilike(f"%{query}%")
        )

    all_services = services_query.all()
    categories = sorted(list(set(s.category for s in Service.query.all())))

    return render_template(
        'services.html',
        services=all_services,
        categories=categories,
        cat_filter=cat_filter,
        query=query
    )
