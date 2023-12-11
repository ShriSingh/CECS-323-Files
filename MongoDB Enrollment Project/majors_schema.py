"""Storing the schema for the Majors table"""
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