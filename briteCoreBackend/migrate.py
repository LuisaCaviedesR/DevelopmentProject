
import os
import ConfigParser
from app import app
from models import Base
from sqlalchemy import create_engine


DEFAULT_CONFIG_FILE = "config.ini"
DEFAULT_CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))


class Migrate(object):

    def __init__(self,):
        config_file_path = os.path.join(
            DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FILE)
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(config_file_path)
        db = 'postgres'
        self.create_schemas(db)

    def create_schemas(self, db):
        url = self.config.get(db, 'db_url').format(
            db_user=self.config.get(db, 'db_user'),
            db_pass=self.config.get(db, 'db_pass'),
            db_host=self.config.get(db, 'db_host'),
            db_name=self.config.get(db, 'db_name'))

        engine = create_engine(url)
        Base.metadata.bind = engine
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

if __name__ == '__main__':
    Migrate()
