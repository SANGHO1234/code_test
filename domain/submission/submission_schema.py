import datetime
from pydantic import BaseModel, field_validator
from fastapi import HTTPException

class SubmissionCreate(BaseModel):
    username: str
    password: str
    code: str

    @field_validator('username', 'password', 'code')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail='미 입력 항목 존재')
        return v
    

class SubmissionPatch(BaseModel):
    id: int
    status: str

    @field_validator('id')
    @classmethod
    def not_empty_id(cls, v):
        if not v:
            raise HTTPException(status_code=500, detail='미 입력 항목 존재')
        return v
    
    @field_validator('status')
    @classmethod
    def not_empty_status(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=500, detail='미 입력 항목 존재')
        return v
    

class SubmissionGet(BaseModel):
    username: str
    password: str
    id: int

    @field_validator('username', 'password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=500, detail='미 입력 항목 존재')
        return v
    
    @field_validator('id')
    def not_empty_id(cls, v):
        if not v:
            raise HTTPException(status_code=500, detail='미 입력 항목 존재')
        return v
    

class SubmissionCreateResult(BaseModel):
    id: int
    username: str


class SubmissionPatchResult(BaseModel):
    id: int
    status: str


class FectchNewResult(BaseModel):
    id: int


class SubmissionGetResult(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: str
    