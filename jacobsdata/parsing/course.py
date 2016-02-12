from jacobsdata import queries

def parse_all_courses(username, password, parsed_users):
    """
    Parses all courses from LDAP. 
    """
    
    # find out the fields we need
    fields = set()
    for c in components:
        fields.update(c.fields)
    
    # get all the students with the given fields
    courses = queries.get_all_courses(username, password)
    
    if courses == None:
        return None
    
    # parse all the users individually
    return list(map(lambda u:parse_course(c, parsed_users), courses))

def parse_course(course, parsed_users):
    """
    Parses a single course from LDAP
    """
    
    print(course)
    return None
    