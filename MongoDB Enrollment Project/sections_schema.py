"""Storing the schema for the Sections table"""
sections_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A section of a course offered by the University.",
        "required": ["section_number", "course_number", "semester", "section_year", "building", "room", "schedule",
                     "start_time", "instructor"],
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