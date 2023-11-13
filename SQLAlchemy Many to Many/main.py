import logging
from constants import *
from menu_definitions import menu_main, add_menu, delete_menu, list_menu, debug_select, introspection_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Student import Student
from Section import Section
from Major import Major
from StudentMajor import StudentMajor
from Enrollments import Enrollments
from Option import Option
from Menu import Menu
from datetime import time


def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


# The add_department() was also edited and reworked a bit
def add_department(session: Session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_abbreviation: bool = False
    unique_office = False
    unique_description = False
    name: str = ''
    abbreviation: str = ''
    chair_name = ''
    building = ''
    office = ''
    description = ''
    while not unique_abbreviation or not unique_office or not unique_description:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        chair_name = input("Department chair name--> ")
        building = input("Department building--> ")
        office = input("Department office--> ")
        description = input("Department description--> ")

        # Check if the attributes are unique
        abbreviation_count = session.query(Department).filter(Department.abbreviation == abbreviation).count()
        chair_name_count = session.query(Department).filter(Department.chair_Name == chair_name).count()
        office_count = session.query(Department).filter(Department.building == building,
                                                        Department.office == office).count()
        description_count = session.query(Department).filter(Department.description == description).count()

        unique_abbreviation = abbreviation_count == 0
        unique_chair_name = chair_name_count == 0
        unique_office = office_count == 0
        unique_description = description_count == 0

        if not unique_abbreviation:
            print("We already have a department with the same abbreviation. Try again.")
        elif not unique_chair_name:
            print("We already have a department with the same chair name. Try again.")
        elif not unique_office:
            print("We already have a department with the same office. Try again.")
        elif not unique_description:
            print("We already have a department with the same description. Try again.")

    new_department = Department(abbreviation, name, chair_name, building, office, description)
    session.add(new_department)


def add_course(session: Session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.departmentAbbreviation == department.abbreviation,
                       Course.course_number == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)


def add_major(session: Session):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this major?")
    department: Department = select_department(sess)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count: int = session.query(Major).filter(Major.department_abbreviation == department.abbreviation,
                                                      ).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    while not unique_email or not unique_name:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == last_name,
                                                        Student.firstName == first_name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.email == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that email address.  Try again.")
    new_student = Student(last_name, first_name, email)
    session.add(new_student)


def add_student_major(sess):
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That student already has that major.  Try again.")
        student = select_student(sess)
        major = select_major(sess)
    student.add_major(major)
    """The student object instance is mapped to a specific row in the Student table.  But adding
    the new major to its list of majors does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Student's majors list inside of the
    add_major method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_major method.  So instead, I add the student to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this student 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(student)  # add the StudentMajor to the session
    sess.flush()


def add_major_student(sess):
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That major already has that student.  Try again.")
        major = select_major(sess)
        student = select_student(sess)
    major.add_student(student)
    """The major object instance is mapped to a specific row in the Major table.  But adding
    the new student to its list of students does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Major's students list inside of the
    add_student method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_student method.  So instead, I add the major to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this major 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(major)  # add the StudentMajor to the session
    sess.flush()


def select_department(sess: Session) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_department: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_course(sess: Session) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                                    Course.course_number == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.course_number == course_number).first()
    return course


def select_student(sess) -> Student:
    """
    Select a student by the combination of the last and first.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == last_name,
                                                     Student.firstName == first_name).count()
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    student: Student = sess.query(Student).filter(Student.lastName == last_name,
                                                  Student.firstName == first_name).first()
    return student


def select_major(sess) -> Major:
    """
    Select a major by its name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = sess.query(Major).filter(Major.name == name).count()
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    major: Major = sess.query(Major).filter(Major.name == name).first()
    return major


def delete_student(session: Session):
    """
    Prompt the user for a student to delete and delete them.
    :param session:     The current connection to the database.
    :return:            None
    """
    student: Student = select_student(session)
    """This is a bit ghetto.  The relationship from Student to StudentMajor has 
    cascade delete, so this delete will work even if a student has declared one
    or more majors.  I could write a method on Student that would return some
    indication of whether it has any children, and use that to let the user know
    that they cannot delete this particular student.  But I'm too lazy at this
    point.
    """
    session.delete(student)


