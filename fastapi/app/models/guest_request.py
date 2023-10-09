from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class GuestRequest(BaseModel):
    full_name: str = Field(..., description="The full name of the guest")
    alt_name: str = Field(None, description="An alternate name for the guest")
    salute: str = Field(None, description="A salutation for the guest")
    title: str = Field(None, description="The title of the guest")
    organization: str = Field(None, description="The organization of the guest")
    country: str = Field(None, description="The country of the guest")
    email: EmailStr = Field(None, description="The email address of the guest")
    phone: str = Field(None, description="The phone number of the guest")
    details: str = Field(None, description="Details in JSON String")

    class Config:
        orm_mode = True


class GuestUpdateRequest(BaseModel):
    id: int = Field(..., description="The unique identifier for the guest")
    full_name: str = Field(None,description="The full name of the guest")
    alt_name: str = Field(None, description="An alternate name for the guest")
    salute: str = Field(None, description="A salutation for the guest")
    title: str = Field(None, description="The title of the guest")
    organization: str = Field(None, description="The organization of the guest")
    country: str = Field(None, description="The country of the guest")
    email: str = Field(None, description="The email address of the guest")
    phone: str = Field(None, description="The phone number of the guest")
    details: str = Field(None, description="Details in JSON String")

    class Config:
        orm_mode = True