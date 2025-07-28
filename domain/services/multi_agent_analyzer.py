#!/usr/bin/env python3
"""
🤖 MULTI-AGENT ANALYZER SERVICE
==============================
Core domain service for multi-agent analysis processing.

Domain-Driven Design: Core domain service containing business logic.
Orchestrates 12 specialized AI agents for comprehensive content analysis.
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
from openai import AsyncOpenAI

from ..entities.tweet import Tweet
from ..entities.analysis_result import AnalysisResult, AnalysisStatus, MediaAnalysisResult, ThreadAnalysisResult
from infrastructure.prompts.agent_prompts import AgentPrompts


def convert_enums_to_strings(obj: Any) -> Any:
    """
    Recursively convert all Enum objects to their string values in nested data structures.
    
    Args:
        obj: The object to convert
        
    Returns:
        Object with all Enums converted to strings
    """
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {key: convert_enums_to_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_enums_to_strings(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_enums_to_strings(item) for item in obj)
    else:
        return obj


class MultiAgentAnalyzer:
    """
    🤖 Multi-agent analyzer for comprehensive social media content analysis
    
    Orchestrates 12 specialized AI agents:
    1. Summary Agent - Title and abstract generation
    2. Input Preprocessor - Data cleansing and normalization
    3. Context Evaluator - Quality scoring for content context
    4. Fact Checker - Accuracy verification and factual assessment
    5. Depth Analyzer - Content complexity and analytical depth
    6. Relevance Analyzer - Real-world importance assessment
    7. Structure Analyzer - Content organization assessment
    8. Reflective Agent - Meta-analysis and critical evaluation
    9. Metadata Ranking Agent - User credibility assessment
    10. Consensus Agent - Agreement and consensus evaluation
    11. Score Consolidator - Aggregated results calculation
    12. Validator - Final validation and quality assurance
    """
    
    def __init__(self, openai_api_key: str):
        """Initialize multi-agent analyzer"""
        self.logger = logging.getLogger(__name__)
        self.prompts = AgentPrompts()
        
        # Configure OpenAI client
        self.openai_client = AsyncOpenAI(api_key=openai_api_key)
        
        # Agent configuration with importance weights for score consolidation
        self.agent_weights = {
            'summary_agent': 0.10,          # 10% - Title and abstract quality
            'input_preprocessor': 0.05,     # 5% - Data quality
            'context_evaluator': 0.15,     # 15% - Context richness (high importance)
            'fact_checker': 0.18,          # 18% - Factual accuracy (highest importance)
            'depth_analyzer': 0.12,        # 12% - Analytical depth
            'relevance_analyzer': 0.15,    # 15% - Real-world relevance (high importance)
            'structure_analyzer': 0.08,    # 8% - Content organization
            'reflective_agent': 0.07,      # 7% - Critical evaluation
            'metadata_ranking_agent': 0.06, # 6% - User credibility
            'consensus_agent': 0.04,       # 4% - Agreement assessment
            'score_consolidator': 0.0,     # 0% - Meta-agent (doesn't contribute to own score)
            'validator': 0.0               # 0% - Meta-agent (doesn't contribute to own score)
        }
        
        # Ordered agent execution sequence
        self.agent_sequence = [
            'summary_agent',
            'input_preprocessor', 
            'context_evaluator',
            'fact_checker',
            'depth_analyzer',
            'relevance_analyzer',
            'structure_analyzer',
            'reflective_agent',
            'metadata_ranking_agent',
            'consensus_agent',
            'score_consolidator',
            'validator'
        ]
    
    async def analyze_tweet(self, tweet: Tweet, run_id: str) -> AnalysisResult:
        """
        Analyze a tweet using all 12 agents
        
        Args:
            tweet: Tweet entity to analyze
            run_id: Unique run identifier
            
        Returns:
            Complete analysis result
        """
        start_time = datetime.now()
        self.logger.info(f"🔍 Starting comprehensive analysis for tweet {tweet.tweet_id}")
        
        # Create analysis result
        analysis_result = AnalysisResult(
            content_id=tweet.tweet_id,
            run_id=run_id,
            analysis_timestamp=start_time
        )
        
        # Prepare comprehensive input for agents
        comprehensive_input = self._prepare_comprehensive_input(tweet)
        
        # Execute agents with smart parallelization
        agent_responses = {}
        
        # Phase 1: Execute independent analysis agents in parallel (first 10 agents)
        independent_agents = self.agent_sequence[:10]  # Exclude score_consolidator and validator
        self.logger.info(f"🚀 Phase 1: Executing {len(independent_agents)} analysis agents in parallel...")
        
        parallel_start_time = datetime.now()
        parallel_tasks = []
        
        for agent_name in independent_agents:
            task = self._execute_agent_with_metadata(agent_name, comprehensive_input, {})
            parallel_tasks.append(task)
        
        # Wait for all parallel agents to complete with timeout protection
        try:
            parallel_results = await asyncio.wait_for(
                asyncio.gather(*parallel_tasks, return_exceptions=True),
                timeout=300  # 5 minutes timeout for all parallel agents
            )
            
            # Process parallel results
            for i, result in enumerate(parallel_results):
                agent_name = independent_agents[i]
                if isinstance(result, Exception):
                    self.logger.error(f"❌ {agent_name} failed: {str(result)}")
                    # Add failed response
                    analysis_result.add_agent_response(
                        agent_name=agent_name,
                        response_data={'error': str(result), 'agent_score': 5.0},
                        execution_time=0.0,
                        status=AnalysisStatus.FAILED,
                        error_message=str(result)
                    )
                    agent_responses[agent_name] = {'error': str(result), 'agent_score': 5.0}
                else:
                    agent_responses[agent_name] = result['response']
                    analysis_result.add_agent_response(
                        agent_name=agent_name,
                        response_data=result['response'],
                        execution_time=result['execution_time'],
                        status=AnalysisStatus.SUCCESS
                    )
                    self.logger.info(f"✅ {agent_name} completed in {result['execution_time']:.2f}s")
            
            parallel_time = (datetime.now() - parallel_start_time).total_seconds()
            self.logger.info(f"🎉 Phase 1 completed in {parallel_time:.2f}s (parallel execution)")
            
        except asyncio.TimeoutError:
            self.logger.error("⏰ Parallel agent execution timed out after 5 minutes")
            # Handle timeout by providing default responses
            for agent_name in independent_agents:
                if agent_name not in agent_responses:
                    agent_responses[agent_name] = {'error': 'timeout', 'agent_score': 5.0}
                    analysis_result.add_agent_response(
                        agent_name=agent_name,
                        response_data={'error': 'timeout', 'agent_score': 5.0},
                        execution_time=0.0,
                        status=AnalysisStatus.FAILED,
                        error_message="Agent execution timed out"
                    )
        
        # Phase 2: Execute dependent agents sequentially (score_consolidator and validator)
        dependent_agents = ['score_consolidator', 'validator']
        self.logger.info(f"🔄 Phase 2: Executing {len(dependent_agents)} dependent agents sequentially...")
        
        for agent_name in dependent_agents:
            self.logger.info(f"🔍 Executing {agent_name}")
            
            try:
                agent_start_time = datetime.now()
                
                # Get appropriate prompt for dependent agents
                if agent_name == 'score_consolidator':
                    prompt = self.prompts.get_score_consolidator_prompt()
                    input_data = {
                        'comprehensive_input': comprehensive_input,
                        'all_agent_responses': json.dumps(agent_responses, indent=2, default=str)
                    }
                elif agent_name == 'validator':
                    prompt = self.prompts.get_validator_prompt()
                    input_data = {
                        'comprehensive_input': comprehensive_input,
                        'all_agent_responses': json.dumps(agent_responses, indent=2, default=str)
                    }
                
                # Format prompt with input data
                formatted_prompt = prompt.format(**input_data)
                
                # Execute agent with timeout
                response = await asyncio.wait_for(
                    self._execute_agent(formatted_prompt),
                    timeout=60  # 1 minute timeout per dependent agent
                )
                
                # Calculate execution time
                execution_time = (datetime.now() - agent_start_time).total_seconds()
                
                # Parse and store response
                parsed_response = self._parse_json_safe(response, agent_name)
                agent_responses[agent_name] = parsed_response
                
                # Add to analysis result
                analysis_result.add_agent_response(
                    agent_name=agent_name,
                    response_data=parsed_response,
                    execution_time=execution_time,
                    status=AnalysisStatus.SUCCESS
                )
                
                self.logger.info(f"✅ {agent_name} completed in {execution_time:.2f}s")
                
            except asyncio.TimeoutError:
                self.logger.error(f"⏰ {agent_name} timed out after 60 seconds")
                # Add timeout response
                agent_responses[agent_name] = {'error': 'timeout', 'agent_score': 5.0}
                analysis_result.add_agent_response(
                    agent_name=agent_name,
                    response_data={'error': 'timeout', 'agent_score': 5.0},
                    execution_time=60.0,
                    status=AnalysisStatus.FAILED,
                    error_message="Agent execution timed out"
                )
            except Exception as e:
                self.logger.error(f"❌ Error executing {agent_name}: {str(e)}")
                # Add error response
                agent_responses[agent_name] = {'error': str(e), 'agent_score': 5.0}
                analysis_result.add_agent_response(
                    agent_name=agent_name,
                    response_data={'error': str(e), 'agent_score': 5.0},
                    execution_time=0.0,
                    status=AnalysisStatus.FAILED,
                    error_message=str(e)
                )
                
                # Add error response
                analysis_result.add_agent_response(
                    agent_name=agent_name,
                    response_data={'error': str(e)},
                    execution_time=0.0,
                    status=AnalysisStatus.FAILED,
                    error_message=str(e)
                )
        
        # Calculate consolidated score
        self._calculate_consolidated_score(analysis_result, agent_responses)
        
        # Set total processing time
        analysis_result.total_processing_time = (datetime.now() - start_time).total_seconds()
        analysis_result.overall_status = AnalysisStatus.SUCCESS
        
        # Convert enums to strings for JSON serialization
        analysis_result = convert_enums_to_strings(analysis_result)
        
        self.logger.info(f"🎉 Analysis complete for tweet {tweet.tweet_id} in {analysis_result.total_processing_time:.2f}s")
        
        return analysis_result
    
    def _prepare_comprehensive_input(self, tweet: Tweet) -> str:
        """Prepare comprehensive input string for agents"""
        return f"""
