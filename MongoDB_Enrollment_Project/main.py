import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from datetime import datetime
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
import schemas
def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)

def add_department(db):
    """
    Add a new department, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    departments collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the department's collection.
    :return:            None
    """

    try:
        # Create a "pointer" to the departments collection within the db database.
        collection = db["departments"]

        name = input("Department name--> ")

        abbreviation = input("Department abbreviation--> ")
        chairName = input("Chair name--> ")
        building = input("Building--> ")
        office = int(input("Office#--> "))
        description = input("Description--> ")

        # Build a new departments document preparatory to storing it
        department = {
            "name": name,
            "abbreviation": abbreviation,
            "chair_name": chairName,
            "building": building,
            "office": office,
            "description": description,
            "majors": [],
            "course": []
        }
        results = collection.insert_one(department)

    except Exception as exception:
        print(exception)
        return add_department(db)

def add_major(db):
    """
    Add a new major, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    departments collection.
    :param collection:  The pointer to the major's collection.
    :return:            None
    """
    try:
        # A major cannot exist without a department, so select a
        # department this major will be offered by
        print("Which department will this major belong to")
        department = select_department(db)
        # Create a "pointer" to the majors collection within the db database.
        collection = db["majors"]

        # Ask about information necessary to create major
        name = input("Major Name--> ")
        description = input("Major Description--> ")

        # Build a new majors document preparatory to storing it
        major = {
            "name": name,
            "description": description,
            "major_students": []
        }
        results = collection.insert_one(major)

        # Major has been created, so now add it to the list of majors in department chosen
        collection2 = db["departments"]
        results2 = collection2.update_one({"_id": department["_id"]}, {"$push": {"majors": major["_id"]}})

    except Exception as exception:
        print(exception)
        return add_major(db)


def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    departments collection.
    :param collection:  The pointer to the student's collection.
    :return:            None
    """

    try:
        # Create a "pointer" to the departments collection within the db database.
        collection = db["students"]

        lastname = input("Student last name--> ")
        firstname = input("Student first name--> ")
        email = input("Student's email--> ")

        # Build a new students document preparatory to storing it
        student = {
            "last_name": lastname,
            "first_name": firstname,
            "e_mail": email,
        }
        results = collection.insert_one(student)

    except Exception as exception:
        print(exception)
        return add_student(db)


def add_major_student(db):
    """
    :param collection:  The pointer to the major's collection.
    :return:            None
    Add a major to a student in majorstudent
    """
    try:
        print("Assigning a major to a student...")
        major = select_major(db)
        student = select_student(db)
        collection = db["majorstudents"]
        collection2 = db["majors"]

        majorstudent = {
            "student": student["_id"],
            "major_name": major["name"],
            "declaration_date": datetime.utcnow()
        }
        results = collection.insert_one(majorstudent)
        result2 = collection2.update_one({"_id": major["_id"]}, {"$push": {"major_students": majorstudent["_id"]}})

    except Exception as exception:
        print(exception)
        return add_major_student(db)


def select_department(db):
    """
    Select a department by abbreviation.
    :param db:      The connection to the database.
    :return:        The selected department as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Department document from
                    the database.
    """
    # Create a connection to the departments collection from this database
    collection = db["departments"]
    found: bool = False
    abbreviation: str = ''

    while not found:
        abbreviation = input("Department abbreviation--> ")
        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    found_department = collection.find_one({"abbreviation": abbreviation})
    return found_department

def select_major(db):
    """
    Select a major by name.
    :param db:      The connection to the database.
    :return:        The selected major as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Major document from
                    the database.
    """
    # Create a connection to the departments collection from this database
    collection = db["majors"]
    found: bool = False
    name: str = ''

    while not found:
        name = input("Major name--> ")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No major with that name.  Try again.")
    found_major = collection.find_one({"name": name})
    return found_major


def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student


def select_course(db):
    """
    Select a course by course name and department abbreviation.
    :param db: The connection to the database.
    :return: The selected course as a dict.
    """
    collection = db["courses"]
    found = False

    while not found:
        course_name = input("Course name--> ")
        department_abbreviation = input("Department abbreviation--> ")

        count = collection.count_documents({
            "course_name": course_name,
            "department_abbreviation": department_abbreviation
        })
        found = count == 1

        if not found:
            print("No course found with that name and department abbreviation. Try again.")

    found_course = collection.find_one({
        "course_name": course_name,
        "department_abbreviation": department_abbreviation
    })
    return found_course


def select_section(db):
    """
    Select a section by course number, semester, and section year.
    :param db: The connection to the database.
    :return: The selected section as a dict.
    """
    collection = db["sections"]
    found = False

    course = select_course(db)

    if course:
        course_number = course["course_number"]

        while not found:
            section_number = int(input("Section number--> "))
            semester = input("Semester--> ")
            section_year = int(input("Section year--> "))
            building = input("Building--> ")
            room = int(input("Room--> "))
            schedule = input("Schedule (e.g., MW, TuTh) --> ")
            start_time = input("Start Time (format HH:MM AM/PM) --> ")
            instructor = input("Instructor --> ")

            count = collection.count_documents({
                "course_number": course_number,
                "section_number": section_number,
                "semester": semester,
                "section_year": section_year,
                "building": building,
                "room": room,
                "schedule": schedule,
                "start_time": start_time,
                "instructor": instructor
            })
            found = count == 1

            if not found:
                print("No section found with the previous fields. Try again.")

    found_section = collection.find_one({
        "course_number": course_number,
        "section_number": section_number,
        "semester": semester,
        "section_year": section_year,
        "building": building,
        "room": room,
        "schedule": schedule,
        "start_time": start_time,
        "instructor": instructor
    })
    return found_section

def delete_department(db):
    """
    Delete a department from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # department isn't a Department object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected department, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["departments"]
    result1 = departments.find({"majors": {"$exist": "true"}})
    if result1:
        print("Majors rely on this department. You cannot delete. Try again.")
        return delete_major(db)
    # department["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} department(s).")


