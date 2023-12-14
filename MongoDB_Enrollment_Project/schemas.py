departments_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "A department of a university",
            "required": ["name", "abbreviation", "chair_name", "building", "office", "description", "majors"],
            "additionalProperties": False,
            "properties": {
                "_id": {},
                "name": {
                    "bsonType": "string",
                    "description": "name of department",
                    "minLength": 6,
                    "maxLength": 50
                },
                "abbreviation": {
                    "bsonType": "string",
                    "description": "abbreviation of department",
                    "maxLength": 6
                },
                "chair_name": {
                    "bsonType": "string",
                    "description": "chair name of department",
                    "maxLength": 80
                },
                "building": {
                    "bsonType": "string",
                    "description": "building of department",
                    "enum": ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3",
                                "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"]
                },
                "office": {
                    "bsonType": "number",
                    "description": "office number of department",
                    "minimum": 100,
                    "maximum": 600
                },
                "description": {
                    "bsonType": "string",
                    "description": "description of building",
                    "minimum": 10,
                    "maximum": 80
                },
                "majors": {
                    "bsonType": "array",
                    "description": "majors belonging to department",
                    "uniqueItems": True,
                    "items": {
                        "bsonType": "objectId"
                    }
                },
                "courses": {
                "bsonType": "array",
                "uniqueItems": True,
                "items": {
                    "bsonType": "objectId",
                    "ref": "courses"
                }
            }
            }
        }
    }

majorstudents_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "A student enrolled in a major",
            "required": ["student", "major_name", "declaration_date"],
            "additionalProperties": False,
            "properties": {
                "_id": {},
                "student": {
                    "bsonType": "objectId",
                    "description": "student Id representing student information",
                },
                "major_name": {
                    "bsonType": "string",
                    "description": "name of major",
                    "minLength": 7,
                    "maxLength": 20
                },
                "declaration_date": {
                    "bsonType": "date",
                    "description": "date student enrolls in major",
                },
            }
        }
    }

# Adding tht student's schema
students_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A person attending university to earn a degree or credential",
        "required": ["last_name", "first_name", "e_mail"],
        "additionalProperties": True,
        "properties": {
            "_id": {},
            "last_name": {
                "bsonType": "string",
                "description": "surname of the student",
                "minLength": 3,
                "maxLength": 80
            },
            "first_name": {
                "bsonType": "string",
                "description": "given name of the student",
                "minLength": 3,
                "maxLength": 80
            },
            "e_mail": {
                "bsonType": "string",
                "description": "electronic mail address of the student",
                "minLength": 10,
                "maxLength": 255
            },
            "enrollments": {
                "bsonType": "array",
                "uniqueItems": True,
                "items": {
                    "bsonType": "objectId",
                    "ref": "enrollments"
                }
            }
        }
    }
}

# Adding the major's schema
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
            "major_students": {
                "bsonType": "array",
                "uniqueItem": True,
                "items": {
                    "bsonType": "objectId"
                }
            }
        }
    }
}

courses_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A class that a student may enroll in, offered by the University.",
        "required": ["number", "name"],
        "additionalProperties": False,
        "properties": {
            "_id": {},
            "department_abbreviation" : {
                "bsonType": "string",
                "description": "abbreviation of department",
                "maxLength": 6
            },
            "course_name": {
                "bsonType": "string",
                "description": "name of course",
                "minLength": 10,
                "maxLength": 50
            },
            "course_number": {
                "bsonType": "int",
                "minimum": 100,
                "exclusiveMaximum": 700
            },
            "description": {
                "bsonType": "string",
                "description": "description of course",
                "minimum": 10,
                "maximum": 80
            },
            "units": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 5
            },
            "sections": {
                "bsonType": "array",
                "uniqueItems": True,
                "items": {
                    "bsonType": "objectId",
                    "ref": "sections"
                }
            }
        }
}}

enrollments_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'validates the values when creating a new enrollment',
            'required': ['student_id', 'section_number', 'semester', 'section_year', 'abbreviation',
                         'course_number'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'student_id': {
                    'bsonType': 'int',
                    'description': 'validates the student id'
                },
                'section_number': {
                    'bsonType': 'int',
                    'description': 'validate the section number',
                },
                'semester': {
                    'bsonType': 'string',
                    'description': 'validates the building from a list of available buildings',
                    # enum for semesters?
                },
                'section_year': {
                    'bsonType': 'int',
                    'description': 'validate the section year'
                },
                'abbreviation': {
                    'bsonType': 'string',
                    'description': 'validate length of the abbreviation',
                    'maxLength': 6
                },
                'course_number': {
                    'bsonType': 'int',
                    'description': 'validate length of the chair name',
                    'minimum': 100,
                    'maximum': 699
                },
                'enrollment_type': {
                    'oneOf': [
                        {
                            # passfail
                            'bsonType': 'object',
                            'description': 'validates the pass/fail',
                            'required': ['application_date'],
                            'additionalProperties': False,
                            'properties': {
                                '_id': {},
                                'application_date': {
                                    'bsonType': 'datetime',
                                    'description': 'validate application date'
                                }
                            }
                        },
                        {
                            # lettergrade
                            'bsonType': 'object',
                            'description': 'validates the letter grade',
                            'required': ['min_satisfactory'],
                            'additionalProperties': False,
                            'properties': {
                                '_id': {},
                                'min_satisfactory': {
                                    'bsonType': 'string',
                                    'description': 'validate minimum satisfactory grade',
                                    'enum': ['A', 'B', 'C']
                                }
                            }
                        }
                    ],
                    'description': 'Either pass_fail or letter_grade'
                }
            }
        }
    }
}

sections_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A section of a course offered by the University.",
        "required": ["section_number", "course_number", "semester", "section_year", "building", "room", "schedule", "start_time", "instructor"],
        "additionalProperties": False,
        "properties": {
            "_id": {},
            "section_number": {
                "bsonType": "int",
                "description": "section number",
                "minimum": 1
            },
            "course_number": {
                "bsonType": "int",
                "description": "course number",
                "minimum": 100,
                "exclusiveMaximum": 700
            },
            "semester": {
                "bsonType": "string",
                "description": "semester",
                "enum": ["Fall", "Spring", "Summer I", "Summer II", "Summer III", "Winter"]
            },
            "section_year": {
                "bsonType": "int",
                "description": "section year"
            },
            "building": {
                "bsonType": "string",
                "description": "building",
                "enum": ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"]
            },
            "room": {
                "bsonType": "int",
                "description": "room",
                "minimum": 1,
                "maximum": 999
            },
            "schedule": {
                "bsonType": "string",
                "description": "schedule",
                "enum": ["MW", "TuTh", "MWF", "F", "S"]
            },
            "start_time": {
                "bsonType": "string",
                "description": "start time",
                "pattern": "^([8-9]|1[0-2]):[0-5][0-9] (AM|PM)$"
            },
            "instructor": {
                "bsonType": "string",
                "description": "instructor",
                "minLength": 3,
                "maxLength": 80
            },
            "enrollments": {
                "bsonType": "array",
                "uniqueItems": True,
                "items": {
                    "bsonType": "objectId",
                    "ref": "enrollments"
                }
            }
        }
    }
}