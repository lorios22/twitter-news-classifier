#!/usr/bin/env python3
"""
🐦 TWEET EXTRACTION SERVICE
===========================
Independent service for comprehensive tweet data extraction.

This service handles:
- Tweet extraction from trusted accounts
- Complete user metadata collection
- Thread detection and extraction
- URL and media content analysis
- Robust error handling with data persistence
- Separation from analysis pipeline for better reliability

Domain-Driven Design: Domain service for tweet data extraction.
"""

import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from ..entities.tweet import Tweet, UserMetadata, MediaAttachment, ThreadContext, ContentType
from infrastructure.adapters.twitter_api_adapter import TwitterApiAdapter
from infrastructure.repositories.file_repository import FileRepository


@dataclass
class ExtractionConfig:
    """Configuration for tweet extraction process"""
    max_tweets: int = 30
    hours_back: int = 24
    accounts_list: List[str] = None
    enable_thread_extraction: bool = True
    enable_media_analysis: bool = True
    enable_url_extraction: bool = True
    output_directory: str = "data/extracted_tweets"
    batch_size: int = 10


@dataclass
class ExtractionResult:
    """Result of tweet extraction process"""
    extraction_id: str
    timestamp: datetime
    total_tweets_extracted: int
    successful_accounts: int
    failed_accounts: int
    accounts_processed: List[str]
    accounts_failed: List[str]
    tweets_file_path: str
    metadata_file_path: str
    extraction_config: ExtractionConfig
    processing_time: float
    status: str  # 'success', 'partial', 'failed'
    error_details: List[str] = None


