import school_mosreg_api
from .. import types

class APIUtils:
    """Sync Utils for SchoolMosregRUAPI\n~~~"""
    
    def __init__(self, api: "school_mosreg_api.api.SchoolMosregRUAPI") -> None:
        self.api = api
    
    def get_user_school_by_educationType(self, user: str | int = "me", educationType: str = "Regular") -> types.School:
        """Get user school by param: educationType (``str``)"""
        
        schools_ids = self.api.get_user_schools(user=user)
        schools = [self.api.get_school(school=school) for school in schools_ids]
        
        for school in schools:
            if school.educationType == educationType:
                return school

    def get_person_parsed_fio(self, person_id: int | str = "me", firstName: bool = True, lastName: bool = True, middleName: bool = True) -> str:
        """Get parsed person FIO."""
        
        person = self.api.get_person(person=person_id)
        FIO = ""
        
        if lastName:
            FIO += f"{person.lastName or '-'} "
        
        if firstName:
            FIO += f"{person.firstName or '-'} "
        
        if middleName:
            FIO += f"{person.middleName or '-'}"
        
        return FIO
    