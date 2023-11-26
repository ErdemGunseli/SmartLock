from dependencies import db_dependency, user_dependency
from hardware_interface import hw

from fastapi import APIRouter, Query, HTTPException
from starlette import status as st

router = APIRouter(prefix="/action", tags=["actions"])


@router.get("/", status_code=st.HTTP_200_OK)
# The user_dependency is for injection, we don't actually need a parameter:
async def read_locked(_: user_dependency):
    return {"locked": hw.is_locked()}


@router.put("/set_locked", status_code=st.HTTP_200_OK)
# '...' indicates that a parameter is mandatory:
async def update_locked(_: user_dependency, lock: int = Query(..., ge=0, le=1, description="Unlock (0) or Lock (1)")):
    # Locking or unlocking the door depending on query parameter; raising exception if operation fails:
    if (lock == 0 and not hw.unlock()) or (lock == 1 and not hw.lock()): 
        raise HTTPException(status_code=st.HTTP_400_BAD_REQUEST, detail="Communication with Arduino failed")