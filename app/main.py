from fastapi import FastAPI
from app.api.routes import set_routes
from pydantic import BaseModel
from typing import List

app = FastAPI()

class LicenseSchema(BaseModel):
    license_number: str
    license_type: str
    status: str

class BusinessSchema(BaseModel):
    dba_number: str
    name: str
    business_type: str
    licenses: List[LicenseSchema]

set_routes(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Business License API"}

@app.get("/businesses", response_model=List[BusinessSchema])
def get_businesses():
    # Replace with actual DB query
    return [
        {"dba_number": "12345", "name": "Keith's Coffee", "business_type": "Retail", "licenses": []},
        {"dba_number": "67890", "name": "Jane's Bakery", "business_type": "Food Service", "licenses": []}
    ]
'''
# For when we have a seeded database
from app.services.business_service import BusinessService
from app.database import get_db
from fastapi import Depends
@router.get("/businesses")
def read_businesses(db: Session = Depends(get_db)):
    service = BusinessService(db)
    return service.get_all_businesses()
'''

@app.get("/licenses", response_model=List[LicenseSchema])
def get_licenses():
    # Replace with actual DB query
    return [
        {"license_number": "ABC123", "license_type": "Retail", "status": "Active"},
        {"license_number": "XYZ456", "license_type": "Food Service", "status": "Expired"}
    ]