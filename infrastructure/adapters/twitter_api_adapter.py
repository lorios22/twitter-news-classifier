#!/usr/bin/env python3
"""
🐦 TWITTER API ADAPTER
=====================
Infrastructure adapter for Twitter API integration.

Domain-Driven Design: Infrastructure layer adapter for external services.
Handles all Twitter API communication and data transformation.
"""

import os
import time
import tweepy
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from domain.entities.tweet import Tweet, UserMetadata, MediaAttachment, ThreadContext


@dataclass
class TwitterApiConfig:
    """Twitter API configuration"""
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
    bearer_token: str


class TwitterApiAdapter:
    """
    🐦 Twitter API adapter for external service integration
    
    Handles all Twitter API communication including:
    - Tweet extraction from specific accounts
    - User metadata retrieval
    - Media attachment processing
    - Thread conversation extraction
    - Rate limiting and error handling
    """
    
    def __init__(self, config: TwitterApiConfig):
        """Initialize Twitter API adapter with configuration"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize Twitter API client with comprehensive authentication
        self.client = tweepy.Client(
            bearer_token=config.bearer_token,
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            access_token=config.access_token,
            access_token_secret=config.access_token_secret,
            wait_on_rate_limit=True
        )
        
        # Comprehensive tweet fields for maximum data extraction
        self.tweet_fields = [
            'id', 'text', 'created_at', 'author_id', 'conversation_id',
            'in_reply_to_user_id', 'public_metrics', 'context_annotations',
            'entities', 'geo', 'lang', 'possibly_sensitive', 'referenced_tweets',
            'reply_settings', 'source', 'withheld'
        ]
        
        # Comprehensive user fields
        self.user_fields = [
            'id', 'name', 'username', 'created_at', 'description', 'entities',
            'location', 'pinned_tweet_id', 'profile_image_url', 'protected',
            'public_metrics', 'url', 'verified', 'withheld'
        ]
        
        # Media fields for attachments
        self.media_fields = [
            'duration_ms', 'height', 'media_key', 'preview_image_url',
            'type', 'url', 'width', 'public_metrics', 'alt_text'
        ]
        
        # Expansions for comprehensive data
        self.expansions = [
            'author_id', 'referenced_tweets.id', 'referenced_tweets.id.author_id',
            'entities.mentions.username', 'attachments.poll_ids',
            'attachments.media_keys', 'in_reply_to_user_id', 'geo.place_id'
        ]
    
    @classmethod
    def from_env(cls) -> 'TwitterApiAdapter':
        """Create adapter from environment variables"""
        config = TwitterApiConfig(
            consumer_key=os.getenv('TWITTER_API_KEY', ''),
            consumer_secret=os.getenv('TWITTER_API_SECRET', ''),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN', ''),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET', ''),
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN', '')
        )
        return cls(config)
    
    def extract_tweets_from_accounts(self, account_usernames: List[str], 
                                   max_tweets: int = 30,
                                   hours_back: int = 24) -> List[Tweet]:
        """
        Extract tweets from specified accounts
        
        Args:
            account_usernames: List of Twitter usernames (without @)
            max_tweets: Maximum number of tweets to extract
            hours_back: How many hours back to search
            
        Returns:
            List of Tweet entities
        """
        self.logger.info(f"🐦 Starting tweet extraction from {len(account_usernames)} accounts")
        self.logger.info(f"🎯 Target: {max_tweets} tweets from last {hours_back} hours")
        
        tweets = []
        # Smart distribution: ensure we get enough tweets while respecting API limits
        # For 48 accounts and 30 tweets target: extract 5-10 tweets per account until we reach target
        tweets_per_account = max(5, min(10, (max_tweets * 2) // len(account_usernames)))  # Oversampling
        
        # Calculate time boundary - format for RFC3339 compliance (no microseconds)
        since_time = datetime.now() - timedelta(hours=hours_back)
        since_time = since_time.replace(microsecond=0)  # Remove microseconds for RFC3339
        
        self.logger.info(f"📊 Strategy: {tweets_per_account} tweets per account, targeting {max_tweets} total")
        
        accounts_processed = 0
        successful_extractions = 0
        
        for username in account_usernames:
            try:
                self.logger.info(f"📥 Extracting from @{username} ({accounts_processed + 1}/{len(account_usernames)})...")
                
                # Add small delay to be respectful to API
                if accounts_processed > 0 and accounts_processed % 10 == 0:
                    self.logger.info(f"⏸️ Brief pause after {accounts_processed} accounts...")
                    time.sleep(2)
                
                # Get user information first
                user_response = self.client.get_user(
                    username=username,
                    user_fields=self.user_fields
                )
                
                if not user_response.data:
                    self.logger.warning(f"❌ User @{username} not found")
                    accounts_processed += 1
                    continue
                
                user = user_response.data
                
                # Get user's recent tweets
                tweets_response = self.client.get_users_tweets(
                    id=user.id,
                    max_results=min(tweets_per_account, 100),  # API limit is 100, minimum 5
                    tweet_fields=self.tweet_fields,
                    user_fields=self.user_fields,
                    media_fields=self.media_fields,
                    expansions=self.expansions,
                    exclude=['retweets', 'replies'],  # Only original content
                    start_time=since_time.isoformat() + 'Z'  # RFC3339 with Z suffix
                )
                
                if not tweets_response.data:
                    self.logger.info(f"📭 No recent tweets found for @{username}")
                    accounts_processed += 1
                    continue
                
                # Process tweets
                account_tweets_added = 0
                for tweet_data in tweets_response.data:
                    if len(tweets) >= max_tweets:
                        break
                    
                    tweet = self._convert_to_tweet_entity(tweet_data, user, tweets_response)
                    tweets.append(tweet)
                    account_tweets_added += 1
                    
                self.logger.info(f"✅ Added {account_tweets_added} tweets from @{username}")
                successful_extractions += 1
                accounts_processed += 1
                
            except tweepy.TooManyRequests:
                self.logger.warning(f"⏸️ Rate limit reached at account @{username}. Stopping extraction.")
                break
            except Exception as e:
                self.logger.error(f"❌ Error extracting from @{username}: {str(e)}")
                accounts_processed += 1
                continue
            
            if len(tweets) >= max_tweets:
                self.logger.info(f"🎯 Target of {max_tweets} tweets reached!")
                break
        
        self.logger.info(f"🎉 Extraction complete: {len(tweets)} tweets from {successful_extractions}/{accounts_processed} accounts")
        return tweets[:max_tweets]
    
    def _convert_to_tweet_entity(self, tweet_data: Any, user_data: Any, 
                               response_includes: Any) -> Tweet:
        """Convert Twitter API response to Tweet entity"""
        
        # Extract user metadata
        user_metadata = UserMetadata(
            user_id=str(user_data.id),
            username=user_data.username,
            display_name=user_data.name,
            created_at=user_data.created_at,
            description=user_data.description or "",
            verified=user_data.verified or False,
            profile_image_url=user_data.profile_image_url or "",
            public_metrics=user_data.public_metrics or {}
        )
        
        # Extract media attachments
        media_attachments = self._extract_media_attachments(tweet_data, response_includes)
        
        # Extract external links
        external_links = self._extract_external_links(tweet_data)
        
        # Extract thread context
        thread_context = ThreadContext(
            conversation_id=str(tweet_data.conversation_id) if tweet_data.conversation_id else None,
            is_thread=tweet_data.conversation_id != tweet_data.id,
            in_reply_to_user_id=str(tweet_data.in_reply_to_user_id) if tweet_data.in_reply_to_user_id else None
        )
        
        # Get public metrics
        metrics = tweet_data.public_metrics or {}
        
        return Tweet(
            tweet_id=str(tweet_data.id),
            text=tweet_data.text,
            created_at=tweet_data.created_at,
            author_username=user_data.username,
            author_id=str(user_data.id),
            like_count=metrics.get('like_count', 0),
            retweet_count=metrics.get('retweet_count', 0),
            reply_count=metrics.get('reply_count', 0),
            quote_count=metrics.get('quote_count', 0),
            user_metadata=user_metadata,
            media_attachments=media_attachments,
            external_links=external_links,
            thread_context=thread_context
        )
    
    def _extract_media_attachments(self, tweet_data: Any, response_includes: Any) -> MediaAttachment:
        """Extract media attachments from tweet data"""
        media_attachment = MediaAttachment()
        
        # Extract images and videos
        if hasattr(response_includes, 'media') and response_includes.media:
            for media in response_includes.media:
                if media.type in ['photo', 'video', 'animated_gif']:
                    media_info = {
                        'type': media.type,
                        'url': media.url or media.preview_image_url,
                        'width': getattr(media, 'width', None),
                        'height': getattr(media, 'height', None),
                        'alt_text': getattr(media, 'alt_text', '')
                    }
                    if media.type == 'photo':
                        media_attachment.images_analyzed.append(media_info)
        
        # Set summary
        media_attachment.summary = {
            'total_links_found': len(media_attachment.links_analyzed),
            'total_images_found': len(media_attachment.images_analyzed),
            'links_successfully_analyzed': len(media_attachment.links_analyzed),
            'images_successfully_analyzed': len(media_attachment.images_analyzed),
            'has_external_content': len(media_attachment.links_analyzed) > 0 or len(media_attachment.images_analyzed) > 0,
            'analysis_complete': True
        }
        
        return media_attachment
    
    def _extract_external_links(self, tweet_data: Any) -> List[str]:
        """Extract external links from tweet entities"""
        links = []
        
        if hasattr(tweet_data, 'entities') and tweet_data.entities:
            if hasattr(tweet_data.entities, 'urls') and tweet_data.entities.urls:
                for url_entity in tweet_data.entities.urls:
                    if hasattr(url_entity, 'expanded_url'):
                        links.append(url_entity.expanded_url)
                    elif hasattr(url_entity, 'url'):
                        links.append(url_entity.url)
        
        return links
    
    def get_conversation_tweets(self, conversation_id: str, max_tweets: int = 10) -> List[Dict[str, Any]]:
        """
        Get tweets from a conversation thread
        
        Args:
            conversation_id: Twitter conversation ID
            max_tweets: Maximum tweets to retrieve
            
        Returns:
            List of tweet dictionaries
        """
        try:
            # Search for tweets in the conversation
            query = f"conversation_id:{conversation_id}"
            
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_tweets, 100),
                tweet_fields=self.tweet_fields,
                user_fields=self.user_fields,
                expansions=self.expansions
            )
            
            if not response.data:
                return []
            
            # Convert to simple dictionaries
            thread_tweets = []
            for tweet in response.data:
                thread_tweets.append({
                    'id': str(tweet.id),
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                    'author_id': str(tweet.author_id),
                    'public_metrics': tweet.public_metrics or {}
                })
            
            return thread_tweets
            
        except Exception as e:
            self.logger.error(f"❌ Error getting conversation {conversation_id}: {str(e)}")
            return []
    
    def test_connection(self) -> bool:
        """Test Twitter API connection"""
        try:
            response = self.client.get_me()
            if response.data:
                self.logger.info(f"✅ Twitter API connection successful: @{response.data.username}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Twitter API connection failed: {str(e)}")
            return False 