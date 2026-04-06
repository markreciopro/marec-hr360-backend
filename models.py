from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Employee(Base):
    __tablename__ = "employees"

    # Primary Identifiers
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    
    # Workforce Details
    full_name = Column(String)
    department = Column(String)
    role = Column(String)
    
    # Financials & Status
    salary = Column(Float)
    hire_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="Active") # Active, Terminated, On Leave