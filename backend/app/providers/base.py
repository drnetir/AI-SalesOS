from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import Any
@dataclass
class ProviderResult:
    success:bool
    text:str=""
    provider:str=""
    model:str=""
    usage:dict[str,Any]|None=None
    error:str|None=None
class AIProvider(ABC):
    name="unknown"
    @abstractmethod
    async def generate(self,system_prompt:str,user_prompt:str)->ProviderResult: ...
    async def health(self): return True
