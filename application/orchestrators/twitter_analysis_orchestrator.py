#!/usr/bin/env python3
"""
🎯 TWITTER ANALYSIS ORCHESTRATOR
================================
Main orchestrator for the complete Twitter news classification workflow.

This orchestrator manages:
- Phase 1: Tweet extraction with comprehensive metadata
- Phase 2: Multi-agent analysis of extracted data
- Error handling and recovery between phases
- Data persistence and workflow management
- Integration of results

Domain-Driven Design: Application orchestrator for complete workflow.
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from domain.services.core_analysis.tweet_extraction_service import TweetExtractionService, ExtractionConfig, ExtractionResult
from domain.services.core_analysis.multi_agent_analysis_service import MultiAgentAnalysisService, AnalysisConfig
from domain.services.core_analysis.multi_agent_analysis_service import AnalysisResult as ServiceAnalysisResult
from domain.services.core_analysis.multi_agent_analyzer import MultiAgentAnalyzer
from infrastructure.adapters.twitter_api_adapter import TwitterApiAdapter, TwitterApiConfig
from infrastructure.repositories.file_repository import FileRepository


@dataclass
class WorkflowConfig:
    """Configuration for complete analysis workflow"""
    # Tweet extraction settings
    max_tweets: int = 30
    hours_back: int = 24
    trusted_accounts: List[str] = None
    
    # Analysis settings
    max_retries: int = 3
    retry_delay: int = 30
    batch_size: int = 5
    continue_on_api_failure: bool = True
    
    # Output settings
    output_base_directory: str = "data/workflow_runs"
    cleanup_old_runs: bool = True
    max_old_runs_to_keep: int = 5
    
    # Error handling
    enable_extraction_recovery: bool = True
    enable_analysis_recovery: bool = True
    save_intermediate_results: bool = True


@dataclass
class WorkflowResult:
    """Result of complete workflow execution"""
    workflow_id: str
    timestamp: datetime
    extraction_result: Optional[ExtractionResult]
    analysis_result: Optional[ServiceAnalysisResult]
    total_processing_time: float
    overall_status: str  # 'success', 'partial', 'extraction_failed', 'analysis_failed'
    phase_completed: str  # 'extraction', 'analysis', 'both', 'none'
    error_summary: List[str]
    data_preserved: bool
    recommendations: List[str]


class TwitterAnalysisOrchestrator:
    """
    🎯 Main Twitter Analysis Orchestrator
    
    Manages the complete workflow from tweet extraction to analysis results.
    
    Features:
    - Two-phase processing with independent error handling
    - Data persistence between phases
    - Recovery from API failures
    - Comprehensive workflow management
    - Clean separation of concerns
    """
    
    def __init__(self,
                 twitter_api_key: str,
                 twitter_api_secret: str,
                 twitter_access_token: str,
                 twitter_access_token_secret: str,
                 twitter_bearer_token: str,
                 openai_api_key: str):
        """Initialize the orchestrator with all required API keys"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize core services
        self.file_repository = FileRepository()
        
        # Create Twitter API configuration
        twitter_config = TwitterApiConfig(
            consumer_key=twitter_api_key,
            consumer_secret=twitter_api_secret,
            access_token=twitter_access_token,
            access_token_secret=twitter_access_token_secret,
            bearer_token=twitter_bearer_token
        )
        
        self.twitter_adapter = TwitterApiAdapter(config=twitter_config)
        
        self.extraction_service = TweetExtractionService(
            twitter_adapter=self.twitter_adapter,
            file_repository=self.file_repository
        )
        
        self.multi_agent_analyzer = MultiAgentAnalyzer(openai_api_key)
        
        self.analysis_service = MultiAgentAnalysisService(
            multi_agent_analyzer=self.multi_agent_analyzer,
            file_repository=self.file_repository
        )
        
        # Workflow statistics
        self.workflow_stats = {
            'workflows_executed': 0,
            'successful_extractions': 0,
            'successful_analyses': 0,
            'total_tweets_processed': 0,
            'total_errors': 0
        }
    
    async def execute_complete_workflow(self, config: WorkflowConfig) -> WorkflowResult:
        """
        Execute the complete Twitter analysis workflow
        
        Args:
            config: Workflow configuration
            
        Returns:
            WorkflowResult with complete execution details
        """
        start_time = datetime.now()
        workflow_id = f"WORKFLOW_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info("=" * 60)
        self.logger.info(f"🚀 STARTING TWITTER ANALYSIS WORKFLOW: {workflow_id}")
        self.logger.info("=" * 60)
        
        # Create workflow directory
        workflow_dir = Path(config.output_base_directory) / workflow_id
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize result tracking
        extraction_result = None
        analysis_result = None
        error_summary = []
        phase_completed = "none"
        data_preserved = False
        
        try:
            # Cleanup old runs if enabled
            if config.cleanup_old_runs:
                await self._cleanup_old_workflow_runs(config)
            
            # PHASE 1: TWEET EXTRACTION
            self.logger.info("📡 PHASE 1: TWEET EXTRACTION")
            self.logger.info("-" * 40)
            
            extraction_result = await self._execute_extraction_phase(config, workflow_dir)
            
            if extraction_result and extraction_result.status in ['success', 'partial']:
                phase_completed = "extraction"
                data_preserved = True
                self.workflow_stats['successful_extractions'] += 1
                self.workflow_stats['total_tweets_processed'] += extraction_result.total_tweets_extracted
                
                self.logger.info(f"✅ Extraction phase completed: {extraction_result.total_tweets_extracted} tweets extracted")
                
                # PHASE 2: MULTI-AGENT ANALYSIS
                self.logger.info("🤖 PHASE 2: MULTI-AGENT ANALYSIS")
                self.logger.info("-" * 40)
                
                analysis_result = await self._execute_analysis_phase(
                    extraction_result, config, workflow_dir
                )
                
                if analysis_result and analysis_result.status in ['success', 'partial']:
                    phase_completed = "both"
                    self.workflow_stats['successful_analyses'] += 1
                    
                    self.logger.info(f"✅ Analysis phase completed: {analysis_result.successful_analyses} analyses completed")
                else:
                    error_summary.append("Analysis phase failed but extraction data preserved")
                    if analysis_result and analysis_result.error_details:
                        error_summary.extend(analysis_result.error_details)
            else:
                error_summary.append("Extraction phase failed")
                if extraction_result and extraction_result.error_details:
                    error_summary.extend(extraction_result.error_details)
            
            # Calculate final status
            if phase_completed == "both":
                overall_status = "success"
            elif phase_completed == "extraction":
                overall_status = "analysis_failed"
            else:
                overall_status = "extraction_failed"
            
        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            error_summary.append(error_msg)
            overall_status = "extraction_failed"
            self.workflow_stats['total_errors'] += 1
        
        # Calculate processing time
        total_processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create workflow result
        workflow_result = WorkflowResult(
            workflow_id=workflow_id,
            timestamp=start_time,
            extraction_result=extraction_result,
            analysis_result=analysis_result,
            total_processing_time=total_processing_time,
            overall_status=overall_status,
            phase_completed=phase_completed,
            error_summary=error_summary,
            data_preserved=data_preserved,
            recommendations=self._generate_workflow_recommendations(
                extraction_result, analysis_result, error_summary
            )
        )
        
        # Save workflow result
        await self._save_workflow_result(workflow_result, workflow_dir)
        
        # Log final summary
        self._log_workflow_summary(workflow_result)
        
        self.workflow_stats['workflows_executed'] += 1
        return workflow_result
    
    async def _execute_extraction_phase(self, 
                                       config: WorkflowConfig, 
                                       workflow_dir: Path) -> Optional[ExtractionResult]:
        """Execute tweet extraction phase"""
        try:
            extraction_config = ExtractionConfig(
                max_tweets=config.max_tweets,
                hours_back=config.hours_back,
                accounts_list=config.trusted_accounts,
                enable_thread_extraction=True,
                enable_media_analysis=True,
                enable_url_extraction=True,
                output_directory=str(workflow_dir / "extraction"),
                batch_size=10
            )
            
            return await self.extraction_service.extract_comprehensive_data(extraction_config)
            
        except Exception as e:
            self.logger.error(f"❌ Extraction phase failed: {str(e)}")
            return None
    
    async def _execute_analysis_phase(self, 
                                    extraction_result: ExtractionResult,
                                    config: WorkflowConfig,
                                    workflow_dir: Path) -> Optional[ServiceAnalysisResult]:
        """Execute multi-agent analysis phase"""
        try:
            analysis_config = AnalysisConfig(
                input_tweets_file=extraction_result.tweets_file_path,
                output_directory=str(workflow_dir / "analysis"),
                max_retries=config.max_retries,
                retry_delay=config.retry_delay,
                batch_size=config.batch_size,
                enable_error_recovery=config.enable_analysis_recovery,
                continue_on_failure=config.continue_on_api_failure,
                save_intermediate_results=config.save_intermediate_results
            )
            
            return await self.analysis_service.analyze_extracted_data(analysis_config)
            
        except Exception as e:
            self.logger.error(f"❌ Analysis phase failed: {str(e)}")
            return None
    
    async def _cleanup_old_workflow_runs(self, config: WorkflowConfig):
        """Clean up old workflow runs to save space"""
        try:
            base_dir = Path(config.output_base_directory)
            if not base_dir.exists():
                return
            
            # Get all workflow directories
            workflow_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('WORKFLOW_')]
            
            # Sort by creation time (newest first)
            workflow_dirs.sort(key=lambda x: x.stat().st_ctime, reverse=True)
            
            # Remove old runs beyond the limit
            if len(workflow_dirs) > config.max_old_runs_to_keep:
                old_runs = workflow_dirs[config.max_old_runs_to_keep:]
                
                for old_run in old_runs:
                    try:
                        import shutil
                        shutil.rmtree(old_run)
                        self.logger.info(f"🧹 Cleaned up old workflow run: {old_run.name}")
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to clean up {old_run.name}: {str(e)}")
                        
        except Exception as e:
            self.logger.warning(f"⚠️ Cleanup failed: {str(e)}")
    
    async def _save_workflow_result(self, result: WorkflowResult, workflow_dir: Path):
        """Save workflow result to file"""
        try:
            result_file = workflow_dir / 'workflow_result.json'
            
            # Convert result to dictionary for JSON serialization
            result_dict = asdict(result)
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"💾 Workflow result saved: {result_file}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to save workflow result: {str(e)}")
    
    def _generate_workflow_recommendations(self, 
                                         extraction_result: Optional[ExtractionResult],
                                         analysis_result: Optional[ServiceAnalysisResult],
                                         errors: List[str]) -> List[str]:
        """Generate recommendations based on workflow execution"""
        recommendations = []
        
        if extraction_result and extraction_result.status == 'success':
            recommendations.append("✅ Tweet extraction completed successfully")
            
            if analysis_result and analysis_result.status == 'success':
                recommendations.append("✅ Multi-agent analysis completed successfully")
                recommendations.append("📊 Complete workflow successful - results ready for use")
            elif analysis_result and analysis_result.status == 'partial':
                recommendations.append("⚠️ Partial analysis completed - consider retrying failed tweets")
            else:
                recommendations.append("❌ Analysis failed but tweet data preserved - can retry analysis phase")
                recommendations.append("💡 Check OpenAI API key and rate limits")
        else:
            recommendations.append("❌ Tweet extraction failed - check Twitter API credentials")
            recommendations.append("💡 Verify account list and API permissions")
        
        if len(errors) > 5:
            recommendations.append("⚠️ High error rate detected - consider reducing batch size or increasing delays")
        
        return recommendations
    
    def _log_workflow_summary(self, result: WorkflowResult):
        """Log comprehensive workflow summary"""
        self.logger.info("=" * 60)
        self.logger.info("📊 WORKFLOW EXECUTION SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"🆔 Workflow ID: {result.workflow_id}")
        self.logger.info(f"⏱️  Total Time: {result.total_processing_time:.2f} seconds")
        self.logger.info(f"📈 Overall Status: {result.overall_status}")
        self.logger.info(f"🏁 Phases Completed: {result.phase_completed}")
        self.logger.info(f"💾 Data Preserved: {result.data_preserved}")
        
        if result.extraction_result:
            self.logger.info(f"📡 Tweets Extracted: {result.extraction_result.total_tweets_extracted}")
        
        if result.analysis_result:
            self.logger.info(f"🤖 Analyses Completed: {result.analysis_result.successful_analyses}")
        
        if result.error_summary:
            self.logger.info(f"❌ Errors: {len(result.error_summary)}")
        
        self.logger.info("=" * 60)
        
        # Log recommendations
        if result.recommendations:
            self.logger.info("💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                self.logger.info(f"   {rec}")
            self.logger.info("=" * 60)
    
    def get_workflow_stats(self) -> Dict:
        """Get workflow execution statistics"""
        return self.workflow_stats.copy()
    
    def reset_workflow_stats(self):
        """Reset workflow statistics"""
        self.workflow_stats = {
            'workflows_executed': 0,
            'successful_extractions': 0,
            'successful_analyses': 0,
            'total_tweets_processed': 0,
            'total_errors': 0
        } 