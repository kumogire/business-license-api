from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class License(Base):
    __tablename__ = 'licenses'
    id = Column(Integer, primary_key=True)
    license_number = Column(String, unique=True)
    license_type = Column(String)
    issue_date = Column(Date)
    expiration_date = Column(Date)
    issuing_authority = Column(String)
    status = Column(String)
    bia_type = Column(String)
    bia_zone = Column(String)
    conditions = Column(String)
    renewal_requirements = Column(String)
    business_id = Column(Integer, ForeignKey('businesses.id'))

    business = relationship('Business', back_populates='licenses')
    __table_args__ = (
        {'extend_existing': True}
    )
    def __repr__(self):
        return f"<License(id={self.id}, license_number={self.license_number}, business_id={self.business_id})>"