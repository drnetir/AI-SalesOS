import json,hashlib
from datetime import datetime,timezone
from ..database import transaction
SCHEMA="AI_TASK_HANDOFF_V1"
def now():return datetime.now(timezone.utc).isoformat()
def save_checkpoint(task_id,state):
    s=dict(state);s["schema"]=SCHEMA;s["last_checkpoint"]=now()
    payload=json.dumps({k:v for k,v in s.items() if k!="integrity_hash"},ensure_ascii=False,sort_keys=True)
    s["integrity_hash"]=hashlib.sha256(payload.encode()).hexdigest()
    with transaction() as db:db.execute("INSERT INTO checkpoints(task_id,checkpoint_json,created_at) VALUES(?,?,?)",(task_id,json.dumps(s,ensure_ascii=False),now()))
    return s
def get_latest_checkpoint(task_id):
    with transaction() as db:r=db.execute("SELECT checkpoint_json FROM checkpoints WHERE task_id=? ORDER BY id DESC LIMIT 1",(task_id,)).fetchone()
    return json.loads(r["checkpoint_json"]) if r else None
def get_checkpoints(task_id):
    with transaction() as db:rows=db.execute("SELECT * FROM checkpoints WHERE task_id=? ORDER BY id",(task_id,)).fetchall()
    return [dict(r)|{"checkpoint":json.loads(r["checkpoint_json"])} for r in rows]
