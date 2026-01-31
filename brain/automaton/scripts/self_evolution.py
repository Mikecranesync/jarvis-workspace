#!/usr/bin/env python3
"""
Self-Evolution Engine — Core of the Autonomous System

Analyzes experiences, identifies improvements, and evolves strategies.
Part of the Automaton self-evolving system.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

AUTOMATON_DIR = Path(__file__).parent.parent
LEARNING_DIR = AUTOMATON_DIR / "learning"
PROCEDURES_DIR = AUTOMATON_DIR / "procedures"
METRICS_DIR = AUTOMATON_DIR / "metrics"

class SelfEvolutionEngine:
    """Drives autonomous self-improvement."""
    
    def __init__(self):
        self.evolution_log = AUTOMATON_DIR / "evolution-log.md"
        
    def analyze_and_evolve(self) -> Dict:
        """Main evolution cycle."""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "analyses": [],
            "improvements": [],
            "new_procedures": [],
            "metrics_updates": []
        }
        
        # 1. Analyze learning data
        analysis = self._analyze_learning_data()
        results["analyses"].append(analysis)
        
        # 2. Identify improvement opportunities
        opportunities = self._identify_opportunities(analysis)
        results["improvements"] = opportunities
        
        # 3. Check procedure coverage
        procedure_gaps = self._check_procedure_gaps(analysis)
        results["new_procedures"] = procedure_gaps
        
        # 4. Update evolution log
        self._log_evolution(results)
        
        return results
    
    def _analyze_learning_data(self) -> Dict:
        """Analyze learning experiences for patterns."""
        experiences_file = LEARNING_DIR / "experiences.jsonl"
        metrics_file = METRICS_DIR / "task_metrics.json"
        
        analysis = {
            "total_experiences": 0,
            "success_rate": 0,
            "task_type_distribution": {},
            "failure_patterns": [],
            "improvement_areas": []
        }
        
        if not experiences_file.exists():
            return analysis
        
        experiences = []
        with open(experiences_file) as f:
            for line in f:
                experiences.append(json.loads(line.strip()))
        
        if not experiences:
            return analysis
        
        analysis["total_experiences"] = len(experiences)
        
        # Calculate success rate
        successes = len([e for e in experiences if e.get("outcome") == "success"])
        analysis["success_rate"] = successes / len(experiences) if experiences else 0
        
        # Task type distribution
        for exp in experiences:
            tt = exp.get("task_type", "unknown")
            if tt not in analysis["task_type_distribution"]:
                analysis["task_type_distribution"][tt] = {"total": 0, "success": 0}
            analysis["task_type_distribution"][tt]["total"] += 1
            if exp.get("outcome") == "success":
                analysis["task_type_distribution"][tt]["success"] += 1
        
        # Identify low-performing task types
        for tt, data in analysis["task_type_distribution"].items():
            if data["total"] >= 3:
                rate = data["success"] / data["total"]
                if rate < 0.7:
                    analysis["improvement_areas"].append({
                        "task_type": tt,
                        "success_rate": rate,
                        "suggestion": f"Create or improve procedure for {tt}"
                    })
        
        return analysis
    
    def _identify_opportunities(self, analysis: Dict) -> List[Dict]:
        """Identify specific improvement opportunities."""
        opportunities = []
        
        # Low success rate tasks
        for area in analysis.get("improvement_areas", []):
            opportunities.append({
                "type": "procedure_improvement",
                "target": area["task_type"],
                "reason": f"Low success rate: {area['success_rate']*100:.0f}%",
                "action": "Review and document better approach"
            })
        
        # Overall low success rate
        if analysis.get("success_rate", 1) < 0.8:
            opportunities.append({
                "type": "system_improvement",
                "target": "overall_approach",
                "reason": f"Overall success rate: {analysis['success_rate']*100:.0f}%",
                "action": "Review recent failures and add verification steps"
            })
        
        return opportunities
    
    def _check_procedure_gaps(self, analysis: Dict) -> List[str]:
        """Identify task types without documented procedures."""
        gaps = []
        
        # Get all task types from experiences
        task_types = set(analysis.get("task_type_distribution", {}).keys())
        
        # Check which have procedures
        for tt in task_types:
            # Simple check - look for procedure files mentioning this task type
            has_procedure = False
            for proc_file in PROCEDURES_DIR.rglob("*.md"):
                if proc_file.name != "README.md":
                    content = proc_file.read_text()
                    if tt.lower() in content.lower():
                        has_procedure = True
                        break
            
            if not has_procedure and analysis["task_type_distribution"][tt]["total"] >= 3:
                gaps.append(tt)
        
        return gaps
    
    def _log_evolution(self, results: Dict):
        """Log evolution results."""
        log_entry = f"""
