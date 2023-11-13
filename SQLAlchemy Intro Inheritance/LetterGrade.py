from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped
from Enrollment import Enrollment


class LetterGrade(Enrollment):
    # Naming the table
    __tablename__ = "letter_grade"
    # Giving a surrogate key
    letterGradeId: Mapped[int] = mapped_column('letter_grade_id',
                                               ForeignKey("enrollments.enrollment_id",
                                                          ondelete="CASCADE"), primary_key=True)
    # Writing the minSatisfactory value("letter grade")
    minSatisfactory: Mapped[str] = mapped_column('min_satisfactory',
                                                 CheckConstraint("min_satisfactory IN ('A', 'B', 'C', 'D', 'F')",
                                                                 name="letter_grade_constraint"))
    __mapper_args__ = {"polymorphic_identity": "letter_grade"}

    # Making a constructor
    def __init__(self, section, student, min_satisfactory: String):
        super().__init__(section, student)
        self.minSatisfactory = min_satisfactory

    def __str__(self):
        """
        Outputting the "Letter Grade" with the enrollment, section, and student info
        :return:
        """
        return f"| Letter Grade: {self.minSatisfactory} | {super().__str__()}"
