from . import component

class CountryComponent(component.UserParsingComponent):
    fields = ['extensionAttribute5']
    
    def parse(self, user):
        country = self.getAttribute(user, 'extensionAttribute5')
        
        return {
            'country': country
        }