#!/usr/bin/env python3
"""
Narration Script Templates for The Automaton
Pre-built templates for common content scenarios
"""

from typing import Dict, Any
from datetime import datetime

# Template library
TEMPLATES = {
    "terminal_demo": """
{intro}

What you're seeing here is {description}.

{steps}

{conclusion}
""",

    "before_after": """
Let me show you a before and after comparison.

Before: {before_description}

After: {after_description}

The key difference is {key_difference}.
""",

    "build_progress": """
Day {day} of building {project_name}.

Today I {accomplishment}.

{details}

Next up: {next_steps}
""",

    "tutorial": """
In this video, I'll show you how to {task}.

Here's what you'll need: {requirements}

Step one: {step1}
Step two: {step2}
Step three: {step3}

And that's it! {outro}
""",

    "announcement": """
Big news!

{announcement}

This means {implications}.

{call_to_action}
""",

    "demo_video": """
Watch this.

{setup}

{action}

{result}

{closing}
""",

    "daily_recap": """
Here's what happened today, {date}.

{summary}

Key wins: {wins}

Tomorrow: {tomorrow}
""",

    "error_fix": """
So I ran into a problem.

{problem}

Here's how I fixed it:

{solution}

Lesson learned: {lesson}
""",

    "factory_io_demo": """
This is a Factory I/O simulation running on a real Allen-Bradley PLC.

Right now, {current_state}.

Watch what happens when {trigger}.

{observation}

This is exactly why we need AI monitoring - {insight}.
""",

    "edge_deployment": """
This device costs fifty dollars.

It's running {model_name} locally.

No internet required. No cloud. Just plug it in.

{demo_action}

{result}

This is the future of industrial AI.
"""
}


def get_template(name: str) -> str:
    """Get a template by name."""
    return TEMPLATES.get(name, TEMPLATES["demo_video"])


def list_templates() -> list:
    """List all available templates."""
    return list(TEMPLATES.keys())


def fill_template(name: str, **kwargs) -> str:
    """Fill a template with provided values.
    
    Args:
        name: Template name
        **kwargs: Template variables
        
    Returns:
        Filled template string
    """
    template = get_template(name)
    
    # Add defaults
    defaults = {
        "date": datetime.now().strftime("%B %d"),
        "intro": "Hey everyone.",
        "conclusion": "That's it for now.",
        "outro": "Thanks for watching.",
        "closing": "And that's how it's done.",
    }
    
    # Merge defaults with provided kwargs
    for key, value in defaults.items():
        if key not in kwargs:
            kwargs[key] = value
    
    # Fill template
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return f"Missing template variable: {e}"


def generate_build_day_script(day: int, project: str, 
                               accomplishment: str, 
                               details: str = "",
                               next_steps: str = "") -> str:
    """Generate a build-in-public daily script.
    
    Args:
        day: Day number
        project: Project name
        accomplishment: What was accomplished
        details: Additional details
        next_steps: What's coming next
        
    Returns:
        Complete narration script
    """
    return fill_template(
        "build_progress",
        day=day,
        project_name=project,
        accomplishment=accomplishment,
        details=details or "I'll share more details in the next update.",
        next_steps=next_steps or "Stay tuned."
    )


def generate_demo_script(setup: str, action: str, 
                         result: str, closing: str = None) -> str:
    """Generate a demo video script.
    
    Args:
        setup: What we're looking at
        action: What happens
        result: The outcome
        closing: Final words
        
    Returns:
        Complete narration script
    """
    return fill_template(
        "demo_video",
        setup=setup,
        action=action,
        result=result,
        closing=closing or "And that's the demo."
    )


# Pre-built scripts for Tuesday demo
TUESDAY_DEMO_SCRIPTS = {
    "intro": """
This is ShopTalk. A pocket-sized industrial AI expert.

It costs fifty dollars. It works offline. It speaks any language.

Watch.
""",

    "spanish_query": """
I'm going to ask it a question in Spanish.

¿Cuál es el estado de la máquina?

That means: What's the status of the machine?
""",

    "response": """
It understood the question and responded in Spanish.

No internet connection. No cloud. Everything runs locally.

This device can diagnose factory equipment anywhere in the world.
""",

    "outro": """
Built in four days. Running on a fifty dollar board.

This is the future of industrial maintenance.

DM me if you want one for your factory.
"""
}


if __name__ == "__main__":
    # Demo
    print("=== Available Templates ===")
    for t in list_templates():
        print(f"  - {t}")
    
    print("\n=== Sample Build Day Script ===")
    script = generate_build_day_script(
        day=1,
        project="ShopTalk Edge AI",
        accomplishment="set up the BeagleBone and connected it to Factory I/O",
        details="The simulation is now feeding real data to our world model training pipeline.",
        next_steps="training the model overnight."
    )
    print(script)
