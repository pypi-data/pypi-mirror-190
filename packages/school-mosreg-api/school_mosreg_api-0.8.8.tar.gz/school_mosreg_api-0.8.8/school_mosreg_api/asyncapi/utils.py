import school_mosreg_api
from .. import types

class AsyncAPIUtils:
    """Async Utils for AsyncSchoolMosregRUAPI\n~~~"""
    
    def __init__(self, api: "school_mosreg_api.asyncapi.AsyncSchoolMosregRUAPI") -> None:
        self.api = api
    
    async def get_user_school_by_educationType(self, user: str | int = "me", educationType: str = "Regular") -> types.School:
        """Get user school by param: educationType (``str``)"""
        
        schools_ids = await self.api.get_user_schools(user=user)
        schools = [await self.api.get_school(school=school) for school in schools_ids]
        
        for school in schools:
            if school.educationType == educationType:
                return school

    async def get_person_parsed_fio(self, person_id: int | str = "me", firstName: bool = True, lastName: bool = True, middleName: bool = True) -> str:
        """Get parsed person FIO."""
        
        person = await self.api.get_person(person=person_id)
        FIO = ""
        
        if lastName:
            FIO += f"{person.lastName or '-'} "
        
        if firstName:
            FIO += f"{person.firstName or '-'} "
        
        if middleName:
            FIO += f"{person.middleName or '-'}"
        
        return FIO
    