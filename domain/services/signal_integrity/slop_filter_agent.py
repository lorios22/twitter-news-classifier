#!/usr/bin/env python3
"""
🧽 AI SLOP FILTER AGENT
=====================
Agent for detecting low-effort, cliché-ridden, or AI-generated content.

This agent identifies "sloppy" content to prevent dull or synthetic-sounding
tweets from contaminating the analysis pipeline.

Domain-Driven Design: Domain service for content quality analysis.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
import numpy as np


@dataclass
class SlopResult:
    """Result of slop filter analysis"""
    is_sloppy: bool
    slop_score: float
    reasoning: str
    content_authenticity: str = "Acceptable"


class SlopFilterAgent:
    """
    🧽 AI Slop Filter Agent
    
    Detects low-effort or AI-generated-sounding tweets to maintain
    narrative clarity and content quality.
    
    Features:
    - Cliché and pattern detection
    - Embedding similarity to known slop
    - Redundancy analysis
    - Author fingerprinting
    - Factual content preservation
    """
    
    def __init__(self, memory_store: Dict[str, Any]):
        """Initialize slop filter agent"""
        self.logger = logging.getLogger(__name__)
        self.memory_store = memory_store
        
        # Common crypto/AI slop clichés
        self.cliche_patterns = [
            # Hype patterns
            r'\bgame[- ]?changer\b',
            r'\bparadigm shift\b',
            r'\brevolution(?:ary|ize)\b',
            r'\bto the moon\b',
            r'\bmoon(?:ing|shot)\b',
            r'\bonly time will tell\b',
            r'\bnext big thing\b',
            r'\bhuge news\b',
            r'\bbig announcement\b',
            r'\bmassive\b.*\bpotential\b',
            r'\bmind[- ]?blow(?:ing|n)\b',
            
            # Generic AI patterns
            r'\bin today\'s\s+(?:digital\s+)?(?:world|landscape|age)\b',
            r'\bas we move forward\b',
            r'\bat the end of the day\b',
            r'\bwhen all is said and done\b',
            r'\bthe bottom line is\b',
            r'\blet\'s be honest\b',
            r'\blet me tell you\b',
            r'\bhere\'s the thing\b',
            r'\bthe fact of the matter is\b',
            
            # Crypto-specific slop
            r'\bthis could be huge\b',
            r'\bprice prediction\b.*\bmoon\b',
            r'\b(?:100|1000)x\s+gains?\b',
            r'\bmake you rich\b',
            r'\bgems?\s+(?:hidden|secret)\b',
            r'\bnot financial advice\b.*\bbut\b',
            r'\bdyor\b.*\bbut\b',
            
            # Excessive punctuation patterns
            r'!{3,}',              # Multiple exclamation marks
            r'\?{2,}',             # Multiple question marks
            r'\.{3,}',             # Multiple dots beyond ellipsis
            
            # All caps words (often hype)
            r'\b[A-Z]{4,}\b',      # Words in all caps (4+ letters)
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.cliche_patterns
        ]
        
        # Known slop clusters (simplified embeddings approach)
        self.slop_clusters = {
            'generic_hype': [
                'huge potential', 'game changer', 'revolutionary', 'to the moon',
                'massive gains', 'next big thing', 'paradigm shift'
            ],
            'clickbait': [
                'you won\'t believe', 'shocking truth', 'secret revealed',
                'what they don\'t want you to know', 'hidden gem'
            ],
            'ai_filler': [
                'in today\'s digital world', 'as we move forward', 'at the end of the day',
                'the bottom line is', 'when all is said and done'
            ]
        }
        
        # Words that indicate substance (should reduce slop score)
        self.substance_indicators = [
            'data', 'analysis', 'research', 'study', 'report', 'evidence',
            'statistics', 'metrics', 'measurement', 'findings', 'results',
            'conclusion', 'methodology', 'technical', 'implementation',
            'documentation', 'specification', 'protocol', 'algorithm'
        ]
        
        # Factual content patterns that should be preserved
        self.factual_patterns = [
            r'\b\d+(?:\.\d+)?%\b',          # Percentages
            r'\$\d+(?:,\d{3})*(?:\.\d{2})?\b',  # Dollar amounts
            r'\b\d+(?:,\d{3})*\s+(?:users?|transactions?|tokens?)\b',  # Quantities
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # Dates
            r'\bhttps?://\S+\b',            # URLs (often reference sources)
        ]
    
    async def analyze_slop(self, tweet_text: str, author_handle: str) -> SlopResult:
        """
        Analyze tweet for slop characteristics
        
        Args:
            tweet_text: The tweet content to analyze
            author_handle: Twitter handle of the author
            
        Returns:
            SlopResult with slop analysis
        """
        try:
            # Step 1: Count cliché occurrences
            cliche_score, cliche_count = self._calculate_cliche_score(tweet_text)
            
            # Step 2: Calculate redundancy score
            redundancy_score = self._calculate_redundancy(tweet_text)
            
            # Step 3: Check for embedding similarity to slop clusters
            similarity_score = self._calculate_similarity_score(tweet_text)
            
            # Step 4: Check for factual content that should be preserved
            factual_adjustment = self._calculate_factual_adjustment(tweet_text)
            
            # Step 5: Combine scores
            raw_score = (
                cliche_score * 0.4 +
                redundancy_score * 0.3 +
                similarity_score * 0.3
            )
            
            # Apply factual content adjustment
            adjusted_score = max(0.0, raw_score - factual_adjustment)
            
            # Step 6: Make determination
            is_sloppy = adjusted_score > 0.7
            
            # Step 7: Generate reasoning
            reasoning = self._generate_reasoning(
                cliche_count, redundancy_score, similarity_score, factual_adjustment
            )
            
            # Step 8: Update author's slop fingerprint
            self._update_author_fingerprint(author_handle, adjusted_score)
            
            return SlopResult(
                is_sloppy=is_sloppy,
                slop_score=round(adjusted_score, 2),
                reasoning=reasoning
            )
            
        except Exception as e:
            self.logger.error(f"Error in slop analysis: {e}")
            return SlopResult(
                is_sloppy=False,
                slop_score=0.0,
                reasoning="Error in analysis"
            )
    
    def _calculate_cliche_score(self, text: str) -> tuple[float, int]:
        """Calculate score based on cliché patterns"""
        cliche_count = 0
        
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text)
            cliche_count += len(matches)
        
        # Normalize score (diminishing returns)
        score = min(1.0, cliche_count * 0.15)
        
        return score, cliche_count
    
    def _calculate_redundancy(self, text: str) -> float:
        """Calculate redundancy based on word repetition and predictability"""
        words = text.lower().split()
        
        if len(words) < 3:
            return 0.0
        
        # Calculate unique word ratio
        unique_words = set(words)
        unique_ratio = len(unique_words) / len(words)
        
        # Calculate repetition score (lower unique ratio = higher redundancy)
        repetition_score = 1 - unique_ratio
        
        # Check for common filler words
        filler_words = {
            'like', 'just', 'really', 'very', 'so', 'actually', 'basically',
            'literally', 'totally', 'absolutely', 'definitely', 'obviously'
        }
        
        filler_count = sum(1 for word in words if word in filler_words)
        filler_ratio = filler_count / len(words)
        
        # Combine scores
        redundancy = (repetition_score * 0.7) + (filler_ratio * 0.3)
        
        return min(1.0, redundancy)
    
    def _calculate_similarity_score(self, text: str) -> float:
        """Calculate similarity to known slop clusters (simplified)"""
        text_lower = text.lower()
        max_similarity = 0.0
        
        for cluster_name, phrases in self.slop_clusters.items():
            cluster_hits = 0
            for phrase in phrases:
                if phrase in text_lower:
                    cluster_hits += 1
            
            # Calculate similarity as ratio of hits
            if phrases:
                similarity = cluster_hits / len(phrases)
                max_similarity = max(max_similarity, similarity)
        
        return min(1.0, max_similarity * 2)  # Amplify for sensitivity
    
    def _calculate_factual_adjustment(self, text: str) -> float:
        """Calculate adjustment for factual content that should be preserved"""
        factual_score = 0.0
        
        # Check for factual patterns
        for pattern in self.factual_patterns:
            matches = re.findall(pattern, text)
            factual_score += len(matches) * 0.1
        
        # Check for substance indicators
        text_lower = text.lower()
        substance_count = sum(1 for word in self.substance_indicators if word in text_lower)
        factual_score += substance_count * 0.05
        
        # Check for URLs (often indicate sourced content)
        url_count = len(re.findall(r'https?://\S+', text))
        factual_score += url_count * 0.2
        
        # Cap the adjustment
        return min(0.5, factual_score)
    
    def _generate_reasoning(self, cliche_count: int, redundancy: float, 
                          similarity: float, factual_adj: float) -> str:
        """Generate human-readable reasoning for the slop determination"""
        reasons = []
        
        if cliche_count > 0:
            reasons.append(f"{cliche_count} cliché phrase(s)")
        
        if redundancy > 0.5:
            reasons.append("high word repetition")
        
        if similarity > 0.3:
            reasons.append("matches known slop patterns")
        
        if factual_adj > 0.1:
            reasons.append(f"contains factual content (adjustment: -{factual_adj:.1f})")
        
        if not reasons:
            return "No significant slop indicators detected"
        
        return "Detected: " + ", ".join(reasons)
    
    def _update_author_fingerprint(self, author_handle: str, slop_score: float):
        """Update author's slop fingerprint in memory"""
        key = f"slop_fingerprint:{author_handle}"
        
        profile = self.memory_store.get(key, {
            "count": 0,
            "avg_slop": 0.0,
            "total_slop": 0.0,
            "last_scores": []
        })
        
        # Update running statistics
        profile["count"] += 1
        profile["total_slop"] += slop_score
        profile["avg_slop"] = profile["total_slop"] / profile["count"]
        
        # Keep last 10 scores for trend analysis
        profile["last_scores"].append(slop_score)
        if len(profile["last_scores"]) > 10:
            profile["last_scores"] = profile["last_scores"][-10:]
        
        self.memory_store[key] = profile
        
        self.logger.debug(f"Updated slop fingerprint for {author_handle}: avg={profile['avg_slop']:.3f}")
    
    def get_author_slop_history(self, author_handle: str) -> Optional[Dict[str, Any]]:
        """Get author's slop history from memory"""
        key = f"slop_fingerprint:{author_handle}"
        return self.memory_store.get(key)
    
    def is_author_chronic_slopper(self, author_handle: str, threshold: float = 0.6) -> bool:
        """Check if author consistently produces sloppy content"""
        profile = self.get_author_slop_history(author_handle)
        
        if not profile or profile["count"] < 5:  # Need minimum sample size
            return False
        
        return profile["avg_slop"] > threshold
    
    def should_preserve_content(self, tweet_text: str, slop_score: float) -> bool:
        """
        Determine if content should be preserved despite sloppiness
        
        Args:
            tweet_text: Original tweet text
            slop_score: Calculated slop score
            
        Returns:
            Boolean indicating if content has redeeming value
        """
        # Always preserve if slop score is not too high
        if slop_score < 0.8:
            return True
        
        # Check for high-value indicators even in sloppy content
        high_value_indicators = [
            r'\$\d+(?:M|million|B|billion)\b',  # Large monetary amounts
            r'\b\d+(?:\.\d+)?%\s+(?:gain|loss|increase|decrease)\b',  # Specific metrics
            r'\b(?:breaking|confirmed|official|announced)\b',  # News indicators
            r'\b(?:partnership|acquisition|merger|funding)\b',  # Business events
            r'\b(?:upgrade|launch|release|deployment)\b',  # Technical events
        ]
        
        text_lower = tweet_text.lower()
        for pattern in high_value_indicators:
            if re.search(pattern, text_lower):
                return True
        
        return False