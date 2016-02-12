from . import component

from datetime import date

class ActiveComponent(component.CourseParsingComponent):
    fields = ['whenCreated', 'whenChanged']
    
    def parse(self, course, parsed_users):
        # WARNING: This entire parsingcomponent is a hack. 
        # but we have nothing better for now
        # at least it is better than Stefans campusnet login
        
        # get the dates when it was created and modified
        created = self.getAttribute(course, 'whenCreated', '')
        modified = self.getAttribute(course, 'whenChanged', '')
        
        # get the date of this entry
        td = created
        if modified != '':
            td = modified
        
        active = True
        
        # if we have a modification date
        if td != '':
            
            # get the current semester
            now = date.today()
            now_sem = self.getSemester(now.year, now.month)
            
            try:
                # and the course semester
                course_year = int(td[0:4])
                course_month = int(td[4:6])
                c_sem = self.getSemester(course_year, course_month)
                
                # if they are the same the course is 'active', else it is not
                active = (now_sem == c_sem)
            except Exception as e:
                pass
        
        return {
            'active': active
        }
    def getSemester(self, year, month):
        if month == 1:
            return "fall %d" % (year - 1)
        elif month <= 6:
            return "spring %d" % (year)
        else:
            return "fall %d" % (year)