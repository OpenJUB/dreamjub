from . import component

class MemberComponent(component.CourseParsingComponent):
    fields = ['member']
    
    def parse(self, course, parsed_users):
        
        # get all the course members (as parsed_user objects)
        members = self.getAttribute(course, 'member', single=False)
        memberlist = list(filter(lambda u:u!=None, map(lambda u:self.getUserByLDAP(u, parsed_users), members)))
        
        # filter them into faculty and students
        instructors = list(filter(lambda u:u["isFaculty"], memberlist))
        students = list(filter(lambda u:not u["isFaculty"], memberlist))
        
        instructors_un = list(map(lambda u:u["username"], instructors))
        students_un = list(map(lambda u:u["username"], students))
        
        return {
            #'instructors': instructors_un, # empty
            'students': students_un
        }
    def getUserByLDAP(self, ldap_dn, parsed_users):
        for u in parsed_users:
            if u["ldap_dn"] == ldap_dn:
                return u
        
        print("Warning: Course has unknown 'member' with LDAP DN %r" % (ldap_dn))
        return None