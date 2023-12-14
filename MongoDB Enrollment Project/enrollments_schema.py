"""Storing the schema for the Enrollments table"""
enrollments_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'validates the values when creating a new enrollment',
            'required': ['student', 'section', 'enrollment_type'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'student': {
                    'bsonType': 'objectId',
                    'description': 'student enrolling in section'
                },
                'section': {
                    'bsonType': 'objectId',
                    'description': 'section a student enrolls in'
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