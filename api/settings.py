import os
from pydantic import BaseSettings

from api.storage import (
    IStorage, LocalStorage
)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          'upload')


class Settings(BaseSettings):
    db_uri: str = 'sqlite:///../file.db'
    storage: IStorage = LocalStorage(local_dir=UPLOAD_DIR)


settings = Settings()
