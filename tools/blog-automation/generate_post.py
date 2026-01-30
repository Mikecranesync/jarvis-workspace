#!/usr/bin/env python3
"""
FactoryLM Blog Post Generator
Multi-agent system: Researcher → Writer → Editor → Publisher

Uses:
- Perplexity API for research
- Claude API for writing/editing
- GitHub API for publishing
"""

import os
import json
import requests
from datetime import datetime

# API Keys (from environment)
PERPLEXITY_KEY = os.environ.get('PERPLEXITY_API_KEY')
ANTHROPIC_KEY = os.environ.get('ANTHROPIC_API_KEY')

def research_topic(topic: str) -> str:
    """Use Perplexity to research a topic"""
    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={
            "Authorization": f"Bearer {PERPLEXITY_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "sonar",
            "messages": [{
                "role": "user",
                "content": f"Research for a technical blog post about: {topic}. "
                          f"Focus on industrial maintenance, PLC diagnostics, and practical tips. "
                          f"Include specific error codes, troubleshooting steps, and real-world examples."
            }]
        }
    )
    return response.json()['choices'][0]['message']['content']

def write_post(topic: str, research: str) -> str:
    """Use Claude to write the blog post"""
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4000,
            "messages": [{
                "role": "user",
                "content": f"""Write a comprehensive SEO-optimized blog post for FactoryLM.

Topic: {topic}

Research:
{research}

Requirements:
- 1500-2000 words
- Include H2 and H3 headings
- Add a table of common error codes if relevant
- Include troubleshooting steps
- Add a CTA for FactoryLM at the end
- Write in a helpful, expert tone (20 years maintenance experience)
- Include target keywords naturally

Output format: Markdown with frontmatter (title, description, date, tags)"""
            }]
        }
    )
    return response.json()['content'][0]['text']

def edit_post(draft: str) -> str:
    """Use Claude to edit and polish the post"""
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4000,
            "messages": [{
                "role": "user",
                "content": f"""Edit this blog post for clarity, flow, and SEO optimization.

Draft:
{draft}

Tasks:
1. Fix any grammatical issues
2. Improve transitions between sections
3. Ensure keywords are naturally placed
4. Add internal links where appropriate
5. Verify technical accuracy
6. Make the CTA compelling

Output the final polished post in Markdown format."""
            }]
        }
    )
    return response.json()['content'][0]['text']

def generate_blog_post(topic: str) -> dict:
    """Full pipeline: Research → Write → Edit"""
    print(f"🔍 Researching: {topic}")
    research = research_topic(topic)
    
    print(f"✍️ Writing draft...")
    draft = write_post(topic, research)
    
    print(f"📝 Editing...")
    final = edit_post(draft)
    
    # Generate filename
    slug = topic.lower().replace(' ', '-').replace('/', '-')[:50]
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date}-{slug}.md"
    
    return {
        "filename": filename,
        "content": final,
        "topic": topic,
        "date": date
    }

# Topic ideas for FactoryLM blog
TOPIC_IDEAS = [
    "Siemens S7-1200 Error Codes Complete Guide",
    "Allen-Bradley CompactLogix Troubleshooting Tips",
    "5 Common VFD Faults and How to Fix Them",
    "How to Read PLC Diagnostic Buffers Like a Pro",
    "Predictive Maintenance vs Reactive: The Real Cost",
    "Capturing Tribal Knowledge Before Your Best Tech Retires",
    "Mobile CMMS: Why Your Techs Need Smartphones",
    "AI in Industrial Maintenance: What's Real vs Hype",
    "Reducing Diagnostic Time from Hours to Minutes",
    "The Hidden Cost of Unfamiliar Error Codes"
]

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else TOPIC_IDEAS[0]
    result = generate_blog_post(topic)
    
    # Save to file
    with open(f"posts/{result['filename']}", 'w') as f:
        f.write(result['content'])
    
    print(f"✅ Generated: posts/{result['filename']}")