def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_student_major(sess):
    """Undeclare a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)


def delete_major_student(sess):
    """Remove a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def list_department(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_course(sess: Session):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = list(sess.query(Course).order_by(Course.course_number))
    for course in courses:
        print(course)


def list_student(sess: Session):
    """
    List all Students currently in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_major(sess: Session):
    """
    List all majors in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    majors: [Major] = list(sess.query(Major).order_by(Major.department_abbreviation))
    for major in majors:
        print(major)


def list_student_major(sess: Session):
    """Prompt the user for the student, and then list the majors that the student has declared.
    :param sess:    The connection to the database
    :return:        None
    """
    student: Student = select_student(sess)
    recs = sess.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_major_student(sess: Session):
    """Prompt the user for the major, then list the students who have that major declared.
    :param sess:    The connection to the database.
    :return:        None
    """
    major: Major = select_major(sess)
    recs = sess.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def move_course_to_new_department(sess: Session):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param sess:    The connection to the database.
    :return:        None
    """
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = select_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = sess.query(Course). \
                filter(Course.departmentAbbreviation == new_department.abbreviation,
                       Course.course_number == course.course_number).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def boilerplate(sess):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param sess:    The session that's open.
    :return:        None
    """
    department: Department = Department('CECS', 'Computer Engineering Computer Science')
    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')
    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')
    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')
    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')
    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')
    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    sess.add(department)
    sess.add(major1)
    sess.add(major2)
    sess.add(student1)
    sess.add(student2)
    sess.add(student3)
    sess.flush()  # Force SQLAlchemy to update the database, although not commit


def session_rollback(sess):
    """
    Give the user a chance to roll back to the most recent commit point.
    :param sess:    The connection to the database.
    :return:        None
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())


# Writing new code from here on out
def select_section(sess: Session):
    """
    Function to select a section from the database
    """
    section_found = False
    abbreviation: str = ''
    course_number: int = -1
    section_number: int = -1
    section_year: int = -1
    semester: str = ''

    while not section_found:
        abbreviation = input("Enter the department abbreviation: ")
        course_number = int(input("Enter the course number: "))
        section_number = int(input("Enter the section number: "))
        section_year = int(input("Enter the section year: "))
        semester = input("Enter the semester: ")

        uniqueness_check = sess.query(Section).filter(Section.departmentAbbreviation == abbreviation,
                                                      Section.course_number == course_number,
                                                      Section.section_number == section_number,
                                                      Section.section_year == section_year,
                                                      Section.semester == semester).count()
        section_found = uniqueness_check == 1
        if not section_found:
            print("There is ano section with that information. Please try again.")

    section_check = sess.query(Section).filter(Section.departmentAbbreviation == abbreviation,
                                               Section.course_number == course_number,
                                               Section.section_number == section_number,
                                               Section.section_year == section_year,
                                               Section.semester == semester).first()

    return section_check


def time_check() -> time:
    """
    Function to whether the time value entered is valid
    """
    # Setting the status of the time value to entered is 'False'
    time_status = False
    while not time_status:
        time_entered = input("Input start time: ")
        # Checking if the number of integer values for time is 7 or 8
        if len(time_entered) != 7 and len(time_entered) != 8:
            print("Invalid time format. Please try something like '1:30PM' or '01:30PM'")
        else:
            # Checking when the colon is in the time value
            if time_entered[1] == ":":
                time_status = True
                # Checking 'PM' is entered for times after 12:00
                if time_entered[5:] == "PM":
                    # Converting the time to 24-hour format
                    hour_value = int(time_entered[0]) + 12
                else:
                    hour_value = int(time_entered[0])
                minute_value = int(time_entered[2:4])
            elif time_entered[2] == ":":
                time_status = True
                # Checking 'PM' is entered for times after 12:00
                if time_entered[6:] == "PM":
                    # Converting the time to 24-hour format
                    hour_value = int(time_entered[:2]) + 12
                else:
                    hour_value = int(time_entered[:2])
                minute_value = int(time_entered[3:5])
            else:
                print("Invalid time format. Please try something like '1:30PM' or '01:30PM'")

    return time(hour_value, minute_value, 0)


def add_section(sess: Session):
    """
    Adds a section to a course in the database
    """
    print("Select the course to add a section for...")
    course: Course = select_course(sess)
    # Allowed semester values
    semester_values = ['Fall', 'Winter', 'Spring', 'Summer I', 'Summer II']
    # Allowed days of the week
    day_values = ['MW', 'TuTh', 'MWF', 'F', 'S']
    # Allowed building values
    building_values = ['VEC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', 'SSPA']

    # Setting the status of the section to entered is 'False'
    section_status = False

    while not section_status:
        valid_semester_value = False
        valid_day_value = False
        valid_building_value = False
        while not valid_semester_value:
            semester = input("Enter semester: ")
            if semester not in semester_values:
                print("Semester has to be 'Fall', 'Winter', 'Spring', 'Summer I', or 'Summer II'. Please try again.")
            else:
                valid_semester_value = True
        section_year = int(input("Enter section year: "))
        while not valid_day_value:
            days = input("Enter days: ")
            if days not in day_values:
                print("Days have to be 'MW', 'TuTh', 'MWF', 'F', or 'S'. Please try again.")
            else:
                valid_day_value = True
        start_time = time_check()

        instructor = input("Enter instructor name: ")
        instructor_check = sess.query(Section).filter(
            Section.section_year == section_year,
            Section.semester == semester,
            Section.schedule == days,
            Section.start_time == start_time,
            Section.instructor == instructor
        ).count()

        unique_instructor = instructor_check == 0
        if not unique_instructor:
            print("The entered instuctor is already booked for the scheduled time. Please try again.")
        else:
            while not valid_building_value:
                building = input("Enter building: ")
                if building not in building_values:
                    print("Building has to be 'VEC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', or 'SSPA'. Please try again.")
                else:
                    valid_building_value = True
            room = int(input("Enter room number: "))

            selection_check = sess.query(Section).filter(Section.section_year == section_year,
                                                         Section.semester == semester,
                                                         Section.schedule == days,
                                                         Section.start_time == start_time,
                                                         Section.building == building,
                                                         Section.room == room).count()

            unique_selection = selection_check == 0
            if not unique_selection:
                print("The selection for room is already reserved. Please try again.")
    section = Section(course, section_year, semester, section_year, building, room, days, start_time, instructor)
    sess.add(section)


def add_student_to_section(sess: Session):
    """
    Function to enroll a student in a section
    """
    student: Student = select_student(sess)
    section: Section = select_section(sess)

    student_section_check = sess.query(Enrollments).filter(Enrollments.student_id == student.studentID,
                                                           Enrollments.department_abbreviation == section.departmentAbbreviation,
                                                           Enrollments.course_number == section.course_number,
                                                           Enrollments.section_number == section.section_number,
                                                           Enrollments.section_year == section.section_year,
                                                           Enrollments.semester == section.semester).count()
    uniqueness_check = student_section_check == 0
    while not uniqueness_check:
        print("Input student is already present in the section. Please try again")
        student = select_student(sess)
        section = select_section(sess)
    student.add_section(section)
    sess.add(student)
    sess.flush()


def add_section_to_student(sess: Session):
    """
    Function to enroll a student in a section
    """
    section: Section = select_section(sess)
    student: Student = select_student(sess)
    section_student_check = sess.query(Enrollments).filter(Enrollments.student_id == student.studentID,
                                                           Enrollments.department_abbreviation == section.departmentAbbreviation,
                                                           Enrollments.course_number == section.course_number,
                                                           Enrollments.section_number == section.section_number,
                                                           Enrollments.section_year == section.section_year,
                                                           Enrollments.semester == section.semester).count()
    uniqueness_check = section_student_check == 0
    while not uniqueness_check:
        print("Input section already has the student. Please try again.")
        section = select_section(sess)
        student = select_student(sess)
    section.add_student(student)
    sess.add(section)
    sess.flush()


def delete_section(sess: Session):
    """
    Function to delete a section from the database
    """
    section: Section = select_section(sess)
    # Calculates the number of students in the section
    number_of_students = sess.query(Section).join(
        Enrollments,
        (Enrollments.department_abbreviation == Section.departmentAbbreviation) &
        (Enrollments.course_number == Section.course_number) &
        (Enrollments.section_number == Section.section_number) &
        (Enrollments.section_year == Section.section_year) &
        (Enrollments.semester == Section.semester)).join(Student, Enrollments.student_id == Student.studentID).filter(
        (section.department_abbreviation == Section.departmentAbbreviation) &
        (section.course_number == Section.course_number) &
        (section.section_number == Section.section_number) &
        (section.section_year == Section.section_year) &
        (section.semester == Section.semester)
    ).count()

    if number_of_students > 0:
        print(f"You need to remove {number_of_students} students from the section before deleting it.")
    else:
        sess.delete(section)


def delete_student_to_section(sess):
    """
    Function to remove a student from a section
    """
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    student.remove_section(section)


def delete_section_to_student(sess):
    """
    Function to remove a section from a student is enrolled in
    """
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    section.remove_student(student)


def list_section(sess: Session):
    """
    Function to list all the sections in the database
    """
    # Initializing section found status, department abbreviation, course number
    section_found = False
    department_abbreviation = ''
    course_number = -1

    while not section_found:
        department_abbreviation = input("Enter the department abbreviation: ")
        course_number = int(input("Enter the course number: "))
        unique_section = sess.query(Section).filter(Section.department_abbreviation == department_abbreviation,
                                                    Section.course_number == course_number).count()
        section_found = unique_section >= 1
        if not section_found:
            print("There is no section with that information. Please try again.")
    sections: [Section] = list(sess.query(Section).filter(Section.department_abbreviation == department_abbreviation,
                                                          Section.course_number == course_number))
    print(f"Prints all sections for {course_number} course number in {department_abbreviation} department...")
    for section in sections:
        print(section)


def list_student_to_section(sess: Session):
    """
    Lists all the students enrolled in a section
    """
    student: Student = select_student(sess)
    # Counting all the students in a particular section
    student_section_count = sess.query(Student).join(Enrollments, Student.studentID == Enrollments.student_id).join(
        Section,
        (Enrollments.department_abbreviation == Section.departmentAbbreviation) &
        (Enrollments.course_number == Section.course_number) &
        (Enrollments.section_number == Section.section_number) &
        (Enrollments.section_year == Section.section_year) &
        (Enrollments.semester == Section.semester)).filter(
        (Student.studentID == student.studentID)).add_columns(
        Student.lastName, Student.firstName, Section.course_number, Section.section_number).all()
    # Printing out the results
    for student in student_section_count:
        print(f"Student name: {student.lastName}, {student.firstName} | Section Number: {student.section_number} |")


def list_section_to_student(sess: Session):
    """
    Lists all the sections enrolled in by a student
    """
    section: Section = select_section(sess)
    # Counting all the sections enrolled in by a student
    section_student_count = sess.query(Section).join(
        Enrollments,
        (Enrollments.department_abbreviation == Section.department_abbreviation) &
        (Enrollments.course_number == Section.course_number) &
        (Enrollments.section_number == Section.section_number) &
        (Enrollments.section_year == Section.section_year) &
        (Enrollments.semester == Section.semester)).join(
        Student, Enrollments.student_id == Student.studentID).filter(
        (section.department_abbreviation == Section.departmentAbbreviation) &
        (section.course_number == Section.course_number) &
        (section.section_number == Section.section_number) &
        (section.section_year == Section.section_year) &
        (section.semester == Section.semester)
    ).add_columns(
        Student.lastName, Student.firstName, Section.course_number, Section.section_number).all()
    # Printing out the results
    for section in section_student_count:
        print(f"Student name: {section.lastName}, {section.firstName} | "
              f"Course & Section Number: {section.course_number}-{section.section_number}|")


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
