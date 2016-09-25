from . import component


class NameComponent(component.UserParsingComponent):
    """ Represents the name of a user. """

    fields = ['displayName']

    def parse(self, user: dict) -> dict:
        # get the name of the user
        name = self.get_attribute(user, 'displayName', '').split(', ')

        # make sure we have two parts of it
        if len(name) != 2:
            print("Warning: Weird 'displayName' attribute: %r" % (name))
            name = [self.get_attribute(user, 'displayName', ''), '']

        firstName = name[1]
        lastName = name[0]

        return {
            'firstName': firstName,
            'lastName': lastName
        }
