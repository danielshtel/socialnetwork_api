from fastapi import Depends, HTTPException, status

from .user import User


class Auth:

    # @staticmethod
    # async def __fake_decode_user(token: str):
    #     return await User.get_by_username(token)
    #
    # @classmethod
    # async def __get_current_user(cls,token: str = Depends(oauth2_scheme)):
    #     user = await cls.__fake_decode_user(token)
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail='Invalid auth credentials',
    #             headers={'WWW-Authenticate': 'Bearer'}
    #         )
    #     return user

    @classmethod
    async def get_current_active_user(cls, current_user: User = Depends(User.get_current_user)):
        if current_user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Inactive user'
            )
        return current_user
