from . import component

RoleMap = {
    # Students
    'Student': 'Student',  
    'Gueststudent': 'Student (guest)', 
    'Exchange Student': 'Student (exchange)', 
    'external Student': 'Student (external)', 
    'Visiting Student': 'Student (visiting)', 
    
    # Student Assistants
    'Teaching Assistant': 'Teaching Assistant', 
    'Research Assistant': 'Research Assistant', 

    # Faculty / Research
    'Professor': 'Professor', 
    'Visiting Professor': 'Professor (Visiting)', 
    'Adjunct Professor': 'Professor (Adjunct)', 
    'Lecturer': 'Lecturer', 
    'University Lecturer': 'Lecturer (University)', 
    'Further Lecturer': 'Lecturer (other)', 
    'external Instructor': 'Instructor (external)', 
    'sonstige Faculty': 'Faculty (other)', 

    # Research
    'Scientific Fellow': 'Scientific Fellow', 
    'Research Associate': 'Research Associate', 

    # Admin
    'President/Vice President': 'President & Vice President', 
    'Director': 'Director', 
    'Assistant': 'Assistant',
    
    # Staff 
    'Technician': 'Technician', 
    'Mitarbeiter sonstige': 'Staff (other)', 
    
    # Other
    'Praktikant': 'Intern', 
    'Temporary Access': 'Temporary'
}

StudentRoles = ['Student (guest)', 'Student (exchange)', 'Student (external)', 'Student (visiting)']
StudentAssistantRoles = ['Teaching Assistant', 'Research Assistant']
ResearchRoles = ['Professor', 'Scientific Fellow', 'Research Associate', 'Research Assistant']
FacultyRoles = ['Professor', 'Professor (Visiting)', 'Professor (Adjunct)', 'Lecturer',  'Lecturer (University)', 'Lecturer (other)', 'Instructor (external)', 'Faculty (other)']
AdminRoles = ['President & Vice President', 'Director', 'Assistant']
StaffRoles = ['Technician', 'Staff (other)']
OtherRoles = ['Intern', 'Temporary']




class RoleComponent(component.UserParsingComponent):
    fields = ['employeeType']
    
    def parse(self, user):
        
        # parse the employee type and get all the roles
        rroles = self.getAttribute(user, 'employeeType', '').split(";")
        roles = list(filter(lambda r: r!=None, map(lambda r: self.parseRole(r), rroles)))
        
        # check for all the roles
        isStudent = self.containsAny(roles, StudentRoles)
        isStudentAssistant = self.containsAny(roles, StudentAssistantRoles)
        isResearch = self.containsAny(roles, ResearchRoles)
        isFaculty = self.containsAny(roles, FacultyRoles)
        isAdmin = self.containsAny(roles, AdminRoles)
        isStaff = self.containsAny(roles, StaffRoles)
        isOther = self.containsAny(roles, OtherRoles)
        
        return {
            'roles': roles, 
            
            'isStudent': isStudent, 
            'isStudentAssistant': isStudentAssistant, 
            'isResearch': isResearch, 
            'isFaculty' : isFaculty,
            'isAdmin': isAdmin, 
            'isStaff': isStaff, 
            'isOther': isOther
        }
    def parseRole(self, r):
        try:
            return RoleMap[r.strip()]
        except:
            return None
    def containsAny(self, haystack, needles):
        for h in haystack:
            if h in needles:
                return True
        return False
        