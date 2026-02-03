"""
FactoryLM Plane Integration
Created: 2026-02-03T02:14:00Z

Syncs traced actions and sessions to Plane project management.
"""

import os
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime

# Plane configuration
PLANE_HOST = os.environ.get('PLANE_HOST', 'https://plane.factorylm.com')
PLANE_API_KEY = os.environ.get('PLANE_API_KEY', '')
PLANE_WORKSPACE = os.environ.get('PLANE_WORKSPACE', 'factorylm')
PLANE_PROJECT = os.environ.get('PLANE_PROJECT', 'ops')


class PlaneSync:
    """
    Sync observability data to Plane for project tracking.
    
    Usage:
        sync = PlaneSync()
        issue = await sync.create_issue(
            title="Setup PLC laptop remote access",
            description="Configure Jarvis Node API...",
            labels=["infrastructure", "automation"]
        )
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        host: Optional[str] = None,
        workspace: Optional[str] = None,
        project: Optional[str] = None
    ):
        self.api_key = api_key or PLANE_API_KEY
        self.host = host or PLANE_HOST
        self.workspace = workspace or PLANE_WORKSPACE
        self.project = project or PLANE_PROJECT
        self.client = httpx.AsyncClient(
            base_url=f"{self.host}/api/v1",
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated request to Plane API."""
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    async def list_projects(self) -> List[Dict]:
        """List all projects in workspace."""
        return await self._request("GET", f"/workspaces/{self.workspace}/projects/")
    
    async def create_issue(
        self,
        title: str,
        description: str,
        priority: str = "medium",  # urgent, high, medium, low, none
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a new issue in Plane.
        
        Args:
            title: Issue title
            description: Issue description (markdown supported)
            priority: urgent, high, medium, low, none
            state: Issue state ID
            labels: List of label IDs
            assignees: List of user IDs
            metadata: Additional metadata to store
        """
        payload = {
            "name": title,
            "description_html": f"<p>{description}</p>",
            "priority": priority,
        }
        
        if state:
            payload["state"] = state
        if labels:
            payload["labels"] = labels
        if assignees:
            payload["assignees"] = assignees
        
        return await self._request(
            "POST",
            f"/workspaces/{self.workspace}/projects/{self.project}/issues/",
            json=payload
        )
    
    async def update_issue(self, issue_id: str, **updates) -> Dict:
        """Update an existing issue."""
        return await self._request(
            "PATCH",
            f"/workspaces/{self.workspace}/projects/{self.project}/issues/{issue_id}/",
            json=updates
        )
    
    async def add_comment(self, issue_id: str, comment: str) -> Dict:
        """Add a comment to an issue."""
        return await self._request(
            "POST",
            f"/workspaces/{self.workspace}/projects/{self.project}/issues/{issue_id}/comments/",
            json={"comment_html": f"<p>{comment}</p>"}
        )
    
    async def sync_session_to_issue(
        self,
        session_key: str,
        title: str,
        actions: List[Dict],
        outcome: str = "completed"
    ) -> Dict:
        """
        Create or update an issue from a traced session.
        
        Args:
            session_key: Session identifier
            title: Issue title
            actions: List of traced actions
            outcome: Session outcome
        """
        # Build description from actions
        action_lines = []
        for action in actions:
            status_emoji = "✅" if action.get('status') == 'success' else "❌"
            action_lines.append(
                f"- {status_emoji} `{action.get('action_type', 'unknown')}` on `{action.get('target', 'unknown')}`: "
                f"`{action.get('command', '')[:50]}...`"
            )
        
        description = f"""
## Session: {session_key}

### Actions Performed
{chr(10).join(action_lines) if action_lines else "No actions recorded"}

### Outcome
{outcome}

### Timestamp
{datetime.utcnow().isoformat()}Z

---
*Auto-generated from FactoryLM observability trace*
"""
        
        return await self.create_issue(
            title=title,
            description=description,
            priority="medium"
        )


# Quick test
if __name__ == "__main__":
    import asyncio
    
    async def test():
        sync = PlaneSync()
        
        # Test list projects
        projects = await sync.list_projects()
        print(f"Projects: {projects}")
        
        await sync.close()
    
    asyncio.run(test())
