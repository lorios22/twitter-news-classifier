#!/usr/bin/env python3
"""
🧠 MEMORY NAMESPACE MANAGER
==========================
Manager for organizing and accessing different memory namespaces used by
the signal integrity agents.

This manager provides a structured way to handle persistent memory for:
- Sarcasm detection patterns
- Cross-platform echo metrics
- Content quality fingerprints
- Editorial compliance tracking
- Temporal analysis data

Domain-Driven Design: Domain service for memory management.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class MemoryStats:
    """Statistics about memory usage"""
    total_entries: int
    namespaces: Dict[str, int]
    oldest_entry: Optional[str] = None
    newest_entry: Optional[str] = None
    total_size_estimate: int = 0  # Rough size estimate in bytes


class MemoryNamespaceManager:
    """
    🧠 Memory Namespace Manager
    
    Manages different memory namespaces for signal integrity agents:
    
    Namespaces:
    - sarcasm_vector:<author> - Author sarcasm patterns and history
    - echo_map:<topic> - Cross-platform discussion metrics by topic
    - slop_fingerprint:<author> - Content quality patterns by author
    - ban_term_stats:<author> - Editorial violation tracking by author
    - latency_flags:<timestamp> - Temporal analysis results
    - visual_table_trace:<hash> - Image analysis cache (for future Visual Chart Translator)
    """
    
    def __init__(self, memory_store: Dict[str, Any]):
        """Initialize memory namespace manager"""
        self.logger = logging.getLogger(__name__)
        self.memory_store = memory_store
        
        # Define namespace schemas for validation
        self.namespace_schemas = {
            'sarcasm_vector': {
                'required_fields': ['total_tweets', 'sarcastic_tweets', 'sarcasm_rate'],
                'optional_fields': ['last_updated', 'examples', 'confidence_history']
            },
            'echo_map': {
                'required_fields': ['last_seen', 'echo_velocity'],
                'optional_fields': ['reddit_threads', 'farcaster_refs', 'discord_refs', 
                                  'previous_velocity', 'velocity_change', 'total_mentions']
            },
            'slop_fingerprint': {
                'required_fields': ['count', 'avg_slop'],
                'optional_fields': ['total_slop', 'last_scores', 'last_updated']
            },
            'ban_term_stats': {
                'required_fields': ['count', 'total_weight'],
                'optional_fields': ['violations', 'avg_weight', 'last_updated']
            },
            'latency_flags': {
                'required_fields': ['asset', 'price_change_pct', 'delta_seconds'],
                'optional_fields': ['tweet_text', 'tweet_time', 'flagged_at']
            },
            'visual_table_trace': {
                'required_fields': ['table', 'veracity_check', 'chart_confidence'],
                'optional_fields': ['extracted_at', 'image_hash', 'source_url']
            }
        }
    
    # Sarcasm Vector Methods
    def get_author_sarcasm_profile(self, author_handle: str) -> Dict[str, Any]:
        """Get author's sarcasm profile"""
        key = f"sarcasm_vector:{author_handle}"
        return self.memory_store.get(key, {
            'total_tweets': 0,
            'sarcastic_tweets': 0,
            'sarcasm_rate': 0.0,
            'last_updated': datetime.now().isoformat()
        })
    
    def update_author_sarcasm_profile(self, author_handle: str, is_sarcastic: bool, 
                                    confidence: float = None):
        """Update author's sarcasm profile"""
        profile = self.get_author_sarcasm_profile(author_handle)
        
        profile['total_tweets'] += 1
        if is_sarcastic:
            profile['sarcastic_tweets'] += 1
        
        profile['sarcasm_rate'] = profile['sarcastic_tweets'] / profile['total_tweets']
        profile['last_updated'] = datetime.now().isoformat()
        
        if confidence is not None:
            if 'confidence_history' not in profile:
                profile['confidence_history'] = []
            profile['confidence_history'].append(confidence)
            # Keep only last 20 confidence scores
            profile['confidence_history'] = profile['confidence_history'][-20:]
        
        key = f"sarcasm_vector:{author_handle}"
        self.memory_store[key] = profile
        
        self.logger.debug(f"Updated sarcasm profile for {author_handle}: rate={profile['sarcasm_rate']:.3f}")
    
    # Echo Map Methods
    def get_topic_echo_history(self, topic: str) -> Dict[str, Any]:
        """Get echo history for a topic"""
        key = f"echo_map:{topic}"
        return self.memory_store.get(key, {})
    
    def update_topic_echo_metrics(self, topic: str, reddit_threads: int, 
                                farcaster_refs: int, discord_refs: int, 
                                echo_velocity: float):
        """Update echo metrics for a topic"""
        key = f"echo_map:{topic}"
        prev_data = self.memory_store.get(key, {})
        
        new_data = {
            'last_seen': datetime.now().isoformat(),
            'reddit_threads': reddit_threads,
            'farcaster_refs': farcaster_refs,
            'discord_refs': discord_refs,
            'echo_velocity': echo_velocity,
            'total_mentions': reddit_threads + farcaster_refs + discord_refs
        }
        
        # Track velocity changes
        if prev_data.get('echo_velocity') is not None:
            new_data['previous_velocity'] = prev_data['echo_velocity']
            new_data['velocity_change'] = echo_velocity - prev_data['echo_velocity']
        
        self.memory_store[key] = new_data
        
        self.logger.debug(f"Updated echo metrics for '{topic}': velocity={echo_velocity:.2f}")
    
    def get_trending_topics(self, hours: int = 24, min_velocity: float = 0.5) -> List[Dict[str, Any]]:
        """Get topics that are trending based on recent echo velocity"""
        trending = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for key, data in self.memory_store.items():
            if key.startswith('echo_map:'):
                topic = key.replace('echo_map:', '')
                last_seen_str = data.get('last_seen')
                
                if last_seen_str:
                    try:
                        last_seen = datetime.fromisoformat(last_seen_str)
                        if (last_seen > cutoff_time and 
                            data.get('echo_velocity', 0) >= min_velocity):
                            trending.append({
                                'topic': topic,
                                'echo_velocity': data['echo_velocity'],
                                'total_mentions': data.get('total_mentions', 0),
                                'last_seen': last_seen_str,
                                'velocity_change': data.get('velocity_change', 0)
                            })
                    except ValueError:
                        continue
        
        # Sort by echo velocity
        trending.sort(key=lambda x: x['echo_velocity'], reverse=True)
        return trending
    
    # Slop Fingerprint Methods
    def get_author_slop_profile(self, author_handle: str) -> Dict[str, Any]:
        """Get author's content quality profile"""
        key = f"slop_fingerprint:{author_handle}"
        return self.memory_store.get(key, {
            'count': 0,
            'avg_slop': 0.0,
            'total_slop': 0.0,
            'last_scores': [],
            'last_updated': datetime.now().isoformat()
        })
    
    def update_author_slop_profile(self, author_handle: str, slop_score: float):
        """Update author's content quality profile"""
        profile = self.get_author_slop_profile(author_handle)
        
        profile['count'] += 1
        profile['total_slop'] += slop_score
        profile['avg_slop'] = profile['total_slop'] / profile['count']
        profile['last_updated'] = datetime.now().isoformat()
        
        # Keep last 10 scores for trend analysis
        profile['last_scores'].append(slop_score)
        if len(profile['last_scores']) > 10:
            profile['last_scores'] = profile['last_scores'][-10:]
        
        key = f"slop_fingerprint:{author_handle}"
        self.memory_store[key] = profile
        
        self.logger.debug(f"Updated slop profile for {author_handle}: avg={profile['avg_slop']:.3f}")
    
    def get_chronic_sloppers(self, threshold: float = 0.7, min_count: int = 5) -> List[Dict[str, Any]]:
        """Get authors who consistently produce low-quality content"""
        chronic_sloppers = []
        
        for key, data in self.memory_store.items():
            if key.startswith('slop_fingerprint:'):
                author = key.replace('slop_fingerprint:', '')
                
                if (data.get('count', 0) >= min_count and 
                    data.get('avg_slop', 0) >= threshold):
                    chronic_sloppers.append({
                        'author': author,
                        'avg_slop': data['avg_slop'],
                        'tweet_count': data['count'],
                        'recent_trend': data.get('last_scores', [])[-3:] if data.get('last_scores') else []
                    })
        
        # Sort by average slop score
        chronic_sloppers.sort(key=lambda x: x['avg_slop'], reverse=True)
        return chronic_sloppers
    
    # Banned Terms Methods
    def get_author_ban_stats(self, author_handle: str) -> Dict[str, Any]:
        """Get author's banned phrase violation statistics"""
        key = f"ban_term_stats:{author_handle}"
        return self.memory_store.get(key, {
            'count': 0,
            'total_weight': 0.0,
            'violations': {},
            'avg_weight': 0.0,
            'last_updated': datetime.now().isoformat()
        })
    
    def update_author_ban_stats(self, author_handle: str, banned_terms: List[str], 
                              total_weight: float):
        """Update author's banned phrase statistics"""
        stats = self.get_author_ban_stats(author_handle)
        
        stats['count'] += 1
        stats['total_weight'] += total_weight
        stats['avg_weight'] = stats['total_weight'] / stats['count']
        stats['last_updated'] = datetime.now().isoformat()
        
        # Track specific violations
        for term in banned_terms:
            clean_term = term.lower().strip()
            stats['violations'][clean_term] = stats['violations'].get(clean_term, 0) + 1
        
        key = f"ban_term_stats:{author_handle}"
        self.memory_store[key] = stats
        
        self.logger.debug(f"Updated ban stats for {author_handle}: avg_weight={stats['avg_weight']:.2f}")
    
    def get_most_violated_terms(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Get the most commonly violated banned terms"""
        term_counts = {}
        
        for key, data in self.memory_store.items():
            if key.startswith('ban_term_stats:'):
                violations = data.get('violations', {})
                for term, count in violations.items():
                    term_counts[term] = term_counts.get(term, 0) + count
        
        # Sort and return top N
        sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'term': term, 'violation_count': count} for term, count in sorted_terms[:top_n]]
    
    # Latency Flags Methods
    def store_latency_flag(self, asset: str, tweet_text: str, tweet_time: datetime,
                          price_change_pct: float, delta_seconds: int):
        """Store a latency flag event"""
        key = f"latency_flags:{tweet_time.strftime('%Y%m%d_%H%M%S')}"
        
        flag_data = {
            'asset': asset,
            'tweet_text': tweet_text[:200],  # Truncate for storage
            'tweet_time': tweet_time.isoformat(),
            'price_change_pct': price_change_pct,
            'delta_seconds': delta_seconds,
            'flagged_at': datetime.now().isoformat()
        }
        
        self.memory_store[key] = flag_data
        
        self.logger.info(f"Stored latency flag: {asset} moved {price_change_pct:.2f}% {delta_seconds}s before tweet")
    
    def get_recent_latency_flags(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent latency flag events"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        flags = []
        
        for key, data in self.memory_store.items():
            if key.startswith('latency_flags:'):
                flagged_at_str = data.get('flagged_at')
                if flagged_at_str:
                    try:
                        flagged_at = datetime.fromisoformat(flagged_at_str)
                        if flagged_at > cutoff_time:
                            flags.append(data)
                    except ValueError:
                        continue
        
        # Sort by flagged time
        flags.sort(key=lambda x: x.get('flagged_at', ''), reverse=True)
        return flags
    
    # Utility Methods
    def get_memory_statistics(self) -> MemoryStats:
        """Get comprehensive memory usage statistics"""
        namespaces = {}
        oldest_entry = None
        newest_entry = None
        oldest_time = None
        newest_time = None
        
        for key, data in self.memory_store.items():
            # Count by namespace
            namespace = key.split(':')[0] if ':' in key else 'unknown'
            namespaces[namespace] = namespaces.get(namespace, 0) + 1
            
            # Track oldest/newest entries
            timestamp_fields = ['last_updated', 'last_seen', 'flagged_at']
            for field in timestamp_fields:
                if field in data:
                    try:
                        entry_time = datetime.fromisoformat(data[field])
                        if oldest_time is None or entry_time < oldest_time:
                            oldest_time = entry_time
                            oldest_entry = key
                        if newest_time is None or entry_time > newest_time:
                            newest_time = entry_time
                            newest_entry = key
                    except (ValueError, TypeError):
                        continue
        
        # Rough size estimate
        total_size = len(json.dumps(self.memory_store, default=str))
        
        return MemoryStats(
            total_entries=len(self.memory_store),
            namespaces=namespaces,
            oldest_entry=oldest_entry,
            newest_entry=newest_entry,
            total_size_estimate=total_size
        )
    
    def cleanup_old_entries(self, days: int = 30) -> int:
        """Clean up entries older than specified days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        keys_to_remove = []
        
        for key, data in self.memory_store.items():
            should_remove = False
            
            # Check various timestamp fields
            timestamp_fields = ['last_updated', 'last_seen', 'flagged_at']
            for field in timestamp_fields:
                if field in data:
                    try:
                        entry_time = datetime.fromisoformat(data[field])
                        if entry_time < cutoff_time:
                            should_remove = True
                            break
                    except (ValueError, TypeError):
                        continue
            
            if should_remove:
                keys_to_remove.append(key)
        
        # Remove old entries
        for key in keys_to_remove:
            del self.memory_store[key]
        
        self.logger.info(f"Cleaned up {len(keys_to_remove)} old memory entries (older than {days} days)")
        return len(keys_to_remove)
    
    def export_namespace(self, namespace: str) -> Dict[str, Any]:
        """Export all entries from a specific namespace"""
        exported = {}
        prefix = f"{namespace}:"
        
        for key, value in self.memory_store.items():
            if key.startswith(prefix):
                exported[key] = value
        
        return exported
    
    def validate_namespace_entry(self, namespace: str, data: Dict[str, Any]) -> List[str]:
        """Validate entry against namespace schema"""
        errors = []
        schema = self.namespace_schemas.get(namespace)
        
        if not schema:
            return [f"Unknown namespace: {namespace}"]
        
        # Check required fields
        for field in schema['required_fields']:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Check for unexpected fields
        allowed_fields = set(schema['required_fields'] + schema['optional_fields'])
        for field in data.keys():
            if field not in allowed_fields:
                errors.append(f"Unexpected field: {field}")
        
        return errors