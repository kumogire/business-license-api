from app.database import engine
from app.models.base import Base
from app.models.business import Business
from app.models.license import License

# Create all tables
Base.metadata.create_all(bind=engine)