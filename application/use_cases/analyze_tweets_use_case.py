#!/usr/bin/env python3
"""
🎯 ANALYZE TWEETS USE CASE
=========================
Application layer use case for orchestrating tweet analysis workflow.

Domain-Driven Design: Application layer use case orchestrating domain services.
Coordinates Twitter extraction, multi-agent analysis, and result persistence.
"""

import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from domain.entities.tweet import Tweet
from domain.entities.analysis_result import AnalysisResult
from domain.services.multi_agent_analyzer import MultiAgentAnalyzer
from infrastructure.adapters.twitter_api_adapter import TwitterApiAdapter
from infrastructure.repositories.file_repository import FileRepository


@dataclass
class AnalysisConfig:
    """Configuration for tweet analysis"""
    max_tweets: int = 30
    hours_back: int = 24
    enable_thread_analysis: bool = True
    enable_media_analysis: bool = True
    output_format: str = "json"
    save_individual_results: bool = True
    generate_summary: bool = True


class AnalyzeTweetsUseCase:
    """
    🎯 Main use case for comprehensive tweet analysis
    
    Orchestrates the complete workflow:
    1. Extract tweets from specified accounts via Twitter API
    2. Analyze each tweet using multi-agent system
    3. Process threads and media content
    4. Save individual and summary results
    5. Generate comprehensive reports
    """
    
    def __init__(self, 
                 twitter_adapter: TwitterApiAdapter,
                 multi_agent_analyzer: MultiAgentAnalyzer,
                 file_repository: FileRepository):
        """Initialize use case with required dependencies"""
        self.twitter_adapter = twitter_adapter
        self.multi_agent_analyzer = multi_agent_analyzer
        self.file_repository = file_repository
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def create_from_env(cls) -> 'AnalyzeTweetsUseCase':
        """Create use case instance from environment variables"""
        # Initialize dependencies
        twitter_adapter = TwitterApiAdapter.from_env()
        
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        multi_agent_analyzer = MultiAgentAnalyzer(openai_api_key)
        file_repository = FileRepository()
        
        return cls(twitter_adapter, multi_agent_analyzer, file_repository)
    
    async def execute(self, 
                     account_usernames: List[str], 
                     config: AnalysisConfig) -> Dict[str, Any]:
        """
        Execute complete tweet analysis workflow
        
        Args:
            account_usernames: List of Twitter account usernames to analyze
            config: Analysis configuration parameters
            
        Returns:
            Analysis execution summary
        """
        run_id = f"TWITTER_ANALYSIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        
        self.logger.info(f"🚀 Starting tweet analysis workflow: {run_id}")
        self.logger.info(f"📊 Configuration: {config.max_tweets} tweets, {config.hours_back}h back")
        self.logger.info(f"🎯 Target accounts: {len(account_usernames)} accounts")
        
        try:
            # Step 1: Extract tweets from Twitter API
            self.logger.info("📥 Step 1: Extracting tweets from Twitter API...")
            tweets = await self._extract_tweets(account_usernames, config)
            
            if not tweets:
                self.logger.warning("⚠️ No tweets extracted. Ending analysis.")
                return self._create_summary(run_id, [], start_time, "No tweets found")
            
            # Step 2: Analyze tweets using multi-agent system
            self.logger.info(f"🤖 Step 2: Analyzing {len(tweets)} tweets with multi-agent system...")
            analysis_results = await self._analyze_tweets(tweets, run_id, config)
            
            # Step 3: Save individual results
            if config.save_individual_results:
                self.logger.info("💾 Step 3: Saving individual analysis results...")
                await self._save_individual_results(analysis_results, run_id)
            
            # Step 4: Generate and save summary
            if config.generate_summary:
                self.logger.info("📋 Step 4: Generating analysis summary...")
                summary = await self._generate_summary(analysis_results, run_id, start_time)
                await self._save_summary(summary, run_id)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"🎉 Analysis workflow completed in {execution_time:.2f}s")
            
            return self._create_summary(run_id, analysis_results, start_time, "success")
            
        except Exception as e:
            self.logger.error(f"❌ Analysis workflow failed: {str(e)}")
            return self._create_summary(run_id, [], start_time, f"failed: {str(e)}")
    
    async def _extract_tweets(self, 
                            account_usernames: List[str], 
                            config: AnalysisConfig) -> List[Tweet]:
        """Extract tweets from specified accounts"""
        return self.twitter_adapter.extract_tweets_from_accounts(
            account_usernames=account_usernames,
            max_tweets=config.max_tweets,
            hours_back=config.hours_back
        )
    
    async def _analyze_tweets(self, 
                            tweets: List[Tweet], 
                            run_id: str, 
                            config: AnalysisConfig) -> List[AnalysisResult]:
        """Analyze tweets using multi-agent system"""
        analysis_results = []
        
        for i, tweet in enumerate(tweets, 1):
            self.logger.info(f"📊 Analyzing tweet {i}/{len(tweets)}: {tweet.tweet_id}")
            
            try:
                # Perform multi-agent analysis
                result = await self.multi_agent_analyzer.analyze_tweet(tweet, run_id)
                analysis_results.append(result)
                
                self.logger.info(f"✅ Tweet {tweet.tweet_id} analyzed successfully")
                
            except Exception as e:
                self.logger.error(f"❌ Failed to analyze tweet {tweet.tweet_id}: {str(e)}")
                continue
        
        return analysis_results
    
    async def _save_individual_results(self, 
                                     analysis_results: List[AnalysisResult], 
                                     run_id: str):
        """Save individual analysis results to files"""
        for result in analysis_results:
            # Save JSON result
            json_filename = f"content_{result.content_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            await self.file_repository.save_analysis_result(result, run_id, json_filename)
            
            # Save markdown report
            md_filename = f"content_{result.content_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            markdown_content = self._generate_markdown_report(result)
            await self.file_repository.save_text_file(markdown_content, run_id, md_filename)
    
    async def _generate_summary(self, 
                              analysis_results: List[AnalysisResult], 
                              run_id: str, 
                              start_time: datetime) -> Dict[str, Any]:
        """Generate comprehensive analysis summary"""
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Calculate statistics
        total_items = len(analysis_results)
        successful_analyses = sum(1 for r in analysis_results if r.overall_status.value == "success")
        failed_analyses = total_items - successful_analyses
        
        # Calculate average scores
        valid_scores = [r.consolidated_score.consolidated_score for r in analysis_results 
                       if r.consolidated_score]
        average_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
        
        # Count thread and media analyses
        thread_count = sum(1 for r in analysis_results if r.has_thread_analysis)
        media_count = sum(1 for r in analysis_results if r.has_media_analysis)
        
        # Collect processing times
        processing_times = [r.total_processing_time for r in analysis_results]
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0.0
        
        return {
            "run_id": run_id,
            "generation_timestamp": datetime.now().isoformat(),
            "total_processing_time": execution_time,
            "analysis_overview": {
                "total_items_processed": total_items,
                "successful_analyses": successful_analyses,
                "failed_analyses": failed_analyses,
                "success_rate": (successful_analyses / total_items * 100) if total_items > 0 else 0.0,
                "average_quality_score": average_score
            },
            "thread_detection_results": {
                "threads_detected": thread_count,
                "thread_detection_rate": (thread_count / total_items * 100) if total_items > 0 else 0.0
            },
            "media_analysis_results": {
                "items_with_media": media_count,
                "media_analysis_rate": (media_count / total_items * 100) if total_items > 0 else 0.0
            },
            "performance_metrics": {
                "average_processing_time_per_item": avg_processing_time,
                "total_execution_time": execution_time,
                "error_rate": (failed_analyses / total_items * 100) if total_items > 0 else 0.0
            },
            "detailed_results": [
                {
                    "content_id": result.content_id,
                    "quality_score": result.consolidated_score.consolidated_score if result.consolidated_score else 0.0,
                    "processing_time": result.total_processing_time,
                    "status": result.overall_status.value,
                    "has_thread_analysis": result.has_thread_analysis,
                    "has_media_analysis": result.has_media_analysis
                }
                for result in analysis_results
            ]
        }
    
    async def _save_summary(self, summary: Dict[str, Any], run_id: str):
        """Save analysis summary to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"enhanced_analysis_summary_{run_id}_{timestamp}.md"
        
        markdown_summary = self._generate_summary_markdown(summary)
        await self.file_repository.save_text_file(markdown_summary, run_id, filename, subfolder="summary")
    
    def _generate_markdown_report(self, result: AnalysisResult) -> str:
        """Generate markdown report for individual analysis result"""
        score = result.consolidated_score.consolidated_score if result.consolidated_score else 0.0
        
        return f"""# Analysis Report for Content {result.content_id}

