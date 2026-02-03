"""
FactoryLM Observability Package

Components:
- tracer: Message and action tracing to PostgreSQL
- plane_sync: Sync to Plane project management
- action_extractor: Extract actions from conversation text
"""

from .tracer import ObservabilityTracer, ActionTrace, get_tracer
from .action_extractor import ActionExtractor, ExtractedAction
from .plane_sync import PlaneSync

__all__ = [
    'ObservabilityTracer', 
    'ActionTrace', 
    'get_tracer',
    'ActionExtractor',
    'ExtractedAction',
    'PlaneSync'
]
__version__ = '0.1.0'
