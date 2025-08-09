#!/usr/bin/env python3
"""
📡 ECHO MAPPER AGENT
==================
Agent for tracking cross-platform virality and echo metrics.

This agent measures how widely a topic is reverberating across other platforms
like Reddit, Farcaster, Discord, and other communities.

Domain-Driven Design: Domain service for cross-platform echo analysis.
"""

import json
import logging
import asyncio
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import aiohttp
from datetime import datetime, timedelta

# Note: In production, you would install: pip install praw aiohttp


@dataclass
class EchoResult:
    """Result of cross-platform echo analysis"""
    reddit_threads: int
    farcaster_refs: int
    discord_refs: int
    echo_velocity: float
    virality_assessment: str = "Low"


class EchoMapperAgent:
    """
    📡 Echo Mapper Agent
    
    Tracks cross-platform virality by searching Reddit, Farcaster, and other
    platforms for mentions of the tweet's topic.
    
    Features:
    - Keyword and topic extraction
    - Multi-platform search (Reddit, Farcaster, etc.)
    - Echo velocity calculation
    - Memory-based trending analysis
    - Asynchronous processing
    """
    
    def __init__(self, memory_store: Dict[str, Any], reddit_config: Optional[Dict] = None):
        """Initialize echo mapper agent"""
        self.logger = logging.getLogger(__name__)
        self.memory_store = memory_store
        self.reddit_config = reddit_config or {}
        
        # Platform search timeouts
        self.search_timeout = 10  # seconds
        
        # Initialize Reddit client with real API
        self.reddit_available = False
        self.reddit = None
        
        if (reddit_config and 
            reddit_config.get('client_id') and 
            reddit_config.get('client_secret')):
            try:
                import praw
                self.reddit = praw.Reddit(
                    client_id=reddit_config.get('client_id'),
                    client_secret=reddit_config.get('client_secret'),
                    user_agent=reddit_config.get('user_agent', 'EchoMapperAgent/1.0')
                )
                self.reddit_available = True
                self.logger.info("Reddit API initialized successfully")
            except Exception as e:
                self.logger.warning(f"Reddit API initialization failed: {e}")
                self.reddit_available = False
        else:
            self.logger.info("Reddit API credentials not provided - feature disabled")
        
        # Crypto-related subreddits to monitor
        self.crypto_subreddits = [
            "CryptoCurrency",
            "Bitcoin",
            "Ethereum", 
            "DeFi",
            "altcoin",
            "CryptoMarkets",
            "cryptocurrencynews",
            "blockchain"
        ]
    
    async def analyze_echo(self, tweet_text: str, tweet_time: Optional[datetime] = None) -> EchoResult:
        """
        Analyze cross-platform echo for tweet content
        
        Args:
            tweet_text: The tweet content to analyze
            tweet_time: When the tweet was posted (for time-based analysis)
            
        Returns:
            EchoResult with cross-platform metrics
        """
        try:
            # Step 1: Extract keywords and topics
            keywords = self._extract_keywords(tweet_text)
            if not keywords:
                return EchoResult(0, 0, 0, 0.0)
            
            # Step 2: Expand keywords for better search coverage
            expanded_keywords = self._expand_keywords(keywords)
            
            # Step 3: Search platforms in parallel
            search_tasks = [
                self._search_reddit(expanded_keywords),
                self._search_farcaster(expanded_keywords),
                self._search_discord(expanded_keywords)
            ]
            
            results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Process results safely
            reddit_count = results[0] if isinstance(results[0], int) else 0
            farcaster_count = results[1] if isinstance(results[1], int) else 0
            discord_count = results[2] if isinstance(results[2], int) else 0
            
            # Step 4: Calculate echo velocity
            echo_velocity = self._calculate_echo_velocity(
                reddit_count, farcaster_count, discord_count
            )
            
            # Step 5: Store in memory for historical tracking
            main_topic = "_".join(keywords[:3])
            self._update_echo_memory(main_topic, reddit_count, farcaster_count, discord_count, echo_velocity)
            
            return EchoResult(
                reddit_threads=reddit_count,
                farcaster_refs=farcaster_count,
                discord_refs=discord_count,
                echo_velocity=echo_velocity
            )
            
        except Exception as e:
            self.logger.error(f"Error in echo analysis: {e}")
            return EchoResult(0, 0, 0, 0.0)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract crypto-specific keywords from tweet for searching"""
        # Remove URLs, mentions, hashtags for cleaner keyword extraction
        clean_text = re.sub(r'http\S+|@\w+|#\w+', '', text)
        
        # Known crypto ticker symbols (more specific than generic pattern)
        known_tickers = [
            'BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'AVAX', 'MATIC', 'LINK', 'UNI', 'AAVE',
            'COMP', 'MKR', 'YFI', 'SUSHI', 'CRV', 'BAL', 'SNX', 'LUNA', 'ATOM', 'FTM'
        ]
        
        # Specific crypto terms (not generic words)
        crypto_specific_terms = [
            r'\b\w+coin\b',     # *coin patterns
            r'\bdefi\b',        # DeFi
            r'\bnfts?\b',       # NFT/NFTs
            r'\bdaos?\b',       # DAO/DAOs
            r'\btvl\b',         # TVL
            r'\bstaking\b',     # Staking
            r'\bliquidity\b',   # Liquidity
            r'\bprotocols?\b',  # Protocol/Protocols
            r'\bdapps?\b',      # DApp/DApps
            r'\bweb3\b',        # Web3
            r'\bblockchain\b',  # Blockchain
            r'\bcrypto(?:currency)?\b',  # Crypto/Cryptocurrency
            r'\bmarket cap\b',  # Market cap
            r'\balt(?:coin)?s?\b',  # Alt/Altcoin/Alts
        ]
        
        keywords = []
        
        # Check for known ticker symbols only
        text_upper = clean_text.upper()
        for ticker in known_tickers:
            if re.search(rf'\b{ticker}\b', text_upper):
                keywords.append(ticker)
        
        # Extract specific crypto terms
        for pattern in crypto_specific_terms:
            matches = re.findall(pattern, clean_text, re.IGNORECASE)
            keywords.extend([match.lower() for match in matches])
        
        # Only look for crypto project names if we already have crypto context
        if keywords:  # Only if we found crypto-specific terms
            # Look for known crypto project names
            known_projects = ['Ethereum', 'Bitcoin', 'Solana', 'Avalanche', 'Polygon', 'Uniswap', 'Aave']
            for project in known_projects:
                if re.search(rf'\b{project}\b', clean_text, re.IGNORECASE):
                    keywords.append(project.lower())
        
        # Remove duplicates
        unique_keywords = list(set(keywords))
        
        return unique_keywords[:3]  # Limit to top 3 crypto-specific keywords
    
    def _expand_keywords(self, keywords: List[str]) -> List[str]:
        """Expand keywords with known synonyms and variations"""
        expanded = keywords.copy()
        
        # Common expansions for crypto terms
        expansions = {
            'BTC': ['Bitcoin', 'bitcoin'],
            'ETH': ['Ethereum', 'ethereum', 'ether'],
            'DeFi': ['decentralized finance', 'defi'],
            'NFT': ['non-fungible token', 'nft'],
            'DAO': ['decentralized autonomous organization', 'dao'],
            'TVL': ['total value locked', 'tvl'],
            'DEX': ['decentralized exchange', 'dex'],
            'CEX': ['centralized exchange', 'cex'],
        }
        
        for keyword in keywords:
            if keyword.upper() in expansions:
                expanded.extend(expansions[keyword.upper()])
        
        return list(set(expanded))  # Remove duplicates
    
    async def _search_reddit(self, keywords: List[str]) -> int:
        """Search Reddit for keyword mentions using real API only"""
        if not self.reddit_available:
            self.logger.info("Reddit API not configured - returning 0 results")
            return 0
        
        try:
            # Only use real Reddit API - no simulation
            import praw
            
            total_threads = 0
            for keyword in keywords[:3]:  # Limit API calls
                for subreddit_name in self.crypto_subreddits:
                    try:
                        subreddit = self.reddit.subreddit(subreddit_name)
                        results = list(subreddit.search(keyword, limit=10, sort='new', time_filter='day'))
                        total_threads += len(results)
                    except Exception as e:
                        self.logger.warning(f"Reddit search failed for {subreddit_name}: {e}")
                        continue
            return min(total_threads, 20)  # Cap at reasonable number
            
        except Exception as e:
            self.logger.warning(f"Reddit search failed: {e}")
            return 0
    
    async def _search_farcaster(self, keywords: List[str]) -> int:
        """Search Farcaster for keyword mentions using real API only"""
        try:
            # Only use real Farcaster API when available - no simulation
            # Since Farcaster API is not commonly available, return 0
            self.logger.info("Farcaster API not implemented - returning 0 results")
            return 0
            
        except Exception as e:
            self.logger.warning(f"Farcaster search failed: {e}")
            return 0
    
    async def _search_discord(self, keywords: List[str]) -> int:
        """Search Discord for keyword mentions using real API only"""
        try:
            # Only use real Discord API when available - no simulation
            # Discord search is very limited due to API restrictions
            # Since Discord bot API is not commonly available, return 0
            self.logger.info("Discord API not implemented - returning 0 results")
            return 0
            
        except Exception as e:
            self.logger.warning(f"Discord search failed: {e}")
            return 0
    
    def _calculate_echo_velocity(self, reddit_count: int, farcaster_count: int, discord_count: int) -> float:
        """Calculate normalized echo velocity score"""
        total_mentions = reddit_count + farcaster_count + discord_count
        
        # Use exponential decay to normalize (prevents unbounded growth)
        # Formula: 1 - e^(-total/scaling_factor)
        scaling_factor = 10  # Adjust based on expected volume
        velocity = 1 - (2.718 ** (-total_mentions / scaling_factor))
        
        return round(min(velocity, 1.0), 2)
    
    def _update_echo_memory(self, topic: str, reddit: int, farcaster: int, discord: int, velocity: float):
        """Update memory with echo metrics for historical tracking"""
        key = f"echo_map:{topic}"
        
        echo_data = {
            "last_seen": datetime.now().isoformat(),
            "reddit_threads": reddit,
            "farcaster_refs": farcaster,
            "discord_refs": discord,
            "echo_velocity": velocity,
            "total_mentions": reddit + farcaster + discord
        }
        
        # Get previous data for trend analysis
        prev_data = self.memory_store.get(key, {})
        if prev_data:
            echo_data["previous_velocity"] = prev_data.get("echo_velocity", 0.0)
            echo_data["velocity_change"] = velocity - prev_data.get("echo_velocity", 0.0)
        
        self.memory_store[key] = echo_data
        
        self.logger.debug(f"Updated echo memory for topic '{topic}': {echo_data}")
    
    def get_topic_history(self, topic: str) -> Optional[Dict[str, Any]]:
        """Get historical echo data for a topic"""
        key = f"echo_map:{topic}"
        return self.memory_store.get(key)