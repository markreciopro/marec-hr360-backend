# models.py

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employeeid = Column(String, index=True)
    fullname = Column(String)
    department = Column(String)
    jobtitle = Column(String)
    status = Column(String)
    hiredate = Column(String)  # keep string for flexibility
    salary = Column(Integer)