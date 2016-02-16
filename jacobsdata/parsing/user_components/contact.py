from . import component
from jacobsdata.parsing.user_components.buildings import rooms

class ContactComponent(component.UserParsingComponent):
    fields = ['telephoneNumber', 'physicalDeliveryOfficeName']
    
    def parse(self, user):
        # get phone and room
        phone = self.getAttribute(user, 'telephoneNumber', '')
        room = self.getAttribute(user, 'room', '')
        
        
        # try and get the building from either the room or phone
        building = ''
        building_ok = True
        
        if phone:
            building_ok = False
            r = rooms.getRoomByPhone(phone)
            if r != None:
                building = r['building']
                building_ok = True
        
        if room and building == '':
            building_ok = False
            r = rooms.getRoomByRoom(room)
            if r != None:
                building = r['building']
                building_ok = True
        
        
        # check if we have an on-campus phone number
        isCampusPhone = (len(phone) == 4)
        
        # warn only if we have a campus phone
        # since non-campus phones are ignored either way
        if not building_ok and isCampusPhone:
            if phone != '' and room == '':
                #print("Warning: Missing room information for telephoneNumber %r" % (phone))
                pass
            else:
                print("Warning: Unknown 'telephoneNumber'/'physicalDeliveryOfficeName' combination: %r %r" % (phone, room))
        
        # HACK for privacy: hide all non campus phone numbers
        if isCampusPhone:
            phone = ''
        
        return {
            'phone': phone, 
            'isCampusPhone': isCampusPhone,
            
            'room': room, 
            'building': building, 
        }