from app.models.license import License
from sqlalchemy.orm import Session

class LicenseService:
    def __init__(self, db: Session):
        self.db = db

    def create_license(self, license_data):
        license_obj = License(**license_data)
        self.db.add(license_obj)
        self.db.commit()
        self.db.refresh(license_obj)
        return license_obj

    def get_license(self, license_id):
        return self.db.query(License).filter(License.id == license_id).first()

    def get_all_licenses(self):
        return self.db.query(License).all()