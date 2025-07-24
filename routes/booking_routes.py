from flask import Blueprint, request, jsonify
from app import db
from models import Booking
from flask_jwt_extended import jwt_required, get_jwt_identity

booking_bp = Blueprint('booking', __name__)

# Create a booking
@booking_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    current_user = get_jwt_identity()
    data = request.json
    new_booking = Booking(
        provider_id=data['provider_id'],
        customer_id=current_user['id'],
        status='pending'
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Booking created", "booking_id": new_booking.id})

# Get bookings for a provider or customer
@booking_bp.route('/', methods=['GET'])
@jwt_required()
def get_bookings():
    current_user = get_jwt_identity()
    role = current_user['role']
    if role == 'provider':
        bookings = Booking.query.filter_by(provider_id=current_user['id']).all()
    else:
        bookings = Booking.query.filter_by(customer_id=current_user['id']).all()
    output = []
    for b in bookings:
        output.append({
            "id": b.id,
            "provider_id": b.provider_id,
            "customer_id": b.customer_id,
            "date_time": b.date_time,
            "status": b.status
        })
    return jsonify(output)

# Update booking status (for provider/admin)
@booking_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    data = request.json
    booking = Booking.query.get_or_404(booking_id)
    booking.status = data.get('status', booking.status)
    db.session.commit()
    return jsonify({"message": "Booking status updated"})
