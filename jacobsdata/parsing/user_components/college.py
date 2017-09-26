from . import component
from jacobsdata.parsing.user_components.buildings import rooms

college_map = {
    'Alfried Krupp College': 'Krupp',
    'College III': 'C3',
    'College Nordmetall': 'Nordmetall',
    'Mercator College': 'Mercator',
    '': ''
}

college_choices = [college_map[k] for k in college_map]


class CollegeComponent(component.UserParsingComponent):
    """ Represents the college of a user. """

    fields = ['houseIdentifier', 'telephoneNumber',
              'physicalDeliveryOfficeName']

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

        # fallack to parsing from the building
        if college == '':
            # check if we have the phone
            phone = self.get_attribute(user, 'telephoneNumber', '')
            room = self.get_attribute(user, 'room', '')

            # Booleans indicating if we have room and phone number
            hasPhone = phone != ''
            hasRoom = room != ''

            building = ''

            if hasPhone:
                room_obj = rooms.get_room_by_phone(phone)

                if room_obj is not None:
                    building = room_obj["building"]

            elif hasRoom and not hasPhone:
                room_obj = rooms.get_room_by_room(room)
                if room_obj is not None:
                    building = room_obj["building"]

            if building in college_choices:
                college = building

        return {
            'college': college
        }
