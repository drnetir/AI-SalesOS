from .base import AIProvider,ProviderResult
from ..config import settings
class OpenAIProvider(AIProvider):
    name="openai"
    def __init__(self): self.api_key=settings.openai_api_key
    async def generate(self,system_prompt,user_prompt):
        if not self.api_key:return ProviderResult(False,provider=self.name,error="OPENAI_API_KEY is not configured")
        try:
            from openai import AsyncOpenAI
            r=await AsyncOpenAI(api_key=self.api_key).responses.create(model="gpt-5-mini",instructions=system_prompt,input=user_prompt)
            return ProviderResult(True,r.output_text,self.name,"gpt-5-mini")
        except Exception as e:return ProviderResult(False,provider=self.name,error=str(e))
    async def health(self):return bool(self.api_key)
