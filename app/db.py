import os
from dotenv import load_dotenv
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

load_dotenv()

def make_engine(var_name='DATABASE_URL'):
  url = os.environ[var_name]
  url = url.replace("postgresql://", "postgresql+psycopg://", 1) 
  return create_engine(url, pool_pre_ping=True)

engine = make_engine()
SessionLocal = sessionmaker(bind=engine)