from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    department = Column(String)
    salary = Column(Float)
    roi_impact = Column(Float) # The metric for your MAREC Insights logic