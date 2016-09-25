from . import component

import re

status_map = {
    'ug': 'undergrad',
    'm': 'master',
    'fy': 'foundation-year',
    'phd': 'phd',
    'int_phd': 'phd-integrated',
    'winter_school': 'winter',
    'guest': 'guest',
    '': ''
}

degree_map = {
    'EX_BSc': 'Bachelor of Science',
    'EX_BA': 'Bachelor of Art',
    'EX_MSc': 'Master of Science',
    'EX_MA': 'Master of Art',
    'EX_PHD': 'PhD'
}


class StatusComponent(component.UserParsingComponent):
    """ Represents the status of a single user. """

    fields = ['extensionAttribute2', 'extensionAttribute3']

    def parse(self, user: dict) -> dict:

        major = self.get_attribute(user, 'extensionAttribute3', '')

        # split the raw description into parts
        desc = self.get_attribute(user, 'extensionAttribute2', '')
        description = re.sub(r'\(.*\)', '',
                             desc.replace('int ', 'int_').replace('class ',
                                                                  '').replace(
                                 'winter school', 'winter_school')).split(' ')

        # all the info description contains
        status = ''
        year = ''
        majorShort = ''
        degree = ''

        if len(description) > 0:
            try:
                status = status_map[description[0].lower()]
            except:
                print(
                    "Warning: Unknown 'extensionAttribute2' part for " +
                    "status: %r" % (
                        description[0]))

        if len(description) > 1 and description[1].startswith("EX_"):
            try:
                degree = degree_map[description[1]]
            except:
                print(
                    "Warning: Unknown 'extensionAttribute2' part for " +
                    "degree: %r" % (
                        description[1]))
        else:
            if len(description) > 1:

                ystr = description[1]

                try:
                    if ystr.endswith("_s"):
                        year = "%2d (spring)" % int(ystr[:-2])
                    elif ystr.endswith("_f"):
                        year = "%2d (fall)" % int(ystr[:-2])
                    else:
                        year = "%2d" % int(ystr)
                except:
                    print(
                        "Warning: Unknown 'extensionAttribute2' part for " +
                        "year: %r" % (
                            description[1]))

            if len(description) > 2:
                majorShort = ' '.join(description[2:]).strip()

        return {
            'status': status,
            'year': year,
            'majorShort': majorShort,
            'major': major,

            'degree': degree
        }
