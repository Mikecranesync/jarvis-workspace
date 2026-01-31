#!/usr/bin/env python3
"""
Learning Logger — Self-Improvement Through Experience Tracking

Logs every task with outcomes to enable pattern recognition and strategy adaptation.
Part of the Automaton self-evolving system.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import os

# Paths
AUTOMATON_DIR = Path(__file__).parent.parent
LEARNING_DIR = AUTOMATON_DIR / "learning"
METRICS_DIR = AUTOMATON_DIR / "metrics"
PROCEDURES_DIR = AUTOMATON_DIR / "procedures"

@dataclass
class Experience:
    """A single learning experience."""
    timestamp: str
    task_type: str
    task_description: str
    actions_taken: List[str]
    outcome: str  # success, partial, failure
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
    lessons_learned: Optional[str] = None
    strategy_used: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class LearningLogger:
    """Logs and analyzes learning experiences."""
    
    def __init__(self):
        LEARNING_DIR.mkdir(parents=True, exist_ok=True)
        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        self.experiences_file = LEARNING_DIR / "experiences.jsonl"
        self.metrics_file = METRICS_DIR / "task_metrics.json"
        self.patterns_file = LEARNING_DIR / "patterns.json"
        
    def log_experience(self, experience: Experience) -> str:
        """Log a new experience."""
        exp_dict = experience.to_dict()
        exp_id = hashlib.md5(
            f"{experience.timestamp}{experience.task_description}".encode()
        ).hexdigest()[:12]
        exp_dict["id"] = exp_id
        
        # Append to experiences file
        with open(self.experiences_file, "a") as f:
            f.write(json.dumps(exp_dict) + "\n")
        
        # Update metrics
        self._update_metrics(experience)
        
        return exp_id
    
    def _update_metrics(self, experience: Experience):
        """Update task success metrics."""
        metrics = self._load_metrics()
        
        task_type = experience.task_type
        if task_type not in metrics:
            metrics[task_type] = {
                "total": 0,
                "success": 0,
                "partial": 0,
                "failure": 0,
                "avg_duration": 0,
                "last_updated": ""
            }
        
        m = metrics[task_type]
        m["total"] += 1
        m[experience.outcome] = m.get(experience.outcome, 0) + 1
        
        if experience.duration_seconds:
            old_avg = m["avg_duration"]
            old_count = m["total"] - 1
            m["avg_duration"] = (old_avg * old_count + experience.duration_seconds) / m["total"]
        
        m["last_updated"] = experience.timestamp
        m["success_rate"] = m["success"] / m["total"] if m["total"] > 0 else 0
        
        self._save_metrics(metrics)
    
    def _load_metrics(self) -> Dict:
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                return json.load(f)
        return {}
    
    def _save_metrics(self, metrics: Dict):
        with open(self.metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)
    
    def get_experiences(self, task_type: Optional[str] = None, 
                       outcome: Optional[str] = None,
                       limit: int = 100) -> List[Dict]:
        """Retrieve past experiences with optional filters."""
        if not self.experiences_file.exists():
            return []
        
        experiences = []
        with open(self.experiences_file) as f:
            for line in f:
                exp = json.loads(line.strip())
                if task_type and exp.get("task_type") != task_type:
                    continue
                if outcome and exp.get("outcome") != outcome:
                    continue
                experiences.append(exp)
        
        return experiences[-limit:]
    
    def get_success_rate(self, task_type: str) -> float:
        """Get success rate for a task type."""
        metrics = self._load_metrics()
        if task_type in metrics:
            return metrics[task_type].get("success_rate", 0)
        return 0.0
    
    def identify_failure_patterns(self) -> List[Dict]:
        """Analyze failures to identify patterns."""
        failures = self.get_experiences(outcome="failure", limit=50)
        
        patterns = {}
        for exp in failures:
            # Group by task type
            task_type = exp.get("task_type", "unknown")
            if task_type not in patterns:
                patterns[task_type] = {
                    "count": 0,
                    "common_errors": {},
                    "examples": []
                }
            
            patterns[task_type]["count"] += 1
            
            # Track error messages
            error = exp.get("error_message", "unknown")
            if error:
                patterns[task_type]["common_errors"][error] = \
                    patterns[task_type]["common_errors"].get(error, 0) + 1
            
            if len(patterns[task_type]["examples"]) < 3:
                patterns[task_type]["examples"].append(exp)
        
        # Save patterns for future reference
        with open(self.patterns_file, "w") as f:
            json.dump(patterns, f, indent=2)
        
        return [{"task_type": k, **v} for k, v in patterns.items()]
    
    def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on learning data."""
        metrics = self._load_metrics()
        patterns = self.identify_failure_patterns()
        
        suggestions = []
        
        # Find low success rate tasks
        for task_type, data in metrics.items():
            if data.get("success_rate", 1) < 0.7 and data.get("total", 0) >= 3:
                suggestions.append(
                    f"Task '{task_type}' has {data['success_rate']*100:.0f}% success rate. "
                    f"Review procedures and add better error handling."
                )
        
        # Find repeated failures
        for pattern in patterns:
            if pattern["count"] >= 3:
                errors = pattern.get("common_errors", {})
                top_error = max(errors.items(), key=lambda x: x[1])[0] if errors else "unknown"
                suggestions.append(
                    f"Task '{pattern['task_type']}' failed {pattern['count']} times. "
                    f"Common error: {top_error[:100]}. Consider creating a procedure."
                )
        
        return suggestions
    
    def generate_daily_report(self) -> str:
        """Generate a daily learning report."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        experiences = self.get_experiences(limit=1000)
        
        today_exps = [e for e in experiences if e.get("timestamp", "").startswith(today)]
        
        if not today_exps:
            return f"# Learning Report — {today}\n\nNo experiences logged today."
        
        success = len([e for e in today_exps if e.get("outcome") == "success"])
        partial = len([e for e in today_exps if e.get("outcome") == "partial"])
        failure = len([e for e in today_exps if e.get("outcome") == "failure"])
        total = len(today_exps)
        
        report = f"""# Learning Report — {today}

