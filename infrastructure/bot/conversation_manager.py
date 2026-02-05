# Source: Agent-Factory/agent_factory/integrations/telegram/conversation_manager.py - Imported 2025-01-18
"""
Conversation Manager for Telegram Bot

Manages multi-turn conversations with context awareness, enabling the bot to:
- Remember previous messages
- Reference past topics
- Maintain conversation state
- Learn from interactions

Part of Phase 1: Natural Language Evolution
"""

import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class Message:
    """Single message in conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass 
class MessageHistory:
    """Collection of messages."""
    messages: List[Message]
    
    def __init__(self):
        self.messages = []
    
    def get_messages(self, limit: Optional[int] = None) -> List[Message]:
        """Get messages with optional limit."""
        if limit:
            return self.messages[-limit:]
        return self.messages


@dataclass
class Session:
    """Conversation session."""
    user_id: str
    session_id: Optional[str] = None
    history: Optional[MessageHistory] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    last_active: Optional[datetime] = None
    
    def __post_init__(self):
        if self.session_id is None:
            self.session_id = f"session_{self.user_id}_{int(datetime.now().timestamp())}"
        if self.history is None:
            self.history = MessageHistory()
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()
    
    def add_user_message(self, content: str, metadata: Optional[Dict] = None) -> Message:
        """Add user message to session."""
        msg = Message(role="user", content=content, metadata=metadata)
        self.history.messages.append(msg)
        self.last_active = datetime.now()
        return msg
    
    def add_assistant_message(self, content: str, metadata: Optional[Dict] = None) -> Message:
        """Add assistant message to session."""
        msg = Message(role="assistant", content=content, metadata=metadata)
        self.history.messages.append(msg)
        self.last_active = datetime.now()
        return msg


@dataclass
class ConversationContext:
    """
    Extracted context from conversation history.

    Provides structured information about what's been discussed.
    """
    last_topic: Optional[str] = None
    last_equipment_type: Optional[str] = None
    last_intent_type: Optional[str] = None
    mentioned_equipment: List[str] = None
    unresolved_issues: List[str] = None
    follow_up_count: int = 0

    def __post_init__(self):
        if self.mentioned_equipment is None:
            self.mentioned_equipment = []
        if self.unresolved_issues is None:
            self.unresolved_issues = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationContext":
        """Load from dictionary"""
        return cls(**data)


class ConversationManager:
    """
    Manages conversation sessions for Telegram users.

    Features:
    - Session persistence across bot restarts
    - Conversation history with context window
    - Context extraction for intelligent responses
    - Automatic session cleanup (old sessions)

    Usage:
        >>> manager = ConversationManager()
        >>> session = manager.get_or_create_session(user_id="123")
        >>> manager.add_user_message(session, "Motor running hot")
        >>> manager.add_bot_message(session, "Let me help diagnose that...")
        >>> context = manager.get_context(session)
        >>> print(context.last_topic)  # "motor overheating"
    """

    def __init__(self, db = None):
        """
        Initialize conversation manager.

        Args:
            db: Database instance. If None, uses in-memory storage.
        """
        self.db = db
        self.active_sessions: Dict[str, Session] = {}  # In-memory cache
        self.context_window_size = 10  # Last N messages to include in context

    def get_or_create_session(self, user_id: str, telegram_username: Optional[str] = None) -> Session:
        """
        Get existing session or create new one for user.

        Args:
            user_id: Telegram user ID (as string)
            telegram_username: Optional username for new sessions

        Returns:
            Session instance with conversation history
        """
        # Check in-memory cache first
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            session.last_active = datetime.now()
            return session

        # Try to load from database if available
        session = None
        if self.db:
            session = self._load_session_from_db(user_id)

        if session is None:
            # Create new session
            session = Session(
                user_id=user_id,
                metadata={
                    "telegram_username": telegram_username,
                    "created_via": "telegram_bot",
                    "platform": "telegram"
                }
            )

        # Cache it
        self.active_sessions[user_id] = session
        return session

    def add_user_message(
        self,
        session: Session,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Add user message to session.

        Args:
            session: Conversation session
            content: Message text from user
            metadata: Optional metadata (intent, equipment info, etc.)

        Returns:
            Created Message object
        """
        msg = session.add_user_message(content, metadata)
        self._update_context(session)
        return msg

    def add_bot_message(
        self,
        session: Session,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Add bot response message to session.

        Args:
            session: Conversation session
            content: Bot's response text
            metadata: Optional metadata (confidence, atoms used, etc.)

        Returns:
            Created Message object
        """
        msg = session.add_assistant_message(content, metadata)
        return msg

    def get_context(self, session: Session) -> ConversationContext:
        """
        Extract structured context from conversation history.

        Analyzes recent messages to understand:
        - What was last discussed
        - Equipment mentioned
        - Unresolved issues
        - Follow-up patterns

        Args:
            session: Conversation session

        Returns:
            ConversationContext with extracted information
        """
        # Get recent messages
        recent_messages = session.history.get_messages(limit=self.context_window_size)

        if not recent_messages:
            return ConversationContext()

        # Extract context from messages
        context = ConversationContext()

        for msg in recent_messages:
            if msg.role == "user":
                # Extract equipment mentions
                equipment_keywords = ["motor", "vfd", "plc", "conveyor", "pump", "valve", "sensor"]
                for keyword in equipment_keywords:
                    if keyword in msg.content.lower() and keyword not in context.mentioned_equipment:
                        context.mentioned_equipment.append(keyword)

                # Check for follow-up indicators
                follow_up_phrases = ["what about", "tell me more", "can you explain", "how do i", "also"]
                if any(phrase in msg.content.lower() for phrase in follow_up_phrases):
                    context.follow_up_count += 1

            # Get metadata from messages
            if msg.metadata:
                if "intent_type" in msg.metadata:
                    context.last_intent_type = msg.metadata["intent_type"]
                if "equipment_type" in msg.metadata:
                    context.last_equipment_type = msg.metadata["equipment_type"]
                if "topic" in msg.metadata:
                    context.last_topic = msg.metadata["topic"]

        # Last user message is current topic
        last_user_msgs = [m for m in recent_messages if m.role == "user"]
        if last_user_msgs:
            last_content = last_user_msgs[-1].content
            # Simple topic extraction (first few words)
            words = last_content.lower().split()[:5]
            context.last_topic = " ".join(words)

        return context

    def get_context_window(self, session: Session, n: Optional[int] = None) -> List[Message]:
        """
        Get last N messages for context.

        Args:
            session: Conversation session
            n: Number of messages. If None, uses context_window_size

        Returns:
            List of recent messages
        """
        limit = n or self.context_window_size
        return session.history.get_messages(limit=limit)

    def get_context_summary(self, session: Session) -> str:
        """
        Generate natural language summary of conversation context.

        Useful for passing to LLM for context-aware responses.

        Args:
            session: Conversation session

        Returns:
            Human-readable context summary
        """
        context = self.get_context(session)
        recent_messages = self.get_context_window(session, n=5)

        summary_parts = []

        # Conversation length
        total_messages = len(session.history.messages)
        if total_messages > 0:
            summary_parts.append(f"Conversation has {total_messages} messages.")

        # Recent topic
        if context.last_topic:
            summary_parts.append(f"User is asking about: {context.last_topic}")

        # Equipment context
        if context.mentioned_equipment:
            equipment_str = ", ".join(context.mentioned_equipment)
            summary_parts.append(f"Equipment mentioned: {equipment_str}")

        # Follow-up indicator
        if context.follow_up_count > 0:
            summary_parts.append(f"This is a follow-up question (count: {context.follow_up_count})")

        # Recent exchange
        if recent_messages:
            summary_parts.append("\nRecent exchange:")
            for msg in recent_messages[-3:]:  # Last 3 messages
                role = "User" if msg.role == "user" else "Bot"
                content_preview = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
                summary_parts.append(f"{role}: {content_preview}")

        return "\n".join(summary_parts) if summary_parts else "No previous conversation context."

    def save_session(self, session: Session) -> bool:
        """
        Persist session to database.

        Args:
            session: Session to save

        Returns:
            True if successful, False otherwise
        """
        if not self.db:
            return False
            
        try:
            # Implementation would depend on database interface
            return True

        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def _load_session_from_db(self, user_id: str) -> Optional[Session]:
        """Load session from database"""
        if not self.db:
            return None
            
        try:
            # Implementation would depend on database interface
            return None

        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def _update_context(self, session: Session):
        """Update session metadata with current context"""
        context = self.get_context(session)
        session.metadata["context"] = context.to_dict()
        session.metadata["last_update"] = datetime.now().isoformat()

    def cleanup_old_sessions(self, days: int = 30):
        """
        Remove sessions older than N days.

        Args:
            days: Age threshold in days
        """
        try:
            cutoff = datetime.now() - timedelta(days=days)
            if self.db:
                # Database cleanup would go here
                pass
                
            # Also clear from memory cache
            expired_users = [
                user_id for user_id, session in self.active_sessions.items()
                if session.last_active < cutoff
            ]
            for user_id in expired_users:
                del self.active_sessions[user_id]

        except Exception as e:
            print(f"Error cleaning up sessions: {e}")