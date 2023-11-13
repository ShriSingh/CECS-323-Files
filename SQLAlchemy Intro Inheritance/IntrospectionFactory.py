from menu_definitions import introspection_select


# Adding Introspection Factory from previous assignments
class IntrospectionFactory:
    _singleton = None
    introspection_type: int

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls.introspection_type = introspection_select.menu_prompt()
            cls._singleton = super(IntrospectionFactory, cls).__new__(cls, *args, **kwargs)
        return cls._singleton
