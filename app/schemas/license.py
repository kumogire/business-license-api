from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class LicenseStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    EXPIRED = "expired"

class LicenseType(str, Enum):
    BUSINESS = "business"
    PROFESSIONAL = "professional"
    TRADE = "trade"
    FOOD_SERVICE = "food_service"
    RETAIL = "retail"

class LicenseBase(BaseModel):
    license_number: str = Field(..., min_length=1, max_length=50)
    business_name: str = Field(..., min_length=1, max_length=255)
    business_type: LicenseType
    status: LicenseStatus = LicenseStatus.ACTIVE
    issued_date: datetime
    expiration_date: datetime
    issuing_authority: str = Field(..., min_length=1, max_length=255)
    
    # Address
    street_address: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=50)
    zip_code: str = Field(..., min_length=5, max_length=20)
    
    # Contact (optional)
    contact_person: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    
    # Additional details
    description: Optional[str] = None
    conditions: Optional[str] = None
    is_renewable: bool = True
    
    @validator('expiration_date')
    def expiration_after_issued(cls, v, values):
        if 'issued_date' in values and v <= values['issued_date']:
            raise ValueError('Expiration date must be after issued date')
        return v

class LicenseCreate(LicenseBase):
    pass

class LicenseUpdate(BaseModel):
    business_name: Optional[str] = Field(None, min_length=1, max_length=255)
    business_type: Optional[LicenseType] = None
    status: Optional[LicenseStatus] = None
    expiration_date: Optional[datetime] = None
    street_address: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=50)
    zip_code: Optional[str] = Field(None, min_length=5, max_length=20)
    contact_person: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    conditions: Optional[str] = None
    is_renewable: Optional[bool] = None

class LicenseResponse(LicenseBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LicenseSearchFilters(BaseModel):
    license_number: Optional[str] = None
    business_name: Optional[str] = None
    business_type: Optional[LicenseType] = None
    status: Optional[LicenseStatus] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    expires_before: Optional[datetime] = None
    expires_after: Optional[datetime] = None
    
class PaginatedResponse(BaseModel):
    items: List[LicenseResponse]
    total: int
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1, le=100)
    pages: int
    
    @validator('pages', pre=True, always=True)
    def calculate_pages(cls, v, values):
        total = values.get('total', 0)
        size = values.get('size', 1)
        return (total + size - 1) // size
