from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    job_title = Column(String)
    company_name = Column(String)
    linkedin_url = Column(String)
    email = Column(String)
    email_status = Column(String)
    company_website = Column(String)
    industry = Column(String)
    location = Column(String)
    rating = Column(Float)
    source_url = Column(String) 