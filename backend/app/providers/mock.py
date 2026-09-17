from .base import AIProvider,ProviderResult
class MockProvider(AIProvider):
    name="mock"
    async def generate(self,system_prompt,user_prompt):
        return ProviderResult(True,"Task step completed by Mock Worker.","mock","mock-v1",{"input_tokens":0,"output_tokens":0})
