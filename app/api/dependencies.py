from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.core.database import get_db
from app.schemas.license import LicenseSearchFilters, PaginatedResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

class CommonQueryParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(20, ge=1, le=100, description="Page size"),
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size

async def get_search_filters(
    license_number: Optional[str] = Query(None, description="License number to search for"),
    business_name: Optional[str] = Query(None, description="Business name to search for"),
    business_type: Optional[str] = Query(None, description="Type of business license"),
    status: Optional[str] = Query(None, description="License status"),
    city: Optional[str] = Query(None, description="City where business is located"),
    state: Optional[str] = Query(None, description="State where business is located"),
    zip_code: Optional[str] = Query(None, description="ZIP code of business"),
) -> LicenseSearchFilters:
    return LicenseSearchFilters(
        license_number=license_number,
        business_name=business_name,
        business_type=business_type,
        status=status,
        city=city,
        state=state,
        zip_code=zip_code,
    )