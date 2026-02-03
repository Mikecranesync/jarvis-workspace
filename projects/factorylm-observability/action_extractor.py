"""
FactoryLM Action Extractor
Created: 2026-02-03T02:15:00Z

Extracts actionable items from conversations using pattern matching
and optional LLM analysis.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ExtractedAction:
    """Represents an extracted action from conversation."""
    action_type: str
    target: str
    command: str
    confidence: float
    source_text: str


class ActionExtractor:
    """
    Extract actions from conversation text.
    
    Recognizes patterns like:
    - SSH commands: ssh user@host "command"
    - API calls: curl http://...
    - File operations: write to /path, read /path
    - Shell commands: run/execute "command"
    """
    
    # Pattern definitions
    PATTERNS = [
        # SSH commands
        {
            'type': 'ssh',
            'pattern': r'ssh\s+(\S+@\S+)\s+["\']([^"\']+)["\']',
            'groups': ['target', 'command'],
            'confidence': 0.95
        },
        # Curl API calls
        {
            'type': 'api_call',
            'pattern': r'curl\s+.*?(https?://[^\s]+)',
            'groups': ['target'],
            'confidence': 0.9
        },
        # File writes
        {
            'type': 'file_write',
            'pattern': r'(?:write|create|save)\s+(?:to\s+)?["\']?(/[^\s"\']+)["\']?',
            'groups': ['target'],
            'confidence': 0.8
        },
        # Ping commands
        {
            'type': 'network_test',
            'pattern': r'ping\s+.*?(\d+\.\d+\.\d+\.\d+|\S+\.\S+)',
            'groups': ['target'],
            'confidence': 0.9
        },
        # Shell commands
        {
            'type': 'shell',
            'pattern': r'(?:run|execute|ran)\s+["\']([^"\']+)["\']',
            'groups': ['command'],
            'confidence': 0.7
        },
        # Scheduled tasks
        {
            'type': 'scheduled_task',
            'pattern': r'schtasks\s+/(?:create|run|delete)\s+.*?/tn\s+["\']?(\S+)["\']?',
            'groups': ['target'],
            'confidence': 0.95
        },
        # Service management
        {
            'type': 'service',
            'pattern': r'(?:start|stop|restart)\s+(?:service\s+)?["\']?(\S+)["\']?',
            'groups': ['target'],
            'confidence': 0.75
        },
        # Notifications
        {
            'type': 'notify',
            'pattern': r'(?:send|sent)\s+(?:a\s+)?(?:notification|toast|alert)',
            'groups': [],
            'confidence': 0.85
        },
    ]
    
    def __init__(self):
        self.compiled_patterns = [
            {
                **p,
                'compiled': re.compile(p['pattern'], re.IGNORECASE)
            }
            for p in self.PATTERNS
        ]
    
    def extract_from_text(self, text: str) -> List[ExtractedAction]:
        """
        Extract actions from conversation text.
        
        Args:
            text: Conversation or log text to analyze
            
        Returns:
            List of extracted actions
        """
        actions = []
        
        for pattern_def in self.compiled_patterns:
            matches = pattern_def['compiled'].finditer(text)
            
            for match in matches:
                groups = match.groups()
                
                # Build action based on pattern type
                target = ""
                command = match.group(0)
                
                if 'target' in pattern_def['groups'] and groups:
                    target_idx = pattern_def['groups'].index('target')
                    if target_idx < len(groups):
                        target = groups[target_idx]
                
                if 'command' in pattern_def['groups'] and groups:
                    cmd_idx = pattern_def['groups'].index('command')
                    if cmd_idx < len(groups):
                        command = groups[cmd_idx]
                
                action = ExtractedAction(
                    action_type=pattern_def['type'],
                    target=target or 'localhost',
                    command=command,
                    confidence=pattern_def['confidence'],
                    source_text=match.group(0)
                )
                actions.append(action)
        
        # Deduplicate by (type, target, command)
        seen = set()
        unique_actions = []
        for action in actions:
            key = (action.action_type, action.target, action.command[:50])
            if key not in seen:
                seen.add(key)
                unique_actions.append(action)
        
        return unique_actions
    
    def extract_from_messages(self, messages: List[Dict]) -> List[ExtractedAction]:
        """
        Extract actions from a list of message dictionaries.
        
        Args:
            messages: List of message dicts with 'content' field
            
        Returns:
            List of extracted actions
        """
        all_text = "\n".join(
            msg.get('content', '') 
            for msg in messages 
            if msg.get('content')
        )
        return self.extract_from_text(all_text)
    
    def summarize_session(self, actions: List[ExtractedAction]) -> Dict[str, Any]:
        """
        Summarize extracted actions.
        
        Args:
            actions: List of extracted actions
            
        Returns:
            Summary dict with counts and details
        """
        by_type = {}
        for action in actions:
            if action.action_type not in by_type:
                by_type[action.action_type] = []
            by_type[action.action_type].append(action)
        
        return {
            'total_actions': len(actions),
            'by_type': {
                action_type: len(items) 
                for action_type, items in by_type.items()
            },
            'unique_targets': list(set(a.target for a in actions if a.target)),
            'high_confidence': len([a for a in actions if a.confidence >= 0.9])
        }


# Test with tonight's session
if __name__ == "__main__":
    test_text = """
    I ran ssh hharp@100.72.2.99 "hostname" and got LAPTOP-0KA3C70H.
    Then I did curl http://100.72.2.99:8765/health to test the API.
    The service wasn't running so I executed schtasks /create /tn JarvisNode 
    to create a scheduled task.
    Finally I sent a notification to confirm it was working.
    """
    
    extractor = ActionExtractor()
    actions = extractor.extract_from_text(test_text)
    
    print("Extracted actions:")
    for action in actions:
        print(f"  - {action.action_type}: {action.target} -> {action.command[:50]}... (conf: {action.confidence})")
    
    summary = extractor.summarize_session(actions)
    print(f"\nSummary: {summary}")