TWEET CONTENT:
{tweet.text}

AUTHOR INFORMATION:
- Username: @{tweet.author_username}
- Display Name: {tweet.user_metadata.display_name if tweet.user_metadata else 'N/A'}
- Verified: {tweet.user_metadata.verified if tweet.user_metadata else 'N/A'}
- Followers: {tweet.user_metadata.public_metrics.get('followers_count', 'N/A') if tweet.user_metadata else 'N/A'}
- Account Created: {tweet.user_metadata.created_at if tweet.user_metadata else 'N/A'}
- Bio: {tweet.user_metadata.description if tweet.user_metadata else 'N/A'}

ENGAGEMENT METRICS:
- Likes: {tweet.like_count}
- Retweets: {tweet.retweet_count}
- Replies: {tweet.reply_count}
- Quotes: {tweet.quote_count}
- Engagement Score: {tweet.engagement_score:.2f}/10

TECHNICAL METADATA:
- Tweet ID: {tweet.tweet_id}
- Created: {tweet.created_at}
- Is Thread: {tweet.is_thread_tweet}
- Has Media: {tweet.has_media}
- External Links: {len(tweet.external_links)} links found
- Content Type: {tweet.content_type.value if tweet.content_type else 'N/A'}

MEDIA & LINKS:
{self._format_media_links(tweet)}

