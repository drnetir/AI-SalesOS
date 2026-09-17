from .base import AIProvider,ProviderResult
from ..config import settings
class GeminiProvider(AIProvider):
    name="gemini"
    def __init__(self):self.api_key=settings.gemini_api_key
    async def generate(self,system_prompt,user_prompt):
        if not self.api_key:return ProviderResult(False,provider=self.name,error="GEMINI_API_KEY is not configured")
        try:
            from google import genai
            r=genai.Client(api_key=self.api_key).models.generate_content(model="gemini-2.5-flash",contents=f"SYSTEM:\n{system_prompt}\nUSER:\n{user_prompt}")
            return ProviderResult(True,r.text or "",self.name,"gemini-2.5-flash")
        except Exception as e:return ProviderResult(False,provider=self.name,error=str(e))
    async def health(self):return bool(self.api_key)