## Overview
- **Content ID:** {result.content_id}
- **Run ID:** {result.run_id}
- **Analysis Timestamp:** {result.analysis_timestamp}
- **Quality Score:** {score:.1f}/10
- **Processing Time:** {result.total_processing_time:.2f}s
- **Status:** {result.overall_status.value}

## Agent Analysis Summary
- **Success Rate:** {result.success_rate:.1f}%
- **Average Agent Score:** {result.average_agent_score:.1f}
- **Agents Executed:** {len(result.agent_responses)}

## Key Findings
{self._extract_key_findings(result)}

## Thread Analysis
{'✅ Thread detected and analyzed' if result.has_thread_analysis else '❌ No thread detected'}

## Media Analysis  
{'✅ Media content analyzed' if result.has_media_analysis else '❌ No media content'}

---
*Generated by Enhanced Social Media Multi-Agent Analyzer v{result.analysis_version}*
"""
    
    def _extract_key_findings(self, result: AnalysisResult) -> str:
        """Extract key findings from agent responses"""
        findings = []
        
        # Extract summary if available
        if 'summary_agent' in result.agent_responses:
            summary_data = result.agent_responses['summary_agent'].response_data
            if 'title' in summary_data:
                findings.append(f"**Title:** {summary_data['title']}")
            if 'abstract' in summary_data:
                findings.append(f"**Abstract:** {summary_data['abstract'][:200]}...")
        
        # Extract key themes
        if 'summary_agent' in result.agent_responses:
            summary_data = result.agent_responses['summary_agent'].response_data
            if 'key_themes' in summary_data:
                themes = ', '.join(summary_data['key_themes'][:5])  # Top 5 themes
                findings.append(f"**Key Themes:** {themes}")
        
        return '\n'.join(findings) if findings else "No key findings extracted."
    
    def _generate_summary_markdown(self, summary: Dict[str, Any]) -> str:
        """Generate markdown summary report"""
        return f"""# 🚀 Enhanced Multi-Agent Analysis Summary

