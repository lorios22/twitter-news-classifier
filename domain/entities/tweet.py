#!/usr/bin/env python3
"""
🐦 TWEET ENTITY
==============
Core domain entity representing a social media tweet.

Domain-Driven Design: Core domain entity with business logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Any
from enum import Enum


class ContentType(Enum):
    """Content type classification"""
    ANNOUNCEMENT = "announcement"
    ANALYSIS = "analysis"
    NEWS = "news"
    DISCUSSION = "discussion"
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional"
    OTHER = "other"


@dataclass
class UserMetadata:
    """User metadata information"""
    user_id: str
    username: str
    display_name: str
    created_at: datetime
    description: str
    verified: bool
    profile_image_url: str
    public_metrics: Dict[str, int]


@dataclass
class MediaAttachment:
    """Media attachment information"""
    links_analyzed: List[Dict[str, Any]] = field(default_factory=list)
    images_analyzed: List[Dict[str, Any]] = field(default_factory=list)
    total_processing_time: float = 0.0
    summary: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreadContext:
    """Thread context information"""
    conversation_id: Optional[str] = None
    is_thread: bool = False
    in_reply_to_user_id: Optional[str] = None
    thread_position: Optional[int] = None


@dataclass
class Tweet:
    """
    🐦 Core Tweet entity representing social media content
    
    Contains all tweet information including metadata, content,
    and analysis context for comprehensive processing.
    """
    
    # Core tweet data
    tweet_id: str
    text: str
    created_at: datetime
    author_username: str
    author_id: str
    
    # Engagement metrics
    like_count: int = 0
    retweet_count: int = 0
    reply_count: int = 0
    quote_count: int = 0
    
    # Rich metadata
    user_metadata: Optional[UserMetadata] = None
    media_attachments: Optional[MediaAttachment] = None
    external_links: List[str] = field(default_factory=list)
    thread_context: Optional[ThreadContext] = None
    conversation_context: Optional[Dict[str, Any]] = None
    
    # Analysis metadata
    content_type: Optional[ContentType] = None
    processing_timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.processing_timestamp is None:
            self.processing_timestamp = datetime.now()
    
    @property
    def engagement_score(self) -> float:
        """Calculate engagement score based on metrics"""
        total_engagement = self.like_count + self.retweet_count + self.reply_count + self.quote_count
        return min(10.0, total_engagement / 100.0)  # Normalized to 0-10 scale
    
    @property
    def has_media(self) -> bool:
        """Check if tweet has media attachments"""
        if not self.media_attachments:
            return False
        return (len(self.media_attachments.links_analyzed) > 0 or 
                len(self.media_attachments.images_analyzed) > 0)
    
    @property
    def is_thread_tweet(self) -> bool:
        """Check if tweet is part of a thread"""
        return self.thread_context is not None and self.thread_context.is_thread
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tweet to dictionary representation"""
        return {
            "tweet_id": self.tweet_id,
            "text": self.text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "author_username": self.author_username,
            "author_id": self.author_id,
            "like_count": self.like_count,
            "retweet_count": self.retweet_count,
            "reply_count": self.reply_count,
            "quote_count": self.quote_count,
            "user_metadata": self.user_metadata.__dict__ if self.user_metadata else None,
            "media_attachments": self.media_attachments.__dict__ if self.media_attachments else None,
            "external_links": self.external_links,
            "thread_context": self.thread_context.__dict__ if self.thread_context else None,
            "conversation_context": self.conversation_context,
            "content_type": self.content_type.value if self.content_type else None,
            "processing_timestamp": self.processing_timestamp.isoformat() if self.processing_timestamp else None,
            "engagement_score": self.engagement_score,
            "has_media": self.has_media,
            "is_thread_tweet": self.is_thread_tweet
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tweet':
        """Create Tweet from dictionary representation"""
        # Convert datetime strings back to datetime objects
        created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now()
        processing_timestamp = datetime.fromisoformat(data['processing_timestamp']) if data.get('processing_timestamp') else None
        
        # Convert user metadata
        user_metadata = None
        if data.get('user_metadata'):
            user_data = data['user_metadata']
            user_created_at = datetime.fromisoformat(user_data['created_at']) if user_data.get('created_at') else datetime.now()
            user_metadata = UserMetadata(
                user_id=user_data.get('user_id', ''),
                username=user_data.get('username', ''),
                display_name=user_data.get('display_name', ''),
                created_at=user_created_at,
                description=user_data.get('description', ''),
                verified=user_data.get('verified', False),
                profile_image_url=user_data.get('profile_image_url', ''),
                public_metrics=user_data.get('public_metrics', {})
            )
        
        # Convert media attachments
        media_attachments = None
        if data.get('media_attachments'):
            media_data = data['media_attachments']
            media_attachments = MediaAttachment(
                links_analyzed=media_data.get('links_analyzed', []),
                images_analyzed=media_data.get('images_analyzed', []),
                total_processing_time=media_data.get('total_processing_time', 0.0),
                summary=media_data.get('summary', {})
            )
        
        # Convert thread context
        thread_context = None
        if data.get('thread_context'):
            thread_data = data['thread_context']
            thread_context = ThreadContext(
                conversation_id=thread_data.get('conversation_id'),
                is_thread=thread_data.get('is_thread', False),
                in_reply_to_user_id=thread_data.get('in_reply_to_user_id'),
                thread_position=thread_data.get('thread_position')
            )
        
        # Convert content type
        content_type = None
        if data.get('content_type'):
            try:
                content_type = ContentType(data['content_type'])
            except ValueError:
                content_type = ContentType.OTHER
        
        return cls(
            tweet_id=data.get('tweet_id', ''),
            text=data.get('text', ''),
            created_at=created_at,
            author_username=data.get('author_username', ''),
            author_id=data.get('author_id', ''),
            like_count=data.get('like_count', 0),
            retweet_count=data.get('retweet_count', 0),
            reply_count=data.get('reply_count', 0),
            quote_count=data.get('quote_count', 0),
            user_metadata=user_metadata,
            media_attachments=media_attachments,
            external_links=data.get('external_links', []),
            thread_context=thread_context,
            conversation_context=data.get('conversation_context'),
            content_type=content_type,
            processing_timestamp=processing_timestamp
        ) 