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


def add_major(db):
    """
    Add a new major, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    departments collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the major's collection.
    :return:            None
    """

    try:
        # Create a "pointer" to the majors collection within the db database.
        collection = db["majors"]

        # A major cannot exist without a department, so select a department this major
        #will be offered by
        department = select_department

        # Now, ask about information necessary to create major
        name = input("Major Name--> ")
        description = input("Major Description--> ")

        # Build a new majors document preparatory to storing it
        major = {
            "name": name,
            "description": description
        }
        results = collection.insert_one(major)

        # Major is created, so now add it to the list of majors in department chose
        collection2 = db["departments"]
        results2 = collection2.update_one({"_id": department["_id"]}, {"$push": {"majors": [major["_id"]]}})


    except Exception as exception:
        print(exception)
        return add_major(db)

def add_major_to_student(db):
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

        #student doesn't need a major, so if student doesn't have a major[], do $set
        have = collection.find({"_id": student["_id"]}, {"majors": {"$exists": "true"}})
        if have != student:
            result = collection.update_one({"_id": major["_id"]}, {"$set": {"majors": [major["_id"]]}})
        #student could have multiple majors, so do push
        else:
            result = collection.update_one({"_id": major["_id"]}, {"$push": {"majors": [major["_id"]]}})

    except Exception as exception:
        print(exception)
        return add_major_to_student(db)




def add_major_to_department(db):
    """
    :param collection:  The pointer to the major's collection.
    :return:            None
    major has to belong to a department so, maybe I don't need to
    add_major_to_department and can instead do this in add_major
    """

    try:

        major = select_major(db)
        major_id_add = major["_id"] #returns the _id value from the selected major document.

        collection2 = db["departments"]
        #select a department
        department = select_department

        #if a department doesn't have any majors in it yet
        x = 0
        if x == 1:
            results = collection2.update_one({"_id": department["_id"]}, {"$set": {"majors": [major_id_add]}})

        else:
            results = collection2.update_one({"_id": department["_id"]}, {"$push": {"majors": major_id_add}})


    except Exception as exception:
        print(exception)
        return add_major_to_department(db)


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


def delete_major(db):
    """
    Delete a department from the database.
    :param db:  The current database connection.
    :return:    None
    """

    major = select_major(db)
    # Create a "pointer" to the students collection within the db database.
    majors = db["majors"]
    # department["_id"] returns the _id value from the selected student document.
    deleted = majors.delete_one({"_id": major["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} major(s).")

def delete_major_department(db):
    pass

def delete_major_student(db):
    pass


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


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->')
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


    majors = db["majors"]

    majors_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "A major of a university",
            "required": ["name", "description"],
            "additionalProperties": False,
            "properties": {
                "_id": {},
                "name": {
                    "bsonType": "string",
                    "description": "name of major",
                    "minLength": 10,
                    "maxLength": 50
                },
                "description": {
                    "bsonType": "string",
                    "description": "description of major",
                    "minimum": 10,
                    "maximum": 80
                },
            }
        }
    }

#######################
    db.command("collMod", "majors", validator=majors_validator)

    major_count = majors.count_documents({})
    print(f"Majors in the collection so far: {major_count}")

    # ************************** Set up the departments collection
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



    pprint(majors.index_information())
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
