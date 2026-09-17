import json,uuid
from datetime import datetime,timezone
from ..database import transaction
from ..config import settings
from ..providers.router import ProviderRouter
from ..providers.mock import MockProvider
from ..providers.openai import OpenAIProvider
from ..providers.gemini import GeminiProvider
from ..providers.anthropic import AnthropicProvider
from .checkpoint import save_checkpoint,get_latest_checkpoint,get_checkpoints
from .context import build_compact_context,context_to_prompt
def now():return datetime.now(timezone.utc).isoformat()
class Orchestrator:
    def __init__(self):self.router=ProviderRouter([OpenAIProvider(),GeminiProvider(),AnthropicProvider(),MockProvider()])
    def create_task(self,objective,metadata=None):
        tid=str(uuid.uuid4());state={"task_id":tid,"objective":objective,"status":"queued","current_step":None,"completed_steps":[],"pending_steps":["Execute objective"],"decisions":[],"constraints":metadata or {},"critical_facts":{},"tool_results":[],"artifacts":[],"errors":[],"next_action":None,"provider_history":[],"steps":0}
        with transaction() as db:db.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?)",(tid,objective,"queued",json.dumps(state,ensure_ascii=False),now(),now()))
        save_checkpoint(tid,state);return state
    def get_state(self,tid):
        with transaction() as db:r=db.execute("SELECT state_json FROM tasks WHERE task_id=?",(tid,)).fetchone()
        return json.loads(r["state_json"]) if r else None
    def _save(self,s):
        with transaction() as db:db.execute("UPDATE tasks SET status=?,state_json=?,updated_at=? WHERE task_id=?",(s["status"],json.dumps(s,ensure_ascii=False),now(),s["task_id"]))
    async def resume(self,tid,preferred=None,max_steps=1):
        s=self.get_state(tid)
        if not s:return None
        if s["status"] in ("completed","cancelled"):return s
        s["status"]="running"
        for _ in range(max_steps):
            if not s["pending_steps"]:s["status"]="completed";break
            step=s["pending_steps"].pop(0);s["current_step"]=step
            ctx=build_compact_context(s,step)
            r=await self.router.execute("You are a worker in AI-SalesOS. Continue only from compact task state; do not reconstruct the full conversation.",context_to_prompt(ctx),preferred)
            s["provider_history"].append({"provider":r.provider,"model":r.model,"success":r.success});s["steps"]+=1
            if r.success:s["completed_steps"].append({"step":step,"result":r.text});s["next_action"]=None
            else:s["errors"].append(r.error);s["pending_steps"].insert(0,step);s["status"]="paused";break
            if s["steps"]%settings.checkpoint_every_steps==0:save_checkpoint(tid,s)
        if not s["pending_steps"]:s["status"]="completed"
        self._save(s);save_checkpoint(tid,s);return s
    def pause(self,tid):
        s=self.get_state(tid)
        if s:s["status"]="paused";self._save(s);save_checkpoint(tid,s)
        return s
    def cancel(self,tid):
        s=self.get_state(tid)
        if s:s["status"]="cancelled";self._save(s);save_checkpoint(tid,s)
        return s
    def handoff(self,tid):return get_latest_checkpoint(tid)
    def checkpoints(self,tid):return get_checkpoints(tid)
