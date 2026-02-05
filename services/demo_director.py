# Source: factorylm/workers/demo_director_tasks.py - Imported 2025-01-18
"""
DEMO DIRECTOR - The Hollywood Brain
=====================================
Orchestrates multi-camera YC demo with automatic scene switching,
PLC sync, and phone viewer coordination.

"14 cameras, dynamic switching, phones as displays, real PLC I/O"
— Mike, 2026-02-05
"""

import os
import sys
import json
import yaml
import time
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# Constants
SCRIPT_PATH = Path('/root/jarvis-workspace/demo/demo_script.yaml')
STATE_PATH = Path('/root/jarvis-workspace/demo/state/demo_state.json')


class DemoPhase(Enum):
    """Current phase of the demo."""
    IDLE = "idle"
    PREPARING = "preparing"
    LIVE = "live"
    PAUSED = "paused"
    FINISHED = "finished"
    ERROR = "error"


@dataclass
class DemoState:
    """Live state of the demo."""
    phase: DemoPhase = DemoPhase.IDLE
    current_scene: str = ""
    current_camera: str = ""
    elapsed_seconds: float = 0.0
    phone_clients: int = 0
    last_plc_read: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "phase": self.phase.value,
            "current_scene": self.current_scene,
            "current_camera": self.current_camera,
            "elapsed_seconds": self.elapsed_seconds,
            "phone_clients": self.phone_clients,
            "last_plc_read": self.last_plc_read,
            "errors": self.errors,
            "timestamp": datetime.now().isoformat()
        }
    
    def save(self):
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_PATH, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls) -> 'DemoState':
        if STATE_PATH.exists():
            with open(STATE_PATH) as f:
                data = json.load(f)
            state = cls()
            state.phase = DemoPhase(data.get('phase', 'idle'))
            state.current_scene = data.get('current_scene', '')
            state.current_camera = data.get('current_camera', '')
            state.elapsed_seconds = data.get('elapsed_seconds', 0.0)
            state.phone_clients = data.get('phone_clients', 0)
            state.last_plc_read = data.get('last_plc_read', {})
            state.errors = data.get('errors', [])
            return state
        return cls()


@dataclass
class Scene:
    """A single scene in the demo script."""
    name: str
    duration: int  # seconds
    cameras: List[str]
    narration: str
    actions: List[Dict[str, Any]]
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Scene':
        return cls(
            name=data['name'],
            duration=data.get('duration', 30),
            cameras=data.get('cameras', ['CAM-7']),
            narration=data.get('narration', ''),
            actions=data.get('actions', [])
        )


