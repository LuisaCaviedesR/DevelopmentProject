import os
import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from models import InsurerModel, FieldTypeModel, RiskTypeModel, FieldRiskTypeModel, Base


DEFAULT_CONFIG_FILE = "config.ini"
DEFAULT_CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))


class Seeds(object):

    def __init__(self):
        config_file_path = os.path.join(
            DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FILE)
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(config_file_path)
        self.session = self.db_session()
        self.create_data()

    def db_session(self, session=None, db='postgres'):
        if session is not None:
            return session

        url = self.config.get(db, 'db_url').format(db_user=self.config.get(db, 'db_user'), db_pass=self.config.get(
            db, 'db_pass'), db_host=self.config.get(db, 'db_host'), db_name=self.config.get(db, 'db_name'))
        engine = create_engine(url)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)

        return DBSession()

    def create_data(self):
        # data in insurer table
        params = [{"insurer_name": "Chub corp", "insurer_description": "Created for test"},
                  {"insurer_name": "CNA Financial",
                      "insurer_description": "Created for test"},
                  {"insurer_name": "Country Financial", "insurer_description": "Created for test"}]
        for data in params:
            self.create_insurer(data)

        # data in FieldType tables
        params = [{"field_name": "text"}, {"field_name": "number"},
                  {"field_name": "date"}, {"field_name": "enum"}]
        for data in params:
            self.create_fieldType(data)

        # get insurer keys
        insurers = self.session.query(InsurerModel).all()
        params = []
        for insurer in insurers:
            params.append({"risk_name": "Risk Type", "insurer_key": insurer.insurer_key,
                           "risk_description": "created for test"})

        # data in FieldType tables
        for data in params:
            self.create_riskType(data)

        # get risk type
        riskType = self.session.query(RiskTypeModel).first()
        

        # getting field types
        field_types = self.session.query(FieldTypeModel).all()
        enum_info = ""
        params = []
        for field_type in field_types:
            if field_type.field_name == 'enum':
                enum_info = {"enum1":"option1","enum2":"option2","option3":"enum3"}
            params.append({"field_type_key": field_type.field_type_key,
                           "risk_type_key": riskType.risk_type_key, "field_name": "Test", "field_enum": enum_info})
        for data in params:
            self.create_riskFieldsType(data)

    def create_insurer(self, params):
        try:
            insurer = InsurerModel(params)
            self.session.add(insurer)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print format(e)

    def create_fieldType(self, params):
        try:
            field_types = FieldTypeModel(params)
            self.session.add(field_types)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print format(e)

    def create_riskType(self, params):
        try:
            field_types = RiskTypeModel(params)
            self.session.add(field_types)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print format(e)

    def create_riskFieldsType(self, params):
        try:
            field_types = FieldRiskTypeModel(params)
            self.session.add(field_types)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print format(e)


if __name__ == '__main__':
    Seeds()
