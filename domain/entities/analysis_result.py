#!/usr/bin/env python3
"""
📊 ANALYSIS RESULT ENTITY
=========================
Core domain entity representing analysis results from multi-agent processing.

Domain-Driven Design: Core domain entity containing analysis outcomes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum


class AnalysisStatus(Enum):
    """Analysis status enumeration"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    PENDING = "pending"


class QualityLevel(Enum):
    """Quality level classification"""
    EXCELLENT = "excellent"  # 9-10
    GOOD = "good"           # 7-8.9
    AVERAGE = "average"     # 5-6.9
    POOR = "poor"          # 3-4.9
    VERY_POOR = "very_poor" # 0-2.9


@dataclass
class AgentResponse:
    """Individual agent response data"""
    agent_name: str
    response_data: Dict[str, Any]
    agent_score: float
    execution_time: float
    status: AnalysisStatus
    error_message: Optional[str] = None


@dataclass
class ConsolidatedScore:
    """Consolidated scoring information"""
    total_agents_contributing: int
    individual_scores: Dict[str, float]
    weighted_average: float
    consolidated_score: float
    score_range: str
    confidence_interval: str
    status: AnalysisStatus
    detailed_reasoning: str


@dataclass
class MediaAnalysisResult:
    """Media analysis results"""
    links_analyzed: List[Dict[str, Any]] = field(default_factory=list)
    images_analyzed: List[Dict[str, Any]] = field(default_factory=list)
    total_processing_time: float = 0.0
    summary: Dict[str, Any] = field(default_factory=dict)
    analysis_complete: bool = True


@dataclass
class ThreadAnalysisResult:
    """Thread analysis results"""
    is_thread: bool = False
    thread_tweets: List[Dict[str, Any]] = field(default_factory=list)
    thread_summary: str = ""
    conversation_context: Optional[Dict[str, Any]] = None


@dataclass
class AnalysisResult:
    """
    📊 Core Analysis Result entity representing comprehensive analysis outcomes
    
    Contains all analysis results from multi-agent processing including
    individual agent responses, consolidated scores, and metadata.
    """
    
    # Core identification
    content_id: str
    run_id: str
    analysis_timestamp: datetime
    
    # Agent responses
    agent_responses: Dict[str, AgentResponse] = field(default_factory=dict)
    
    # Consolidated results
    consolidated_score: Optional[ConsolidatedScore] = None
    
    # Media and thread analysis
    media_analysis: Optional[MediaAnalysisResult] = None
    thread_analysis: Optional[ThreadAnalysisResult] = None
    
    # Overall analysis metadata
    total_processing_time: float = 0.0
    analysis_version: str = "4.0"
    analysis_type: str = "enhanced_multi_agent"
    overall_status: AnalysisStatus = AnalysisStatus.PENDING
    
    # Quality assessment
    quality_level: Optional[QualityLevel] = None
    quality_indicators: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization processing"""
        if not self.analysis_timestamp:
            self.analysis_timestamp = datetime.now()
        
        # Determine quality level based on consolidated score
        if self.consolidated_score:
            score = self.consolidated_score.consolidated_score
            if score >= 9.0:
                self.quality_level = QualityLevel.EXCELLENT
            elif score >= 7.0:
                self.quality_level = QualityLevel.GOOD
            elif score >= 5.0:
                self.quality_level = QualityLevel.AVERAGE
            elif score >= 3.0:
                self.quality_level = QualityLevel.POOR
            else:
                self.quality_level = QualityLevel.VERY_POOR
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate of agent responses"""
        if not self.agent_responses:
            return 0.0
        
        successful = sum(1 for response in self.agent_responses.values() 
                        if response.status == AnalysisStatus.SUCCESS)
        return successful / len(self.agent_responses) * 100.0
    
    @property
    def average_agent_score(self) -> float:
        """Calculate average score across all agents"""
        if not self.agent_responses:
            return 0.0
        
        scores = [response.agent_score for response in self.agent_responses.values() 
                 if response.status == AnalysisStatus.SUCCESS]
        return sum(scores) / len(scores) if scores else 0.0
    
    @property
    def has_media_analysis(self) -> bool:
        """Check if media analysis was performed"""
        return (self.media_analysis is not None and 
                self.media_analysis.analysis_complete)
    
    @property
    def has_thread_analysis(self) -> bool:
        """Check if thread analysis was performed"""
        return (self.thread_analysis is not None and 
                self.thread_analysis.is_thread)
    
    def add_agent_response(self, agent_name: str, response_data: Dict[str, Any], 
                          execution_time: float, status: AnalysisStatus = AnalysisStatus.SUCCESS,
                          error_message: Optional[str] = None):
        """Add an agent response to the analysis result"""
        # Extract agent score from response data
        agent_score = response_data.get('agent_score', 5.0)  # Default fallback
        
        self.agent_responses[agent_name] = AgentResponse(
            agent_name=agent_name,
            response_data=response_data,
            agent_score=agent_score,
            execution_time=execution_time,
            status=status,
            error_message=error_message
        )
    
    def set_consolidated_score(self, total_agents: int, individual_scores: Dict[str, float],
                              weighted_avg: float, final_score: float, reasoning: str):
        """Set the consolidated scoring information"""
        score_values = list(individual_scores.values())
        score_range = f"{min(score_values):.1f} - {max(score_values):.1f}" if score_values else "N/A"
        confidence_interval = f"±{(max(score_values) - min(score_values)) / 2:.1f}" if len(score_values) > 1 else "±0.0"
        
        self.consolidated_score = ConsolidatedScore(
            total_agents_contributing=total_agents,
            individual_scores=individual_scores,
            weighted_average=weighted_avg,
            consolidated_score=final_score,
            score_range=score_range,
            confidence_interval=confidence_interval,
            status=AnalysisStatus.SUCCESS,
            detailed_reasoning=reasoning
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis result to dictionary representation"""
        return {
            "content_id": self.content_id,
            "run_id": self.run_id,
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
            "agent_responses": {
                name: {
                    "agent_name": response.agent_name,
                    "response_data": response.response_data,
                    "agent_score": response.agent_score,
                    "execution_time": response.execution_time,
                    "status": response.status.value,
                    "error_message": response.error_message
                }
                for name, response in self.agent_responses.items()
            },
            "consolidated_score": {
                "total_agents_contributing": self.consolidated_score.total_agents_contributing,
                "individual_scores": self.consolidated_score.individual_scores,
                "weighted_average": self.consolidated_score.weighted_average,
                "consolidated_score": self.consolidated_score.consolidated_score,
                "score_range": self.consolidated_score.score_range,
                "confidence_interval": self.consolidated_score.confidence_interval,
                "status": self.consolidated_score.status.value,
                "detailed_reasoning": self.consolidated_score.detailed_reasoning
            } if self.consolidated_score else None,
            "media_analysis": self.media_analysis.__dict__ if self.media_analysis else None,
            "thread_analysis": self.thread_analysis.__dict__ if self.thread_analysis else None,
            "total_processing_time": self.total_processing_time,
            "analysis_version": self.analysis_version,
            "analysis_type": self.analysis_type,
            "overall_status": self.overall_status.value,
            "quality_level": self.quality_level.value if self.quality_level else None,
            "quality_indicators": self.quality_indicators,
            "success_rate": self.success_rate,
            "average_agent_score": self.average_agent_score,
            "has_media_analysis": self.has_media_analysis,
            "has_thread_analysis": self.has_thread_analysis
        } 