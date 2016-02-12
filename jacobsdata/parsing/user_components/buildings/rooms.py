import functools

def buildingToList(building):
    r_m = lambda r: {'building': building.name, 'room': cleanRoom(r['room']), 'phone': cleanPhone(r['phone'])}
    return list(map(r_m, building.rooms))

@functools.lru_cache()
def getAll():
    from jacobsdata.parsing.user_components.buildings.college import ciii, krupp, mercator, nordmetall
    from jacobsdata.parsing.user_components.buildings.research import i, ii, iii, iv, v
    from jacobsdata.parsing.user_components.buildings.other import campus_center, misc, rlh, south_hall
    
    return (
        buildingToList(i) +
        buildingToList(ii) +
        buildingToList(iii) +
        buildingToList(iv) +
        buildingToList(v) +
        
        buildingToList(ciii) +
        buildingToList(krupp) +
        buildingToList(mercator) +
        buildingToList(nordmetall) +
        
        buildingToList(campus_center) +
        buildingToList(misc) +
        buildingToList(rlh) +
        buildingToList(south_hall)
    )

def getRoomByPhone(phone):
    cp = cleanPhone(phone)
    for r in getAll():
        if r['phone'] == cp:
            return r
    return None
def getRoomByRoom(room):
    cr = cleanRoom(room)
    
    for r in getAll():
        if r['room'] == cr:
            return r
    return None
            
    
def cleanRoom(room):
    return str(room).strip()

def cleanPhone(phone):
    return str(phone).strip()