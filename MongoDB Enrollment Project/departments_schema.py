"""Storing the schema for the Departments table"""
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
        }
    }
}
