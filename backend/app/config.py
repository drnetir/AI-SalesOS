import os
from dataclasses import dataclass
@dataclass(frozen=True)
class Settings:
    app_name:str=os.getenv("APP_NAME","AI-SalesOS / فروش‌یار ۳۶۰")
    checkpoint_every_steps:int=int(os.getenv("CHECKPOINT_EVERY_STEPS","3"))
    max_context_memories:int=int(os.getenv("MAX_CONTEXT_MEMORIES","8"))
    openai_api_key:str|None=os.getenv("OPENAI_API_KEY")
    gemini_api_key:str|None=os.getenv("GEMINI_API_KEY")
    anthropic_api_key:str|None=os.getenv("ANTHROPIC_API_KEY")
settings=Settings()
