from app.db import SessionLocal
from app.models import User

with SessionLocal() as db:
    user = User(username="test_user", password_hash="test")
    db.add(user)
    db.commit()

    found = db.query(User).filter_by(username="test_user").first()
    print(f"Found user: {found.username}, ID: {found.id}")

    db.delete(found)
    db.commit()