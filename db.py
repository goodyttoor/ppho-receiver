import os

from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

db_url = os.environ.get('DATABASE_URL')
db_port = os.environ.get('DATABASE_PORT')
db_name = os.environ.get('DATABASE_NAME')
db_user = os.environ.get('DATABASE_USER')
db_pass = os.environ.get('DATABASE_PASS')

engine = create_engine('mysql://{db_user}:{db_pass}@{db_url}:{db_port}/{db_name}'.format(
    db_url=db_url,
    db_port=db_port,
    db_name=db_name,
    db_user=db_user,
    db_pass=db_pass
), echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
