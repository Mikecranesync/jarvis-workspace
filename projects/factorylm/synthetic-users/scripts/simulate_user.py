#!/usr/bin/env python3
"""
Synthetic User Simulator for FactoryLM

Runs a synthetic user persona through test scenarios using browser automation.
Semi-autonomous - executes activities and reports results.
"""

import yaml
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse
import random
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
PERSONAS_DIR = BASE_DIR / "personas"
LOGS_DIR = BASE_DIR / "logs"
ACTIVITIES_DIR = BASE_DIR / "activities"

class SyntheticUser:
    """A synthetic user that can execute activities autonomously."""
    
    def __init__(self, persona_path: str):
        self.persona_path = Path(persona_path)
        self.persona = self._load_persona()
        self.session_log = []
        self.start_time = None
        
    def _load_persona(self) -> Dict:
        """Load persona from YAML file."""
        with open(self.persona_path) as f:
            return yaml.safe_load(f)
    
    @property
    def name(self) -> str:
        return self.persona.get('name', 'Unknown')
    
    @property
    def role(self) -> str:
        return self.persona.get('role', 'Unknown')
    
    @property
    def language(self) -> str:
        return self.persona.get('language', 'en')
    
    @property
    def tech_comfort(self) -> str:
        return self.persona.get('tech_comfort', 'medium')
    
    def start_session(self):
        """Start a new testing session."""
        self.start_time = datetime.utcnow()
        self.session_log = []
        logger.info(f"Starting session for {self.name} ({self.role})")
        self._log_action("session_start", {"persona": self.name})
    
    def _log_action(self, action: str, details: Dict):
        """Log an action to the session log."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "details": details
        }
        self.session_log.append(entry)
    
    def think(self, context: str) -> str:
        """
        Simulate user thinking based on persona characteristics.
        Returns a prompt that can be sent to an LLM for decision making.
        """
        prompt = f"""You are {self.name}, a {self.role} with {self.persona.get('experience_years', '?')} years of experience.

Background: {self.persona.get('background', 'N/A')}

Your tech comfort level: {self.tech_comfort}
Your communication style: {self.persona.get('personality', {}).get('communication_style', 'normal')}

Pain points you experience:
{chr(10).join('- ' + p for p in self.persona.get('pain_points', []))}

Goals you're trying to achieve:
{chr(10).join('- ' + g for g in self.persona.get('goals', []))}

Current context: {context}

