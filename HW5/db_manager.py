from typing import Dict

from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

from flask import abort

Base = declarative_base()


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(JSONB)
    cv_results = Column(JSONB)
    ready = Column(Boolean, default=False)


class DBManager:

    def __init__(self, db_info: Dict[str, str]):
        """
        :param db_info: dictionary with all info for connecting to DB:
                        drivername, host, port, username,
                        password, database
        """

        self.engine = create_engine(URL(**db_info))
        self.Session = sessionmaker(bind=self.engine)

    def create_db(self):
        Base.metadata.create_all(self.engine)
        return 'succesfull'

    def get_model(self, model_id):
        session = self.Session()
        found = session.query(Model).filter_by(id=model_id).first()
        if found is None:
            abort(404, f'model with id {model_id} not found')
        session.close()
        return found

    def add_model(self, model_info):
        session = self.Session()
        add_model = Model(model=model_info['model'],
                          cv_results=model_info['cv_results'],
                          ready=True)
        session.add(add_model)
        session.commit()
        model_id = add_model.id
        session.close()
        return model_id