def delete_student(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    student = select_student(db)
    # Create a "pointer" to the students collection within the db database.
    students = db["students"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = students.delete_one({"_id": student["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} students.")


def delete_major(db):
    major = select_major(db)
    # Create a "pointer" to the majors collection within the db database.
    majors = db["majors"]
    # major["_id"] returns the _id value from the selected major document.
    # make sure student doesn't depend on major
    collection = db["majorstudents"]
    result = collection.count_documents({"major_name": major["name"]})
    if result > 0:
        print("Students rely on this major. You cannot delete major. Try again.")
        return delete_major(db)
    # find department document where major array has that major_id
    collection2 = db["departments"]
    result2 = collection2.find_one({"majors": {"$eq": major["_id"]}}) #because a major can only belong to one department
    collection2.update_one({"_id": result2["_id"]}, {"$pull": {"majors": major["_id"]}})
    deleted = majors.delete_one({"_id": major["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} majors.")


def delete_student_major(db):
    print("Choose the student to un-enroll from a major")
    student = select_student(db)
    collection = db["students"]
    # check if student has any majors to begin with
    collection = db["majorstudents"]
    if collection.find_one({"student": student["_id"]}) is None:
        print("Student doesn't have any majors to delete. Try again.")
        return delete_student_major(db)

    found = collection.find({"student": student["_id"]})
    print("Major(s) of ", student["first_name"], student["last_name"], ":")
    list1 = []
    i = 1
    for majorstudent in found:
        print(f"\t{i} --> ", majorstudent["major_name"])
        list1.append(majorstudent["major_name"])
        i += 1

    user = int(input("Input number corresponding to major--> "))

    while user < 1 or user >= i:
        print("Invalid input. Try again.")
        user = int(input("Input number corresponding to major--> "))

    collection.delete_one({"student": student["_id"], "major_name": list1[(user-1)]})
    print("Student has been successfully removed from student.")






def list_department(db):
    """
    List all the departments, sorted by the name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from departments.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)


def list_major(db):
    """
    List all the majors, sorted by the name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from departments.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    majors = db["majors"].find({}).sort([("name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for major in majors:
        pprint(major)


def list_student(db):
    """
    List all the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)

def list_major_student(db):
    """
    list majors of a student
    """
    student = select_student(db)

    collection = db["majorstudents"]
    found = collection.find({"student": student["_id"]})
    print("Major(s) of ", student["first_name"], student["last_name"], ":")

    for majorstudent in found:
        print(majorstudent["major_name"])


def add_course(db):
    courses = db["courses"]
    departments = db["departments"]

    department = select_department(db)

    if department:
        department_abbreviation = department["abbreviation"]
        course_name = input("Enter the course name: ")
        course_number = int(input("Enter the course number: "))
        description = input("Enter the course description: ")
        units = int(input("Enter the number of units: "))

        while True:
            # Validate input data against the schema
            course_data = {
                "department_abbreviation": department_abbreviation,
                "course_name": course_name,
                "course_number": course_number,
                "description": description,
                "units": units,
            }

            try:
                # Insert the course into the courses collection
                result = courses.insert_one(course_data)

                # Get the inserted course's _id
                course_id = result.inserted_id

                # Update the corresponding department with the new course reference
                departments.update_one(
                    {"abbreviation": department_abbreviation},
                    {"$addToSet": {"courses": course_id}}
                )

                print("Course and department updated successfully.")
                break
            except Exception as e:
                print(f"Error adding course: {e}")
                add_course()


def list_courses_by_department(db):
    department = select_department(db)

    if not department:
        print("Department not found.")
        return

    collection = db["courses"]
    found = collection.find({"department": department["abbreviation"]})

    if found.count() == 0:
        print(f"No courses found for {department['abbreviation']}")
        return

    print(f"Course(s) of {department['abbreviation']}")

    for courses in found:
        print(courses["course_name"])


def list_sections_by_course(db):
    course = select_course(db)

    if not course:
        print("Course not found.")
        return

    collection = db["sections"]
    found = collection.find({"course": course["course_number"]})

    if found.count() == 0:
        print(f"No sections found for {course['course_number']}")
        return

    print(f"Section(s) of {course['course_number']}")

    for section in found:
        print(f"Semester: {section['semester']}, "
              f"Section Year: {section['section_year']}, "
              f"Building: {section['building']}, "
              f"Room: {section['room']}, "
              f"Schedule: {section['schedule']}, "
              f"Start Time: {section['startTime']}, "
              f"Instructor: {section['instructor']}")


def delete_course(db):
    course_number = input("Enter the course name to delete: ")
    courses_collection = db["Courses"]
    sections_collection = db["Sections"]
    # Try to delete the course
    if sections_collection.count_documents({"course_number": course_number}) > 0:
        print("Cannot delete the course. There are sections associated with it.")
        return

    try:
        result = courses_collection.delete_one({'course_number': course_number})
        if result.deleted_count > 0:
            print(f"Course '{course_number}' deleted successfully.")
        else:
            print(f"Course '{course_number}' not found.")

    except Exception as e:
        print(f"Error deleting course: {e}")


def add_section(db):
    sections_collection = db["Sections"]

    course = select_course(db)

    if course:
        course_number = course["course_number"]
        while True:
            section_number = int(input("Enter the section number: "))
            semester = input("Enter the semester (e.g., Fall, Spring): ")
            section_year = int(input("Enter the section year: "))
            building = input("Enter the building: ")
            room = int(input("Enter the room: "))
            schedule = input("Enter the schedule (e.g., MW, TuTh): ")
            start_time = input("Enter the start time (format HH:MM AM/PM): ")
            instructor = input("Enter the instructor: ")

            section_data = {
                "course_number": course_number,
                "section_number": section_number,
                "semester": semester,
                "section_year": section_year,
                "building": building,
                "room": room,
                "schedule": schedule,
                "start_time": start_time,
                "instructor": instructor
            }

            try:
                result = sections.insert_one(section_data)
                print("Section added successfully.")

                courses.update_one({"course_number": course_number}, {"$addToSet": {"sections": result.inserted_id}})
                print("Reference updated in courses collection.")

                break  # Exit the loop if successful
            except Exception as e:
                print(f"Error adding section: {e}")
                add_section()


def delete_section(db):
    section = select_section()
    course_number = section["course_number"]
    section_number = section["section_number"]

    enrollment_collection = db["Enrollments"]
    sections_collection = db["Sections"]

    if enrollment_collection.count_documents({"course_number" : course_number},{"section_number": section_number}) > 0:
        print("Cannot delete the section. There are enrollments associated with it.")
        return

    try:
        result = sections_collection.delete_one({"course_number" : course_number},{"section_number": section_number})
        if result.deleted_count > 0:
            print(f"Section '{section_number}' of Course {course_number} deleted successfully.")
        else:
            print(f"Section '{section_number}' of Course {course_number} not found.")

    except Exception as e:
        print(f"Error deleting section: {e}")

def add_enrollment(db):
    section_collection = db["Sections"]
    student_collection = db["Students"]
    
    section = select_section(db)

    if section:
        section_number = section["section_number"]




def create_index(collection, index_keys, unique=True, name=None):
    existing_indexes = collection.index_information()
    if name not in existing_indexes:
        collection.create_index(index_keys, unique=unique, name=name)
        print(f"Index '{name}' created.")
    else:
        print(f"Index '{name}' already exists.")


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password[katiemartinezzz] -->')
    username: str = input('Database username [katiemartinezz] -->')
    project: str = input('Mongo project name [cluster0] -->')
    hash_name: str = input('7-character database hash [f9msjoe] -->')
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority&authSource=admin")
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["CECS-323-Spring-2023"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # department is our departments collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.


    departments = db["departments"]
    majors = db["majors"]
    students = db["students"]
    majorstudents = db["majorstudents"]
    courses = db["courses"]
    enrollments = db["enrollments"]
    sections = db["sections"]


#######################
    db.command("collMod", "departments", validator=schemas.departments_validator)
    db.command("collMod", "courses", validator=schemas.courses_validator)
    db.command("collMod", "majors", validator=schemas.majors_validator)
    db.command("collMod", "students", validator=schemas.students_validator)
    db.command("collMod", "majorstudents", validator=schemas.majorstudents_validator)
    db.command("collMod", "enrollments", validator=schemas.enrollments_validator)
    db.command("collMod", "sections", validator=schemas.sections_validator)

    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")

    # ************************** Set up the departments collection
    departments_indexes = departments.index_information()

    if 'departments_name' in departments_indexes.keys():
        print("name index present.")
    else:
        # Create a UNIQUE index on just the name
        departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='departments_name')


    if 'departments_abbreviation' in departments_indexes.keys():
        print("abbreviation index present.")
    else:
        # Create a UNIQUE index on just the abbreviation
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation')

    if 'departments_chair_names' in departments_indexes.keys():
        print("chair name index present.")
    else:
        # Create a single UNIQUE index on the chair name.
        departments.create_index([('chair_name', pymongo.ASCENDING)],
                              unique=True,
                              name="departments_chair_name")

    if 'departments_building_and_office' in departments_indexes.keys():
        print("building and office index present.")
    else:
        # Create a single UNIQUE index on BOTH the building and office.
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                              unique=True,
                              name="departments_building_and_office")

    major_count = majors.count_documents({})
    print(f"Majors in the collection so far: {major_count}")

    # ************************** Set up the sections collection

    # Create the indexes
    create_index(sections, [('course_number', pymongo.ASCENDING), ('section_number', pymongo.ASCENDING),
                            ('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING)],
                 name='course_section_semester_year_index')
    create_index(sections,
                 [('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING), ('building', pymongo.ASCENDING),
                  ('room', pymongo.ASCENDING), ('schedule', pymongo.ASCENDING), ('start_time', pymongo.ASCENDING)],
                 name='semester_building_room_schedule_start_time_index')
    create_index(sections,
                 [('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING), ('schedule', pymongo.ASCENDING),
                  ('start_time', pymongo.ASCENDING), ('instructor', pymongo.ASCENDING)],
                 name='semester_schedule_start_time_instructor_index')
    create_index(sections, [('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                            ('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING),
                            ('student_id', pymongo.ASCENDING)], name='semester_department_course_student_index')
    # ************************** Set up the majors collection
    majors_indexes = majors.index_information()

    if 'majors_name' in majors_indexes.keys():
        print("name index present.")
    else:
        # Create a UNIQUE index on just the name
        majors.create_index([('name', pymongo.ASCENDING)], unique=True, name='majors_name')


    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

    # ************************** Set up the courses collection
    courses_indexes = courses.index_information()

    if 'department_abbreviation_course_number' in courses_indexes.keys():
        print("department abbreviation and course number index present.")
    else:
        # Create a UNIQUE index on department abbreviation and course number
        courses.create_index(
            [('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING)],
            unique=True,
            name='department_abbreviation_course_number'
        )

    if 'department_abbreviation_course_name' in courses_indexes.keys():
        print("department abbreviation and course name index present.")
    else:
        # Create a UNIQUE index on department abbreviation and course name
        courses.create_index(
            [('department_abbreviation', pymongo.ASCENDING), ('course_name', pymongo.ASCENDING)],
            unique=True,
            name='department_abbreviation_course_name'
        )

    course_count = courses.count_documents({})
    print(f"Courses in the collection so far: {course_count}")

    # Add more indexes as needed based on your requirements

    section_count = sections.count_documents({})
    print(f"Sections in the collection so far: {section_count}")

    # ************************** Set up the sections collection
    sections_indexes = sections.index_information()

    if 'sections_name' in sections_indexes.keys():
        print("name index present.")
    else:
        # Create a UNIQUE index on just the section name
        sections.create_index([('section_name', pymongo.ASCENDING)], unique=True, name='sections_name')

    # ************************** Set up the students collection
    students_indexes = students.index_information()
    if 'students_last_and_first_names' in students_indexes.keys():
        print("first and last name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                              unique=True,
                              name="students_last_and_first_names")
    if 'students_e_mail' in students_indexes.keys():
        print("e-mail address index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')

    # ************************** Set up the majorstudents collection
    majorstudents_indexes = majorstudents.index_information()
    if 'majorstudents_student_majorname' in students_indexes.keys():
        print("majorstudent index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        majorstudents.create_index([('student', pymongo.ASCENDING), ('major_name', pymongo.ASCENDING)],
                              unique=True,
                              name="majorstudents_student")

    #pprint(students.index_information())
    #pprint(majors.index_information())
    #pprint(departments.index_information())
    # ************************** Set up the enrollments collection
    enrollments = db["enrollments"]
    enrollment_count = enrollments.count_documents({})
    print(f"Enrollments in the collection so far: {enrollment_count}")
    enrollments_indexes = enrollments.index_information()
    if 'enrollment_id' in enrollments_indexes.keys():
        print("enrollment id index present.")
    else:
        enrollments.create_index([('student_id', pymongo.ASCENDING), ('section_number', pymongo.ASCENDING)],
                                 unique=True, name='enrollment_id')
    if 'current_enrollment' in enrollments_indexes.keys():
        print("enrollment index present.")
    else:
        enrollments.create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                                  ('department_abbreviation', pymongo.ASCENDING),
                                  ('course_number', pymongo.ASCENDING),
                                  ('student_id', pymongo.ASCENDING)],
                                 unique=True, name='current_enrollment')
    pprint(enrollments.index_information())

    # ************************** Set up the passfail collection
    passfail = db["pass_fail"]
    passfail_count = passfail.count_documents({})
    print(f"Enrollmentts in the collection so far: {passfail_count}")
    pass_fail_indexes = passfail.index_information()
    if 'pass_fail_id' in pass_fail_indexes.keys():
        print("passfail grade present.")
    else:
        # id?
        # passfail.create_index([('enrollment_id', pymongo.ASCENDING)], unique=True, name='pass_fail_id')
        passfail.create_index([('passfail_id', pymongo.ASCENDING)], unique=True, name='pass_fail_id')
    if 'pass_fail_application_date' in pass_fail_indexes.keys():
        print("application date present.")
    else:
        passfail.create_index([('application_date', pymongo.ASCENDING)], unique=True,
                              name='pass_fail_application_date')
    pprint(passfail.index_information())

    # ************************** Set up the lettergrade collection
    lettergrade = db["letter_grade"]
    letter_grade_count = lettergrade.count_documents({})
    print(f"Enrollmentts in the collection so far: {passfail_count}")
    letter_grade_indexes = lettergrade.index_information()
    if 'letter_grade_id' in letter_grade_indexes.keys():
        print("letter grade present")
    else:
        # id?
        # lettergrade.create_index([('enrollment_id', pymongo.ASCENDING),], unique=True, name='letter_grade_id')
        lettergrade.create_index([('lettergrade_id', pymongo.ASCENDING), ], unique=True, name='letter_grade_id')
    if 'minimum_satisfactory' in letter_grade_indexes.keys():
        print("minimum satisfactory present")
    else:
        lettergrade.create_index([('min_satisfactory', pymongo.ASCENDING), ], unique=True,
                                 name='minimum_satisfactory')
    pprint(lettergrade.index_information())

    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

