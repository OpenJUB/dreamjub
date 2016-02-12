from jacobsdata.parsing import user, course
def parse_all(u, password):
    """
    Parses users and courses from LDAP. 
    """
    
    # parse all the users
    users = user.parse_all_users(u, password)
    if users == None:
        return (None, None)
    
    courses = course.parse_all_courses(u, password, users)
    
    if courses == None:
        return (None, None)
    
    return (users, courses)
    
    