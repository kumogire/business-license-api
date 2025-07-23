from app.models.business import Business
from sqlalchemy.orm import Session

class BusinessService:
    def __init__(self, db: Session):
        self.db = db

    def create_business(self, business_data):
        business_obj = Business(**business_data)
        self.db.add(business_obj)
        self.db.commit()
        self.db.refresh(business_obj)
        return business_obj

    def get_business(self, business_id):
        return self.db.query(Business).filter(Business.id == business_id).first()

    def get_all_businesses(self):
        return self.db.query(Business).all()