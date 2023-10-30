from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Department(Base):
    """An organization within a particular college within a university.  Each
    department offers one or more major fields of study to its students, and
    within each major, some number of courses.  Each course is offered on
    a regular basis as a scheduled section of a given course.
    """
    __tablename__ = "departments"  # Give SQLAlchemy the name of the table.
    # Making all the columns(attributes) of the table
    abbreviation: Mapped[str] = mapped_column('abbreviation', String,
                                              nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    '''Adding columns from the previous assignment'''
    chair_name: Mapped[str] = mapped_column('chair_name', String(80), nullable=False)
    building: Mapped[str] = mapped_column('building', String(10), nullable=False)
    office: Mapped[int] = mapped_column('office', Integer, nullable=False)
    description: Mapped[str] = mapped_column('description', String(80), nullable=False)

    '''Making the relationships to Major and Course tables('''
    # The list of majors in this department
    majors: Mapped[List["Major"]] = relationship(back_populates="department")
    # The list of courses offered by this department
    courses: Mapped[List["Course"]] = relationship(back_populates="department")

    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want two separate uniqueness
    # constraints (candidate keys).
    __table_args__ = (
        # Pasting the unique constraints from the previous assignment
        UniqueConstraint("abbreviation", name="departments_uk_01"),
        UniqueConstraint("chair_name", name="departments_uk_02"),
        UniqueConstraint("building", "office", name="departments_uk_03"),
        UniqueConstraint("description", name="departments_uk_04")
    )

    def __init__(self, abbreviation, name, chair_name, building, office, description):
        self.abbreviation = abbreviation
        self.name = name
        '''Using constructors from previous assignment'''
        self.chair_name = chair_name
        self.building = building
        self.office = office
        self.description = description

    def add_course(self, course):
        if course not in self.courses:
            self.courses.add(course)  # I believe this will update the course as well.

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return f"Department Abbreviation: {self.abbreviation} | Name: {self.name} | Number course offered: {len(self.courses)} |" \
               f"Chair Name: {self.chair_name} | Building: {self.building} | Office: {self.office} | Description: {self.description} |"
