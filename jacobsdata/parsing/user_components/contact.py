from . import component
from jacobsdata.parsing.user_components.buildings import rooms


class ContactComponent(component.UserParsingComponent):
    """ Represents the basic contact information of a user. """

    fields = ['telephoneNumber', 'physicalDeliveryOfficeName']

    def parse(self, user: dict) -> dict:
        # get phone and room
        phone = self.get_attribute(user, 'telephoneNumber', '')
        room = self.get_attribute(user, 'room', '')

        # try and get the building from either the room or phone
        building = ''
        building_ok = True

        if phone:
            building_ok = False
            r = rooms.get_room_by_phone(phone)
            if r is not None:
                building = r['building']
                building_ok = True

        if room and building == '':
            building_ok = False
            r = rooms.get_room_by_room(room)
            if r is not None:
                building = r['building']
                building_ok = True

        # check if we have an on-campus phone number
        isCampusPhone = (len(phone) == 4)

        # warn only if we have a campus phone since non-campus phones are
        # ignored either way
        if not building_ok and isCampusPhone:
            if phone != '' and room == '':
                print(
                    "Warning: Missing room information for " +
                    "telephoneNumber {}".format(phone))
            else:
                print(
                    "Warning: Unknown 'telephoneNumber'/" +
                    "'physicalDeliveryOfficeName' combination: {} {}".format(
                        phone, room))

        # HACK for privacy: hide all non campus phone numbers
        if not isCampusPhone:
            phone = ''

        return {
            'phone': phone,
            'isCampusPhone': isCampusPhone,

            'room': room,
            'building': building,
        }
