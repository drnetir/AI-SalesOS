from typing import Any
from pydantic import BaseModel,Field
class CreateTaskRequest(BaseModel):
    objective:str
    metadata:dict[str,Any]=Field(default_factory=dict)
class ResumeTaskRequest(BaseModel):
    provider:str|None=None
    max_steps:int=1
class MemoryCreateRequest(BaseModel):
    scope:str
    key:str
    value:str
    task_id:str|None=None
    importance:int=5
