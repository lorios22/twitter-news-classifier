#!/usr/bin/env python3
"""
📋 ENHANCED SCORE CONSOLIDATOR
=============================
Enhanced score consolidation logic that incorporates the new signal integrity agents.

This consolidator combines traditional agent scores with the new signal integrity
adjustments to produce more accurate and context-aware final scores.

Domain-Driven Design: Domain service for enhanced score consolidation.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ...entities.analysis_result import AnalysisResult, AnalysisStatus


@dataclass
class ScoreAdjustment:
    """Represents a score adjustment from signal integrity agents"""
    agent_name: str
    adjustment_type: str  # 'boost', 'penalty', 'modifier'
    adjustment_value: float
    reason: str
    confidence: float = 1.0


@dataclass
class ConsolidationResult:
    """Result of score consolidation"""
    base_score: float
    adjustments: List[ScoreAdjustment]
    final_score: float
    quality_flags: List[str]
    confidence_level: str
    reasoning: str


class EnhancedScoreConsolidator:
    """
    📋 Enhanced Score Consolidator
    
    Consolidates scores from all agents including the new signal integrity agents.
    
    Features:
    - Traditional weighted scoring
    - Signal integrity adjustments
    - Context-aware scoring
    - Quality flag management
    - Confidence assessment
    """
    
    def __init__(self, agent_weights: Dict[str, float]):
        """Initialize enhanced score consolidator"""
        self.logger = logging.getLogger(__name__)
        self.agent_weights = agent_weights
        
        # Define score adjustment parameters
        self.adjustment_config = {
            'sarcasm_protection': {
                'max_boost': 2.0,
                'threshold': 0.5  # Sarcasm probability threshold
            },
            'echo_velocity_boost': {
                'max_boost': 1.5,
                'threshold': 0.5,  # Echo velocity threshold
                'scaling': 2.0
            },
            'slop_penalty': {
                'max_penalty': 2.5,
                'threshold': 0.7,  # Slop score threshold
                'scaling': 3.0
            },
            'tone_penalty': {
                'max_penalty': 2.0,
                'threshold': 0.3,  # Tone penalty threshold
                'scaling': 2.5
            }
        }
    
    def consolidate_scores(self, analysis_result: AnalysisResult) -> ConsolidationResult:
        """
        Consolidate all agent scores with signal integrity adjustments
        
        Args:
            analysis_result: Analysis result containing all agent responses
            
        Returns:
            ConsolidationResult with final score and reasoning
        """
        try:
            # Step 1: Calculate base score from traditional agents
            base_score, individual_scores = self._calculate_base_score(analysis_result)
            
            # Step 2: Apply signal integrity adjustments
            adjustments = self._calculate_signal_adjustments(analysis_result)
            
            # Step 3: Calculate final score
            final_score = self._apply_adjustments(base_score, adjustments)
            
            # Step 4: Generate quality flags
            quality_flags = self._generate_quality_flags(analysis_result, adjustments)
            
            # Step 5: Assess confidence level
            confidence_level = self._assess_confidence_level(analysis_result, adjustments)
            
            # Step 6: Generate reasoning
            reasoning = self._generate_reasoning(
                base_score, adjustments, final_score, individual_scores
            )
            
            result = ConsolidationResult(
                base_score=base_score,
                adjustments=adjustments,
                final_score=final_score,
                quality_flags=quality_flags,
                confidence_level=confidence_level,
                reasoning=reasoning
            )
            
            self.logger.info(
                f"Score consolidation complete: {base_score:.2f} → {final_score:.2f} "
                f"({len(adjustments)} adjustments, {confidence_level} confidence)"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in score consolidation: {e}")
            # Return fallback result
            return ConsolidationResult(
                base_score=5.0,
                adjustments=[],
                final_score=5.0,
                quality_flags=['consolidation_error'],
                confidence_level='low',
                reasoning=f"Error in consolidation: {str(e)}"
            )
    
    def _calculate_base_score(self, analysis_result: AnalysisResult) -> Tuple[float, Dict[str, float]]:
        """Calculate base score from traditional agents"""
        individual_scores = {}
        total_weight = 0.0
        weighted_sum = 0.0
        
        # Traditional agents that contribute to base score
        traditional_agents = [
            'summary_agent', 'input_preprocessor', 'context_evaluator',
            'fact_checker', 'depth_analyzer', 'relevance_analyzer',
            'structure_analyzer', 'reflective_agent', 'metadata_ranking_agent',
            'consensus_agent'
        ]
        
        for agent_name in traditional_agents:
            weight = self.agent_weights.get(agent_name, 0.0)
            if weight <= 0:
                continue
                
            agent_response = analysis_result.agent_responses.get(agent_name)
            if not agent_response or agent_response.get('status') != AnalysisStatus.SUCCESS:
                continue
            
            response_data = agent_response.get('response_data', {})
            score = self._extract_agent_score(response_data, agent_name)
            
            if score is not None:
                individual_scores[agent_name] = score
                weighted_sum += score * weight
                total_weight += weight
        
        # Calculate base score
        base_score = weighted_sum / total_weight if total_weight > 0 else 5.0
        
        self.logger.debug(
            f"Base score calculation: {weighted_sum:.2f} / {total_weight:.2f} = {base_score:.2f} "
            f"(from {len(individual_scores)} agents)"
        )
        
        return base_score, individual_scores
    
    def _extract_agent_score(self, response_data: Dict[str, Any], agent_name: str) -> Optional[float]:
        """Extract score from agent response data"""
        # Try standard field first
        score = response_data.get('agent_score')
        
        if score is not None:
            try:
                return float(score)
            except (ValueError, TypeError):
                pass
        
        # Try legacy field names
        legacy_mappings = {
            'summary_agent': 'summary_score',
            'input_preprocessor': 'preprocessing_score',
            'context_evaluator': 'context_score',
            'fact_checker': 'fact_check_score',
            'depth_analyzer': 'depth_score',
            'relevance_analyzer': 'relevance_score',
            'structure_analyzer': 'structure_score',
            'reflective_agent': 'reflection_score',
            'metadata_ranking_agent': 'credibility_score',
            'consensus_agent': 'consensus_score'
        }
        
        legacy_field = legacy_mappings.get(agent_name)
        if legacy_field and legacy_field in response_data:
            try:
                return float(response_data[legacy_field])
            except (ValueError, TypeError):
                pass
        
        # Fallback
        self.logger.warning(f"Could not extract score from {agent_name}")
        return 5.0  # Default fallback score
    
    def _calculate_signal_adjustments(self, analysis_result: AnalysisResult) -> List[ScoreAdjustment]:
        """Calculate adjustments from signal integrity agents"""
        adjustments = []
        
        # Sarcasm Sentinel adjustments
        sarcasm_adj = self._calculate_sarcasm_adjustment(analysis_result)
        if sarcasm_adj:
            adjustments.append(sarcasm_adj)
        
        # Echo Mapper adjustments
        echo_adj = self._calculate_echo_adjustment(analysis_result)
        if echo_adj:
            adjustments.append(echo_adj)
        
        # Slop Filter adjustments
        slop_adj = self._calculate_slop_adjustment(analysis_result)
        if slop_adj:
            adjustments.append(slop_adj)
        
        # Banned Phrase Skeptic adjustments
        tone_adj = self._calculate_tone_adjustment(analysis_result)
        if tone_adj:
            adjustments.append(tone_adj)
        
        return adjustments
    
    def _calculate_sarcasm_adjustment(self, analysis_result: AnalysisResult) -> Optional[ScoreAdjustment]:
        """Calculate sarcasm-based score adjustment"""
        sarcasm_response = analysis_result.agent_responses.get('sarcasm_sentinel')
        if not sarcasm_response or sarcasm_response.get('status') != AnalysisStatus.SUCCESS:
            return None
        
        sarcasm_data = sarcasm_response.get('response_data', {})
        is_sarcastic = sarcasm_data.get('is_sarcastic', False)
        p_sarcasm = sarcasm_data.get('p_sarcasm', 0.0)
        
        if not is_sarcastic or p_sarcasm < self.adjustment_config['sarcasm_protection']['threshold']:
            return None
        
        # Check if fact checker gave a low score that might be due to sarcasm
        fact_response = analysis_result.agent_responses.get('fact_checker')
        if fact_response and fact_response.get('status') == AnalysisStatus.SUCCESS:
            fact_data = fact_response.get('response_data', {})
            fact_score = self._extract_agent_score(fact_data, 'fact_checker')
            
            if fact_score and fact_score < 4.0:
                # Apply sarcasm protection boost
                boost = min(
                    self.adjustment_config['sarcasm_protection']['max_boost'],
                    (0.8 - p_sarcasm) * 3.0  # Stronger boost for higher sarcasm confidence
                )
                
                return ScoreAdjustment(
                    agent_name='sarcasm_sentinel',
                    adjustment_type='boost',
                    adjustment_value=boost,
                    reason=f"Sarcasm protection: prevented over-penalization (p_sarcasm={p_sarcasm:.2f})",
                    confidence=p_sarcasm
                )
        
        return None
    
    def _calculate_echo_adjustment(self, analysis_result: AnalysisResult) -> Optional[ScoreAdjustment]:
        """Calculate echo velocity-based score adjustment"""
        echo_response = analysis_result.agent_responses.get('echo_mapper')
        if not echo_response or echo_response.get('status') != AnalysisStatus.SUCCESS:
            return None
        
        echo_data = echo_response.get('response_data', {})
        echo_velocity = echo_data.get('echo_velocity', 0.0)
        
        if echo_velocity < self.adjustment_config['echo_velocity_boost']['threshold']:
            return None
        
        # Calculate boost based on velocity
        velocity_excess = echo_velocity - self.adjustment_config['echo_velocity_boost']['threshold']
        boost = min(
            self.adjustment_config['echo_velocity_boost']['max_boost'],
            velocity_excess * self.adjustment_config['echo_velocity_boost']['scaling']
        )
        
        if boost > 0.1:  # Only apply significant boosts
            return ScoreAdjustment(
                agent_name='echo_mapper',
                adjustment_type='boost',
                adjustment_value=boost,
                reason=f"Cross-platform viral boost: echo_velocity={echo_velocity:.2f}",
                confidence=min(1.0, echo_velocity)
            )
        
        return None
    
    def _calculate_slop_adjustment(self, analysis_result: AnalysisResult) -> Optional[ScoreAdjustment]:
        """Calculate slop-based score penalty"""
        slop_response = analysis_result.agent_responses.get('slop_filter')
        if not slop_response or slop_response.get('status') != AnalysisStatus.SUCCESS:
            return None
        
        slop_data = slop_response.get('response_data', {})
        slop_score = slop_data.get('slop_score', 0.0)
        
        if slop_score < self.adjustment_config['slop_penalty']['threshold']:
            return None
        
        # Calculate penalty based on slop score
        slop_excess = slop_score - self.adjustment_config['slop_penalty']['threshold']
        penalty = min(
            self.adjustment_config['slop_penalty']['max_penalty'],
            slop_excess * self.adjustment_config['slop_penalty']['scaling']
        )
        
        if penalty > 0.1:  # Only apply significant penalties
            return ScoreAdjustment(
                agent_name='slop_filter',
                adjustment_type='penalty',
                adjustment_value=-penalty,
                reason=f"Content quality penalty: slop_score={slop_score:.2f}",
                confidence=slop_score
            )
        
        return None
    
    def _calculate_tone_adjustment(self, analysis_result: AnalysisResult) -> Optional[ScoreAdjustment]:
        """Calculate tone-based score penalty"""
        tone_response = analysis_result.agent_responses.get('banned_phrase_skeptic')
        if not tone_response or tone_response.get('status') != AnalysisStatus.SUCCESS:
            return None
        
        tone_data = tone_response.get('response_data', {})
        tone_penalty = tone_data.get('tone_penalty', 0.0)
        banned_terms = tone_data.get('banned_terms', [])
        
        if tone_penalty < self.adjustment_config['tone_penalty']['threshold']:
            return None
        
        # Calculate penalty based on tone penalty
        penalty_excess = tone_penalty - self.adjustment_config['tone_penalty']['threshold']
        penalty = min(
            self.adjustment_config['tone_penalty']['max_penalty'],
            penalty_excess * self.adjustment_config['tone_penalty']['scaling']
        )
        
        if penalty > 0.1:  # Only apply significant penalties
            return ScoreAdjustment(
                agent_name='banned_phrase_skeptic',
                adjustment_type='penalty',
                adjustment_value=-penalty,
                reason=f"Editorial tone penalty: {len(banned_terms)} banned terms",
                confidence=tone_penalty
            )
        
        return None
    
    def _apply_adjustments(self, base_score: float, adjustments: List[ScoreAdjustment]) -> float:
        """Apply all adjustments to base score"""
        final_score = base_score
        
        for adjustment in adjustments:
            final_score += adjustment.adjustment_value
            self.logger.debug(
                f"Applied {adjustment.adjustment_type} from {adjustment.agent_name}: "
                f"{adjustment.adjustment_value:+.2f} (reason: {adjustment.reason})"
            )
        
        # Clamp to valid range
        final_score = max(0.1, min(10.0, final_score))
        
        return round(final_score, 2)
    
    def _generate_quality_flags(self, analysis_result: AnalysisResult, 
                              adjustments: List[ScoreAdjustment]) -> List[str]:
        """Generate quality flags based on analysis"""
        flags = []
        
        # Check for signal integrity flags
        for adjustment in adjustments:
            if adjustment.adjustment_type == 'penalty':
                if adjustment.agent_name == 'slop_filter':
                    flags.append('low_content_quality')
                elif adjustment.agent_name == 'banned_phrase_skeptic':
                    flags.append('editorial_violations')
            elif adjustment.adjustment_type == 'boost':
                if adjustment.agent_name == 'echo_mapper':
                    flags.append('viral_content')
                elif adjustment.agent_name == 'sarcasm_sentinel':
                    flags.append('sarcasm_protected')
        
        # Check for sarcasm detection
        sarcasm_response = analysis_result.agent_responses.get('sarcasm_sentinel')
        if sarcasm_response and sarcasm_response.get('status') == AnalysisStatus.SUCCESS:
            sarcasm_data = sarcasm_response.get('response_data', {})
            if sarcasm_data.get('is_sarcastic'):
                flags.append('sarcastic_content')
        
        # Check for latency issues (if present)
        latency_response = analysis_result.agent_responses.get('latency_guard')
        if latency_response and latency_response.get('status') == AnalysisStatus.SUCCESS:
            latency_data = latency_response.get('response_data', {})
            if latency_data.get('repriced'):
                flags.append('temporal_misalignment')
        
        return flags
    
    def _assess_confidence_level(self, analysis_result: AnalysisResult,
                               adjustments: List[ScoreAdjustment]) -> str:
        """Assess confidence level in the final score"""
        # Count successful agents
        successful_agents = sum(
            1 for response in analysis_result.agent_responses.values()
            if response.get('status') == AnalysisStatus.SUCCESS
        )
        
        total_agents = len(analysis_result.agent_responses)
        success_rate = successful_agents / total_agents if total_agents > 0 else 0
        
        # Factor in adjustment confidence
        avg_adjustment_confidence = sum(adj.confidence for adj in adjustments) / len(adjustments) if adjustments else 1.0
        
        # Calculate overall confidence
        overall_confidence = (success_rate + avg_adjustment_confidence) / 2
        
        if overall_confidence >= 0.8:
            return 'high'
        elif overall_confidence >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _generate_reasoning(self, base_score: float, adjustments: List[ScoreAdjustment],
                          final_score: float, individual_scores: Dict[str, float]) -> str:
        """Generate human-readable reasoning for the score"""
        reasoning_parts = []
        
        # Base score explanation
        reasoning_parts.append(
            f"Base score: {base_score:.2f} (weighted average of {len(individual_scores)} traditional agents)"
        )
        
        # Adjustment explanations
        if adjustments:
            reasoning_parts.append("Signal integrity adjustments:")
            for adj in adjustments:
                reasoning_parts.append(f"  • {adj.reason}: {adj.adjustment_value:+.2f}")
        
        # Final score
        total_adjustment = sum(adj.adjustment_value for adj in adjustments)
        reasoning_parts.append(
            f"Final score: {base_score:.2f} + {total_adjustment:+.2f} = {final_score:.2f}"
        )
        
        return " | ".join(reasoning_parts)
    
    def get_score_breakdown(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """Get detailed breakdown of score calculation"""
        consolidation_result = self.consolidate_scores(analysis_result)
        
        return {
            'base_score': consolidation_result.base_score,
            'final_score': consolidation_result.final_score,
            'adjustments': [
                {
                    'agent': adj.agent_name,
                    'type': adj.adjustment_type,
                    'value': adj.adjustment_value,
                    'reason': adj.reason,
                    'confidence': adj.confidence
                }
                for adj in consolidation_result.adjustments
            ],
            'quality_flags': consolidation_result.quality_flags,
            'confidence_level': consolidation_result.confidence_level,
            'reasoning': consolidation_result.reasoning
        }