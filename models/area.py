from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Area(BaseModel, Base):
    __tablename__ = 'areas'
    name = Column(String(60), nullable=False)