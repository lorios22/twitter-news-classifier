#!/usr/bin/env python3
"""
🤖 ENHANCED MULTI-AGENT ANALYZER
================================
Enhanced multi-agent analyzer with 5 new signal integrity agents.

This enhanced analyzer includes the original 12 agents plus:
- Sarcasm Sentinel 🛰️
- Echo Mapper 📡
- Latency Guard ⏱️
- AI Slop Filter 🧽
- Banned Phrase Skeptic 🔍

Domain-Driven Design: Domain service for enhanced multi-agent analysis.
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..core_analysis.multi_agent_analyzer import MultiAgentAnalyzer
from ..signal_integrity.sarcasm_sentinel_agent import SarcasmSentinelAgent
from ..signal_integrity.echo_mapper_agent import EchoMapperAgent
from ..signal_integrity.latency_guard_agent import LatencyGuardAgent
from ..signal_integrity.slop_filter_agent import SlopFilterAgent
from ..signal_integrity.banned_phrase_skeptic_agent import BannedPhraseSkepticAgent
from ...entities.tweet import Tweet
from ...entities.analysis_result import AnalysisResult, AnalysisStatus


@dataclass
class EnhancedAgentConfig:
    """Configuration for enhanced agents"""
    enable_sarcasm_sentinel: bool = True
    enable_echo_mapper: bool = True
    enable_latency_guard: bool = True
    enable_slop_filter: bool = True
    enable_banned_phrase_skeptic: bool = True
    
    # External API configurations
    reddit_config: Optional[Dict] = None
    price_feed_config: Optional[Dict] = None
    
    # Real data only mode - disable agents without real APIs
    real_data_only: bool = True


class EnhancedMultiAgentAnalyzer(MultiAgentAnalyzer):
    """
    🤖 Enhanced Multi-Agent Analyzer
    
    Extends the base MultiAgentAnalyzer with 5 new signal integrity agents
    for input-sovereign classification.
    
    Features:
    - All original 12 agents
    - 5 new signal integrity agents
    - Improved score consolidation
    - Memory-based learning
    - Conditional routing (e.g., Latency Guard)
    """
    
    def __init__(self, openai_api_key: str, config: Optional[EnhancedAgentConfig] = None):
        """Initialize enhanced multi-agent analyzer"""
        # Initialize base analyzer
        super().__init__(openai_api_key)
        
        self.config = config or EnhancedAgentConfig()
        
        # Initialize memory store (in production, this would be LettA)
        self.memory_store = {}
        
        # Check API availability in real data only mode
        if self.config.real_data_only:
            self._check_api_availability()
        
        # Initialize new agents (only if enabled and APIs available in real data mode)
        self.sarcasm_sentinel = SarcasmSentinelAgent(self.openai_client, self.memory_store) if self.config.enable_sarcasm_sentinel else None
        self.echo_mapper = EchoMapperAgent(self.memory_store, self.config.reddit_config) if self.config.enable_echo_mapper else None
        self.latency_guard = LatencyGuardAgent(self.memory_store, self.config.price_feed_config) if self.config.enable_latency_guard else None
        self.slop_filter = SlopFilterAgent(self.memory_store) if self.config.enable_slop_filter else None
        self.banned_phrase_skeptic = BannedPhraseSkepticAgent(self.memory_store) if self.config.enable_banned_phrase_skeptic else None
        
        # Update agent weights to include new agents
        self._update_agent_weights()
        
        # Update agent sequence
        self._update_agent_sequence()
        
        self.logger.info("🚀 Enhanced Multi-Agent Analyzer initialized with signal integrity agents")
    
    def _check_api_availability(self):
        """Check API availability and disable agents without real APIs in real data only mode"""
        import os
        
        # Check Reddit API
        reddit_available = bool(os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'))
        if not reddit_available and self.config.enable_echo_mapper:
            self.logger.warning("Reddit API not available - Echo Mapper will have limited functionality")
            # Don't disable, but configure with None to indicate no Reddit
            if not self.config.reddit_config:
                self.config.reddit_config = None
        
        # Check Exchange APIs
        binance_available = bool(os.getenv('BINANCE_API_KEY'))
        coinbase_available = bool(os.getenv('COINBASE_API_KEY') and 
                                os.getenv('COINBASE_API_SECRET') and 
                                os.getenv('COINBASE_API_PASSPHRASE'))
        
        if not (binance_available or coinbase_available) and self.config.enable_latency_guard:
            self.logger.warning("No Exchange APIs available - Latency Guard will have limited functionality")
            # Don't disable, but configure appropriately
            if not self.config.price_feed_config:
                self.config.price_feed_config = {}
        
        # Log what's available
        available_apis = []
        if reddit_available:
            available_apis.append("Reddit")
        if binance_available:
            available_apis.append("Binance")
        if coinbase_available:
            available_apis.append("Coinbase")
        
        if available_apis:
            self.logger.info(f"Real APIs available: {', '.join(available_apis)}")
        else:
            self.logger.warning("No external APIs configured - agents will work with limited functionality")
    
    def _update_agent_weights(self):
        """Update agent weights to include new agents"""
        # Slightly reduce existing weights to accommodate new agents
        scale_factor = 0.85  # Reduce existing weights by 15%
        
        for agent_name in self.agent_weights:
            if self.agent_weights[agent_name] > 0:
                self.agent_weights[agent_name] *= scale_factor
        
        # Add new agents with appropriate weights
        # These agents primarily influence via score adjustments rather than direct scoring
        self.agent_weights.update({
            'sarcasm_sentinel': 0.03,        # 3% - Tone interpretation
            'echo_mapper': 0.05,             # 5% - Cross-platform relevance
            'latency_guard': 0.02,           # 2% - Temporal validity
            'slop_filter': 0.03,             # 3% - Content quality
            'banned_phrase_skeptic': 0.02,   # 2% - Editorial compliance
        })
        
        # Normalize weights to ensure they sum to 1.0 (excluding meta-agents)
        total_weight = sum(w for w in self.agent_weights.values() if w > 0)
        if total_weight != 1.0:
            adjustment_factor = 1.0 / total_weight
            for agent_name in self.agent_weights:
                if self.agent_weights[agent_name] > 0:
                    self.agent_weights[agent_name] *= adjustment_factor
    
    def _update_agent_sequence(self):
        """Update agent sequence to include new agents in parallel phase"""
        # Insert new agents into the independent analysis phase (before score_consolidator)
        new_agents = []
        if self.config.enable_sarcasm_sentinel:
            new_agents.append('sarcasm_sentinel')
        if self.config.enable_echo_mapper:
            new_agents.append('echo_mapper')
        if self.config.enable_latency_guard:
            new_agents.append('latency_guard')
        if self.config.enable_slop_filter:
            new_agents.append('slop_filter')
        if self.config.enable_banned_phrase_skeptic:
            new_agents.append('banned_phrase_skeptic')
        
        # Insert new agents into parallel phase (before score_consolidator)
        self.agent_sequence = (
            self.agent_sequence[:10] +  # Original 10 agents
            new_agents +                # New signal integrity agents
            ['score_consolidator', 'validator']  # Sequential agents
        )
    
    async def analyze_tweet(self, tweet: Tweet, run_id: str) -> AnalysisResult:
        """
        Enhanced tweet analysis with signal integrity agents
        
        Args:
            tweet: Tweet entity to analyze
            run_id: Unique run identifier
            
        Returns:
            Enhanced analysis result
        """
        start_time = datetime.now()
        self.logger.info(f"🔍 Starting enhanced analysis for tweet {tweet.tweet_id}")
        
        # Check if Latency Guard should gate the analysis
        latency_result = None
        if self.latency_guard:
            latency_result = await self.latency_guard.analyze_latency(
                tweet.text, tweet.created_at
            )
            
            # If repriced, flag for human review
            if latency_result.repriced:
                self.logger.warning(
                    f"⏱️ Latency Guard flagged tweet {tweet.tweet_id} as repriced "
                    f"({latency_result.delta_seconds}s, {latency_result.price_change_pct}%)"
                )
                
                # Create analysis result with human escalation flag
                analysis_result = AnalysisResult(
                    content_id=tweet.tweet_id,
                    run_id=run_id,
                    analysis_timestamp=start_time
                )
                analysis_result.overall_status = AnalysisStatus.REQUIRES_HUMAN_REVIEW
                analysis_result.escalation_reason = f"Latency Guard: Price moved {latency_result.price_change_pct}% before tweet"
                analysis_result.total_processing_time = (datetime.now() - start_time).total_seconds()
                
                return analysis_result
        
        # Proceed with normal analysis
        analysis_result = await super().analyze_tweet(tweet, run_id)
        
        # Add enhanced agent results
        await self._execute_enhanced_agents(tweet, analysis_result)
        
        # Apply score adjustments from new agents
        self._apply_enhanced_score_adjustments(analysis_result)
        
        self.logger.info(f"🎉 Enhanced analysis complete for tweet {tweet.tweet_id}")
        
        return analysis_result
    
    async def _execute_enhanced_agents(self, tweet: Tweet, analysis_result: AnalysisResult):
        """Execute the new signal integrity agents"""
        enhanced_tasks = []
        
        # Prepare for parallel execution of new agents
        if self.sarcasm_sentinel:
            enhanced_tasks.append(
                self._execute_sarcasm_sentinel(tweet, analysis_result)
            )
        
        if self.echo_mapper:
            enhanced_tasks.append(
                self._execute_echo_mapper(tweet, analysis_result)
            )
        
        if self.slop_filter:
            enhanced_tasks.append(
                self._execute_slop_filter(tweet, analysis_result)
            )
        
        if self.banned_phrase_skeptic:
            enhanced_tasks.append(
                self._execute_banned_phrase_skeptic(tweet, analysis_result)
            )
        
        # Execute enhanced agents in parallel
        if enhanced_tasks:
            try:
                await asyncio.wait_for(
                    asyncio.gather(*enhanced_tasks, return_exceptions=True),
                    timeout=60  # 1 minute timeout for enhanced agents
                )
            except asyncio.TimeoutError:
                self.logger.warning("⏰ Enhanced agents execution timed out")
    
    async def _execute_sarcasm_sentinel(self, tweet: Tweet, analysis_result: AnalysisResult):
        """Execute sarcasm sentinel agent"""
        try:
            start_time = datetime.now()
            
            result = await self.sarcasm_sentinel.analyze_sarcasm(
                tweet.text, tweet.author_username
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Convert to agent response format
            response_data = {
                'is_sarcastic': result.is_sarcastic,
                'p_sarcasm': result.p_sarcasm,
                'reason': result.reason,
                'agent_score': 7.0 if not result.is_sarcastic else 8.0  # Higher score if not sarcastic (more reliable)
            }
            
            analysis_result.add_agent_response(
                agent_name='sarcasm_sentinel',
                response_data=response_data,
                execution_time=execution_time,
                status=AnalysisStatus.SUCCESS
            )
            
            self.logger.info(f"🛰️ Sarcasm Sentinel: {'Sarcastic' if result.is_sarcastic else 'Not sarcastic'} (confidence: {result.p_sarcasm})")
            
        except Exception as e:
            self.logger.error(f"❌ Sarcasm Sentinel failed: {e}")
            analysis_result.add_agent_response(
                agent_name='sarcasm_sentinel',
                response_data={'error': str(e), 'agent_score': 5.0},
                execution_time=0.0,
                status=AnalysisStatus.FAILED,
                error_message=str(e)
            )
    
    async def _execute_echo_mapper(self, tweet: Tweet, analysis_result: AnalysisResult):
        """Execute echo mapper agent"""
        try:
            start_time = datetime.now()
            
            result = await self.echo_mapper.analyze_echo(tweet.text, tweet.created_at)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Convert to agent response format
            response_data = {
                'reddit_threads': result.reddit_threads,
                'farcaster_refs': result.farcaster_refs,
                'discord_refs': result.discord_refs,
                'echo_velocity': result.echo_velocity,
                'agent_score': min(10.0, 5.0 + (result.echo_velocity * 5.0))  # Scale velocity to score
            }
            
            analysis_result.add_agent_response(
                agent_name='echo_mapper',
                response_data=response_data,
                execution_time=execution_time,
                status=AnalysisStatus.SUCCESS
            )
            
            self.logger.info(f"📡 Echo Mapper: velocity {result.echo_velocity} (Reddit: {result.reddit_threads}, Farcaster: {result.farcaster_refs})")
            
        except Exception as e:
            self.logger.error(f"❌ Echo Mapper failed: {e}")
            analysis_result.add_agent_response(
                agent_name='echo_mapper',
                response_data={'error': str(e), 'agent_score': 5.0},
                execution_time=0.0,
                status=AnalysisStatus.FAILED,
                error_message=str(e)
            )
    
    async def _execute_slop_filter(self, tweet: Tweet, analysis_result: AnalysisResult):
        """Execute slop filter agent"""
        try:
            start_time = datetime.now()
            
            result = await self.slop_filter.analyze_slop(tweet.text, tweet.author_username)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Convert to agent response format
            response_data = {
                'is_sloppy': result.is_sloppy,
                'slop_score': result.slop_score,
                'reasoning': result.reasoning,
                'agent_score': max(1.0, 10.0 - (result.slop_score * 8.0))  # Inverse relationship
            }
            
            analysis_result.add_agent_response(
                agent_name='slop_filter',
                response_data=response_data,
                execution_time=execution_time,
                status=AnalysisStatus.SUCCESS
            )
            
            self.logger.info(f"🧽 Slop Filter: {'Sloppy' if result.is_sloppy else 'Clean'} (score: {result.slop_score})")
            
        except Exception as e:
            self.logger.error(f"❌ Slop Filter failed: {e}")
            analysis_result.add_agent_response(
                agent_name='slop_filter',
                response_data={'error': str(e), 'agent_score': 5.0},
                execution_time=0.0,
                status=AnalysisStatus.FAILED,
                error_message=str(e)
            )
    
    async def _execute_banned_phrase_skeptic(self, tweet: Tweet, analysis_result: AnalysisResult):
        """Execute banned phrase skeptic agent"""
        try:
            start_time = datetime.now()
            
            # Check if sarcasm was detected to adjust penalty
            sarcasm_response = analysis_result.agent_responses.get('sarcasm_sentinel', {})
            is_sarcastic = sarcasm_response.get('response_data', {}).get('is_sarcastic', False)
            
            result = await self.banned_phrase_skeptic.analyze_banned_phrases(
                tweet.text, tweet.author_username, is_sarcastic
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Convert to agent response format
            response_data = {
                'banned_terms': result.banned_terms,
                'total_weight': result.total_weight,
                'tone_penalty': result.tone_penalty,
                'agent_score': max(1.0, 10.0 - (result.tone_penalty * 8.0))  # Inverse relationship
            }
            
            analysis_result.add_agent_response(
                agent_name='banned_phrase_skeptic',
                response_data=response_data,
                execution_time=execution_time,
                status=AnalysisStatus.SUCCESS
            )
            
            self.logger.info(f"🔍 Banned Phrase Skeptic: {len(result.banned_terms)} terms, penalty {result.tone_penalty}")
            
        except Exception as e:
            self.logger.error(f"❌ Banned Phrase Skeptic failed: {e}")
            analysis_result.add_agent_response(
                agent_name='banned_phrase_skeptic',
                response_data={'error': str(e), 'agent_score': 5.0},
                execution_time=0.0,
                status=AnalysisStatus.FAILED,
                error_message=str(e)
            )
    
    def _apply_enhanced_score_adjustments(self, analysis_result: AnalysisResult):
        """Apply score adjustments from enhanced agents"""
        try:
            # Get current consolidated score
            current_score = analysis_result.consolidated_score or 5.0
            
            # Apply sarcasm adjustment
            sarcasm_response = analysis_result.agent_responses.get('sarcasm_sentinel', {})
            if sarcasm_response.get('status') == AnalysisStatus.SUCCESS:
                sarcasm_data = sarcasm_response.get('response_data', {})
                if sarcasm_data.get('is_sarcastic'):
                    # If sarcastic, ensure fact-checking didn't overly penalize
                    fact_check_response = analysis_result.agent_responses.get('fact_checker', {})
                    if fact_check_response.get('status') == AnalysisStatus.SUCCESS:
                        fact_score = fact_check_response.get('response_data', {}).get('agent_score', 5.0)
                        if fact_score < 4.0:  # Very low fact score might be due to sarcasm
                            current_score = max(current_score, 5.0)  # Don't let it go too low
                            self.logger.info("🛰️ Applied sarcasm adjustment to prevent over-penalization")
            
            # Apply echo velocity boost
            echo_response = analysis_result.agent_responses.get('echo_mapper', {})
            if echo_response.get('status') == AnalysisStatus.SUCCESS:
                echo_data = echo_response.get('response_data', {})
                echo_velocity = echo_data.get('echo_velocity', 0.0)
                if echo_velocity > 0.5:
                    velocity_boost = (echo_velocity - 0.5) * 2.0  # Up to 1 point boost
                    current_score = min(10.0, current_score + velocity_boost)
                    self.logger.info(f"📡 Applied echo velocity boost: +{velocity_boost:.2f}")
            
            # Apply slop penalty
            slop_response = analysis_result.agent_responses.get('slop_filter', {})
            if slop_response.get('status') == AnalysisStatus.SUCCESS:
                slop_data = slop_response.get('response_data', {})
                slop_score = slop_data.get('slop_score', 0.0)
                if slop_score > 0.7:
                    slop_penalty = (slop_score - 0.7) * 3.0  # Up to 0.9 penalty
                    current_score = max(1.0, current_score - slop_penalty)
                    self.logger.info(f"🧽 Applied slop penalty: -{slop_penalty:.2f}")
            
            # Apply banned phrase penalty
            banned_response = analysis_result.agent_responses.get('banned_phrase_skeptic', {})
            if banned_response.get('status') == AnalysisStatus.SUCCESS:
                banned_data = banned_response.get('response_data', {})
                tone_penalty = banned_data.get('tone_penalty', 0.0)
                if tone_penalty > 0.2:
                    penalty_points = tone_penalty * 2.0  # Up to 2 points penalty
                    current_score = max(1.0, current_score - penalty_points)
                    self.logger.info(f"🔍 Applied tone penalty: -{penalty_points:.2f}")
            
            # Update consolidated score
            analysis_result.consolidated_score = round(current_score, 2)
            
        except Exception as e:
            self.logger.error(f"❌ Error applying enhanced score adjustments: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about the memory store"""
        stats = {
            'total_entries': len(self.memory_store),
            'namespaces': {},
            'memory_size_mb': 0  # Placeholder
        }
        
        # Count entries by namespace
        for key in self.memory_store.keys():
            namespace = key.split(':')[0] if ':' in key else 'unknown'
            stats['namespaces'][namespace] = stats['namespaces'].get(namespace, 0) + 1
        
        return stats