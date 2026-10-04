from app.db import SessionLocal, make_engine
from app.models import User
import os

engine = make_engine()
session = SessionLocal(bind=engine)

existing_user = session.query(User).filter_by(username="demo").first()

if existing_user:
  print("Demo user already exists.")
else:
  demo_user = User(username="demo", is_demo=True, password_hash="demo4444")
  session.add(demo_user)
  session.commit()
  print("Demo user created.")  