## Evolution Cycle — {results['timestamp']}

### Analysis
- Total experiences analyzed: {results['analyses'][0].get('total_experiences', 0)}
- Overall success rate: {results['analyses'][0].get('success_rate', 0)*100:.0f}%

### Improvements Identified
"""
        for imp in results.get("improvements", []):
            log_entry += f"- [{imp['type']}] {imp['target']}: {imp['reason']}\n"
        
        if results.get("new_procedures"):
            log_entry += "\n### Procedure Gaps\n"
            for gap in results["new_procedures"]:
                log_entry += f"- Need procedure for: {gap}\n"
        
        log_entry += "\n---\n"
        
        # Append to evolution log
        with open(self.evolution_log, "a") as f:
            f.write(log_entry)
    
    def get_evolution_summary(self) -> str:
        """Get a summary of recent evolution cycles."""
        if not self.evolution_log.exists():
            return "No evolution cycles recorded yet."
        
        content = self.evolution_log.read_text()
        # Get last 3 cycles
        cycles = content.split("## Evolution Cycle")[-4:]
        return "## Evolution Cycle".join(cycles)


class VerificationEngine:
    """Verifies work before committing."""
    
    def __init__(self):
        self.verification_log = AUTOMATON_DIR / "verification-log.md"
    
    def verify_code_change(self, file_path: str) -> Dict:
        """Verify a code change is valid."""
        results = {
            "file": file_path,
            "checks": [],
            "passed": True
        }
        
        path = Path(file_path)
        
        # Check file exists
        if not path.exists():
            results["checks"].append({"check": "file_exists", "passed": False})
            results["passed"] = False
            return results
        
        results["checks"].append({"check": "file_exists", "passed": True})
        
        # Check syntax (Python)
        if path.suffix == ".py":
            import subprocess
            try:
                result = subprocess.run(
                    ["python3", "-m", "py_compile", str(path)],
                    capture_output=True,
                    text=True
                )
                passed = result.returncode == 0
                results["checks"].append({
                    "check": "python_syntax",
                    "passed": passed,
                    "error": result.stderr if not passed else None
                })
                if not passed:
                    results["passed"] = False
            except Exception as e:
                results["checks"].append({
                    "check": "python_syntax",
                    "passed": False,
                    "error": str(e)
                })
                results["passed"] = False
        
        return results
    
    def verify_response(self, response: str, requirements: List[str]) -> Dict:
        """Verify a response meets requirements."""
        results = {
            "requirements": requirements,
            "checks": [],
            "passed": True
        }
        
        for req in requirements:
            # Simple keyword check
            passed = req.lower() in response.lower()
            results["checks"].append({
                "requirement": req,
                "passed": passed
            })
            if not passed:
                results["passed"] = False
        
        return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: self_evolution.py [analyze|evolve|summary|verify]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "analyze":
        engine = SelfEvolutionEngine()
        analysis = engine._analyze_learning_data()
        print(json.dumps(analysis, indent=2))
    
    elif cmd == "evolve":
        engine = SelfEvolutionEngine()
        results = engine.analyze_and_evolve()
        print(json.dumps(results, indent=2))
    
    elif cmd == "summary":
        engine = SelfEvolutionEngine()
        print(engine.get_evolution_summary())
    
    elif cmd == "verify":
        if len(sys.argv) < 3:
            print("Usage: self_evolution.py verify <file_path>")
            sys.exit(1)
        verifier = VerificationEngine()
        results = verifier.verify_code_change(sys.argv[2])
        print(json.dumps(results, indent=2))
