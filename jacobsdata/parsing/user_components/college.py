from . import component

collegeMap = {
    'Alfried Krupp College': 'Krupp', 
    'College III': 'C3', 
    'College Nordmetall': 'Nordmetall', 
    'Mercator College': 'Mercator', 
    '': ''
}


class CollegeComponent(component.UserParsingComponent):
    fields = ['houseIdentifier']
    
    def parse(self, user):
        # get the (raw) houseIdentifier
        houseIdentifier = self.getAttribute(user, 'houseIdentifier', '')
        
        # switch between the colleges
        try:
            college = collegeMap[houseIdentifier]
        except:
            print("Warning: 'houseIdentifier' has unknown value: %r" % (houseIdentifier))
            college = ''
        
        return {
            'college': college
        }