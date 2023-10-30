from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Student(Base):
    """An individual who is currently enrolled or has explicitly stated an intent
    to enroll in one or more classes.  Said individuals may or may not be admitted
    to the university.  For instance, open enrollment students have not (yet) been
    admitted to the university, but they are still students."""
    __tablename__ = "students"  # Give SQLAlchemy th name of the table.
    studentId: Mapped[int] = mapped_column('student_id', Integer, Identity(start=1, cycle=True),
                                           nullable=False, primary_key=True)
    lastName: Mapped[str] = mapped_column('last_name', String(50), nullable=False)
    firstName: Mapped[str] = mapped_column('first_name', String(50), nullable=False)
    eMail: Mapped[str] = mapped_column('e_mail', String(80), nullable=False)
    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want two separate uniqueness
    # constraints (candidate keys).
    __table_args__ = (UniqueConstraint("last_name", "first_name", name="students_uk_01"),
                      UniqueConstraint("e_mail", name="students_uk_02"))

    def __init__(self, last_name: str, first_name: str, e_mail: str):
        self.lastName = last_name
        self.firstName = first_name
        self.eMail = e_mail

    def __str__(self):
        return f"Student id: {self.studentId} name: {self.lastName}, {self.firstName}\nEmail Address: {self.eMail}"
