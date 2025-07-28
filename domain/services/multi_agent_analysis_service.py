#!/usr/bin/env python3
"""
🤖 MULTI-AGENT ANALYSIS SERVICE
===============================
Service for processing pre-extracted tweet data through multi-agent analysis.

This service handles:
- Loading pre-extracted tweet data
- Processing through 12 specialized AI agents
- Robust error handling with retry logic
- Separation from extraction pipeline
- Integration of analysis results with input data

Domain-Driven Design: Application service for multi-agent analysis.
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from ..entities.tweet import Tweet
from ..entities.analysis_result import AnalysisResult, AnalysisStatus, QualityLevel
from .multi_agent_analyzer import MultiAgentAnalyzer
from infrastructure.repositories.file_repository import FileRepository


@dataclass
class AnalysisConfig:
    """Configuration for multi-agent analysis process"""
    input_tweets_file: str
    output_directory: str = "results/analysis"
    max_retries: int = 3
    retry_delay: int = 30  # seconds
    batch_size: int = 5
    enable_error_recovery: bool = True
    continue_on_failure: bool = True
    save_intermediate_results: bool = True


@dataclass
class AnalysisResult:
    """Result of multi-agent analysis process"""
    analysis_id: str
    timestamp: datetime
    input_tweets_file: str
    total_tweets_processed: int
    successful_analyses: int
    failed_analyses: int
    tweets_analyzed: List[str]
    tweets_failed: List[str]
    results_file_path: str
    summary_file_path: str
    analysis_config: AnalysisConfig
    processing_time: float
    status: str  # 'success', 'partial', 'failed'
    error_details: List[str] = None
    agent_performance: Dict[str, Any] = None


class MultiAgentAnalysisService:
    """
    🤖 Multi-Agent Analysis Service
    
    Processes pre-extracted tweet data through comprehensive multi-agent analysis.
    
    Features:
    - Robust error handling with retry logic
    - Batch processing for large datasets
    - Intermediate result saving
    - API failure recovery
    - Comprehensive result integration
    - Independent from extraction pipeline
    """
    
    def __init__(self, 
                 multi_agent_analyzer: MultiAgentAnalyzer,
                 file_repository: FileRepository):
        """Initialize multi-agent analysis service"""
        self.logger = logging.getLogger(__name__)
        self.analyzer = multi_agent_analyzer
        self.file_repository = file_repository
        
        # Analysis statistics
        self.stats = {
            'tweets_processed': 0,
            'successful_analyses': 0,
            'failed_analyses': 0,
            'api_errors': 0,
            'retries_attempted': 0,
            'agent_calls': 0
        }
    
    async def analyze_extracted_data(self, config: AnalysisConfig) -> AnalysisResult:
        """
        Main analysis method - processes pre-extracted tweet data
        
        Args:
            config: Analysis configuration parameters
            
        Returns:
            AnalysisResult with analysis details and file paths
        """
        start_time = datetime.now()
        analysis_id = f"ANALYSIS_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info(f"🚀 Starting multi-agent analysis: {analysis_id}")
        self.logger.info(f"📂 Input file: {config.input_tweets_file}")
        
        # Create output directory
        output_dir = Path(config.output_directory) / analysis_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Phase 1: Load pre-extracted tweet data
            tweets = await self._load_extracted_tweets(config.input_tweets_file)
            
            # Phase 2: Process tweets through multi-agent analysis
            analysis_results, processing_stats = await self._process_tweets_batch(
                tweets, config, output_dir, analysis_id
            )
            
            # Phase 3: Integrate results and save comprehensive output
            results_file, summary_file = await self._save_integrated_results(
                tweets, analysis_results, processing_stats, output_dir, analysis_id
            )
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create analysis result
            result = AnalysisResult(
                analysis_id=analysis_id,
                timestamp=start_time,
                input_tweets_file=config.input_tweets_file,
                total_tweets_processed=len(tweets),
                successful_analyses=processing_stats['successful_analyses'],
                failed_analyses=processing_stats['failed_analyses'],
                tweets_analyzed=processing_stats['tweets_analyzed'],
                tweets_failed=processing_stats['tweets_failed'],
                results_file_path=str(results_file),
                summary_file_path=str(summary_file),
                analysis_config=config,
                processing_time=processing_time,
                status='success' if processing_stats['successful_analyses'] > 0 else 'failed',
                error_details=processing_stats.get('errors', []),
                agent_performance=processing_stats.get('agent_performance', {})
            )
            
            self.logger.info(f"✅ Analysis completed: {processing_stats['successful_analyses']}/{len(tweets)} tweets analyzed")
            self.logger.info(f"📁 Results saved to: {results_file}")
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Analysis failed: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            
            # Return failed result
            return AnalysisResult(
                analysis_id=analysis_id,
                timestamp=start_time,
                input_tweets_file=config.input_tweets_file,
                total_tweets_processed=0,
                successful_analyses=0,
                failed_analyses=0,
                tweets_analyzed=[],
                tweets_failed=[],
                results_file_path="",
                summary_file_path="",
                analysis_config=config,
                processing_time=processing_time,
                status='failed',
                error_details=[error_msg]
            )
    
    async def _load_extracted_tweets(self, tweets_file_path: str) -> List[Tweet]:
        """Load pre-extracted tweets from file"""
        self.logger.info("📂 Phase 1: Loading pre-extracted tweet data...")
        
        try:
            with open(tweets_file_path, 'r', encoding='utf-8') as f:
                tweets_data = json.load(f)
            
            # Convert dictionaries back to Tweet entities
            tweets = []
            for tweet_data in tweets_data:
                try:
                    tweet = Tweet.from_dict(tweet_data)
                    tweets.append(tweet)
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to load tweet {tweet_data.get('id', 'unknown')}: {str(e)}")
                    continue
            
            self.logger.info(f"📊 Loaded {len(tweets)} tweets for analysis")
            return tweets
            
        except Exception as e:
            error_msg = f"Failed to load tweets from {tweets_file_path}: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            raise
    
    async def _process_tweets_batch(self, 
                                  tweets: List[Tweet], 
                                  config: AnalysisConfig,
                                  output_dir: Path,
                                  analysis_id: str) -> Tuple[List[Dict], Dict]:
        """Process tweets through multi-agent analysis with error handling"""
        self.logger.info("🤖 Phase 2: Processing tweets through multi-agent analysis...")
        
        processing_stats = {
            'successful_analyses': 0,
            'failed_analyses': 0,
            'tweets_analyzed': [],
            'tweets_failed': [],
            'errors': [],
            'agent_performance': {},
            'retry_stats': {}
        }
        
        analysis_results = []
        
        # Process tweets in batches
        for i in range(0, len(tweets), config.batch_size):
            batch = tweets[i:i + config.batch_size]
            self.logger.info(f"📊 Processing batch {i//config.batch_size + 1}: {len(batch)} tweets")
            
            for tweet in batch:
                result = await self._analyze_single_tweet_with_retry(
                    tweet, config, processing_stats, analysis_id
                )
                
                if result:
                    analysis_results.append(result)
                    processing_stats['successful_analyses'] += 1
                    processing_stats['tweets_analyzed'].append(tweet.tweet_id)
                    
                    # Save intermediate results if enabled
                    if config.save_intermediate_results:
                        await self._save_intermediate_result(result, output_dir, tweet.tweet_id)
                else:
                    processing_stats['failed_analyses'] += 1
                    processing_stats['tweets_failed'].append(tweet.tweet_id)
                
                self.stats['tweets_processed'] += 1
            
            # Small delay between batches to prevent API overload
            await asyncio.sleep(1)
        
        self.logger.info(f"✅ Batch processing completed: {processing_stats['successful_analyses']} successful, {processing_stats['failed_analyses']} failed")
        return analysis_results, processing_stats
    
    async def _analyze_single_tweet_with_retry(self, 
                                             tweet: Tweet, 
                                             config: AnalysisConfig,
                                             stats: Dict,
                                             analysis_id: str) -> Optional[Dict]:
        """Analyze single tweet with retry logic for API failures"""
        retries = 0
        last_error = None
        
        while retries <= config.max_retries:
            try:
                self.logger.debug(f"🔍 Analyzing tweet {tweet.tweet_id} (attempt {retries + 1})")
                
                # Perform multi-agent analysis
                analysis_result = await self.analyzer.analyze_tweet(tweet, analysis_id)
                
                if analysis_result:
                    # Create integrated result with input data
                    integrated_result = {
                        'tweet_id': tweet.tweet_id,
                        'input_data': tweet.to_dict(),
                        'analysis_result': analysis_result.to_dict() if hasattr(analysis_result, 'to_dict') else analysis_result,
                        'processing_metadata': {
                            'analyzed_at': datetime.now().isoformat(),
                            'attempts': retries + 1,
                            'status': 'success'
                        }
                    }
                    
                    self.logger.debug(f"✅ Successfully analyzed tweet {tweet.tweet_id}")
                    return integrated_result
                else:
                    raise Exception("Analysis returned empty result")
                    
            except Exception as e:
                last_error = str(e)
                retries += 1
                self.stats['api_errors'] += 1
                self.stats['retries_attempted'] += 1
                
                if retries <= config.max_retries:
                    self.logger.warning(f"⚠️ Analysis failed for tweet {tweet.tweet_id} (attempt {retries}): {last_error}")
                    self.logger.info(f"🔄 Retrying in {config.retry_delay} seconds...")
                    
                    # Add error to stats
                    if 'retry_stats' not in stats:
                        stats['retry_stats'] = {}
                    stats['retry_stats'][tweet.tweet_id] = retries
                    
                    # Wait before retry
                    await asyncio.sleep(config.retry_delay)
                else:
                    self.logger.error(f"❌ Max retries exceeded for tweet {tweet.tweet_id}: {last_error}")
                    stats['errors'].append(f"Tweet {tweet.tweet_id}: {last_error}")
                    
                    if not config.continue_on_failure:
                        raise Exception(f"Analysis failed for tweet {tweet.tweet_id} after {config.max_retries} retries")
        
        # Return None if all retries failed
        return None
    
    async def _save_intermediate_result(self, result: Dict, output_dir: Path, tweet_id: str):
        """Save intermediate analysis result"""
        try:
            intermediate_dir = output_dir / 'intermediate'
            intermediate_dir.mkdir(exist_ok=True)
            
            result_file = intermediate_dir / f'tweet_{tweet_id}_analysis.json'
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
                
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to save intermediate result for tweet {tweet_id}: {str(e)}")
    
    async def _save_integrated_results(self, 
                                     tweets: List[Tweet],
                                     analysis_results: List[Dict], 
                                     stats: Dict,
                                     output_dir: Path,
                                     analysis_id: str) -> Tuple[Path, Path]:
        """Save integrated analysis results"""
        self.logger.info("💾 Phase 3: Saving integrated analysis results...")
        
        # Create comprehensive results structure
        integrated_results = {
            'analysis_id': analysis_id,
            'timestamp': datetime.now().isoformat(),
            'input_summary': {
                'total_tweets': len(tweets),
                'tweets_with_media': len([t for t in tweets if t.media_attachments]),
                'tweets_with_threads': len([t for t in tweets if t.thread_context and t.thread_context.is_thread]),
                'tweets_with_urls': len([t for t in tweets if hasattr(t, 'extracted_urls') and t.extracted_urls])
            },
            'analysis_summary': {
                'successful_analyses': stats['successful_analyses'],
                'failed_analyses': stats['failed_analyses'],
                'success_rate': stats['successful_analyses'] / len(tweets) if tweets else 0,
                'processing_stats': self.stats
            },
            'detailed_results': analysis_results,
            'error_analysis': stats.get('errors', []),
            'performance_metrics': stats.get('agent_performance', {})
        }
        
        # Create analysis summary
        summary = {
            'analysis_id': analysis_id,
            'timestamp': datetime.now().isoformat(),
            'overview': {
                'total_tweets_input': len(tweets),
                'successful_analyses': stats['successful_analyses'],
                'failed_analyses': stats['failed_analyses'],
                'success_rate': f"{(stats['successful_analyses'] / len(tweets) * 100):.1f}%" if tweets else "0%"
            },
            'content_analysis': self._generate_content_analysis_summary(analysis_results),
            'quality_metrics': self._calculate_quality_metrics(analysis_results),
            'recommendations': self._generate_recommendations(stats, analysis_results)
        }
        
        # Save files
        results_file = output_dir / 'integrated_analysis_results.json'
        summary_file = output_dir / 'analysis_summary.json'
        
        # Save integrated results
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(integrated_results, f, indent=2, ensure_ascii=False, default=str)
        
        # Save summary
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"💾 Integrated results saved:")
        self.logger.info(f"   📄 Full results: {results_file}")
        self.logger.info(f"   📋 Summary: {summary_file}")
        
        return results_file, summary_file
    
    def _generate_content_analysis_summary(self, results: List[Dict]) -> Dict:
        """Generate content analysis summary from results"""
        if not results:
            return {}
        
        # Extract scores and analyze patterns
        scores = []
        categories = {}
        
        for result in results:
            analysis = result.get('analysis_result', {})
            if 'consolidated_score' in analysis:
                score_data = analysis['consolidated_score']
                scores.append(score_data.get('consolidated_score', 0))
        
        return {
            'total_analyzed': len(results),
            'average_score': sum(scores) / len(scores) if scores else 0,
            'score_distribution': {
                'high_quality': len([s for s in scores if s >= 8]),
                'medium_quality': len([s for s in scores if 6 <= s < 8]),
                'low_quality': len([s for s in scores if s < 6])
            }
        }
    
    def _calculate_quality_metrics(self, results: List[Dict]) -> Dict:
        """Calculate quality metrics from analysis results"""
        if not results:
            return {}
        
        return {
            'processing_efficiency': len(results) / self.stats['tweets_processed'] if self.stats['tweets_processed'] > 0 else 0,
            'error_rate': self.stats['api_errors'] / self.stats['tweets_processed'] if self.stats['tweets_processed'] > 0 else 0,
            'retry_rate': self.stats['retries_attempted'] / self.stats['tweets_processed'] if self.stats['tweets_processed'] > 0 else 0
        }
    
    def _generate_recommendations(self, stats: Dict, results: List[Dict]) -> List[str]:
        """Generate recommendations based on analysis results"""
        recommendations = []
        
        if stats['failed_analyses'] > 0:
            recommendations.append(f"Consider increasing retry delay or max retries for {stats['failed_analyses']} failed analyses")
        
        if self.stats['api_errors'] > 10:
            recommendations.append("High API error rate detected - consider implementing rate limiting")
        
        if len(results) > 0:
            recommendations.append("Analysis completed successfully - data ready for further processing")
        
        return recommendations
    
    def get_analysis_stats(self) -> Dict:
        """Get current analysis statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset analysis statistics"""
        self.stats = {
            'tweets_processed': 0,
            'successful_analyses': 0,
            'failed_analyses': 0,
            'api_errors': 0,
            'retries_attempted': 0,
            'agent_calls': 0
        } 