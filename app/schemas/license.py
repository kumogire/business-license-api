from pydantic import BaseModel

class LicenseSchema(BaseModel):
    id: int
    name: str
    status: str

    class Config:
        orm_mode = True