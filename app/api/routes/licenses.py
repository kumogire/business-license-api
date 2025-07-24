from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
import logging

from app.core.database import get_db
from app.services.license_service import LicenseService
from app.schemas.license import (
    LicenseCreate,
    LicenseResponse,
    LicenseUpdate,
    LicenseSearchFilters,
    PaginatedResponse
)
from app.api.dependencies import CommonQueryParams, get_search_filters, limiter
from app.core.config import settings

router = APIRouter(prefix="/licenses", tags=["licenses"])
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=LicenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new business license",
    description="Create a new business license with all required information"
)
@limiter.limit(f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}seconds")
async def create_license(
    request: Request,
    license_data: LicenseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new business license"""
    service = LicenseService(db)
    
    # Check if license number already exists
    existing = await service.get_license_by_number(license_data.license_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="License number already exists"
        )
    
    try:
        license_obj = await service.create_license(license_data)
        return LicenseResponse.from_orm(license_obj)
    except Exception as e:
        logger.error(f"Error creating license: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create license"
        )

@router.get(
    "/search",
    response_model=PaginatedResponse,
    summary="Search business licenses",
    description="Search for business licenses using various filters with pagination"
)
@limiter.limit(f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}seconds")
async def search_licenses(
    request: Request,
    filters: LicenseSearchFilters = Depends(get_search_filters),
    pagination: CommonQueryParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Search for business licenses with filters"""
    service = LicenseService(db)
    
    try:
        return await service.search_licenses(
            filters=filters,
            page=pagination.page,
            size=pagination.size
        )
    except Exception as e:
        logger.error(f"Error searching licenses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search licenses"
        )

@router.get(
    "/{license_id}",
    response_model=LicenseResponse,
    summary="Get license by ID",
    description="Retrieve a specific business license by its ID"
)
@limiter.limit(f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}seconds")
async def get_license(
    request: Request,
    license_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific license by ID"""
    service = LicenseService(db)
    
    license_obj = await service.get_license_by_id(license_id)
    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    return LicenseResponse.from_orm(license_obj)

@router.get(
    "/number/{license_number}",
    response_model=LicenseResponse,
    summary="Get license by number",
    description="Retrieve a specific business license by its license number"
)
@limiter.limit(f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}seconds")
async def get_license_by_number(
    request: Request,
    license_number: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific license by license number"""
    service = LicenseService(db)
    
    license_obj = await service.get_license_by_number(license_number)
    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    return LicenseResponse.from_orm(license_obj)

@router.put(
    "/{license_id}",
    response_model=LicenseResponse,
    summary="Update license",
    description="Update an existing business license"
)
@limiter.limit(f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}seconds")
async def update_license(
    request: Request,
    license_id: UUID,
    license_update: LicenseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing license"""
    service = LicenseService(db)
    
    license_obj = await service.update_license(license_id, license_update)
    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    return LicenseResponse.from_orm(license_obj)

@router.delete(
    "/{license_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete license",
    description="Delete a business license"
)
@limiter.limit(f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}seconds")
async def delete_license(
    request: Request,
    license_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a license"""
    service = LicenseService(db)
    
    success = await service.delete_license(license_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )