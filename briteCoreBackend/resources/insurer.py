import os
import ConfigParser
import sys
import datetime
from models import InsurerModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc


DEFAULT_CONFIG_FILE = "config.ini"
DEFAULT_CONFIG_PATH = os.path.dirname(sys.modules['__main__'].__file__)


class Insurer(object):

    def __init__(self, config_file_path=None):

        if not config_file_path:
            config_file_path = os.path.join(
                DEFAULT_CONFIG_PATH,
                DEFAULT_CONFIG_FILE)

        self.config = ConfigParser.SafeConfigParser()
        self.config.read(config_file_path)
        self.session = self.db_session()

    def __del__(self):
        self.session.close()

    def db_session(self, session=None, db='postgres'):

        if session is not None:
            return session

        url = self.config.get(db, 'db_url').format(
            db_user=self.config.get(db, 'db_user'),
            db_pass=self.config.get(db, 'db_pass'),
            db_host=self.config.get(db, 'db_host'),
            db_name=self.config.get(db, 'db_name'))

        engine = create_engine(url)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)

        return DBSession()

    def find_all(self):
        data = []
        try:
            results = self.session.query(InsurerModel).all()
            if not results:
                raise Exception('Not Found')
            else:
                for result in results:
                    data.append({"name": result.insurer_name, "description": result.insurer_description, "created_at": result.created_on.isoformat(),
                                 "updated_at": result.updated_on.isoformat(), "number": result.insurer_key})
                return data
        except exc.SQLAlchemyError as e:
            print format(e)
            raise Exception('Conflict')
        except Exception as e:
            raise e
