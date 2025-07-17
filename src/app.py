from flask import Flask
import os
from src.database import db

app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:root@localhost:5433/credit_approval')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from src.models.models import setup_models
Customer, Loan = setup_models(db)

def init_routes():
    from src.api.routes import register_routes
    register_routes(app)

init_routes()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)