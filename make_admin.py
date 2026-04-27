from app import app
from models import User, db

with app.app_context():
    username = input("Enter username to make admin: ")
    user = User.query.filter_by(username=username).first()
    
    if not user:
        print(f"❌ User '{username}' not found")
    else:
        print(f"Current user_level: {user.user_level}")
        user.user_level = "5"
        db.session.commit()
        print(f"✅ {username} is now admin level 5!")