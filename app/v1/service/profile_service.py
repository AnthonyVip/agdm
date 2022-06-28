from fastapi import HTTPException, status
from app.v1.model.user_queries import UserQueries


class ProfileService:
    def __init__(self):
        self.QueryClass = UserQueries()

    def get_user_profile(self, user_id: int):
        _profile = self.QueryClass.get_profile(user_id)
        if not _profile:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Profile not found")
        return _profile
