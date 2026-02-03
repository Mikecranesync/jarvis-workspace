"""
FactoryLM Observability Tracer
Created: 2026-02-03T02:13:00Z

Provides tracing, message storage, and action logging for all
Telegram conversations and system actions.
"""

import os
import uuid
import json
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
import asyncpg

# LangFuse imports (optional - graceful fallback if not configured)
try:
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False

# Configuration
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://neondb_owner:npg_c3UNa4KOlCeL@ep-purple-hall-ahimeyn0-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
)

LANGFUSE_HOST = os.environ.get('LANGFUSE_HOST', 'https://us.cloud.langfuse.com')
LANGFUSE_PUBLIC_KEY = os.environ.get('LANGFUSE_PUBLIC_KEY')
LANGFUSE_SECRET_KEY = os.environ.get('LANGFUSE_SECRET_KEY')


@dataclass
class ActionTrace:
    """Represents a single traced action."""
    trace_id: str
    action_type: str  # 'shell', 'api_call', 'file_write', 'ssh', 'notify'
    target: str       # IP, path, URL, etc.
    command: str
    result: Optional[str] = None
    status: str = 'pending'
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    metadata: Optional[Dict] = None

    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}


class ObservabilityTracer:
    """
    Main tracer class for FactoryLM observability.
    
    Usage:
        tracer = ObservabilityTracer()
        await tracer.connect()
        
        # Log a message
        await tracer.log_message(chat_id, user_id, "Hello", is_from_bot=False)
        
        # Trace an action
        async with tracer.trace_action('shell', '100.72.2.99', 'hostname') as action:
            result = run_command(...)
            action.result = result
            action.status = 'success'
    """

    def __init__(self, session_key: Optional[str] = None):
        self.session_key = session_key or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        self.db_pool: Optional[asyncpg.Pool] = None
        self.langfuse: Optional[Any] = None
        self._current_trace_id: Optional[str] = None
        
    async def connect(self):
        """Initialize database connection and LangFuse client."""
        # Database connection
        self.db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
        
        # LangFuse client (if configured)
        if LANGFUSE_AVAILABLE and LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
            self.langfuse = Langfuse(
                public_key=LANGFUSE_PUBLIC_KEY,
                secret_key=LANGFUSE_SECRET_KEY,
                host=LANGFUSE_HOST
            )
            print(f"[Tracer] LangFuse connected to {LANGFUSE_HOST}")
        else:
            print("[Tracer] LangFuse not configured - using database-only tracing")
    
    async def close(self):
        """Clean up connections."""
        if self.db_pool:
            await self.db_pool.close()
        if self.langfuse:
            self.langfuse.flush()

    def new_trace_id(self) -> str:
        """Generate a new trace ID."""
        self._current_trace_id = str(uuid.uuid4())
        return self._current_trace_id
    
    @property
    def current_trace_id(self) -> Optional[str]:
        return self._current_trace_id

    async def log_message(
        self,
        chat_id: int,
        user_id: int,
        content: str,
        message_id: Optional[int] = None,
        username: Optional[str] = None,
        is_from_bot: bool = False,
        metadata: Optional[Dict] = None
    ) -> int:
        """Log a Telegram message to the database."""
        if not self.db_pool:
            raise RuntimeError("Tracer not connected. Call connect() first.")
        
        trace_id = self._current_trace_id or self.new_trace_id()
        
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO telegram_messages 
                (message_id, chat_id, user_id, username, content, is_from_bot, trace_id, session_key, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7::uuid, $8, $9::jsonb)
                RETURNING id
            """, message_id, chat_id, user_id, username, content, is_from_bot, 
                trace_id, self.session_key, json.dumps(metadata or {}))
            
            return row['id']

    async def log_action(self, action: ActionTrace, parent_message_id: Optional[int] = None) -> int:
        """Log an action to the database."""
        if not self.db_pool:
            raise RuntimeError("Tracer not connected. Call connect() first.")
        
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO action_traces
                (trace_id, parent_message_id, action_type, target, command, result, status, 
                 started_at, completed_at, duration_ms, metadata)
                VALUES ($1::uuid, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11::jsonb)
                RETURNING id
            """, action.trace_id, parent_message_id, action.action_type, action.target,
                action.command, action.result, action.status, action.started_at,
                action.completed_at, action.duration_ms, json.dumps(action.metadata or {}))
            
            return row['id']

    class _ActionContext:
        """Context manager for tracing actions."""
        def __init__(self, tracer: 'ObservabilityTracer', action: ActionTrace, parent_msg_id: Optional[int]):
            self.tracer = tracer
            self.action = action
            self.parent_msg_id = parent_msg_id
            
        async def __aenter__(self):
            return self.action
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            self.action.completed_at = datetime.utcnow()
            if self.action.started_at:
                delta = self.action.completed_at - self.action.started_at
                self.action.duration_ms = int(delta.total_seconds() * 1000)
            
            if exc_type:
                self.action.status = 'failed'
                self.action.result = str(exc_val)
            elif self.action.status == 'pending':
                self.action.status = 'success'
            
            await self.tracer.log_action(self.action, self.parent_msg_id)
            return False  # Don't suppress exceptions

    def trace_action(
        self,
        action_type: str,
        target: str,
        command: str,
        parent_message_id: Optional[int] = None,
        metadata: Optional[Dict] = None
    ) -> _ActionContext:
        """
        Context manager for tracing an action.
        
        Usage:
            async with tracer.trace_action('shell', '100.72.2.99', 'hostname') as action:
                result = await run_command()
                action.result = result
        """
        trace_id = self._current_trace_id or self.new_trace_id()
        action = ActionTrace(
            trace_id=trace_id,
            action_type=action_type,
            target=target,
            command=command,
            metadata=metadata
        )
        return self._ActionContext(self, action, parent_message_id)

    async def get_session_actions(self) -> List[Dict]:
        """Get all actions from the current session."""
        if not self.db_pool:
            return []
        
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM action_traces 
                WHERE trace_id IN (
                    SELECT DISTINCT trace_id FROM telegram_messages WHERE session_key = $1
                )
                ORDER BY started_at
            """, self.session_key)
            
            return [dict(row) for row in rows]

    async def export_workflow(self, name: Optional[str] = None) -> str:
        """Export the current session as a reproducible shell script."""
        actions = await self.get_session_actions()
        
        script_lines = [
            "#!/bin/bash",
            f"# Workflow: {name or self.session_key}",
            f"# Generated: {datetime.utcnow().isoformat()}Z",
            f"# Actions: {len(actions)}",
            "",
            "set -e  # Exit on error",
            ""
        ]
        
        for action in actions:
            if action['action_type'] == 'shell':
                script_lines.append(f"# {action['action_type']} on {action['target']}")
                if action['target'] and action['target'] != 'localhost':
                    script_lines.append(f"ssh {action['target']} \"{action['command']}\"")
                else:
                    script_lines.append(action['command'])
                script_lines.append("")
        
        workflow_script = "\n".join(script_lines)
        
        # Store in database
        if self.db_pool:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO workflow_exports (session_key, workflow_name, workflow_script)
                    VALUES ($1, $2, $3)
                """, self.session_key, name or self.session_key, workflow_script)
        
        return workflow_script


# Singleton instance for easy access
_tracer_instance: Optional[ObservabilityTracer] = None

async def get_tracer(session_key: Optional[str] = None) -> ObservabilityTracer:
    """Get or create the global tracer instance."""
    global _tracer_instance
    if _tracer_instance is None:
        _tracer_instance = ObservabilityTracer(session_key)
        await _tracer_instance.connect()
    return _tracer_instance


# Quick test
if __name__ == "__main__":
    async def test():
        tracer = ObservabilityTracer("test_session")
        await tracer.connect()
        
        # Log a message
        msg_id = await tracer.log_message(
            chat_id=8445149012,
            user_id=8445149012,
            content="Test message",
            username="Mike"
        )
        print(f"Logged message: {msg_id}")
        
        # Trace an action
        async with tracer.trace_action('shell', 'localhost', 'echo hello') as action:
            action.result = "hello"
            action.status = "success"
        
        print("Action traced!")
        
        # Export workflow
        script = await tracer.export_workflow("test_workflow")
        print(f"Exported workflow:\n{script}")
        
        await tracer.close()
    
    asyncio.run(test())
