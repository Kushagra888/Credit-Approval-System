from src.app import app
from src.utils.data_loader import init_db

if __name__ == '__main__':
    with app.app_context():
        init_db()
        print("Database initialized successfully")