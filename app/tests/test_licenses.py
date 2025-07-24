import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import datetime, timedelta

from app.schemas.license import LicenseType, LicenseStatus

@pytest.mark.asyncio
class TestLicenseAPI:
    
    async def test_create_license(self, client: AsyncClient):
        """Test creating a new license"""
        license_data = {
            "license_number": "BL-001-2024",
            "business_name": "Test Business Inc",
            "business_type": LicenseType.BUSINESS,
            "status": LicenseStatus.ACTIVE,
            "issued_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "issuing_authority": "City of Test",
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
            "contact_person": "John Doe",
            "phone": "555-0123",
            "email": "john@testbusiness.com",
            "description": "Test business for API testing",
            "is_renewable": True
        }
        
        response = await client.post("/api/v1/licenses/", json=license_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["license_number"] == license_data["license_number"]
        assert data["business_name"] == license_data["business_name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    async def test_create_duplicate_license_number(self, client: AsyncClient):
        """Test creating a license with duplicate license number"""
        license_data = {
            "license_number": "BL-002-2024",
            "business_name": "First Business",
            "business_type": LicenseType.BUSINESS,
            "issued_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "issuing_authority": "City of Test",
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
        }
        
        # Create first license
        response = await client.post("/api/v1/licenses/", json=license_data)
        assert response.status_code == 201
        
        # Try to create duplicate
        license_data["business_name"] = "Second Business"
        response = await client.post("/api/v1/licenses/", json=license_data)
        assert response.status_code == 409
        assert "License number already exists" in response.json()["detail"]
    
    async def test_get_license_by_number(self, client: AsyncClient):
        """Test getting a license by license number"""
        # First create a license
        license_data = {
            "license_number": "BL-003-2024",
            "business_name": "Test Business",
            "business_type": LicenseType.RETAIL,
            "issued_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "issuing_authority": "City of Test",
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
        }
        
        create_response = await client.post("/api/v1/licenses/", json=license_data)
        assert create_response.status_code == 201
        
        # Get the license by number
        response = await client.get(f"/api/v1/licenses/number/{license_data['license_number']}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["license_number"] == license_data["license_number"]
        assert data["business_name"] == license_data["business_name"]
    
    async def test_get_nonexistent_license(self, client: AsyncClient):
        """Test getting a non-existent license"""
        response = await client.get("/api/v1/licenses/number/NONEXISTENT")
        assert response.status_code == 404
        assert "License not found" in response.json()["detail"]
    
    async def test_search_licenses_no_filters(self, client: AsyncClient):
        """Test searching licenses without filters"""
        response = await client.get("/api/v1/licenses/search")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "pages" in data
        assert isinstance(data["items"], list)
    
    async def test_search_licenses_with_filters(self, client: AsyncClient):
        """Test searching licenses with filters"""
        # Create test licenses
        licenses = [
            {
                "license_number": "SEARCH-001",
                "business_name": "Coffee Shop",
                "business_type": LicenseType.FOOD_SERVICE,
                "city": "Seattle",
                "state": "WA",
                "issued_date": datetime.now().isoformat(),
                "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "issuing_authority": "City of Seattle",
                "street_address": "123 Pike St",
                "zip_code": "98101",
            },
            {
                "license_number": "SEARCH-002",
                "business_name": "Retail Store",
                "business_type": LicenseType.RETAIL,
                "city": "Portland",
                "state": "OR",
                "issued_date": datetime.now().isoformat(),
                "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "issuing_authority": "City of Portland",
                "street_address": "456 Main St",
                "zip_code": "97201",
            }
        ]
        
        for license_data in licenses:
            response = await client.post("/api/v1/licenses/", json=license_data)
            assert response.status_code == 201
        
        # Search by city
        response = await client.get("/api/v1/licenses/search?city=Seattle")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 1
        assert any(item["city"] == "Seattle" for item in data["items"])
        
        # Search by business type
        response = await client.get("/api/v1/licenses/search?business_type=food_service")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 1
        assert any(item["business_type"] == "food_service" for item in data["items"])
    
    async def test_update_license(self, client: AsyncClient):
        """Test updating a license"""
        # Create a license first
        license_data = {
            "license_number": "UPDATE-001",
            "business_name": "Original Name",
            "business_type": LicenseType.BUSINESS,
            "issued_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "issuing_authority": "City of Test",
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
        }
        
        create_response = await client.post("/api/v1/licenses/", json=license_data)
        assert create_response.status_code == 201
        
        created_license = create_response.json()
        license_id = created_license["id"]
        
        # Update the license
        update_data = {
            "business_name": "Updated Name",
            "city": "Updated City"
        }
        
        response = await client.put(f"/api/v1/licenses/{license_id}", json=update_data)
        assert response.status_code == 200
        
        updated_license = response.json()
        assert updated_license["business_name"] == "Updated Name"
        assert updated_license["city"] == "Updated City"
        assert updated_license["license_number"] == license_data["license_number"]  # Unchanged
    
    async def test_delete_license(self, client: AsyncClient):
        """Test deleting a license"""
        # Create a license first
        license_data = {
            "license_number": "DELETE-001",
            "business_name": "To Be Deleted",
            "business_type": LicenseType.BUSINESS,
            "issued_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "issuing_authority": "City of Test",
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
        }
        
        create_response = await client.post("/api/v1/licenses/", json=license_data)
        assert create_response.status_code == 201
        
        created_license = create_response.json()
        license_id = created_license["id"]
        
        # Delete the license
        response = await client.delete(f"/api/v1/licenses/{license_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = await client.get(f"/api/v1/licenses/{license_id}")
        assert response.status_code == 404
    
    async def test_pagination(self, client: AsyncClient):
        """Test pagination in search results"""
        # Create multiple licenses
        for i in range(25):
            license_data = {
                "license_number": f"PAGE-{i:03d}",
                "business_name": f"Business {i}",
                "business_type": LicenseType.BUSINESS,
                "issued_date": datetime.now().isoformat(),
                "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
                "issuing_authority": "City of Test",
                "street_address": f"{i} Test St",
                "city": "Test City",
                "state": "TS",
                "zip_code": "12345",
            }
            
            response = await client.post("/api/v1/licenses/", json=license_data)
            assert response.status_code == 201
        
        # Test first page
        response = await client.get("/api/v1/licenses/search?page=1&size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 1
        assert data["size"] == 10
        assert data["total"] >= 25
        
        # Test second page
        response = await client.get("/api/v1/licenses/search?page=2&size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 2
