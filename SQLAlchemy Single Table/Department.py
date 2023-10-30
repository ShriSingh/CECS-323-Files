"""Newly added code"""
# Importing necessary functions and libraries
from orm_base import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Department(Base):
    """
    Creating the table for the Department class
    """
    # Defining the table name as 'Departments'
    __tablename__ = 'Departments'

    '''Making the columns in the table'''
    # Creating the 'Name' Column - Has string characters of 50, cannot be null, and is the primary key
    Name: Mapped[str] = mapped_column('Name', String(50), nullable=False, primary_key=True)
    # Creating the 'Abbreviation' Column - Has string characters of 6, cannot be null(is mandatory)
    Abbreviation: Mapped[str] = mapped_column('Abbreviation', String(6), nullable=False)
    # Creating the 'chair_name' Column - Has string characters of 80, cannot be null(is mandatory)
    ChairName: Mapped[str] = mapped_column('Chair_Name', String(80), nullable=False)
    # Creating the 'Building' Column - Has string characters of 10, cannot be null(is mandatory)
    Building: Mapped[str] = mapped_column('Building', String(10), nullable=False)
    # Creating the 'Office' Column - Has Integer, cannot be null(is mandatory)
    Office: Mapped[int] = mapped_column('Office', Integer, nullable=False)
    # Creating the 'Phone' Column - Has string characters of 80, cannot be null(is mandatory)
    Description: Mapped[str] = mapped_column('Description', String(80), nullable=False)

    # Defining the unique constraints(candidate keys) for certain columns in the table
    __table_args__ = (
        # No two departments can have the same abbreviation
        UniqueConstraint('Abbreviation', name='Departments_uk_01'),
        # No professor can chair more than one department
        UniqueConstraint('Chair_Name', name='Departments_uk_02'),
        # No two departments can be in the same building and office
        UniqueConstraint('Building', 'Office', name='Departments_uk_03'),
        # No two departments can have the same description
        UniqueConstraint('Description', name='Departments_uk_04'),
    )

    # Defining the constructor for the class
    def __init__(self, name, abbreviation, chair_name, building, office, description):
        self.Name = name
        self.Abbreviation = abbreviation
        self.ChairName = chair_name
        self.Building = building
        self.Office = office
        self.Description = description

    # Defining the string function for the class
    def __str__(self):
        return f"Department Name: {self.Name} | Abbreviation: {self.Abbreviation} | Chair Name: {self.ChairName} | " \
               f"Building: {self.Building} | Office: {self.Office} | Description: {self.Description} |"
