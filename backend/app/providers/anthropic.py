from .base import AIProvider,ProviderResult
from ..config import settings
class AnthropicProvider(AIProvider):
    name="anthropic"
    def __init__(self):self.api_key=settings.anthropic_api_key
    async def generate(self,system_prompt,user_prompt):
        if not self.api_key:return ProviderResult(False,provider=self.name,error="ANTHROPIC_API_KEY is not configured")
        try:
            from anthropic import AsyncAnthropic
            r=await AsyncAnthropic(api_key=self.api_key).messages.create(model="claude-3-5-haiku-latest",max_tokens=2048,system=system_prompt,messages=[{"role":"user","content":user_prompt}])
            return ProviderResult(True,"".join(x.text for x in r.content if getattr(x,"type",None)=="text"),self.name,"claude-3-5-haiku-latest")
        except Exception as e:return ProviderResult(False,provider=self.name,error=str(e))
    async def health(self):return bool(self.api_key)
