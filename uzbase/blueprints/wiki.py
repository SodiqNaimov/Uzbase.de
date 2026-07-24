from flask import Blueprint, render_template
from uzbase.models import WikiItem, WikiCategory

wiki_bp = Blueprint('wiki', __name__)

@wiki_bp.route('/info')
def info():
    categories = WikiCategory.query.all()
    info_items = WikiItem.query.all()
    return render_template('info.html', info_items=info_items, categories=categories)
