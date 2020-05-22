from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///skylink.db', echo=True)
Base = declarative_base()


class Skylink(Base):
    __tablename__ = "skylink"

    id = Column(Integer, primary_key=True)
    Skylink = Column(String)

    def __init__(self, skylink):
        """"""
        self.skylink = skylink

    def __repr__(self):
        return "<Skylink: {}>".format(self.skylink)


class Location(Base):
    """"""
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    location = Column(String)
    

    skylink_id = Column(Integer, ForeignKey("skylink.id"))
    skylink = relationship("Skylink", backref=backref(
        "location", order_by=id))

    def __init__(self, title, date):
        """"""
        self.title = title
        self.date = date
        


# create tables
Base.metadata.create_all(engine)