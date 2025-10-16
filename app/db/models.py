from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class ArgoFloat(Base):
    __tablename__ = "floats"

    id = Column(Integer, primary_key=True, index=True)
    wmo_number = Column(Integer, unique=True, index=True)
    deployment_date = Column(DateTime)
    platform_type = Column(String)

    profiles = relationship("Profile", back_populates="argo_float")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    float_id = Column(Integer, ForeignKey("floats.id"))
    cycle_number = Column(Integer)
    timestamp = Column(DateTime, index=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    profile_summary = Column(String)

    argo_float = relationship("ArgoFloat", back_populates="profiles")
    observations = relationship("Observation", back_populates="profile")

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    pressure = Column(Float)
    temperature = Column(Float)
    salinity = Column(Float)

    profile = relationship("Profile", back_populates="observations")
