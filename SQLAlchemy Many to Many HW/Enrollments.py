# Importing necessary libraries
from orm_base import Base
from sqlalchemy import UniqueConstraint, ForeignKey, Date, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Enrollments(Base):
    """
    Creating the association class between Section and Student.
    """
    # Naming the table
    __tablename__ = "enrollments"

    # Creating a new column to uniquely identify each enrollment
    student_id: Mapped[int] = mapped_column("student_id", nullable=False, primary_key=True)
    # Copying the passed attributes and columns from the Section and Student tables
    department_abbreviation: Mapped[str] = mapped_column("department_abbreviation", nullable=False, primary_key=True)
    course_number: Mapped[int] = mapped_column("course_number", nullable=False, primary_key=True)
    section_number: Mapped[int] = mapped_column("section_number", nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column("semester", nullable=False, primary_key=True)
    section_year: Mapped[int] = mapped_column("section_year", nullable=False, primary_key=True)

    # Mappings to connect the Section and Student tables
    section: Mapped["Section"] = relationship(back_populates="students")
    student: Mapped["Student"] = relationship(back_populates="sections")

    # Making the table arguments to set up the constraints
    __table_args__ = (
        # Setting up the foreign key constraints
        ForeignKeyConstraint([department_abbreviation, course_number, section_number, semester, section_year],
                             ["sections.department_abbreviation", "sections.course_number", "sections.section_number",
                              "sections.semester", "sections.section_year"]),
        ForeignKeyConstraint([student_id], ["students.student_id"]),
        # For never having more than 1 enrollment for a student for the same course in a semester
        UniqueConstraint("department_abbreviation", "course_number", "semester", "section_year", "student_id",
                         name="Enrollments_uk_01")
    )

    def __init__(self, section, student):
        self.section = section
        self.student = student
        self.student_id = student.student_id
        self.department_abbreviation = section.department_abbreviation
        self.course_number = section.course_number
        self.section_number = section.section_number
        self.semester = section.semester
        self.section_year = section.section_year

    def __str__(self):
        return f"Student & Enrollment | Student: {self.student} | " \
               f"Course Number: {self.course_number} | Section: {self.section}|"
