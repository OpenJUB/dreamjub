from . import component

college_map = {
    'Alfried Krupp College': 'Krupp',
    'College III': 'C3',
    'College Nordmetall': 'Nordmetall',
    'Mercator College': 'Mercator',
    '': ''
}


class CollegeComponent(component.UserParsingComponent):
    """ Represents the college of a user. """

    fields = ['houseIdentifier']

    def parse(self, user: dict) -> dict:

        # get the (raw) house_identifier
        house_identifier = self.get_attribute(user, 'house_identifier', '')

        # switch between the colleges
        try:
            college = college_map[house_identifier]
        except:
            print("Warning: 'house_identifier' has unknown value: %r" % (
                house_identifier))
            college = ''

        return {
            'college': college
        }
