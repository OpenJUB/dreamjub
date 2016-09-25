from . import component


class CountryComponent(component.UserParsingComponent):
    """ Represents the country of a user. """

    fields = ['extensionAttribute5']

    def parse(self, user: dict) -> dict:
        country = self.get_attribute(user, 'extensionAttribute5')

        return {
            'country': country
        }
