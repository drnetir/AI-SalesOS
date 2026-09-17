import json
from ..memory.store import search_memory
def build_compact_context(state,query):
    return {"schema":"AI_COMPACT_CONTEXT_V1","task":{k:state.get(k) for k in ("task_id","objective","status","current_step")},"completed_steps":state.get("completed_steps",[]),"pending_steps":state.get("pending_steps",[]),"decisions":state.get("decisions",[]),"constraints":state.get("constraints",{}),"critical_facts":state.get("critical_facts",{}),"relevant_memory":search_memory(query,state["task_id"],8),"tool_results":state.get("tool_results",[]),"artifacts":state.get("artifacts",[]),"errors":state.get("errors",[]),"next_action":state.get("next_action")}
def context_to_prompt(context):return json.dumps(context,ensure_ascii=False,indent=2)
