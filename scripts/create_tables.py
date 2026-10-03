from app.db import make_engine
from app.models import Base

engine = make_engine('DATABASE_URL_POOLED')
Base.metadata.create_all(engine)
print("Tables created successfully.")