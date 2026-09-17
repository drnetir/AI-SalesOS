from fastapi import APIRouter,HTTPException
from ..schemas import CreateTaskRequest,ResumeTaskRequest
from ..ai.orchestrator import Orchestrator
router=APIRouter(prefix="/ai",tags=["AI"]);orc=Orchestrator()
@router.post("/task")
def create(req:CreateTaskRequest):return orc.create_task(req.objective,req.metadata)
@router.get("/task/{task_id}")
def get(task_id):
    s=orc.get_state(task_id)
    if not s:raise HTTPException(404,"Task not found")
    return s
@router.post("/task/{task_id}/resume")
async def resume(task_id,req:ResumeTaskRequest):
    s=await orc.resume(task_id,req.provider,req.max_steps)
    if not s:raise HTTPException(404,"Task not found")
    return s
@router.post("/task/{task_id}/pause")
def pause(task_id):return orc.pause(task_id)
@router.post("/task/{task_id}/cancel")
def cancel(task_id):return orc.cancel(task_id)
@router.get("/task/{task_id}/checkpoints")
def checkpoints(task_id):return orc.checkpoints(task_id)
@router.get("/handoff/{task_id}")
def handoff(task_id):
    h=orc.handoff(task_id)
    if not h:raise HTTPException(404,"Checkpoint not found")
    return h
@router.get("/providers/health")
async def health():return await orc.router.health()
