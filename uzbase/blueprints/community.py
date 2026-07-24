from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, session
from uzbase.models import db, ForumTopic, ForumReply

community_bp = Blueprint('community', __name__)

def validate_csrf(token):
    return session.get('csrf_token') == token

@community_bp.route('/community', methods=['GET', 'POST'])
def community():
    if request.method == 'POST':
        # AJAX/JSON upvoting or regular form posts
        if request.is_json:
            data = request.json
            action = data.get('action')
            topic_id = int(data.get('topic_id'))
        else:
            # CSRF check for form posts
            if not validate_csrf(request.form.get('csrf_token')):
                abort(400, "Invalid CSRF Token")
            action = request.form.get('action')
            topic_id = int(request.form.get('topic_id')) if request.form.get('topic_id') else None

        if action == 'new_topic':
            new_topic = ForumTopic(
                title=request.form.get('title'),
                category=request.form.get('category'),
                author=session.get('username') or 'Anonymous',
                upvotes=1
            )
            db.session.add(new_topic)
            db.session.commit()
        elif action == 'add_comment':
            new_reply = ForumReply(
                topic_id=topic_id,
                author=session.get('username') or 'Anonymous',
                text=request.form.get('text')
            )
            db.session.add(new_reply)
            
            # Send notification to topic author if it's someone else commenting
            topic = ForumTopic.query.get(topic_id)
            if topic and topic.author != new_reply.author:
                from uzbase.models import Notification
                notification = Notification(
                    username=topic.author,
                    message=f"@{new_reply.author} left a comment on your topic: '{topic.title[:30]}...'",
                    topic_id=topic.id,
                    is_read=False
                )
                db.session.add(notification)
                
            db.session.commit()
        elif action == 'upvote':
            if not session.get('username'):
                return jsonify({'success': False, 'error': 'Tizimga kirishingiz kerak'}), 401
            
            topic = ForumTopic.query.get(topic_id)
            if topic:
                from uzbase.models import Upvote
                # Check if this user already upvoted this topic
                existing_vote = Upvote.query.filter_by(username=session['username'], topic_id=topic_id).first()
                if existing_vote:
                    # User already voted, so remove/toggle the vote
                    db.session.delete(existing_vote)
                    topic.upvotes = max(0, topic.upvotes - 1)
                    db.session.commit()
                    return jsonify({'success': True, 'action': 'removed', 'upvotes': topic.upvotes})
                else:
                    # Register the vote
                    new_vote = Upvote(username=session['username'], topic_id=topic_id)
                    db.session.add(new_vote)
                    topic.upvotes += 1
                    db.session.commit()
                    return jsonify({'success': True, 'action': 'added', 'upvotes': topic.upvotes})
                
        return redirect(url_for('community.community'))

    category_filter = request.args.get('category', '')
    query = request.args.get('query', '').lower()

    community_query = ForumTopic.query
    if category_filter:
        community_query = community_query.filter_by(category=category_filter)
    if query:
        community_query = community_query.filter(ForumTopic.title.ilike(f"%{query}%"))

    topics = community_query.order_by(ForumTopic.created_at.desc()).all()
    categories = sorted(list(set(t.category for t in ForumTopic.query.all())))

    user_upvotes = []
    if session.get('username'):
        from uzbase.models import Upvote
        user_upvotes = [v.topic_id for v in Upvote.query.filter_by(username=session['username']).all()]

    return render_template(
        'community.html',
        topics=topics,
        categories=categories,
        category_filter=category_filter,
        query=query,
        user_upvotes=user_upvotes
    )
