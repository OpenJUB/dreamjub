from . import component

class NameComponent(component.UserParsingComponent):
    fields = ['displayName']
    
    def parse(self, user):
        # get the name of the user
        name = self.getAttribute(user, 'displayName', '').split(', ')
        
        # make sure we have two parts of it
        if len(name) != 2:
            print("Warning: Weird 'displayName' attribute: %r" % (name))
            name = [self.getAttribute(user, 'displayName', ''), '']
        
        firstName = name[1]
        lastName = name[0]
        
        return {
            'firstName': firstName, 
            'lastName': lastName
        }
        