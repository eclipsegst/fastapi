from typing import Optional

from pydantic import BaseModel

from app.schemas.user import PublicUser


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Item(ItemInDBBase):
    owner_id: int
    owner: PublicUser

    class Config:
        from_attributes = True


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
