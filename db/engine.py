import databases
import sqlalchemy as sa

from api.settings import settings


database = databases.Database(settings.db_uri)

metadata = sa.MetaData()

engine = sa.create_engine(
    settings.db_uri, connect_args={"check_same_thread": False}
)


def create_meta():
    metadata.create_all(engine, checkfirst=True)
