# Importing libraries
from orm_base import Base
from db_connection import engine
from typing import List
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, Time
from sqlalchemy import String, Integer, Column, Identity, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy.types import Time
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES
from IntrospectionFactory import IntrospectionFactory
from Course import Course
from Enrollments import Enrollments

# Calling the conditional to start over or reuse the tables
introspection_type = IntrospectionFactory().introspection_type


class Section(Base):
    # Naming the table
    __tablename__ = "sections"

    # Bring in the migrated foreign keys
    # To be used as foreign key constraints
    department_abbreviation: Mapped[str] = mapped_column("department_abbreviation", String(10), nullable=False,
                                                         primary_key=True)
    course_number: Mapped[int] = mapped_column("course_number", nullable=False, primary_key=True)
    # Making up columns of the table
    section_number: Mapped[int] = mapped_column("section_number", Integer, Identity(start=1, cycle=True),
                                                nullable=False, primary_key=True)
    # Make the semester to only accept values: 'Fall', 'Winter', 'Spring', 'Summer I', or 'Summer II'
    semester: Mapped[str] = mapped_column("semester", String(10), nullable=False, primary_key=True)
    section_year: Mapped[int] = mapped_column("section_year", Integer, nullable=False, primary_key=True)
    # Make the building to only accept values: 'VEC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', or 'SSPA'
    building: Mapped[str] = mapped_column("building", String(6), nullable=False)
    room: Mapped[int] = mapped_column("room", Integer, nullable=False)
    # Make the schedule to only accept values: 'MW', 'TuTh', 'MWF', 'F', or 'S'
    schedule: Mapped[str] = mapped_column("schedule", String(6), nullable=False)
    start_time: Mapped[Time] = mapped_column("start_time", Time, nullable=False)
    instructor: Mapped[str] = mapped_column("instructor", String(80), nullable=False)

    # Making the relationship to "Course" table
    course: Mapped["Course"] = relationship(back_populates="sections")
    # Making the relationship to "Enrollment" table
    students: Mapped[List["Enrollments"]] = relationship(back_populates="Sections",
                                                         cascade="all, save-update, delete-orphan")

    # Making the table arguments to set up the constraints
    __table_args__ = (
        ForeignKeyConstraint([department_abbreviation, course_number],
                             [Course.department_abbreviation, Course.course_number]),
        # For never having more than 1 section meeting in the same room at the same time
        UniqueConstraint("section_year", "semester", "schedule", "start_time",
                         "building", "room", name="Sections_uk_01"),
        # For never over booking an instructor and have them teaching two sections at the same time
        UniqueConstraint("section_year", "semester", "schedule", "start_time",
                         "instructor", name="Sections_uk_02")
    )

    def __init__(self, course: Course, semester, section_year, building, room, schedule, start_time, instructor):
        self.set_courses(course)
        self.department_abbreviation = self.course.department_abbreviation
        self.semester = semester
        self.section_year = section_year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.start_time = start_time
        self.instructor = instructor

    def add_student(self, student):
        """
        Adds a student to the section by calling the
        Enrollment class if not present
        otherwise returns nothing
        """
        for student_check in self.students:
            if student_check.student == student:
                return
        student_to_section = Enrollments(self, student)

    def remove_student(self, student):
        """
        Removes a student from the section if present
        otherwise returns nothing
        """
        for student_check in self.students:
            if student_check.student == student:
                self.students.remove(student_check)
                return

    def set_courses(self, course: Course):
        """
        Sets the course for the section
        by calling the constructor and its columns
        """
        self.course = course
        self.course_number = course.course_number
        self.department_abbreviation = course.department_abbreviation

    def __str__(self):
        return f"Department Abbreviation: {self.department_abbreviation} | Section Number: {self.section_number} " \
               f"Course Number: {self.course_number} | Semester: {self.semester} |" \
               f"Section Year: {self.section_year} | Building: {self.building} |" \
               f"Room: {self.room} | Schedule: {self.schedule} |" \
               f"Start Time: {self.start_time} | Instructor: {self.instructor}"
