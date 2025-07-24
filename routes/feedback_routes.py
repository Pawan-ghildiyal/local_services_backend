from flask import Blueprint, request, jsonify
from app import db
from models import Feedback
from flask_jwt_extended import jwt_required, get_jwt_identity

feedback_bp = Blueprint('feedback', __name__)

# Add feedback
@feedback_bp.route('/', methods=['POST'])
@jwt_required()
def add_feedback():
    current_user = get_jwt_identity()
    data = request.json
    new_feedback = Feedback(
        provider_id=data['provider_id'],
        customer_id=current_user['id'],
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({"message": "Feedback added"})

# Get feedback for a provider
@feedback_bp.route('/<int:provider_id>', methods=['GET'])
def get_feedback(provider_id):
    feedbacks = Feedback.query.filter_by(provider_id=provider_id).all()
    output = []
    for f in feedbacks:
        output.append({
            "id": f.id,
            "provider_id": f.provider_id,
            "customer_id": f.customer_id,
            "rating": f.rating,
            "comment": f.comment
        })
    return jsonify(output)
