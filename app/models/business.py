from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from app.models.base import Base

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True)
    dba_number = Column(String, unique=True)
    name = Column(String)
    business_type = Column(String)
    physical_address = Column(String)
    mailing_address = Column(String)
    owner_name = Column(String)
    owner_contact = Column(String)
    employee_count = Column(Integer)
    start_date = Column(Date)

    licenses = relationship('License', back_populates='business')
    __table_args__ = (
        {'extend_existing': True}
    )
    def __repr__(self):
        return f"<Business(id={self.id}, dba_number={self.dba_number}, name={self.name})>"