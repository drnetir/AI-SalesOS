from .base import ProviderResult
class ProviderRouter:
    def __init__(self,providers):self.providers=list(providers)
    async def execute(self,system_prompt,user_prompt,preferred=None):
        ordered=self.providers
        if preferred:ordered=[p for p in self.providers if p.name==preferred]+[p for p in self.providers if p.name!=preferred]
        errors=[]
        for p in ordered:
            r=await p.generate(system_prompt,user_prompt)
            if r.success:return r
            errors.append({"provider":p.name,"error":r.error})
        return ProviderResult(False,provider="router",error=str(errors))
    async def health(self):
        out=[]
        for p in self.providers:
            try:ok=await p.health()
            except:ok=False
            out.append({"provider":p.name,"available":ok})
        return out