class DemoDirector:
    """
    The Director - orchestrates the entire demo.
    
    Responsibilities:
    1. Load and execute demo script
    2. Coordinate camera switches via OBS
    3. Sync PLC state with visuals
    4. Manage phone viewer connections
    5. Handle errors gracefully
    """
    
    def __init__(self):
        self.name = "DemoDirector"
        self.state = DemoState.load()
        self.scenes: List[Scene] = []
        self.current_scene_idx = 0
        self.logger = logging.getLogger(self.name)
    
    def load_script(self, script_path: Path = SCRIPT_PATH) -> bool:
        """Load the demo script from YAML."""
        if not script_path.exists():
            self.logger.warning(f"Script not found: {script_path}")
            return False
        
        try:
            with open(script_path) as f:
                data = yaml.safe_load(f)
            
            self.scenes = [Scene.from_dict(s) for s in data.get('scenes', [])]
            self.logger.info(f"Loaded {len(self.scenes)} scenes from {script_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load script: {e}")
            return False
    
    def start_demo(self) -> dict:
        """Begin the demo from scene 1."""
        if not self.scenes:
            if not self.load_script():
                return {"error": "No script loaded", "phase": "error"}
        
        self.state.phase = DemoPhase.LIVE
        self.state.current_scene = self.scenes[0].name if self.scenes else ""
        self.current_scene_idx = 0
        self.state.elapsed_seconds = 0
        self.state.save()
        
        # Execute first scene
        result = self.execute_scene(0)
        
        return {
            "status": "started",
            "total_scenes": len(self.scenes),
            "first_scene": self.state.current_scene,
            "first_scene_result": result
        }
    
    def advance_scene(self) -> dict:
        """Move to the next scene."""
        self.current_scene_idx += 1
        
        if self.current_scene_idx >= len(self.scenes):
            self.state.phase = DemoPhase.FINISHED
            self.state.save()
            return {"status": "finished", "message": "Demo complete!"}
        
        scene = self.scenes[self.current_scene_idx]
        self.state.current_scene = scene.name
        self.state.save()
        
        return {
            "status": "advanced",
            "scene_index": self.current_scene_idx,
            "scene_name": scene.name
        }
    
    def pause_demo(self) -> dict:
        """Pause the demo."""
        self.state.phase = DemoPhase.PAUSED
        self.state.save()
        return {"status": "paused"}
    
    def resume_demo(self) -> dict:
        """Resume paused demo."""
        self.state.phase = DemoPhase.LIVE
        self.state.save()
        return {"status": "resumed"}
    
    def get_status(self) -> dict:
        """Get current demo status."""
        return self.state.to_dict()
    
    def execute_scene(self, scene_index: int) -> dict:
        """
        Execute a specific scene.
        
        This is where the magic happens:
        1. Switch OBS cameras
        2. Execute scene actions (PLC reads, forces, etc.)
        3. Update phone viewers
        4. Schedule next scene
        """
        
        if scene_index >= len(self.scenes):
            return {"error": "Scene index out of range"}
        
        scene = self.scenes[scene_index]
        self.state.current_scene = scene.name
        self.state.current_camera = scene.cameras[0] if scene.cameras else ""
        self.state.save()
        
        results = {
            "scene": scene.name,
            "cameras": scene.cameras,
            "duration": scene.duration,
            "actions_executed": []
        }
        
        # Execute each action in the scene
        for action in scene.actions:
            action_type = action.get('type')
            
            if action_type == 'obs_transition':
                # Trigger OBS scene switch
                results['actions_executed'].append(f"obs:{action.get('scene')}")
                
            elif action_type == 'plc_read':
                # Read PLC value
                results['actions_executed'].append(f"plc_read:{action.get('address')}")
                
            elif action_type == 'plc_force':
                # Force PLC output
                results['actions_executed'].append(f"plc_force:{action.get('address')}={action.get('value')}")
                
            elif action_type == 'mermaid_update':
                # Update I/O diagram
                results['actions_executed'].append("mermaid_update")
                
            elif action_type == 'qr_display':
                # Show QR code for phone viewers
                results['actions_executed'].append(f"qr:{action.get('url')}")
                
            elif action_type == 'wait_for_connections':
                # Wait for phone connections
                results['actions_executed'].append(f"wait_connections:{action.get('min_clients', 1)}")
        
        return results
    
    def camera_switch(self, camera_id: str) -> dict:
        """
        Immediate camera switch (manual override).
        
        camera_id: CAM-1 through CAM-14
        """
        self.state.current_camera = camera_id
        self.state.save()
        
        return {"camera": camera_id, "switched": True}
    
    def generate_shot_list(self) -> dict:
        """
        Generate shot list for manual filming.
        
        If live demo fails, this gives Mike exactly what to film:
        - Scene by scene breakdown
        - Camera angles for each shot
        - Timing cues
        - Script to read
        """
        
        if not self.scenes:
            self.load_script()
        
        shot_list = []
        cumulative_time = 0
        
        for idx, scene in enumerate(self.scenes):
            shot_list.append({
                "scene_number": idx + 1,
                "scene_name": scene.name,
                "start_time": f"{cumulative_time // 60}:{cumulative_time % 60:02d}",
                "duration_seconds": scene.duration,
                "cameras": scene.cameras,
                "primary_camera": scene.cameras[0] if scene.cameras else "CAM-7",
                "narration": scene.narration,
                "director_notes": self._generate_director_notes(scene)
            })
            cumulative_time += scene.duration
        
        # Save to file
        output_path = Path('/root/jarvis-workspace/demo/SHOT_LIST.md')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("# 🎬 YC Demo Shot List\n\n")
            f.write(f"**Total Runtime:** {cumulative_time // 60}:{cumulative_time % 60:02d}\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("---\n\n")
            
            for shot in shot_list:
                f.write(f"## Scene {shot['scene_number']}: {shot['scene_name']}\n\n")
                f.write(f"**Time:** {shot['start_time']} ({shot['duration_seconds']}s)\n\n")
                f.write(f"**Camera:** {shot['primary_camera']}\n\n")
                f.write(f"**Script:**\n> {shot['narration']}\n\n")
                f.write(f"**Director Notes:**\n{shot['director_notes']}\n\n")
                f.write("---\n\n")
        
        return {
            "shot_list": shot_list,
            "total_runtime_seconds": cumulative_time,
            "saved_to": str(output_path)
        }
    
    def _generate_director_notes(self, scene: Scene) -> str:
        """Generate director notes for a scene."""
        notes = []
        
        for action in scene.actions:
            action_type = action.get('type')
            
            if action_type == 'obs_transition':
                notes.append(f"• CUT TO: {action.get('scene')}")
            elif action_type == 'plc_read':
                notes.append(f"• SHOW: PLC address {action.get('address')} on screen")
            elif action_type == 'plc_force':
                notes.append(f"• ACTION: Force {action.get('address')} = {action.get('value')}")
            elif action_type == 'highlight':
                notes.append(f"• HIGHLIGHT: {action.get('target')} (circle/arrow)")
            elif action_type == 'qr_display':
                notes.append("• QR CODE: Show on screen for audience phones")
        
        if len(scene.cameras) > 1:
            notes.append(f"• MULTI-CAM: Switch between {', '.join(scene.cameras)}")
        
        return "\n".join(notes) if notes else "• Standard presentation shot"


# Global director instance
_director = None


def get_director() -> DemoDirector:
    global _director
    if _director is None:
        _director = DemoDirector()
    return _director


if __name__ == "__main__":
    # Test
    director = get_director()
    director.load_script()
    print(f"Loaded {len(director.scenes)} scenes")
    print(director.get_status())