**Run ID:** {summary['run_id']}  
**Generated:** {summary['generation_timestamp']}  
**Total Processing Time:** {summary['total_processing_time']:.2f} seconds

---

## 📊 Analysis Overview

### Content Analysis Results
- **Total Items Processed:** {summary['analysis_overview']['total_items_processed']}
- **Successful Analyses:** {summary['analysis_overview']['successful_analyses']}
- **Failed Analyses:** {summary['analysis_overview']['failed_analyses']}
- **Success Rate:** {summary['analysis_overview']['success_rate']:.1f}%
- **Average Quality Score:** {summary['analysis_overview']['average_quality_score']:.2f}/10

### Thread Detection Results
- **Threads Detected:** {summary['thread_detection_results']['threads_detected']}
- **Thread Detection Rate:** {summary['thread_detection_results']['thread_detection_rate']:.1f}%

### Media Analysis Results
- **Items with Media:** {summary['media_analysis_results']['items_with_media']}
- **Media Analysis Rate:** {summary['media_analysis_results']['media_analysis_rate']:.1f}%

---

## 🎯 Performance Metrics

- **Average Processing Time per Item:** {summary['performance_metrics']['average_processing_time_per_item']:.2f} seconds
- **Total Execution Time:** {summary['performance_metrics']['total_execution_time']:.2f} seconds
- **Error Rate:** {summary['performance_metrics']['error_rate']:.1f}%

---

## 📋 Detailed Results

### Successfully Analyzed Content

{self._format_detailed_results(summary['detailed_results'])}

---

## 🔧 Configuration Used

- **Analysis Type:** Enhanced Multi-Agent
- **Thread Analysis:** True
- **Media Analysis:** True
- **Link Analysis:** True
- **Output Formats:** json, markdown

---

*Generated by Enhanced Social Media Multi-Agent Analyzer v4.0*
"""
    
    def _format_detailed_results(self, detailed_results: List[Dict[str, Any]]) -> str:
        """Format detailed results for markdown"""
        if not detailed_results:
            return "No results to display."
        
        result_lines = []
        for i, result in enumerate(detailed_results, 1):
            result_lines.append(f"""#### {i}. Content ID: {result['content_id']}
- **Quality Score:** {result['quality_score']:.1f}/10
- **Processing Time:** {result['processing_time']:.2f}s
- **Status:** {result['status']}
- **Thread Analysis:** {'✅' if result['has_thread_analysis'] else '❌'}
- **Media Analysis:** {'✅' if result['has_media_analysis'] else '❌'}
""")
        
        return '\n'.join(result_lines)
    
    def _create_summary(self, 
                       run_id: str, 
                       results: List[AnalysisResult], 
                       start_time: datetime, 
                       status: str) -> Dict[str, Any]:
        """Create execution summary"""
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "run_id": run_id,
            "status": status,
            "execution_time": execution_time,
            "tweets_processed": len(results),
            "successful_analyses": sum(1 for r in results if r.overall_status.value == "success"),
            "timestamp": datetime.now().isoformat()
        } 