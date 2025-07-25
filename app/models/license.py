from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from .base import Base, TimestampMixin

class LicenseStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    EXPIRED = "expired"

class LicenseType(str, enum.Enum):
    BUSINESS = "business"
    PROFESSIONAL = "professional"
    TRADE = "trade"
    FOOD_SERVICE = "food_service"
    RETAIL = "retail"

class BusinessLicense(Base, TimestampMixin):
    __tablename__ = "business_licenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_number = Column(String(50), unique=True, nullable=False, index=True)
    business_name = Column(String(255), nullable=False, index=True)
    business_type = Column(Enum(LicenseType), nullable=False)
    status = Column(Enum(LicenseStatus), nullable=False, default=LicenseStatus.ACTIVE)
    issued_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False, index=True)
    issuing_authority = Column(String(255), nullable=False)
    
    # Address fields
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    zip_code = Column(String(20), nullable=False, index=True)
    
    # Contact information
    contact_person = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    
    # Additional details
    description = Column(Text)
    conditions = Column(Text)
    is_renewable = Column(Boolean, default=True)

    def __repr__(self):
        return f"<BusinessLicense {self.license_number}: {self.business_name}>"