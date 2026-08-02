from app import app
from models import User, db

with app.app_context():
    username = input("Enter username to make admin: ")
    user = User.query.filter_by(username=username).first()

    if not user:
        print(f"❌ User '{username}' not found")
    else:
        print(f"Current is_admin: {user.is_admin}")
        user.is_admin = True
        db.session.commit()
        print(f"✅ {username} is now an admin!")
