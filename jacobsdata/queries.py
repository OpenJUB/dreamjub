from . import settings
from . import auth

from ldap3 import SUBTREE, ALL_ATTRIBUTES

def get_all_courses(username, password, attributes = ALL_ATTRIBUTES):
    """
    Gets a (raw) list of all courses. 
    
    Note: This method may take a long time to fetch all courses. 
    """
    
    # authenticate and return None if it fails
    conn = auth.connect_and_bind(username, password)
    
    if conn == None:
        return None
    
    # make a paged search
    results = conn.extend.standard.paged_search(
        search_base = 'ou=groups,%s' % (settings.LDAP_BASE_DN),
        search_filter = '(&(objectclass=group)(sAMAccountName=GS-CAMPUSNET-COURSE-*))',
        search_scope = SUBTREE,
        attributes = ALL_ATTRIBUTES, 
        paged_size = settings.LDAP_PAGE_SIZE,
        generator = False
    )
    
    # unbind
    conn.unbind()
    
    # return a list of results
    return list(results)

def get_all_users(username, password, attributes = ALL_ATTRIBUTES):
    """
    Gets a (raw) list of all users inside LDAP. 
    
    Note: This method may take a long time to fetch all students. 
    """
    
    # authenticate and return None if it fails
    conn = auth.connect_and_bind(username, password)
    
    if conn == None:
        return None
    
    # make a paged search
    results = conn.extend.standard.paged_search(
        search_base = 'ou=users,%s' % (settings.LDAP_BASE_DN),
        search_filter = '(objectclass=person)',
        search_scope = SUBTREE,
        attributes = attributes, 
        paged_size = settings.LDAP_PAGE_SIZE,
        generator = False
    )
    
    # unbind
    conn.unbind()
    
    # return a list of results
    return list(results)