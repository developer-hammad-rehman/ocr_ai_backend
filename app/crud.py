from sqlmodel import SQLModel, Session, create_engine
from app import settings
from app.models import FileUpload, Users

connection_string = str(settings.DATA_BASE_URL).replace(
    "postgresql", "postgresql+psycopg2"
)

engine = create_engine(connection_string, pool_recycle=300, echo=True)


def create_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session