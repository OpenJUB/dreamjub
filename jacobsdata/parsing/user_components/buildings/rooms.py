import functools
import typing


def building_to_list(building: typing.Any) -> typing.List[dict]:
    """ Turns a building module into a list of rooms. """

    def r_m(r: dict) -> dict:
        return {'building': building.name, 'room': clean_room(r['room']),
                'phone': clean_phone(r['phone'])}

    return list(map(r_m, building.rooms))


@functools.lru_cache()
def get_all() -> typing.List[dict]:
    """ Returns a list of all rooms. """

    from jacobsdata.parsing.user_components.buildings.college import ciii, \
        krupp, mercator, nordmetall
    from jacobsdata.parsing.user_components.buildings.research import i, ii, \
        iii, iv, v
    from jacobsdata.parsing.user_components.buildings.other import \
        campus_center, misc, rlh, south_hall

    return (
        building_to_list(i) +
        building_to_list(ii) +
        building_to_list(iii) +
        building_to_list(iv) +
        building_to_list(v) +

        building_to_list(ciii) +
        building_to_list(krupp) +
        building_to_list(mercator) +
        building_to_list(nordmetall) +

        building_to_list(campus_center) +
        building_to_list(misc) +
        building_to_list(rlh) +
        building_to_list(south_hall)
    )


def get_room_by_phone(phone: typing.Union[int, str]) -> typing.Optional[dict]:
    """ Gets a room by its phone number. """

    cp = clean_phone(phone)
    for r in get_all():
        if r['phone'] == cp:
            return r
    return None


def get_room_by_room(room: str) -> typing.Optional[dict]:
    """ Gets a room by room name. """

    cr = clean_room(room)

    for r in get_all():
        if r['room'] == cr:
            return r
    return None


def clean_room(room: str) -> str:
    """ Cleans up the room name. """

    return str(room).strip()


def clean_phone(phone: typing.Union[int, str]) -> str:
    """ Cleans up a phone number. """

    return str(phone).strip()