## Summary
- Total tasks: {total}
- Success: {success} ({success/total*100:.0f}%)
- Partial: {partial} ({partial/total*100:.0f}%)
- Failure: {failure} ({failure/total*100:.0f}%)

## Task Types
"""
        task_types = {}
        for e in today_exps:
            tt = e.get("task_type", "unknown")
            if tt not in task_types:
                task_types[tt] = {"total": 0, "success": 0}
            task_types[tt]["total"] += 1
            if e.get("outcome") == "success":
                task_types[tt]["success"] += 1
        
        for tt, data in sorted(task_types.items(), key=lambda x: -x[1]["total"]):
            rate = data["success"] / data["total"] * 100
            report += f"- {tt}: {data['total']} tasks, {rate:.0f}% success\n"
        
        suggestions = self.suggest_improvements()
        if suggestions:
            report += "\n## Improvement Suggestions\n"
            for s in suggestions[:5]:
                report += f"- {s}\n"
        
        return report


# CLI interface
if __name__ == "__main__":
    import sys
    
    logger = LearningLogger()
    
    if len(sys.argv) < 2:
        print("Usage: learning_logger.py [log|metrics|patterns|report|suggest]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "metrics":
        metrics = logger._load_metrics()
        print(json.dumps(metrics, indent=2))
    
    elif cmd == "patterns":
        patterns = logger.identify_failure_patterns()
        print(json.dumps(patterns, indent=2))
    
    elif cmd == "report":
        print(logger.generate_daily_report())
    
    elif cmd == "suggest":
        suggestions = logger.suggest_improvements()
        for s in suggestions:
            print(f"• {s}")
    
    elif cmd == "log":
        # Example logging
        exp = Experience(
            timestamp=datetime.utcnow().isoformat(),
            task_type="test",
            task_description="Test logging",
            actions_taken=["action1", "action2"],
            outcome="success"
        )
        exp_id = logger.log_experience(exp)
        print(f"Logged experience: {exp_id}")
