#!/usr/bin/env python3
"""
🛰️ SARCASM SENTINEL AGENT
========================
Agent for detecting sarcasm, irony, and tone-inverted phrasing in tweets.

This agent identifies tweets that use sarcasm or irony so the classifier
doesn't misinterpret ironic statements as factual claims.

Domain-Driven Design: Domain service for sarcasm detection.
"""

import json
import logging
import re
import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
import torch
from openai import AsyncOpenAI

# Note: In production, you would install these packages:
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from sentence_transformers import SentenceTransformer


@dataclass
class SarcasmResult:
    """Result of sarcasm detection analysis"""
    is_sarcastic: bool
    p_sarcasm: float
    reason: str
    confidence_level: str = "Medium"


class SarcasmSentinelAgent:
    """
    🛰️ Sarcasm Sentinel Agent
    
    Detects sarcasm, satire, or tone-inverted phrasing in tweets to prevent
    misinterpretation of ironic statements as factual claims.
    
    Features:
    - Linguistic cue detection (emojis, patterns)
    - MiniLM classifier for sarcasm probability
    - LLM fallback for ambiguous cases
    - Author sarcasm history tracking
    - Context-aware analysis
    """
    
    def __init__(self, openai_client: AsyncOpenAI, memory_store: Dict[str, Any]):
        """Initialize sarcasm sentinel agent"""
        self.logger = logging.getLogger(__name__)
        self.openai_client = openai_client
        self.memory_store = memory_store
        
        # Sarcasm indicators - linguistic cues
        self.sarcasm_indicators = [
            r"🙄",  # Eye roll emoji
            r"😏",  # Smirking face
            r"😜",  # Winking face with tongue
            r"🤡",  # Clown face
            r"/s$",  # Explicit sarcasm marker
            r"\byeah,?\s+right\b",  # "yeah right"
            r"\bsure,?\s+\w+",  # "sure [whatever]"
            r"\btotally\b.*\b(not|never)\b",  # "totally not"
            r"\bgreat\b.*🙄",  # "great" with eye roll
            r"\bwhat\s+could\s+(possibly\s+)?go\s+wrong",  # "what could go wrong"
            r"\bjust\s+what\s+we\s+needed",  # "just what we needed"
            r"\boh\s+wonderful\b",  # "oh wonderful"
        ]
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.sarcasm_indicators]
        
        # Initialize models (simplified for demo - in production would load actual models)
        self.model_available = False
        try:
            # Note: In production, uncomment these lines and install required packages
            # self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-irony")
            # self.model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-irony")
            # self.model_available = True
            pass
        except Exception as e:
            self.logger.warning(f"Could not load sarcasm detection model: {e}")
            self.model_available = False
    
    async def analyze_sarcasm(self, tweet_text: str, author_handle: str, 
                            context: Optional[str] = None) -> SarcasmResult:
        """
        Analyze tweet for sarcasm indicators
        
        Args:
            tweet_text: The tweet content to analyze
            author_handle: Twitter handle of the author
            context: Optional thread context or previous tweets
            
        Returns:
            SarcasmResult with detection results
        """
        try:
            # Step 1: Check for obvious linguistic cues
            cue_score = self._detect_linguistic_cues(tweet_text)
            
            # Step 2: Get model prediction if available
            model_score = 0.0
            if self.model_available:
                model_score = await self._get_model_prediction(tweet_text)
            
            # Step 3: Check author's sarcasm history
            author_prior = self._get_author_sarcasm_prior(author_handle)
            
            # Step 4: Combine scores
            combined_score = self._combine_scores(cue_score, model_score, author_prior)
            
            # Step 5: Use LLM for ambiguous cases
            if 0.4 <= combined_score <= 0.6:
                llm_result = await self._get_llm_analysis(tweet_text, context)
                if llm_result:
                    combined_score = llm_result.get('p_sarcasm', combined_score)
                    reason = llm_result.get('reason', '')
                else:
                    reason = self._generate_reason(cue_score, model_score, author_prior)
            else:
                reason = self._generate_reason(cue_score, model_score, author_prior)
            
            # Step 6: Make final determination
            is_sarcastic = combined_score > 0.5
            
            # Step 7: Update author's sarcasm profile
            self._update_author_profile(author_handle, is_sarcastic, combined_score)
            
            return SarcasmResult(
                is_sarcastic=is_sarcastic,
                p_sarcasm=round(combined_score, 3),
                reason=reason
            )
            
        except Exception as e:
            self.logger.error(f"Error in sarcasm analysis: {e}")
            # Return conservative result on error
            return SarcasmResult(
                is_sarcastic=False,
                p_sarcasm=0.0,
                reason="Error in analysis, defaulting to non-sarcastic"
            )
    
    def _detect_linguistic_cues(self, text: str) -> float:
        """Detect linguistic cues for sarcasm"""
        cue_count = 0
        text_lower = text.lower()
        
        # Check for compiled patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                cue_count += 1
        
        # Additional checks
        if "..." in text and any(word in text_lower for word in ["great", "perfect", "wonderful"]):
            cue_count += 1
        
        # Multiple exclamation marks with positive words might indicate sarcasm
        if re.search(r"!{2,}", text) and any(word in text_lower for word in ["amazing", "fantastic", "brilliant"]):
            cue_count += 0.5
        
        # Normalize to 0-1 scale (diminishing returns)
        return min(1.0, cue_count * 0.3)
    
    async def _get_model_prediction(self, text: str) -> float:
        """Get prediction from transformer model (simplified)"""
        if not self.model_available:
            return 0.0
        
        try:
            # Note: In production, this would use actual model prediction
            # inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
            # with torch.no_grad():
            #     outputs = self.model(**inputs)
            #     prediction = torch.softmax(outputs.logits, dim=-1)
            #     # Assuming binary classification where index 1 is sarcastic
            #     return float(prediction[0][1])
            
            # Simplified heuristic for demo
            return 0.2  # Default low sarcasm probability
            
        except Exception as e:
            self.logger.warning(f"Model prediction failed: {e}")
            return 0.0
    
    def _get_author_sarcasm_prior(self, author_handle: str) -> float:
        """Get author's historical sarcasm rate"""
        key = f"sarcasm_vector:{author_handle}"
        profile = self.memory_store.get(key, {})
        return profile.get("sarcasm_rate", 0.1)  # Default low prior
    
    def _combine_scores(self, cue_score: float, model_score: float, author_prior: float) -> float:
        """Combine different sarcasm indicators into final score"""
        # Weighted combination
        combined = (
            cue_score * 0.5 +      # Linguistic cues most important
            model_score * 0.3 +    # Model prediction
            author_prior * 0.2     # Author history
        )
        return max(0.0, min(1.0, combined))
    
    async def _get_llm_analysis(self, text: str, context: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Use LLM for ambiguous sarcasm cases"""
        try:
            context_str = f"\nContext: {context}" if context else ""
            
            prompt = f"""
Analyze the tone of the following tweet and determine if it's sarcastic:

Tweet: "{text}"{context_str}

Consider:
- Irony or opposite meaning from literal text
- Mocking or humorous tone
- Punctuation and emojis that signal sarcasm
- Context clues

Answer in JSON with keys:
- is_sarcastic (true/false)
- p_sarcasm (0.0 to 1.0)
- reason (brief explanation)

If unsure, lean towards not sarcastic.
"""
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            return json.loads(result_text)
            
        except Exception as e:
            self.logger.warning(f"LLM analysis failed: {e}")
            return None
    
    def _generate_reason(self, cue_score: float, model_score: float, author_prior: float) -> str:
        """Generate explanation for sarcasm detection"""
        reasons = []
        
        if cue_score > 0.3:
            reasons.append("Contains sarcasm indicators (emojis, phrases)")
        if model_score > 0.5:
            reasons.append("Model detected sarcastic tone")
        if author_prior > 0.3:
            reasons.append("Author frequently uses sarcasm")
        
        if not reasons:
            return "No clear sarcasm indicators detected"
        
        return "; ".join(reasons)
    
    def _update_author_profile(self, author_handle: str, is_sarcastic: bool, score: float):
        """Update author's sarcasm profile in memory"""
        key = f"sarcasm_vector:{author_handle}"
        profile = self.memory_store.get(key, {
            "total_tweets": 0,
            "sarcastic_tweets": 0,
            "sarcasm_rate": 0.0
        })
        
        # Update counts
        profile["total_tweets"] += 1
        if is_sarcastic:
            profile["sarcastic_tweets"] += 1
        
        # Update rate
        profile["sarcasm_rate"] = profile["sarcastic_tweets"] / profile["total_tweets"]
        
        # Store updated profile
        self.memory_store[key] = profile
        
        self.logger.debug(f"Updated sarcasm profile for {author_handle}: {profile}")