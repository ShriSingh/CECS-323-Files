import logging
from menu_definitions import menu_main, student_select, debug_select
from db_connection import engine, Session
from orm_base import metadata
from Student import Student
from Department import Department  # --> Importing the newly created Department class
from Option import Option
from Menu import Menu


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    # Note that there is no physical way for us to duplicate the student_id since we are
    # using the Identity "type" for studentId and allowing PostgresSQL to handle that.
    # See more at: https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-identity-column/
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == lastName,
                                                        Student.firstName == firstName).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.eMail == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")
    newStudent = Student(lastName, firstName, email)
    session.add(newStudent)


def select_student_id(sess: Session) -> Student:
    """
    Prompt the user for a specific student by the student ID.  Generally
    this is not a terribly useful approach, but I have it here for
    an example.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    ID: int = -1
    while not found:
        ID = int(input("Enter the student ID--> "))
        id_count: int = sess.query(Student).filter(Student.studentId == ID).count()
        found = id_count == 1
        if not found:
            print("No student with that ID.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.studentId == ID).first()
    return return_student


def select_student_first_and_last_name(sess: Session) -> Student:
    """
    Select a student by the combination of the first and last name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student last name to delete--> ")
        firstName = input("Student first name to delete--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == lastName,
                                                     Student.firstName == firstName).count()
        found = name_count == 1
        if not found:
            print("No student by that name.  Try again.")
    oldStudent = sess.query(Student).filter(Student.lastName == lastName,
                                            Student.firstName == firstName).first()
    return oldStudent


def select_student_email(sess: Session) -> Student:
    """
    Select a student by the e-mail address.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    email: str = ''
    while not found:
        email = input("Enter the student email address --> ")
        id_count: int = sess.query(Student).filter(Student.eMail == email).count()
        found = id_count == 1
        if not found:
            print("No student with that email address.  Try again.")
    return_student: Student = sess.query(Student).filter(Student.eMail == email).first()
    return return_student


def find_student(sess: Session) -> Student:
    """
    Prompt the user for attribute values to select a single student.
    :param sess:    The connection to the database.
    :return:        The instance of Student that the user selected.
                    Note: there is no provision for the user to simply "give up".
    """
    find_student_command = student_select.menu_prompt()
    match find_student_command:
        case "ID":
            old_student = select_student_id(sess)
        case "first/last name":
            old_student = select_student_first_and_last_name(sess)
        case "email":
            old_student = select_student_email(sess)
        case _:
            old_student = None
    return old_student


def delete_student(session: Session):
    """
    Prompt the user for a student by the last name and first name and delete that
    student.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a student")
    oldStudent = find_student(session)
    session.delete(oldStudent)


def list_students(session: Session):
    """
    List all the students, sorted by the last name first, then the first name.
    :param session:
    :return:
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    students: [Student] = list(session.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


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
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
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
    returned_student = sess.query(Student).filter(Student.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def create_new_department(sess: Session):
    """
    Adds in a new department row to the database.
    Checks whether any uniqueness constraints are not violated.
    :param sess:    The connection to the database
    :return:        None
    """
    # Creating a loop to keep prompting the user until a new department is created
    while True:
        print("\nCreating a department...\n")
        # Asking for all the attributes about the department
        name = input("Enter the department name--> ")
        abbreviation = input("Enter the department abbreviation--> ")
        chair_name = input("Enter the department chair name--> ")
        building = input("Enter the department building--> ")
        office = input("Enter the department office--> ")
        description = input("Enter the department description--> ")

        # Configuring the attributes to equal their respective columns in the table while sending the query
        department_exists = sess.query(Department).filter(
            (Department.Abbreviation == abbreviation) |
            (Department.ChairName == chair_name) |
            ((Department.Building == building) & (Department.Office == office)) |
            (Department.Description == description)
        ).first()
        # Checking the query received
        if department_exists:
            # Re-prompting user if any uniqueness constraints are violated
            print("\nDepartment already exists. Try again.\n")
        else:
            # Calling the constructor to create a new department
            new_department = Department(name, abbreviation, chair_name, building, office, description)
            # Adding the new department to the database
            sess.add(new_department)
            # Committing the changes to the database
            sess.commit()
            # Printing a success message
            print("\nDepartment created successfully.\n")
            # Breaking out of the loop
            break


def select_department(sess: Session):
    """
    Displays all the departments and returns exactly one that the
    user had selected. Prompts the user for the field value(s) from
    one of the above uniqueness constraints. Presents the departments
    sorted by their name.
    :param sess:    The connection to the database
    :return:        The instance of department that the user selected.
    """
    # Creating a loop to keep prompting the user until a valid department is selected
    while True:
        # Displaying all the departments present by sending a query
        departments_list = sess.query(Department).order_by(Department.Name).all()
        print("\nSelect a department from the list below...")
        # Printing the departments in a numbered list, with an index printed out with each entry
        for row, department in enumerate(departments_list, start=1):
            print(f"{row}. | {department}")

        # Defining a try-except block to catch any invalid input
        try:
            # Asking the user to select a department
            department_selection = int(input("\nSelect a department(Enter number before each row)--> "))
            # Checking if the input is valid
            if 1 <= department_selection <= len(departments_list):
                # Storing the selected department from the list
                selected_department = departments_list[department_selection - 1]
                # Showing the selected department(I couldn't show it through the return below)
                print(f"\nDepartment selected--> | {selected_department}\n")
                # Returning the selected department for the valid input in delete_department()
                return selected_department
            else:
                # Re-prompting the user if the input is an invalid number
                print("\nInvalid number entered. Try again\n")
        except ValueError:
            # Re-prompting the user if the input is not a number
            print("Invalid input. Try again\n")


def delete_department(sess: Session):
    """
    Deletes a department from the database. Uses 'select_department()'
    to select a department to delete.
    :return:    None
    """
    # Preparing the user to select a department
    print("Select a department to delete...")
    # Calling the 'select_department()' function to select the asked department
    chosen_department = select_department(sess)
    # Checking if the department exists
    if chosen_department:
        print("Deleting department...")
        # Deleting the department if it exists
        sess.delete(chosen_department)
        # Syncing up the deletion with the database
        sess.commit()
        print("Department deleted successfully.")
    else:
        # Printing an error message if the department does not exist
        print("Department chosen does not exist.")


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

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