THREAD CONTEXT:
{self._format_thread_context(tweet)}
""".strip()
    
    def _format_media_links(self, tweet: Tweet) -> str:
        """Format media and links information"""
        if not tweet.external_links and not tweet.has_media:
            return "No external media or links detected."
        
        result = []
        
        if tweet.external_links:
            result.append(f"External Links ({len(tweet.external_links)}):")
            for i, link in enumerate(tweet.external_links, 1):
                result.append(f"  {i}. {link}")
        
        if tweet.has_media and tweet.media_attachments:
            if tweet.media_attachments.images_analyzed:
                result.append(f"Images ({len(tweet.media_attachments.images_analyzed)}):")
                for i, img in enumerate(tweet.media_attachments.images_analyzed, 1):
                    result.append(f"  {i}. {img.get('url', 'N/A')} ({img.get('type', 'unknown')})")
        
        return '\n'.join(result) if result else "No external media or links detected."
    
    def _format_thread_context(self, tweet: Tweet) -> str:
        """Format thread context information"""
        if not tweet.is_thread_tweet:
            return "Not part of a thread conversation."
        
        context = tweet.thread_context
        return f"""
Thread Information:
- Conversation ID: {context.conversation_id}
- In Reply To: {context.in_reply_to_user_id}
- Thread Position: {context.thread_position or 'Unknown'}
""".strip()
    
    def _calculate_consolidated_score(self, analysis_result: AnalysisResult, agent_responses: Dict[str, Any]):
        """Calculate weighted consolidated score from all agent responses"""
        individual_scores = {}
        total_weight = 0.0
        weighted_sum = 0.0
        
        # Extract scores from each agent that contributes to consolidation
        for agent_name, weight in self.agent_weights.items():
            if weight > 0 and agent_name in agent_responses:
                response = agent_responses[agent_name]
                
                # Extract agent_score using standardized field name
                score = response.get('agent_score')
                
                # Fallback to legacy field names if agent_score not found
                if score is None:
                    legacy_fields = [
                        'summary_score', 'preprocessing_score', 'context_score', 
                        'fact_check_score', 'depth_score', 'relevance_score',
                        'structure_score', 'reflection_score', 'credibility_score',
                        'consensus_score'
                    ]
                    
                    for field in legacy_fields:
                        if field in response:
                            score = response[field]
                            break
                
                # Use fallback score if still not found
                if score is None:
                    score = 5.0  # Default fallback
                
                try:
                    score = float(score)
                    individual_scores[agent_name] = score
                    weighted_sum += score * weight
                    total_weight += weight
                except (ValueError, TypeError):
                    self.logger.warning(f"⚠️ Invalid score from {agent_name}: {score}")
                    continue
        
        # Calculate final consolidated score
        if total_weight > 0:
            consolidated_score = weighted_sum / total_weight
            agents_contributing = len(individual_scores)
            
            reasoning = f"Consolidated score calculated from {agents_contributing} agents using standardized 'agent_score' field. " \
                       f"Weighted average prioritizes fact-checking ({self.agent_weights['fact_checker']*100:.0f}%), " \
                       f"context evaluation ({self.agent_weights['context_evaluator']*100:.0f}%), and " \
                       f"relevance analysis ({self.agent_weights['relevance_analyzer']*100:.0f}%) as most critical factors."
        else:
            consolidated_score = 5.0  # Default when no scores available
            agents_contributing = 0
            individual_scores = {}
            reasoning = "No valid agent scores found. Using default score of 5.0."
        
        # Set consolidated score in analysis result
        analysis_result.set_consolidated_score(
            total_agents=agents_contributing,
            individual_scores=individual_scores,
            weighted_avg=consolidated_score,
            final_score=consolidated_score,
            reasoning=reasoning
        ) 
      
    def _parse_json_safe(self, response_text: str, agent_name: str) -> Dict[str, Any]:
        """Safely parse JSON response with multiple fallback strategies"""
        
        # Strategy 1: Direct JSON parsing
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract JSON from code blocks
        try:
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                json_content = response_text[start:end].strip()
                return json.loads(json_content)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Strategy 3: Extract JSON from curly braces
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                json_content = response_text[start:end]
                return json.loads(json_content)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Strategy 4: Return fallback response
        self.logger.warning(f"🔧 JSON parsing failed for {agent_name}, using fallback")
        return {
            'error': f'JSON parsing failed for {agent_name}',
            'raw_response': response_text[:500],  # Truncate long responses
            'agent_score': 5.0,  # Fallback score
            'status': 'failed'
        }
     
    async def _execute_agent(self, prompt: str) -> str:
        """
        Execute a single agent with OpenAI API
        
        Args:
            prompt: Formatted prompt for the agent
            
        Returns:
            Raw response from the agent
        """
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a specialized AI agent for social media content analysis. Always respond with valid JSON format as specified in the prompt."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def _execute_agent_with_metadata(self, agent_name: str, comprehensive_input: str, agent_responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single agent with metadata tracking for parallel execution
        
        Args:
            agent_name: Name of the agent to execute
            comprehensive_input: Prepared input for the agent
            agent_responses: Current agent responses (empty for independent agents)
            
        Returns:
            Dictionary with response data and execution metadata
        """
        start_time = datetime.now()
        
        try:
            # Get appropriate prompt for independent agents
            prompt = getattr(self.prompts, f'get_{agent_name}_prompt')()
            input_data = {'comprehensive_input': comprehensive_input}
            
            # Format prompt with input data
            formatted_prompt = prompt.format(**input_data)
            
            # Execute agent with individual timeout
            response = await asyncio.wait_for(
                self._execute_agent(formatted_prompt),
                timeout=30  # 30 seconds timeout per agent
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Parse response
            parsed_response = self._parse_json_safe(response, agent_name)
            
            return {
                'response': parsed_response,
                'execution_time': execution_time,
                'status': 'success'
            }
            
        except asyncio.TimeoutError:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.warning(f"⏰ {agent_name} timed out after 30 seconds")
            return {
                'response': {'error': 'timeout', 'agent_score': 5.0},
                'execution_time': execution_time,
                'status': 'timeout'
            }
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"❌ {agent_name} failed: {str(e)}")
            return {
                'response': {'error': str(e), 'agent_score': 5.0},
                'execution_time': execution_time,
                'status': 'error'
            } 