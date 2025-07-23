from app.database import SessionLocal
from app.models.business import Business
from app.models.license import License

db = SessionLocal()

# Example business
business = Business(
    dba_number="12345",
    name="Keith's Coffee",
    business_type="Retail",
    physical_address="123 Main St",
    mailing_address="PO Box 1",
    owner_name="Keith",
    owner_contact="555-1234",
    employee_count=5,
    start_date="2020-01-01"
)
db.add(business)
db.commit()
db.refresh(business)

# Example license
license = License(
    license_number="ABC123",
    license_type="Retail",
    issue_date="2020-01-01",
    expiration_date="2025-01-01",
    issuing_authority="City",
    status="Active",
    business_id=business.id
)
db.add(license)
db.commit()
db.close()