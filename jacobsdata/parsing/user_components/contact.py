from . import component
from jacobsdata.parsing.user_components.buildings import rooms


class ContactComponent(component.UserParsingComponent):
    """ Represents the basic contact information of a user. """

    fields = ['telephoneNumber', 'physicalDeliveryOfficeName']

    def parse(self, user: dict) -> dict:
        # get phone and room
        phone = self.get_attribute(user, 'telephoneNumber', '')
        room = self.get_attribute(user, 'room', '')

        # use an empty building by default
        building = ''

        # Booleans indicating if we have room and phone number
        hasPhone = phone != ''
        hasRoom = room != ''

        # is the know phone number on campus?
        isCampusPhone = (len(phone) == 4)

        # Step 1: Complete room, phone, building information as best as
        # possible

        # if we have the phone number, always look up the room inside the
        # database, because the data inside ldap is dirty
        if hasPhone:
            room_obj = rooms.get_room_by_phone(phone)
            if room_obj is not None:
                room = room_obj["room"]
                building = room_obj["building"]
                isCampusPhone = True
            elif hasRoom:
                print("Warning: Missing phone information for " +
                      "physicalDeliveryOfficeName {}".format(room))
            elif isCampusPhone:
                print("Warning: Missing room information for " +
                      "telephoneNumber {}".format(phone))
        # in the case where we only have a room, but not a phone number,
        # we can try to look this up as well.
        # Probably this will not work, since the information
        # is pretty dirty inside LDAP
        elif hasRoom and not hasPhone:
            room_obj = rooms.get_room_by_room(room)
            if room_obj is not None:
                phone = room_obj["phone"]
                building = room_obj["building"]
                isCampusPhone = True
            else:
                print("Warning: Missing phone information for " +
                      "physicalDeliveryOfficeName {}".format(room))

        # for privacy, we hide phone numbers that are not on campus
        if not isCampusPhone:
            phone = ''

        return {
            'phone': phone,
            'isCampusPhone': isCampusPhone,

            'room': room,
            'building': building,
        }
