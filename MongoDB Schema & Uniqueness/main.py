import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu


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


def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection. Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints. Extra credit anyone?
    :param db:  The pointer to the students' collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = collection.count_documents(
            {"last_name": lastName, "first_name": firstName})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name. Try again.")
        if unique_name:
            email_count = collection.count_documents({"e_mail": email})
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address. Try again.")
    # Build a new students document preparatory to storing it
    student = {
        "last_name": lastName,
        "first_name": firstName,
        "e_mail": email
    }
    results = collection.insert_one(student)


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
        name_count: int = collection.count_documents(
            {"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name. Try again.")
    found_student = collection.find_one(
        {"last_name": lastName, "first_name": firstName})
    return found_student


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


def list_student(db):
    """
    Lists all the students, sorted by last name first, then the first name.
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


def add_department(db):
    """
    Adds a new, unique department to the database
    :param db: The connection to the current database
    :return: None
    """
    # Create a "pointer" to the departments collection within the db database.
    department_collection = db["departments"]
    # Initializing all the attributes
    department_name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    # Setting up the uniqueness of the attributes; Initializing them to be False
    unique_name: bool = False  # Unique department name
    unique_abbreviation: bool = False  # Unique department abbreviation
    unique_chair_name: bool = False  # Unique department chair name
    unique_building_office: bool = False  # Unique department building and office
    unique_description: bool = False  # Unique department description

    # A while loop to check all the required uniqueness constraints
    while (not unique_name or not unique_abbreviation or not unique_chair_name
           or not unique_building_office or not unique_description):
        # Asking the user for the attributes
        department_name = input("Department name: ")
        abbreviation = input("Department abbreviation: ")
        chair_name = input("Department chair name: ")
        building = input("Department building: ")
        office = int(input("Department office: "))
        description = input("Department description: ")
        # Checking the name uniqueness
        department_count_1: int = department_collection.count_documents(
            {"name": department_name})
        unique_name = department_count_1 == 0
        if not unique_name:  # If the department name is not unique
            print("We already have a department by that name. Try again.")
        if unique_name:  # If the department name is unique
            # Checking the abbreviation uniqueness
            department_count_2: int = department_collection.count_documents(
                {"abbreviation": abbreviation})
            unique_abbreviation = department_count_2 == 0
            if not unique_abbreviation:  # If the department abbreviation is not unique
                print("We already have a department with that abbreviation. Try again.")
            if unique_abbreviation:  # If the department abbreviation is unique
                # Checking the chair name uniqueness
                department_count_3: int = department_collection.count_documents(
                    {"chair_name": chair_name})
                unique_chair_name = department_count_3 == 0
                if not unique_chair_name:  # If the department chair name is not unique
                    print("We already have a department with that chair name. Try again.")
                if unique_chair_name:  # If the department chair name is unique
                    # Checking the building and office uniqueness
                    department_count_4: int = department_collection.count_documents(
                        {"building": building, "office": office})
                    unique_building_office = department_count_4 == 0
                    if not unique_building_office:  # If the department building and office is not unique
                        print("We already have a department in that building with that office. Try again.")
                    if unique_building_office:  # If the department building and office is unique
                        # Checking the description uniqueness
                        department_count_5: int = department_collection.count_documents(
                            {"description": description})
                        unique_description = department_count_5 == 0
                        if not unique_description:  # If the department description is not unique
                            print("We already have a department with that description. Try again.")
    # Building a department document preparatory to store it
    department = {
        "name": department_name,
        "abbreviation": abbreviation,
        "chair_name": chair_name,
        "building": building,
        "office": office,
        "description": description
    }

    '''New code from here on out'''
    # Using try-except block to catch any constraint violations
    try:
        # Inserting the department document into the database
        results = department_collection.insert_one(department)
        # Indicating the department was added
        print("Department was added successfully")
    except Exception as violation:
        # Indicating the department was not added
        print("Values entered violated the set uniqueness constraints or schema. Try again.")
        print("Error: ", violation)
        # Letting the user try again
        add_department(db)


def select_department(db):
    """
        Selects a department by the name
        :param db: The connection to the database
        :return: The selected department as a dict
    """
    # Create a connection to the departments collection from this database
    department_collection = db["departments"]
    # Setting the department found to be False
    department_found: bool = False
    # Finding the initial department count
    initial_department_count = department_collection.count_documents({})
    # Initializing the department name
    department_name: str = ''
    # A while loop to check if the department is found or not and the initial department count is not 0
    while not department_found and initial_department_count != 0:
        department_name = input("Department name: ")
        # Finding the department by going through the departments collection
        department_count: int = department_collection.count_documents({"name": department_name})
        department_found = department_count == 1  # If the department is found
        if not department_found:  # If the department is not found
            print("No department found by that name. Try again.")
    # Storing the department of the asked name in a variable
    found_department = department_collection.find_one({"name": department_name})
    # Returning the found department
    return found_department


def delete_department(db):
    """
    Deletes a department from the database
    :param db: The connection to the database
    :return: None
    """
    # Calling the select_department function to select the department to be deleted
    department = select_department(db)
    if department is not None:
        # Making a pointer to the departments collection within the db database
        departments = db["departments"]
        # Deleting the department from the database
        deleted = departments.delete_one({"_id": department["_id"]})
        # Printing the number of departments deleted
        print(f"We just deleted: {deleted.deleted_count} department.")
    else:
        print("There are no departments to delete")


def list_department(db):
    """
    Lists all the departments in the database
    and sorts them by name
    :param db: The connection to the database
    :return: None
    """
    # Finds all the departments in the database and sorts them by name
    departments = db["departments"].find(
        {}).sort([("name", pymongo.ASCENDING)])
    # Prints all the departments
    for dept in departments:
        pprint(dept)


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [shriyanshsingh01] -->') or \
                    "shriyanshsingh01"
    project: str = input('Mongo project name [singlecollection] -->') or \
                   "singlecollection"
    hash_name: str = input(
        '7-character database hash [u5t42ge] -->') or "u5t42ge"

    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"

    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")

    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    students = db["students"]
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

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
        students.create_index([('e_mail', pymongo.ASCENDING)],
                              unique=True, name='students_e_mail')
    pprint(students.index_information())

    # Setting up the departments collection
    departments = db["departments"]
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")
    departments_indexes = departments.index_information()
    if 'departments_name' in departments_indexes.keys():
        print("department name present")
    else:
        departments.create_index(
            [('name', pymongo.ASCENDING)], unique=True, name="departments_name")
    if 'departments_abbreviation' in departments_indexes.keys():
        print("abbreviation present")
    else:
        departments.create_index(
            [('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation')
    if 'departments_chair_name' in departments_indexes.keys():
        print("chair name present")
    else:
        departments.create_index(
            [('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_name')
    if 'departments_building_and_office' in departments_indexes.keys():
        print("building and office present")
    else:
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True,
                                 name="departments_building_and_office")
    if 'departments_description' in departments_indexes.keys():
        departments.create_index(
            [('description', pymongo.ASCENDING)], unique=True, name='departments_description')
        print("description present")
    pprint(departments.index_information())

    '''New code from here on out'''
    # Setting up the schema to validate certain values in the departments collection
    departments_validator = {
        "validator":
            {
                "$jsonSchema":
                    {
                        "bsonType": "object",
                        "description": "validates the values when creating a new department",
                        "required": ["name", "abbreviation", "chair_name", "building", "office", "description"],
                        "additionalProperties": False,
                        "properties":
                            {
                                "_id": {},
                                "building":
                                    {
                                        "bsonType": "string",
                                        "description": "validates the building from a list of available buildings",
                                        "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI',
                                                 'NUR', 'VEC']
                                    },
                                "name":
                                    {
                                        "bsonType": "string",
                                        "description": "validate the length of the department name",
                                        "minLength": 10,
                                        "maxLength": 50
                                    },
                                "abbreviation":
                                    {
                                        "bsonType": "string",
                                        "description": "validate length of the abbreviation",
                                        "maxLength": 6
                                    },
                                "chair_name":
                                    {
                                        "bsonType": "string",
                                        "description": "validate length of the chair name",
                                        "maxLength": 80
                                    },
                                "description":
                                    {
                                        "bsonType": "string",
                                        "description": "validate length of the chair name",
                                        "minLength": 10,
                                        "maxLength": 80
                                    }
                            }
                    }
            }
    }
    # Calling the db.command function to validate the departments collection
    db.command("collMod", "departments", **departments_validator)

    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