Based on your persona, what would you do next? What would frustrate you? What would delight you?
Respond in character as {self.name}."""
        
        return prompt
    
    def evaluate_experience(self, scenario_name: str, steps_completed: List[str], 
                           issues_found: List[str], time_taken: float) -> Dict:
        """Evaluate the user experience for a scenario."""
        
        # Adjust expectations based on tech comfort
        time_expectations = {
            'very_low': 2.0,  # Expects 2x more time
            'low': 1.5,
            'medium': 1.0,
            'high': 0.8,
            'very_high': 0.6,
            'expert': 0.5
        }
        
        time_multiplier = time_expectations.get(self.tech_comfort, 1.0)
        adjusted_time = time_taken * time_multiplier
        
        # Calculate satisfaction based on issues and time
        base_satisfaction = 100
        satisfaction = base_satisfaction - (len(issues_found) * 15) - (adjusted_time * 2)
        satisfaction = max(0, min(100, satisfaction))
        
        evaluation = {
            "scenario": scenario_name,
            "persona": self.name,
            "role": self.role,
            "tech_comfort": self.tech_comfort,
            "steps_completed": len(steps_completed),
            "issues_found": issues_found,
            "time_taken_seconds": time_taken,
            "satisfaction_score": satisfaction,
            "would_recommend": satisfaction > 60,
            "feedback": self._generate_feedback(issues_found, satisfaction)
        }
        
        self._log_action("scenario_complete", evaluation)
        return evaluation
    
    def _generate_feedback(self, issues: List[str], satisfaction: float) -> str:
        """Generate in-character feedback."""
        quotes = self.persona.get('quotes', [])
        
        if satisfaction > 80:
            return f"This works well for what I need. {random.choice(quotes) if quotes else ''}"
        elif satisfaction > 50:
            return f"It's okay but could be better. Issues: {', '.join(issues[:2])}"
        else:
            return f"This is frustrating. {random.choice(quotes) if quotes else ''} Problems: {', '.join(issues)}"
    
    def get_test_scenarios(self) -> List[Dict]:
        """Get test scenarios for this persona."""
        return self.persona.get('test_scenarios', [])
    
    def end_session(self) -> Dict:
        """End session and generate report."""
        duration = (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0
        
        report = {
            "persona": self.name,
            "role": self.role,
            "session_duration_seconds": duration,
            "actions_logged": len(self.session_log),
            "log": self.session_log
        }
        
        # Save log to file
        log_file = LOGS_DIR / f"{self.persona.get('id', 'unknown')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Session ended for {self.name}. Log saved to {log_file}")
        return report


class UserSimulator:
    """Runs multiple synthetic users through test scenarios."""
    
    def __init__(self, app_url: str = "http://localhost:3000"):
        self.app_url = app_url
        self.users: List[SyntheticUser] = []
        self.results = []
        
    def load_all_personas(self):
        """Load all persona files."""
        for persona_file in PERSONAS_DIR.rglob("*.yaml"):
            try:
                user = SyntheticUser(persona_file)
                self.users.append(user)
                logger.info(f"Loaded persona: {user.name}")
            except Exception as e:
                logger.error(f"Failed to load {persona_file}: {e}")
        
        logger.info(f"Loaded {len(self.users)} synthetic users")
    
    def load_personas_by_role(self, role_dir: str):
        """Load personas from a specific role directory."""
        role_path = PERSONAS_DIR / role_dir
        if not role_path.exists():
            logger.error(f"Role directory not found: {role_path}")
            return
        
        for persona_file in role_path.glob("*.yaml"):
            user = SyntheticUser(persona_file)
            self.users.append(user)
            logger.info(f"Loaded persona: {user.name}")
    
    def run_simulation(self, user: SyntheticUser, use_browser: bool = False):
        """Run simulation for a single user."""
        user.start_session()
        
        scenarios = user.get_test_scenarios()
        for scenario in scenarios:
            logger.info(f"{user.name} executing scenario: {scenario['name']}")
            
            # Simulate scenario execution
            steps = scenario.get('steps', [])
            completed_steps = []
            issues = []
            
            start_time = time.time()
            
            for step in steps:
                # Simulate step execution with random delays based on tech comfort
                delay = random.uniform(0.5, 2.0)
                if user.tech_comfort in ['low', 'very_low']:
                    delay *= 2
                time.sleep(delay * 0.1)  # Scaled down for testing
                
                completed_steps.append(step)
                
                # Random chance of issue based on tech comfort
                issue_chance = {'very_low': 0.3, 'low': 0.2, 'medium': 0.1, 'high': 0.05, 'very_high': 0.02, 'expert': 0.01}
                if random.random() < issue_chance.get(user.tech_comfort, 0.1):
                    issues.append(f"Confusion at step: {step}")
            
            time_taken = time.time() - start_time
            
            # Evaluate experience
            evaluation = user.evaluate_experience(
                scenario['name'],
                completed_steps,
                issues,
                time_taken
            )
            self.results.append(evaluation)
        
        return user.end_session()
    
    def run_all(self, parallel: int = 1):
        """Run simulation for all loaded users."""
        logger.info(f"Running simulation for {len(self.users)} users")
        
        for user in self.users:
            self.run_simulation(user)
        
        return self.generate_summary()
    
    def generate_summary(self) -> Dict:
        """Generate summary report of all simulations."""
        if not self.results:
            return {"error": "No results to summarize"}
        
        avg_satisfaction = sum(r['satisfaction_score'] for r in self.results) / len(self.results)
        recommend_rate = sum(1 for r in self.results if r['would_recommend']) / len(self.results)
        
        all_issues = []
        for r in self.results:
            all_issues.extend(r.get('issues_found', []))
        
        # Group by role
        by_role = {}
        for r in self.results:
            role = r['role']
            if role not in by_role:
                by_role[role] = []
            by_role[role].append(r['satisfaction_score'])
        
        role_averages = {role: sum(scores)/len(scores) for role, scores in by_role.items()}
        
        summary = {
            "total_users": len(self.users),
            "total_scenarios": len(self.results),
            "average_satisfaction": round(avg_satisfaction, 1),
            "recommendation_rate": f"{recommend_rate*100:.0f}%",
            "total_issues_found": len(all_issues),
            "common_issues": list(set(all_issues))[:10],
            "satisfaction_by_role": role_averages,
            "lowest_satisfaction_role": min(role_averages, key=role_averages.get) if role_averages else None,
            "highest_satisfaction_role": max(role_averages, key=role_averages.get) if role_averages else None
        }
        
        # Save summary
        summary_file = LOGS_DIR / f"summary_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary saved to {summary_file}")
        return summary


def main():
    parser = argparse.ArgumentParser(description="Synthetic User Simulator")
    parser.add_argument("--persona", type=str, help="Path to specific persona file")
    parser.add_argument("--role", type=str, help="Run all personas in a role directory")
    parser.add_argument("--all", action="store_true", help="Run all personas")
    parser.add_argument("--parallel", type=int, default=1, help="Number of parallel users")
    parser.add_argument("--url", type=str, default="http://localhost:3000", help="App URL")
    parser.add_argument("--list", action="store_true", help="List all personas")
    args = parser.parse_args()
    
    simulator = UserSimulator(app_url=args.url)
    
    if args.list:
        simulator.load_all_personas()
        print(f"\n{'='*60}")
        print(f"SYNTHETIC USERS: {len(simulator.users)} total")
        print(f"{'='*60}")
        for user in simulator.users:
            print(f"  [{user.persona.get('id')}] {user.name} - {user.role}")
        return
    
    if args.persona:
        user = SyntheticUser(args.persona)
        simulator.users = [user]
    elif args.role:
        simulator.load_personas_by_role(args.role)
    elif args.all:
        simulator.load_all_personas()
    else:
        parser.print_help()
        return
    
    summary = simulator.run_all(parallel=args.parallel)
    
    print(f"\n{'='*60}")
    print("SIMULATION SUMMARY")
    print(f"{'='*60}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
