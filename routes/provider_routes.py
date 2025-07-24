from flask import Blueprint, request, jsonify
from app import db
from models import Provider, User
from flask_jwt_extended import jwt_required, get_jwt_identity

provider_bp = Blueprint('provider', __name__)

# Create or update provider profile
@provider_bp.route('/', methods=['POST'])
@jwt_required()
def create_or_update_provider():
    current_user = get_jwt_identity()
    data = request.json

    provider = Provider.query.filter_by(user_id=current_user['id']).first()
    if provider:
        # Update
        provider.service_type = data.get('service_type', provider.service_type)
        provider.description = data.get('description', provider.description)
        db.session.commit()
        return jsonify({"message": "Provider profile updated"})
    else:
        # Create
        new_provider = Provider(
            user_id=current_user['id'],
            service_type=data['service_type'],
            description=data.get('description', '')
        )
        db.session.add(new_provider)
        db.session.commit()
        return jsonify({"message": "Provider profile created"})

# List all providers
@provider_bp.route('/', methods=['GET'])
def list_providers():
    providers = Provider.query.all()
    output = []
    for p in providers:
        output.append({
            "id": p.id,
            "user_id": p.user_id,
            "service_type": p.service_type,
            "description": p.description,
            "rating_avg": p.rating_avg
        })
    return jsonify(output)

@provider_bp.route('/search', methods=['GET'])
def search_providers():
    service = request.args.get('service_type', '')
    providers = Provider.query.filter(Provider.service_type.ilike(f"%{service}%")).all()
    output = [{
        "id": p.id,
        "service_type": p.service_type,
        "description": p.description,
        "rating_avg": p.rating_avg
    } for p in providers]
    return jsonify(output)
