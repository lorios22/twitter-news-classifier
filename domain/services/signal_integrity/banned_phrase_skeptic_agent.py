#!/usr/bin/env python3
"""
🔍 BANNED PHRASE SKEPTIC AGENT
=============================
Agent for detecting banned words/phrases and applying tone penalties.

This agent cross-checks tweets against a curated taxonomy of banned terms
and applies tone penalties without eliminating content.

Domain-Driven Design: Domain service for editorial standards enforcement.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class BannedPhraseResult:
    """Result of banned phrase analysis"""
    banned_terms: List[str]
    total_weight: float
    tone_penalty: float
    risk_assessment: str = "Low"


class BannedPhraseSkepticAgent:
    """
    🔍 Banned Phrase Skeptic Agent
    
    Checks tweets against banned words/phrases and applies tone penalties
    to maintain AI Alpha voice guidelines and editorial standards.
    
    Features:
    - Categorized banned phrase taxonomy
    - Weighted penalty system
    - Context-aware detection
    - Author tracking
    - Sarcasm integration
    """
    
    def __init__(self, memory_store: Dict[str, Any]):
        """Initialize banned phrase skeptic agent"""
        self.logger = logging.getLogger(__name__)
        self.memory_store = memory_store
        
        # Banned phrases with categories and weights
        self.banned_taxonomy = {
            # Hype Language (moderate penalty)
            'hype_language': {
                'weight': 1.0,
                'phrases': [
                    {'pattern': r'\bto the moon\b', 'weight': 1.0, 'note': 'Hype language'},
                    {'pattern': r'\bmoon(?:ing|shot)\b', 'weight': 0.8, 'note': 'Hype language'},
                    {'pattern': r'\blambo\b', 'weight': 0.5, 'note': 'Slang/off-brand'},
                    {'pattern': r'\brekt\b', 'weight': 0.5, 'note': 'Slang/informal'},
                    {'pattern': r'\bhodl\b', 'weight': 0.3, 'note': 'Crypto slang'},
                    {'pattern': r'\bwagmi\b', 'weight': 0.4, 'note': 'Crypto slang'},
                    {'pattern': r'\bngmi\b', 'weight': 0.4, 'note': 'Crypto slang'},
                    {'pattern': r'\blfg\b', 'weight': 0.4, 'note': 'Informal acronym'},
                    {'pattern': r'\bfomo\b', 'weight': 0.3, 'note': 'Crypto acronym'},
                    {'pattern': r'\bfud\b', 'weight': 0.3, 'note': 'Crypto acronym'},
                ]
            },
            
            # Unrealistic promises (high penalty)
            'unrealistic_promises': {
                'weight': 1.5,
                'phrases': [
                    {'pattern': r'\b\d+x\s+gains?\b', 'weight': 1.2, 'note': 'Unrealistic promise'},
                    {'pattern': r'\b(?:100|1000)x\b', 'weight': 1.5, 'note': 'Unrealistic multiplier'},
                    {'pattern': r'\bmake you rich\b', 'weight': 1.5, 'note': 'Financial advice'},
                    {'pattern': r'\bguaranteed\s+(?:profit|gains?|returns?)\b', 'weight': 1.8, 'note': 'False guarantee'},
                    {'pattern': r'\beasy money\b', 'weight': 1.0, 'note': 'Misleading claim'},
                    {'pattern': r'\bget rich quick\b', 'weight': 1.5, 'note': 'Unrealistic promise'},
                ]
            },
            
            # Excessive punctuation/caps (low penalty)
            'formatting_issues': {
                'weight': 0.5,
                'phrases': [
                    {'pattern': r'!{3,}', 'weight': 0.3, 'note': 'Excessive punctuation'},
                    {'pattern': r'\?{2,}', 'weight': 0.2, 'note': 'Excessive punctuation'},
                    {'pattern': r'\b[A-Z]{5,}\b', 'weight': 0.4, 'note': 'Excessive caps'},
                    {'pattern': r'🚀{2,}', 'weight': 0.3, 'note': 'Excessive emoji'},
                ]
            },
            
            # Profanity/inappropriate (very high penalty)
            'inappropriate_language': {
                'weight': 2.0,
                'phrases': [
                    {'pattern': r'\bsh[i1]t(?:coin)?\b', 'weight': 1.0, 'note': 'Profanity'},
                    {'pattern': r'\bcrap\b', 'weight': 0.8, 'note': 'Inappropriate'},
                    {'pattern': r'\btrash\b', 'weight': 0.6, 'note': 'Harsh language'},
                    {'pattern': r'\bg[a@]rbage\b', 'weight': 0.6, 'note': 'Harsh language'},
                    {'pattern': r'\bscam\b', 'weight': 0.8, 'note': 'Accusatory language'},
                ]
            },
            
            # Clickbait patterns (moderate penalty)
            'clickbait': {
                'weight': 0.8,
                'phrases': [
                    {'pattern': r'\byou won\'t believe\b', 'weight': 0.8, 'note': 'Clickbait'},
                    {'pattern': r'\bshocking\s+(?:truth|news|revelation)\b', 'weight': 0.8, 'note': 'Clickbait'},
                    {'pattern': r'\bsecret\s+(?:revealed|exposed)\b', 'weight': 0.7, 'note': 'Clickbait'},
                    {'pattern': r'\bwhat\s+they\s+don\'t\s+want\s+you\s+to\s+know\b', 'weight': 0.9, 'note': 'Clickbait'},
                    {'pattern': r'\binsane\s+(?:profits?|gains?)\b', 'weight': 0.8, 'note': 'Clickbait'},
                    {'pattern': r'\bmind[- ]?blow(?:ing|n)\b', 'weight': 0.6, 'note': 'Clickbait'},
                ]
            }
        }
        
        # Compile all patterns for efficiency
        self.compiled_patterns = self._compile_patterns()
        
        # Context exceptions (proper nouns, project names, legitimate uses)
        self.context_exceptions = {
            'moonbeam',     # Moonbeam network
            'moonriver',    # Moonriver network
            'lunar',        # Project names containing "moon"
            'eclipse',      # Eclipse network
            'solana',       # Might contain "sol" but not slang
        }
        
        # Innocent context patterns that should not trigger bans
        self.innocent_contexts = [
            r'\b(?:cooking|eating|food|lunch|dinner|recipe|chef)\b',  # Cooking/food contexts
            r'\b(?:gaming|game|casino|spin|poker|betting)\b',          # Gaming contexts (legitimate)
            r'\b(?:first time|trying|experience|new)\b',              # Personal experiences
            r'\b(?:today|will|lucky|day)\b',                          # General positive language
            r'\b(?:choose|would you|option|preference)\b',            # Choice/preference language
        ]
        
        # Maximum total penalty to prevent excessive punishment
        self.max_penalty = 5.0
    
    def _compile_patterns(self) -> List[Tuple[re.Pattern, float, str]]:
        """Compile all regex patterns with their weights and notes"""
        patterns = []
        
        for category, data in self.banned_taxonomy.items():
            category_weight = data['weight']
            
            for phrase_data in data['phrases']:
                pattern = re.compile(phrase_data['pattern'], re.IGNORECASE)
                weight = phrase_data['weight'] * category_weight
                note = phrase_data['note']
                patterns.append((pattern, weight, note))
        
        return patterns
    
    async def analyze_banned_phrases(self, tweet_text: str, author_handle: str, 
                                   is_sarcastic: bool = False) -> BannedPhraseResult:
        """
        Analyze tweet for banned phrases and calculate tone penalty
        
        Args:
            tweet_text: The tweet content to analyze
            author_handle: Twitter handle of the author
            is_sarcastic: Whether the tweet was flagged as sarcastic
            
        Returns:
            BannedPhraseResult with detected terms and penalties
        """
        try:
            # Step 1: Detect banned terms
            found_terms, total_weight = self._detect_banned_terms(tweet_text)
            
            # Step 2: Apply context adjustments
            adjusted_weight = self._apply_context_adjustments(
                found_terms, total_weight, tweet_text, is_sarcastic
            )
            
            # Step 3: Calculate tone penalty (normalized 0-1)
            tone_penalty = min(1.0, adjusted_weight / self.max_penalty)
            
            # Step 4: Update author statistics
            self._update_author_stats(author_handle, found_terms, adjusted_weight)
            
            # Step 5: Extract clean term names for output
            clean_terms = [self._extract_clean_term(term, tweet_text) for term in found_terms]
            
            return BannedPhraseResult(
                banned_terms=clean_terms,
                total_weight=round(adjusted_weight, 2),
                tone_penalty=round(tone_penalty, 2)
            )
            
        except Exception as e:
            self.logger.error(f"Error in banned phrase analysis: {e}")
            return BannedPhraseResult(
                banned_terms=[],
                total_weight=0.0,
                tone_penalty=0.0
            )
    
    def _detect_banned_terms(self, text: str) -> Tuple[List[str], float]:
        """Detect banned terms and calculate total weight"""
        found_terms = []
        total_weight = 0.0
        
        for pattern, weight, note in self.compiled_patterns:
            matches = pattern.findall(text)
            if matches:
                # Check for context exceptions and innocent contexts
                should_flag = True
                text_lower = text.lower()
                
                # Check specific exceptions
                for exception in self.context_exceptions:
                    if exception in text_lower:
                        # Additional check: is the match part of the exception?
                        for match in matches:
                            if match.lower() in exception or exception in match.lower():
                                should_flag = False
                                break
                
                # Check innocent contexts
                if should_flag:
                    for innocent_pattern in self.innocent_contexts:
                        if re.search(innocent_pattern, text, re.IGNORECASE):
                            should_flag = False
                            self.logger.debug(f"Skipping banned term due to innocent context: {innocent_pattern}")
                            break
                
                if should_flag:
                    # Log what's being detected for debugging
                    self.logger.debug(f"Detected banned term: {matches} (weight: {weight}, note: {note})")
                    found_terms.extend([f"{match} ({note})" for match in matches])
                    total_weight += weight * len(matches)  # Multiple occurrences multiply weight
        
        return found_terms, total_weight
    
    def _apply_context_adjustments(self, found_terms: List[str], total_weight: float,
                                 tweet_text: str, is_sarcastic: bool) -> float:
        """Apply contextual adjustments to the penalty weight"""
        adjusted_weight = total_weight
        
        # Reduce penalty for sarcastic content
        if is_sarcastic:
            adjusted_weight *= 0.6  # 40% reduction for sarcasm
            self.logger.debug("Applied sarcasm adjustment: -40%")
        
        # Reduce penalty if tweet contains valuable information
        value_indicators = [
            r'\$\d+(?:M|million|B|billion)\b',  # Monetary amounts
            r'\b\d+(?:\.\d+)?%\b',             # Percentages
            r'\b(?:partnership|funding|acquisition)\b',  # Business news
            r'\b(?:upgrade|launch|release)\b',  # Technical news
            r'https?://\S+',                   # URLs (sources)
        ]
        
        value_count = sum(1 for pattern in value_indicators 
                         if re.search(pattern, tweet_text, re.IGNORECASE))
        
        if value_count > 0:
            reduction = min(0.3, value_count * 0.1)  # Up to 30% reduction
            adjusted_weight *= (1 - reduction)
            self.logger.debug(f"Applied value content adjustment: -{reduction*100:.1f}%")
        
        # Check for quotes (might be citing someone else's language)
        if '"' in tweet_text or "'" in tweet_text:
            adjusted_weight *= 0.8  # 20% reduction for quoted content
            self.logger.debug("Applied quote adjustment: -20%")
        
        return max(0.0, adjusted_weight)
    
    def _extract_clean_term(self, term: str, text: str) -> str:
        """Extract a clean version of the term for reporting"""
        # For regex matches, try to find the actual text that matched
        # This is a simplified approach - in production might be more sophisticated
        return term.strip().lower()
    
    def _update_author_stats(self, author_handle: str, terms: List[str], weight: float):
        """Update author's banned phrase usage statistics"""
        key = f"ban_term_stats:{author_handle}"
        
        stats = self.memory_store.get(key, {
            "count": 0,
            "total_weight": 0.0,
            "violations": {},
            "avg_weight": 0.0
        })
        
        # Update counts
        stats["count"] += 1
        stats["total_weight"] += weight
        stats["avg_weight"] = stats["total_weight"] / stats["count"]
        
        # Track specific violations
        for term in terms:
            clean_term = term.lower().strip()
            stats["violations"][clean_term] = stats["violations"].get(clean_term, 0) + 1
        
        self.memory_store[key] = stats
        
        self.logger.debug(f"Updated ban stats for {author_handle}: {len(terms)} terms, weight {weight:.2f}")
    
    def get_author_violation_history(self, author_handle: str) -> Optional[Dict[str, Any]]:
        """Get author's banned phrase violation history"""
        key = f"ban_term_stats:{author_handle}"
        return self.memory_store.get(key)
    
    def is_author_chronic_violator(self, author_handle: str, threshold: float = 1.0) -> bool:
        """Check if author consistently violates banned phrase guidelines"""
        stats = self.get_author_violation_history(author_handle)
        
        if not stats or stats["count"] < 5:  # Need minimum sample size
            return False
        
        return stats["avg_weight"] > threshold
    
    def get_violation_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate a report of recent violations for analysis"""
        # In production, this would analyze memory entries from the last N days
        # For now, return a simplified structure
        
        all_authors = {}
        violation_counts = {}
        
        # Scan memory for ban_term_stats entries
        for key, value in self.memory_store.items():
            if key.startswith("ban_term_stats:"):
                author = key.replace("ban_term_stats:", "")
                all_authors[author] = value
                
                # Aggregate violation counts
                for term, count in value.get("violations", {}).items():
                    violation_counts[term] = violation_counts.get(term, 0) + count
        
        # Find top violators and terms
        top_violators = sorted(
            all_authors.items(), 
            key=lambda x: x[1].get("avg_weight", 0), 
            reverse=True
        )[:10]
        
        top_terms = sorted(
            violation_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        return {
            "total_authors_tracked": len(all_authors),
            "top_violators": [{"author": author, "avg_weight": data.get("avg_weight", 0)} 
                            for author, data in top_violators],
            "most_common_violations": [{"term": term, "count": count} 
                                     for term, count in top_terms],
            "total_violations": sum(violation_counts.values())
        }
    
    def should_escalate_for_review(self, result: BannedPhraseResult, author_handle: str) -> bool:
        """
        Determine if a violation should be escalated for human review
        
        Args:
            result: BannedPhraseResult from analysis
            author_handle: Author's handle
            
        Returns:
            Boolean indicating if human review is needed
        """
        # Escalate if very high penalty
        if result.tone_penalty > 0.8:
            return True
        
        # Escalate if author is chronic violator with new severe violation
        if (self.is_author_chronic_violator(author_handle) and 
            result.tone_penalty > 0.5):
            return True
        
        # Escalate if inappropriate language detected
        inappropriate_terms = ['scam', 'trash', 'garbage', 'shit']
        if any(term in result.banned_terms for term in inappropriate_terms):
            return True
        
        return False