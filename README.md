# AI-SalesOS / فروش‌یار ۳۶۰

Provider-agnostic AI orchestration with shared memory, compact checkpoints, resumable tasks and automatic provider failover.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

The Mock provider works without API keys. Optional OpenAI, Gemini and Anthropic providers are supported through environment variables.

## Core architecture
- AI-SalesOS owns task state.
- Providers/models are workers.
- Memory is separate from execution checkpoints.
- Handoff uses compact state instead of replaying the full conversation.
