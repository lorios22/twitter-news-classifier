#!/usr/bin/env python3
"""
💾 FILE REPOSITORY
=================
Infrastructure repository for file-based data persistence.

Domain-Driven Design: Infrastructure layer repository for data persistence.
Handles saving analysis results, reports, and summaries to filesystem.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from domain.entities.analysis_result import AnalysisResult


class EnhancedJSONEncoder(json.JSONEncoder):
    """Enhanced JSON encoder that handles datetime and enum objects"""
    
    def default(self, obj):
        """Convert special objects to JSON-serializable format"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'value'):  # Handle Enum objects
            return obj.value
        elif hasattr(obj, '__dict__'):  # Handle dataclass objects
            return obj.__dict__
        return super().default(obj)


class FileRepository:
    """
    💾 File-based repository for analysis result persistence
    
    Handles:
    - Saving analysis results as JSON and Markdown
    - Creating organized directory structures
    - Managing file naming conventions
    - Ensuring data consistency and error handling
    """
    
    def __init__(self, base_path: str = "results/runs"):
        """Initialize file repository with base path"""
        self.base_path = Path(base_path)
        self.logger = logging.getLogger(__name__)
        
        # Ensure base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    async def save_analysis_result(self, 
                                 result: AnalysisResult, 
                                 run_id: str, 
                                 filename: str,
                                 subfolder: str = "individual_content") -> str:
        """
        Save analysis result as JSON file
        
        Args:
            result: Analysis result to save
            run_id: Run identifier for directory organization
            filename: Name of the file to save
            subfolder: Subfolder within run directory
            
        Returns:
            Full path of saved file
        """
        try:
            # Create directory structure
            run_dir = self.base_path / run_id / subfolder
            run_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert result to dictionary
            if hasattr(result, 'to_dict'):
                result_dict = result.to_dict()
            elif hasattr(result, '__dict__'):
                result_dict = result.__dict__
            else:
                result_dict = result
            
            # Save as JSON with enhanced encoder
            file_path = run_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, 
                         indent=2, 
                         ensure_ascii=False,
                         cls=EnhancedJSONEncoder)
            
            self.logger.info(f"💾 Saved analysis result: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save analysis result {filename}: {str(e)}")
            raise
    
    async def save_text_file(self, 
                            content: str, 
                            run_id: str, 
                            filename: str,
                            subfolder: str = "individual_content") -> str:
        """
        Save text content to file
        
        Args:
            content: Text content to save
            run_id: Run identifier for directory organization
            filename: Name of the file to save
            subfolder: Subfolder within run directory
            
        Returns:
            Full path of saved file
        """
        try:
            # Create directory structure
            run_dir = self.base_path / run_id / subfolder
            run_dir.mkdir(parents=True, exist_ok=True)
            
            # Save text content
            file_path = run_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"💾 Saved text file: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save text file {filename}: {str(e)}")
            raise
    
    async def save_json_data(self, 
                           data: Dict[str, Any], 
                           run_id: str, 
                           filename: str,
                           subfolder: str = "summary") -> str:
        """
        Save dictionary data as JSON file
        
        Args:
            data: Dictionary data to save
            run_id: Run identifier for directory organization
            filename: Name of the file to save
            subfolder: Subfolder within run directory
            
        Returns:
            Full path of saved file
        """
        try:
            # Create directory structure
            run_dir = self.base_path / run_id / subfolder
            run_dir.mkdir(parents=True, exist_ok=True)
            
            # Save as JSON
            file_path = run_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, 
                         indent=2, 
                         ensure_ascii=False,
                         cls=EnhancedJSONEncoder)
            
            self.logger.info(f"💾 Saved JSON data: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save JSON data {filename}: {str(e)}")
            raise
    
    def list_run_directories(self) -> list[str]:
        """List all run directories"""
        try:
            if not self.base_path.exists():
                return []
            
            return [d.name for d in self.base_path.iterdir() 
                   if d.is_dir() and d.name.startswith('TWITTER_ANALYSIS_')]
        except Exception as e:
            self.logger.error(f"❌ Failed to list run directories: {str(e)}")
            return []
    
    def get_run_summary(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get summary information for a specific run"""
        try:
            run_dir = self.base_path / run_id
            if not run_dir.exists():
                return None
            
            # Count files in different subdirectories
            individual_dir = run_dir / "individual_content"
            summary_dir = run_dir / "summary"
            
            individual_count = len(list(individual_dir.glob("*.json"))) if individual_dir.exists() else 0
            summary_files = list(summary_dir.glob("*.md")) if summary_dir.exists() else []
            
            return {
                "run_id": run_id,
                "individual_analyses": individual_count,
                "summary_files": len(summary_files),
                "has_summary": len(summary_files) > 0,
                "created": datetime.fromtimestamp(run_dir.stat().st_ctime).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get run summary for {run_id}: {str(e)}")
            return None
    
    def cleanup_old_runs(self, keep_latest: int = 3) -> int:
        """
        Clean up old run directories, keeping only the latest ones
        
        Args:
            keep_latest: Number of latest runs to keep
            
        Returns:
            Number of directories removed
        """
        try:
            run_dirs = [d for d in self.base_path.iterdir() 
                       if d.is_dir() and d.name.startswith('TWITTER_ANALYSIS_')]
            
            # Sort by creation time (newest first)
            run_dirs.sort(key=lambda x: x.stat().st_ctime, reverse=True)
            
            # Remove old directories
            removed_count = 0
            for old_dir in run_dirs[keep_latest:]:
                try:
                    import shutil
                    shutil.rmtree(old_dir)
                    removed_count += 1
                    self.logger.info(f"🗑️ Removed old run directory: {old_dir.name}")
                except Exception as e:
                    self.logger.error(f"❌ Failed to remove directory {old_dir.name}: {str(e)}")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Failed to cleanup old runs: {str(e)}")
            return 0
    
    def get_latest_run_id(self) -> Optional[str]:
        """Get the ID of the most recent run"""
        try:
            run_dirs = [d for d in self.base_path.iterdir() 
                       if d.is_dir() and d.name.startswith('TWITTER_ANALYSIS_')]
            
            if not run_dirs:
                return None
            
            # Sort by creation time (newest first) 
            latest_dir = max(run_dirs, key=lambda x: x.stat().st_ctime)
            return latest_dir.name
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get latest run ID: {str(e)}")
            return None 