from fastapi import APIRouter
from ..schemas import MemoryCreateRequest
from ..memory.store import save_memory,search_memory
router=APIRouter(prefix="/memory",tags=["Memory"])
@router.post("")
def create(req:MemoryCreateRequest):return {"memory_id":save_memory(req.scope,req.key,req.value,req.task_id,req.importance)}
@router.get("/search")
def search(q="",task_id=None,limit=8):return search_memory(q,task_id,limit)
