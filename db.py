from flask_sqlalchemy import SQLAlchemy

# สร้างอินสแตนซ์ของ SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    """เชื่อมต่อ SQLAlchemy กับ Flask app"""
    db.init_app(app)