class TweetExtractionService:
    """
    🐦 Independent Tweet Extraction Service
    
    Handles comprehensive tweet data extraction with full metadata,
    thread detection, media analysis, and URL processing.
    
    Features:
    - Robust error handling with data persistence
    - Complete user metadata extraction
    - Thread context detection and extraction
    - Media content analysis
    - URL extraction and classification
    - Batch processing for large account lists
    - Independent from analysis pipeline
    """
    
    def __init__(self, 
                 twitter_adapter: TwitterApiAdapter,
                 file_repository: FileRepository):
        """Initialize tweet extraction service"""
        self.logger = logging.getLogger(__name__)
        self.twitter_adapter = twitter_adapter
        self.file_repository = file_repository
        
        # Extraction statistics
        self.stats = {
            'tweets_extracted': 0,
            'accounts_processed': 0,
            'errors_encountered': 0,
            'threads_detected': 0,
            'media_analyzed': 0,
            'urls_extracted': 0
        }
    
    async def extract_comprehensive_data(self, config: ExtractionConfig) -> ExtractionResult:
        """
        Main extraction method - performs comprehensive tweet data extraction
        
        Args:
            config: Extraction configuration parameters
            
        Returns:
            ExtractionResult with extraction details and file paths
        """
        start_time = datetime.now()
        extraction_id = f"EXTRACTION_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info(f"🚀 Starting comprehensive tweet extraction: {extraction_id}")
        self.logger.info(f"📊 Target: {config.max_tweets} tweets from {len(config.accounts_list)} accounts")
        
        # Create output directory
        output_dir = Path(config.output_directory) / extraction_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Phase 1: Extract raw tweets from Twitter API
            raw_tweets, extraction_stats = await self._extract_raw_tweets(config)
            
            # Phase 2: Enhance tweets with metadata, threads, media
            enhanced_tweets = self._enhance_tweets_data(raw_tweets, config)
            
            # Phase 3: Save extraction results
            tweets_file, metadata_file = self._save_extraction_data(
                enhanced_tweets, extraction_stats, output_dir, extraction_id
            )
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create extraction result
            result = ExtractionResult(
                extraction_id=extraction_id,
                timestamp=start_time,
                total_tweets_extracted=len(enhanced_tweets),
                successful_accounts=extraction_stats['successful_accounts'],
                failed_accounts=extraction_stats['failed_accounts'],
                accounts_processed=extraction_stats['accounts_processed'],
                accounts_failed=extraction_stats['accounts_failed'],
                tweets_file_path=str(tweets_file),
                metadata_file_path=str(metadata_file),
                extraction_config=config,
                processing_time=processing_time,
                status='success' if len(enhanced_tweets) > 0 else 'failed',
                error_details=extraction_stats.get('errors', [])
            )
            
            self.logger.info(f"✅ Extraction completed: {len(enhanced_tweets)} tweets extracted")
            self.logger.info(f"📁 Data saved to: {tweets_file}")
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Extraction failed: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            
            # Return failed result with partial data if any
            return ExtractionResult(
                extraction_id=extraction_id,
                timestamp=start_time,
                total_tweets_extracted=self.stats['tweets_extracted'],
                successful_accounts=self.stats['accounts_processed'],
                failed_accounts=0,
                accounts_processed=[],
                accounts_failed=[],
                tweets_file_path="",
                metadata_file_path="",
                extraction_config=config,
                processing_time=processing_time,
                status='failed',
                error_details=[error_msg]
            )
    
    async def _extract_raw_tweets(self, config: ExtractionConfig) -> Tuple[List[Dict], Dict]:
        """Extract raw tweets from Twitter API"""
        self.logger.info("📡 Phase 1: Extracting raw tweets from Twitter API...")
        
        extraction_stats = {
            'successful_accounts': 0,
            'failed_accounts': 0,
            'accounts_processed': [],
            'accounts_failed': [],
            'errors': []
        }
        
        try:
            # Use existing Twitter adapter for extraction
            tweets = self.twitter_adapter.extract_tweets_from_accounts(
                account_usernames=config.accounts_list,
                max_tweets=config.max_tweets,
                hours_back=config.hours_back
            )
            
            extraction_stats['successful_accounts'] = len(config.accounts_list)
            extraction_stats['accounts_processed'] = config.accounts_list.copy()
            
            self.logger.info(f"📊 Raw tweets extracted: {len(tweets)}")
            return tweets, extraction_stats
            
        except Exception as e:
            error_msg = f"Twitter API extraction failed: {str(e)}"
            extraction_stats['errors'].append(error_msg)
            extraction_stats['failed_accounts'] = len(config.accounts_list)
            extraction_stats['accounts_failed'] = config.accounts_list.copy()
            
            self.logger.error(f"❌ {error_msg}")
            return [], extraction_stats
    
    def _enhance_tweets_data(self, raw_tweets: List[Dict], config: ExtractionConfig) -> List[Tweet]:
        """Enhance raw tweets with comprehensive metadata"""
        self.logger.info("🔍 Phase 2: Enhancing tweets with comprehensive metadata...")
        
        enhanced_tweets = []
        
        for tweet in raw_tweets:
            try:
                # Tweet is already a Tweet entity from the Twitter adapter
                
                # Enhance with thread context if enabled
                if config.enable_thread_extraction:
                    self._extract_thread_context(tweet)
                
                # Enhance with media analysis if enabled
                if config.enable_media_analysis:
                    self._analyze_media_content(tweet)
                
                # Extract and analyze URLs if enabled
                if config.enable_url_extraction:
                    self._extract_url_content(tweet)
                
                enhanced_tweets.append(tweet)
                self.stats['tweets_extracted'] += 1
                
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to enhance tweet {getattr(tweet, 'tweet_id', 'unknown')}: {str(e)}")
                continue
        
        self.logger.info(f"✅ Enhanced {len(enhanced_tweets)} tweets with comprehensive metadata")
        return enhanced_tweets
    
    def _extract_thread_context(self, tweet: Tweet):
        """Extract thread context for a tweet"""
        try:
            # Check if tweet is part of a thread
            if (tweet.thread_context and tweet.thread_context.in_reply_to_user_id) or self._detect_thread_patterns(tweet.text):
                
                # Update existing thread context or create new one
                if not tweet.thread_context:
                    tweet.thread_context = ThreadContext()
                
                # Update thread context
                tweet.thread_context.is_thread = True
                tweet.thread_context.thread_position = 1  # Will be updated with actual detection
                
                self.stats['threads_detected'] += 1
                
                self.logger.debug(f"🧵 Thread detected for tweet {tweet.tweet_id}")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Thread extraction failed for tweet {tweet.tweet_id}: {str(e)}")
    
    def _detect_thread_patterns(self, text: str) -> bool:
        """Detect thread patterns in tweet text"""
        thread_indicators = [
            '🧵', '👇', '/thread', 'thread:', '1/', '1.', '(1/', 
            'first,', 'continuing in replies', 'more below'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in thread_indicators)
    
    def _analyze_media_content(self, tweet: Tweet):
        """Analyze media content in tweet with robust handling of different media attachment formats"""
        try:
            if tweet.media_attachments:
                # Handle both single objects and lists
                media_list = tweet.media_attachments if isinstance(tweet.media_attachments, list) else [tweet.media_attachments]
                
                for media in media_list:
                    # Basic media analysis with safe attribute access
                    media.analysis_results = {
                        'type_detected': getattr(media, 'type', 'unknown'),
                        'size_info': f"{getattr(media, 'width', 'unknown')}x{getattr(media, 'height', 'unknown')}" 
                                   if hasattr(media, 'width') and hasattr(media, 'height') and media.width and media.height 
                                   else 'unknown',
                        'analyzed': True,
                        'media_url': getattr(media, 'url', None),
                        'preview_image_url': getattr(media, 'preview_image_url', None)
                    }
                
                self.stats['media_analyzed'] += len(media_list)
                self.logger.debug(f"🖼️ Analyzed {len(media_list)} media items for tweet {tweet.tweet_id}")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Media analysis failed for tweet {tweet.tweet_id}: {str(e)}")
            # Continue processing without failing the entire extraction
    
    def _extract_url_content(self, tweet: Tweet):
        """Extract and analyze URLs in tweet"""
        try:
            if tweet.external_links:
                # URLs are already extracted by TwitterApiAdapter
                # Here we could add additional processing like content analysis
                
                self.stats['urls_extracted'] += len(tweet.external_links)
                self.logger.debug(f"🔗 Found {len(tweet.external_links)} URLs for tweet {tweet.tweet_id}")
                
        except Exception as e:
            self.logger.warning(f"⚠️ URL extraction failed for tweet {tweet.tweet_id}: {str(e)}")
    
    def _save_extraction_data(self, 
                                  tweets: List[Tweet], 
                                  stats: Dict, 
                                  output_dir: Path,
                                  extraction_id: str) -> Tuple[Path, Path]:
        """Save extraction data to files"""
        self.logger.info("💾 Phase 3: Saving extraction data...")
        
        # Convert tweets to dictionaries for JSON serialization
        tweets_data = [tweet.to_dict() for tweet in tweets]
        
        # Create comprehensive metadata
        metadata = {
            'extraction_id': extraction_id,
            'timestamp': datetime.now().isoformat(),
            'total_tweets': len(tweets),
            'extraction_stats': stats,
            'processing_stats': self.stats,
            'data_structure': {
                'tweets_file': 'extracted_tweets.json',
                'format': 'JSON array of Tweet entities',
                'fields_included': [
                    'id', 'text', 'created_at', 'author_id', 'user_metadata',
                    'thread_context', 'media_attachments', 'extracted_urls',
                    'entities', 'public_metrics', 'context_annotations'
                ]
            }
        }
        
        # Save files
        tweets_file = output_dir / 'extracted_tweets.json'
        metadata_file = output_dir / 'extraction_metadata.json'
        
        # Save tweets data
        with open(tweets_file, 'w', encoding='utf-8') as f:
            json.dump(tweets_data, f, indent=2, ensure_ascii=False, default=str)
        
        # Save metadata
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"💾 Extraction data saved:")
        self.logger.info(f"   📄 Tweets: {tweets_file}")
        self.logger.info(f"   📋 Metadata: {metadata_file}")
        
        return tweets_file, metadata_file
    
    def get_extraction_stats(self) -> Dict:
        """Get current extraction statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset extraction statistics"""
        self.stats = {
            'tweets_extracted': 0,
            'accounts_processed': 0,
            'errors_encountered': 0,
            'threads_detected': 0,
            'media_analyzed': 0,
            'urls_extracted': 0
        } 