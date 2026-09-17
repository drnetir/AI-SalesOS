import uuid
from datetime import datetime,timezone
from ..database import transaction
def now():return datetime.now(timezone.utc).isoformat()
def save_memory(scope,key,value,task_id=None,importance=5):
    mid=str(uuid.uuid4())
    with transaction() as db:db.execute("INSERT INTO memories VALUES(?,?,?,?,?,?,?,?)",(mid,scope,task_id,key,value,importance,now(),now()))
    return mid
def search_memory(query="",task_id=None,limit=8):
    with transaction() as db:
        rows=db.execute("SELECT * FROM memories WHERE (? IS NULL OR task_id=? OR scope IN ('identity','semantic')) ORDER BY importance DESC,updated_at DESC LIMIT ?",(task_id,task_id,limit)).fetchall()
    words=set(query.lower().split()); out=[]
    for r in rows:
        text=(r["key"]+" "+r["value"]).lower(); score=sum(w in text for w in words)
        if score or not query:out.append(dict(r)|{"score":score})
    return sorted(out,key=lambda x:(x["score"],x["importance"]),reverse=True)[:limit]
