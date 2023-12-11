import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from departments_schema import departments_validator
from majors_schema import majors_validator
from students_schema import students_validator


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
            "majors": []
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
            "description": description
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
    A major can have many students and a student can have many majors.
    Because there are hundreds of students, it is best for a student to
    keep track of the majors. Therefore, a major is added to a student
    """
    try:
        major = select_major(db)
        student = select_student(db)
        collection = db["students"]

        # student doesn't need a major, so if student doesn't have a list of majors, do $set
        try:
            have = student["majors"]
        except KeyError:
            result = collection.update_one({"_id": student["_id"]}, {"$set": {"majors": [major["_id"]]}})

        else:  # student already has a major
            # check if major is already in student's major list
            if major["_id"] not in student["majors"]:
                result = collection.update_one({"_id": student["_id"]}, {"$push": {"majors": major["_id"]}})
            else:
                print("Student already has that major. Try again.")
                return add_major_student(db)

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
    collection = db["students"]
    result1 = collection.count_documents({"majors": {"$eq": major["_id"]}})
    if result1 > 0:
        print("Students rely on this major. You cannot delete major. Try again.")
        return delete_major(db)
    # find department document where major array has that major_id
    collection2 = db["departments"]
    result2 = collection2.find_one(
        {"majors": {"$eq": major["_id"]}})  # because a major can only belong to one department
    collection2.update_one({"_id": result2["_id"]}, {"$pull": {"majors": major["_id"]}})
    deleted = majors.delete_one({"_id": major["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} majors.")


def delete_major_student(db):
    print("Select student to delete a major from")
    student = select_student(db)
    collection = db["students"]
    # check if student has any majors to begin with
    try:
        collection2 = db["majors"]
        majors = collection2.find({"_id": {"$in": student["majors"]}})
        print("Major(s) of ", student["first_name"], student["last_name"], ":")
        for major in majors:
            print("\t", major["name"])

        print("Select a major based on the information above.")
        major = select_major(db)
        while major["_id"] not in student["majors"]:
            print("student does not have that major. try again.")
            major = select_major(db)

        collection.update_one({"_id": student["_id"]}, {"$pull": {"majors": major["_id"]}})
        print("Major has been successfully deleted from student.")
        if len(student["majors"]) == 1:
            collection.update_one({"_id": student["_id"]}, {"$unset": {"majors": ""}})

    except KeyError:
        print("Student doesn't have any majors to delete. Try again.")
        return delete_major_student(db)


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
    student = select_student(db)
    try:
        collection = db["majors"]
        majors = collection.find({"_id": {"$in": student["majors"]}})
        print("Major(s) of ", student["first_name"], student["last_name"], ":")
        for major in majors:
            print("\t", major["name"])

    except KeyError:
        print("Student does not have any major(s). Try again.")
        return list_major_student(db)


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password[katiemartinezzz] -->')
    username: str = input('Database username [katiemartinezz] -->')
    project: str = input('Mongo project name [cluster0] -->')
    hash_name: str = input('7-character database hash [f9msjoe] -->')
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
    print(
        f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority&authSource=admin")
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

    #######################
    db.command("collMod", "departments", validator=departments_validator)
    db.command("collMod", "majors", validator=majors_validator)
    db.command("collMod", "students", validator=students_validator)

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

    # ************************** Set up the majors collection
    majors_indexes = majors.index_information()

    if 'majors_name' in majors_indexes.keys():
        print("name index present.")
    else:
        # Create a UNIQUE index on just the name
        majors.create_index([('name', pymongo.ASCENDING)], unique=True, name='majors_name')

    if 'majors_description' in majors_indexes.keys():
        print("description index present.")
    else:
        # Create a UNIQUE index on just the description
        majors.create_index([('description', pymongo.ASCENDING)], unique=True, name='majors_description')

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
        students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')

    # pprint(students.index_information())
    # pprint(majors.index_information())
    # pprint(departments.index_information())
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

