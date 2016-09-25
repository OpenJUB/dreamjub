import typing

from . import component

role_map = {
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

StudentRoles = ['Student (guest)', 'Student (exchange)', 'Student (external)',
                'Student (visiting)']
StudentAssistantRoles = ['Teaching Assistant', 'Research Assistant']
ResearchRoles = ['Professor', 'Scientific Fellow', 'Research Associate',
                 'Research Assistant']
FacultyRoles = ['Professor', 'Professor (Visiting)', 'Professor (Adjunct)',
                'Lecturer', 'Lecturer (University)', 'Lecturer (other)',
                'Instructor (external)', 'Faculty (other)']
AdminRoles = ['President & Vice President', 'Director', 'Assistant']
StaffRoles = ['Technician', 'Staff (other)']
OtherRoles = ['Intern', 'Temporary']


class RoleComponent(component.UserParsingComponent):
    """ Represents the roles of a user. """

    fields = ['employeeType']

    def parse(self, user: dict) -> dict:

        # parse the employee type and get all the roles
        rroles = self.get_attribute(user, 'employeeType', '').split(";")
        roles = list(filter(lambda r: r is not None,
                            map(lambda r: self.parse_role(r), rroles)))

        # check for all the roles
        isStudent = self.contains_any(roles, StudentRoles)
        isStudentAssistant = self.contains_any(roles, StudentAssistantRoles)
        isResearch = self.contains_any(roles, ResearchRoles)
        isFaculty = self.contains_any(roles, FacultyRoles)
        isAdmin = self.contains_any(roles, AdminRoles)
        isStaff = self.contains_any(roles, StaffRoles)
        isOther = self.contains_any(roles, OtherRoles)

        return {
            'roles': roles,

            'isStudent': isStudent,
            'isStudentAssistant': isStudentAssistant,
            'isResearch': isResearch,
            'isFaculty': isFaculty,
            'isAdmin': isAdmin,
            'isStaff': isStaff,
            'isOther': isOther
        }

    @staticmethod
    def parse_role(r: str) -> str:
        """ Parses a role name. """

        try:
            return role_map[r.strip()]
        except:
            return None

    @staticmethod
    def contains_any(haystack: typing.List[typing.Any],
                     needles: typing.List[typing.Any]) -> bool:
        """ Checks if a list contains at least one of the needles. """

        for h in haystack:
            if h in needles:
                return True
        return False
