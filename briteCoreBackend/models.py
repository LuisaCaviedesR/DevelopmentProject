from sqlalchemy import Column
from sqlalchemy import Integer, DateTime, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()


class InsurerModel(Base):

    __tablename__ = "Insurers"

    insurer_key = Column(Integer, primary_key=True)
    insurer_name = Column(String(50),unique=True)
    insurer_description = Column(String(255))
    created_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)
    risk_types = relationship("RiskTypeModel")

    def __init__(self, json_data):
        for key, value in json_data.iteritems():
            setattr(self, key, value)


class RiskTypeModel(Base):

    __tablename__ = "RiskTypes"

    risk_type_key = Column(Integer, primary_key=True)
    insurer_key = Column(Integer, ForeignKey(
        "Insurers.insurer_key", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    risk_name = Column(String(50))
    risk_description = Column(String(255))
    created_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)
    field_risks_types = relationship("FieldRiskTypeModel")
    insurer = relationship("InsurerModel", foreign_keys=[insurer_key])  

    def __init__(self, json_data):
        for key, value in json_data.iteritems():
            setattr(self, key, value)


class FieldTypeModel(Base):

    __tablename__ = "FieldTypes"

    field_type_key = Column(Integer, primary_key=True)
    field_name = Column(String(20), unique=True)
    created_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)
    field_risk_types = relationship("FieldRiskTypeModel")

    def __init__(self, json_data):
        for key, value in json_data.iteritems():
            setattr(self, key, value)


class FieldRiskTypeModel(Base):

    __tablename__ = "FieldRiskTypes"

    field_risk_type_key = Column(Integer, primary_key=True)
    field_type_key = Column(Integer, ForeignKey(
        "FieldTypes.field_type_key",onupdate="CASCADE", ondelete="CASCADE"), nullable=False, )
    risk_type_key = Column(Integer, ForeignKey(
        "RiskTypes.risk_type_key",onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    field_name = Column(String(20))
    field_data = Column(String(255))
    field_enum = Column(JSON)
    created_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now)
    updated_on = Column(DateTime, nullable=False,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)
    risks = relationship("RiskTypeModel", foreign_keys=[risk_type_key]) 
    field_types =  relationship("FieldTypeModel", foreign_keys=[field_type_key]) 

    def __init__(self, json_data):
        for key, value in json_data.iteritems():
            setattr(self, key, value)
