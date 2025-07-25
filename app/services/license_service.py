from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID
import logging

from app.models.license import BusinessLicense
from app.schemas.license import (
    LicenseCreate, 
    LicenseUpdate, 
    LicenseSearchFilters,
    PaginatedResponse,
    LicenseResponse
)
from app.core.cache import cache

logger = logging.getLogger(__name__)

class LicenseService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_license(self, license_data: LicenseCreate) -> BusinessLicense:
        """Create a new business license"""
        db_license = BusinessLicense(**license_data.dict())
        self.db.add(db_license)
        await self.db.commit()
        await self.db.refresh(db_license)
        
        # Invalidate cache
        await cache.delete("licenses_*")
        
        logger.info(f"Created license {db_license.license_number}")
        return db_license
    
    async def get_license_by_id(self, license_id: UUID) -> Optional[BusinessLicense]:
        """Get license by ID"""
        cache_key = f"license:{license_id}"
        
        # Try cache first
        cached_license = await cache.get(cache_key)
        if cached_license:
            return cached_license
        
        stmt = select(BusinessLicense).where(BusinessLicense.id == license_id)
        result = await self.db.execute(stmt)
        license_obj = result.scalar_one_or_none()
        
        # Cache the result
        if license_obj:
            await cache.set(cache_key, license_obj)
        
        return license_obj
    
    async def get_license_by_number(self, license_number: str) -> Optional[BusinessLicense]:
        """Get license by license number"""
        cache_key = f"license_num:{license_number}"
        
        cached_license = await cache.get(cache_key)
        if cached_license:
            return cached_license
        
        stmt = select(BusinessLicense).where(
            BusinessLicense.license_number == license_number
        )
        result = await self.db.execute(stmt)
        license_obj = result.scalar_one_or_none()
        
        if license_obj:
            await cache.set(cache_key, license_obj)
        
        return license_obj
    
    async def search_licenses(
        self, 
        filters: LicenseSearchFilters,
        page: int = 1,
        size: int = 20
    ) -> PaginatedResponse:
        """Search licenses with filters and pagination"""
        
        # Build base query
        stmt = select(BusinessLicense)
        count_stmt = select(func.count(BusinessLicense.id))
        
        # Apply filters
        conditions = []
        
        if filters.license_number:
            conditions.append(
                BusinessLicense.license_number.ilike(f"%{filters.license_number}%")
            )
        
        if filters.business_name:
            conditions.append(
                BusinessLicense.business_name.ilike(f"%{filters.business_name}%")
            )
        
        if filters.business_type:
            conditions.append(BusinessLicense.business_type == filters.business_type)
        
        if filters.status:
            conditions.append(BusinessLicense.status == filters.status)
        
        if filters.city:
            conditions.append(BusinessLicense.city.ilike(f"%{filters.city}%"))
        
        if filters.state:
            conditions.append(BusinessLicense.state == filters.state)
        
        if filters.zip_code:
            conditions.append(BusinessLicense.zip_code == filters.zip_code)
        
        if filters.expires_before:
            conditions.append(BusinessLicense.expiration_date <= filters.expires_before)
        
        if filters.expires_after:
            conditions.append(BusinessLicense.expiration_date >= filters.expires_after)
        
        # Apply conditions
        if conditions:
            stmt = stmt.where(and_(*conditions))
            count_stmt = count_stmt.where(and_(*conditions))
        
        # Get total count
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)
        
        # Order by created_at desc
        stmt = stmt.order_by(BusinessLicense.created_at.desc())
        
        # Execute query
        result = await self.db.execute(stmt)
        licenses = result.scalars().all()
        
        # Convert to response models
        license_responses = [LicenseResponse.from_orm(license) for license in licenses]
        
        return PaginatedResponse(
            items=license_responses,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    async def update_license(
        self, 
        license_id: UUID, 
        license_update: LicenseUpdate
    ) -> Optional[BusinessLicense]:
        """Update a license"""
        
        stmt = select(BusinessLicense).where(BusinessLicense.id == license_id)
        result = await self.db.execute(stmt)
        license_obj = result.scalar_one_or_none()
        
        if not license_obj:
            return None
        
        # Update only provided fields
        update_data = license_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(license_obj, field, value)
        
        await self.db.commit()
        await self.db.refresh(license_obj)
        
        # Invalidate cache
        await cache.delete(f"license:{license_id}")
        await cache.delete(f"license_num:{license_obj.license_number}")
        
        logger.info(f"Updated license {license_obj.license_number}")
        return license_obj
    
    async def delete_license(self, license_id: UUID) -> bool:
        """Delete a license"""
        
        stmt = select(BusinessLicense).where(BusinessLicense.id == license_id)
        result = await self.db.execute(stmt)
        license_obj = result.scalar_one_or_none()
        
        if not license_obj:
            return False
        
        await self.db.delete(license_obj)
        await self.db.commit()
        
        # Invalidate cache
        await cache.delete(f"license:{license_id}")
        await cache.delete(f"license_num:{license_obj.license_number}")
        
        logger.info(f"Deleted license {license_obj.license_number}")
        return True