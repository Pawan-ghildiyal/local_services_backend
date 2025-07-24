from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer')  # customer/provider/admin

    def __repr__(self):
        return f"<User {self.email}>"

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_type = db.Column(db.String(120))
    description = db.Column(db.Text)
    rating_avg = db.Column(db.Float, default=0.0)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
