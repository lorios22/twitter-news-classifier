# 🤖 Agent Reference Guide - Twitter News Classifier V2.0

## 📋 Table of Contents
- [Overview](#overview)
- [Signal Integrity Agents](#signal-integrity-agents)
- [Original Multi-Agent System](#original-multi-agent-system)
- [API & MCP Integrations](#api--mcp-integrations)
- [Agent Prompts Reference](#agent-prompts-reference)

---

## 🎯 Overview

This comprehensive reference guide documents all **17 agents** in the Twitter News Classifier system, including their functions, methods, APIs, and the complete prompts used for analysis.

### Agent Categories
- **5 Signal Integrity Agents**: Input validation and signal processing
- **12 Original Multi-Agent System**: Comprehensive content analysis

---

## 🛰️ Signal Integrity Agents

### 1. **Sarcasm Sentinel Agent**

#### **Primary Functions**
```python
class SarcasmSentinelAgent:
    async def analyze_sarcasm(self, text: str, author_handle: str) -> SarcasmResult
    def _prepare_prompt_context(self, text: str, author_handle: str) -> str
    def _parse_sarcasm_response(self, response: str) -> SarcasmResult
```

#### **Key Methods**
- **`analyze_sarcasm()`**: Main analysis method for detecting irony and tone inversion
- **`_prepare_prompt_context()`**: Formats input for OpenAI analysis
- **`_parse_sarcasm_response()`**: Parses JSON response into SarcasmResult dataclass

#### **Output Schema**
```python
@dataclass
class SarcasmResult:
    is_sarcastic: bool
    p_sarcasm: float
    reason: str
    confidence_level: str = "Medium"
```

#### **APIs Used**
- **OpenAI GPT-4**: Sarcasm detection and linguistic analysis
- **Memory Store**: Shared agent communication

#### **Prompt**
```
You are a Sarcasm Sentinel Agent specialized in detecting sarcasm, irony, and tone-inverted phrasing in social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Detect sarcasm and ironic statements including:
1. Tone inversion detection (literal meaning vs. intended meaning)
2. Linguistic cue analysis (emojis, punctuation, phrasing patterns)
3. Context evaluation for ironic intent
4. Confidence assessment in sarcasm detection
5. Author style consideration
6. Contextual sarcasm reasoning

Focus on identifying tweets that use irony or sarcasm so they aren't misinterpreted as factual claims.

RESPONSE FORMAT (JSON):
{
    "is_sarcastic": true/false,
    "p_sarcasm": 0.85,
    "reason": "Uses irony and eye-roll emoji to convey opposite of literal text",
    "linguistic_cues": ["eye_roll_emoji", "exaggerated_praise", "contradictory_context"],
    "confidence_level": "high/medium/low",
    "context_analysis": "detailed analysis of contextual clues",
    "author_style_notes": "observations about author's typical tone",
    "agent_score": 8.5,
    "detailed_reasoning": "Comprehensive sarcasm detection analysis..."
}
```

---

### 2. **Echo Mapper Agent**

#### **Primary Functions**
```python
class EchoMapperAgent:
    async def analyze_echo(self, text: str) -> EchoResult
    def _extract_keywords(self, text: str) -> List[str]
    async def _search_reddit(self, keywords: List[str]) -> int
    def _search_farcaster(self, keywords: List[str]) -> int
    def _search_discord(self, keywords: List[str]) -> int
    def _calculate_echo_velocity(self, reddit: int, farcaster: int, discord: int) -> float
```

#### **Key Methods**
- **`analyze_echo()`**: Main cross-platform virality analysis
- **`_extract_keywords()`**: Crypto-specific keyword extraction with known tickers
- **`_search_reddit()`**: Reddit API integration for subreddit searching
- **`_calculate_echo_velocity()`**: Virality metrics calculation

#### **Output Schema**
```python
@dataclass
class EchoResult:
    reddit_threads: int
    farcaster_refs: int
    discord_refs: int
    echo_velocity: float
    virality_assessment: str = "Low"
```

#### **APIs Used**
- **Reddit API (PRAW)**: Cross-platform detection and subreddit analysis
- **Memory Store**: Shared agent communication
- **Future**: Farcaster API, Discord API (placeholders implemented)

#### **Crypto-Specific Features**
```python
known_tickers = [
    'BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'AVAX', 'MATIC', 'LINK', 'UNI', 'AAVE',
    'COMP', 'MKR', 'YFI', 'SUSHI', 'CRV', 'BAL', 'SNX', 'LUNA', 'ATOM', 'FTM'
]

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
```

#### **Prompt**
```
You are an Echo Mapper Agent specialized in tracking cross-platform virality and discussion metrics.

COMPREHENSIVE INPUT:
{comprehensive_input}

CROSS-PLATFORM DATA:
{cross_platform_data}

TASK: Analyze cross-platform echo and virality including:
1. Reddit discussion volume analysis
2. Farcaster/social platform mention tracking
3. Echo velocity calculation
4. Viral trend identification
5. Platform-specific engagement patterns
6. Topic propagation assessment

Focus on measuring how widely the tweet's topic is being discussed across platforms.

RESPONSE FORMAT (JSON):
{
    "reddit_threads": 4,
    "farcaster_refs": 2,
    "discord_refs": 1,
    "echo_velocity": 0.75,
    "viral_indicators": ["trending_reddit", "multiple_platforms"],
    "platform_breakdown": {"reddit": 4, "farcaster": 2, "discord": 1},
    "trending_analysis": "assessment of viral potential",
    "topic_propagation": "how the topic is spreading",
    "agent_score": 7.8,
    "detailed_reasoning": "Comprehensive cross-platform echo analysis..."
}
```

---

### 3. **Latency Guard Agent**

#### **Primary Functions**
```python
class LatencyGuardAgent:
    async def analyze_latency(self, text: str, timestamp: datetime) -> LatencyResult
    def _extract_asset_symbols(self, text: str) -> List[str]
    async def _fetch_real_price_data(self, asset_symbol: str, timestamp: datetime) -> Optional[Dict]
    async def _fetch_binance_data(self, asset_symbol: str, timestamp: datetime) -> Optional[Dict]
    async def _fetch_coinbase_data(self, asset_symbol: str, timestamp: datetime) -> Optional[Dict]
    def _calculate_time_delta(self, tweet_time: datetime, price_time: datetime) -> int
    def _assess_staleness_risk(self, delta_seconds: int, price_change: float) -> str
```

#### **Key Methods**
- **`analyze_latency()`**: Main market timing analysis
- **`_extract_asset_symbols()`**: Cryptocurrency asset detection
- **`_fetch_real_price_data()`**: Multi-API price data fetching with fallbacks
- **`_calculate_time_delta()`**: Temporal relationship analysis

#### **Output Schema**
```python
@dataclass
class LatencyResult:
    repriced: bool
    delta_seconds: int
    price_change_pct: float
    asset_symbol: Optional[str]
```

#### **APIs Used**
- **Binance API**: Real-time cryptocurrency price feeds
- **Coinbase Developer Platform (CDP) API**: Professional trading data
- **Memory Store**: Shared agent communication

#### **Asset Detection**
```python
asset_patterns = {
    r'\b(?:bitcoin|btc)\b': 'BTC',
    r'\b(?:ethereum|eth)\b': 'ETH',
    r'\b(?:solana|sol)\b': 'SOL',
    r'\b(?:cardano|ada)\b': 'ADA',
    r'\b(?:polkadot|dot)\b': 'DOT',
    r'\b(?:avalanche|avax)\b': 'AVAX',
    r'\b(?:polygon|matic)\b': 'MATIC',
    r'\b(?:chainlink|link)\b': 'LINK',
    r'\b(?:uniswap|uni)\b': 'UNI',
    r'\b(?:aave|aave)\b': 'AAVE',
}
```

#### **Prompt**
```
You are a Latency Guard Agent specialized in detecting temporal misalignment between tweets and market/on-chain events.

COMPREHENSIVE INPUT:
{comprehensive_input}

MARKET DATA:
{market_data}

TASK: Analyze temporal relationships including:
1. Price movement timing analysis
2. On-chain event correlation
3. News staleness detection
4. Market repricing identification
5. Temporal anomaly flagging
6. Front-running signal detection

Focus on identifying cases where news comes after market/on-chain reactions.

RESPONSE FORMAT (JSON):
{
    "repriced": true/false,
    "delta_seconds": 600,
    "price_change_pct": -4.5,
    "asset_symbol": "BTC",
    "temporal_analysis": "detailed timing relationship analysis",
    "market_indicators": ["price_drop_before_tweet", "volume_spike"],
    "on_chain_events": "relevant blockchain activity",
    "staleness_assessment": "evaluation of news timeliness",
    "agent_score": 6.2,
    "detailed_reasoning": "Comprehensive temporal analysis..."
}
```

---

### 4. **AI Slop Filter Agent**

#### **Primary Functions**
```python
class SlopFilterAgent:
    async def analyze_slop(self, text: str, author_handle: str) -> SlopResult
    def _detect_cliche_patterns(self, text: str) -> int
    def _assess_factual_content(self, text: str) -> float
    def _calculate_quality_score(self, cliche_count: int, factual_adjustment: float) -> float
    def _assess_authenticity(self, quality_score: float) -> str
```

#### **Key Methods**
- **`analyze_slop()`**: Main content quality analysis
- **`_detect_cliche_patterns()`**: Pattern matching for generic/AI-generated content
- **`_assess_factual_content()`**: Factual content preservation logic
- **`_calculate_quality_score()`**: Quality metrics calculation

#### **Output Schema**
```python
@dataclass
class SlopResult:
    is_sloppy: bool
    slop_score: float
    reasoning: str
    content_authenticity: str = "Acceptable"
```

#### **APIs Used**
- **Memory Store**: Shared agent communication
- **Pattern Recognition**: Extensive regex patterns for slop detection

#### **Cliché Detection Patterns**
```python
cliche_patterns = [
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
]
```

#### **Prompt**
```
You are an AI Slop Filter Agent specialized in detecting low-effort, cliché-ridden, or AI-generated content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Analyze content quality and authenticity including:
1. Cliché and buzzword detection
2. AI-generated content identification
3. Repetitive pattern analysis
4. Content originality assessment
5. Formulaic writing detection
6. Content value evaluation

Focus on maintaining content quality while preserving valuable factual information.

RESPONSE FORMAT (JSON):
{
    "is_sloppy": true/false,
    "slop_score": 0.65,
    "cliche_count": 3,
    "detected_patterns": ["buzzword_heavy", "formulaic_structure"],
    "authenticity_indicators": ["unique_insight", "specific_details"],
    "quality_assessment": "assessment of overall content quality",
    "preservation_recommendation": "whether content should be preserved",
    "agent_score": 4.2,
    "detailed_reasoning": "Comprehensive content quality analysis..."
}
```

---

### 5. **Banned Phrase Skeptic Agent**

#### **Primary Functions**
```python
class BannedPhraseSkepticAgent:
    async def analyze_banned_phrases(self, text: str, author_handle: str) -> BannedPhraseResult
    def _detect_banned_terms(self, text: str) -> Tuple[List[str], float]
    def _calculate_tone_penalty(self, total_weight: float) -> float
    def _assess_risk_level(self, tone_penalty: float) -> str
```

#### **Key Methods**
- **`analyze_banned_phrases()`**: Main policy compliance analysis
- **`_detect_banned_terms()`**: Context-aware banned phrase detection
- **`_calculate_tone_penalty()`**: Penalty weight calculation
- **`_assess_risk_level()`**: Risk assessment based on violations

#### **Output Schema**
```python
@dataclass
class BannedPhraseResult:
    banned_terms: List[str]
    total_weight: float
    tone_penalty: float
    risk_assessment: str = "Low"
```

#### **APIs Used**
- **Memory Store**: Shared agent communication
- **Pattern Recognition**: Extensive banned phrase taxonomy

#### **Banned Phrase Taxonomy**
```python
banned_phrases = {
    # Financial advice (high penalty)
    (r'\bbuy\s+(?:now|immediately|today)\b', 2.0, "financial advice"),
    (r'\bguaranteed\s+(?:profit|return|gains?)\b', 2.5, "financial promises"),
    (r'\bsure\s+(?:thing|bet|win)\b', 1.8, "certainty claims"),
    
    # Pump language (medium-high penalty)
    (r'\bto\s+the\s+moon\b', 1.5, "pump language"),
    (r'\bmoon(?:ing|shot)\b', 1.3, "pump language"),
    (r'\blambo\b', 1.2, "materialistic hype"),
    (r'\bdiamond\s+hands?\b', 1.0, "meme language"),
    
    # Aggressive language (medium penalty)
    (r'\btrash\b', 1.0, "negative characterization"),
    (r'\bscam\b', 1.5, "fraud accusations"),
    (r'\brekt\b', 0.8, "aggressive language"),
    
    # Excessive caps (low penalty)
    (r'\b[A-Z]{4,}\b', 0.3, "excessive caps"),
    
    # Conspiracy theories (high penalty)
    (r'\brig(?:ged|ging)\b', 2.0, "manipulation claims"),
    (r'\bmanipulat(?:ed|ion)\b', 1.8, "manipulation claims"),
}

# Innocent context exceptions
innocent_contexts = [
    r'\bmoon\s+(?:landing|mission|rover)\b',  # Space references
    r'\bfull\s+moon\b',                       # Astronomical references
    r'\bmoon\s+(?:phase|cycle)\b',            # Natural phenomena
    r'\blamb\s+(?:chop|meat|dinner)\b',       # Food references
    r'\btrash\s+(?:can|bin|pickup)\b',        # Waste management
    r'\bfree\s+(?:shipping|trial|sample)\b',  # Legitimate offers
]
```

#### **Prompt**
```
You are a Banned Phrase Skeptic Agent specialized in detecting banned words/phrases and applying editorial tone penalties.

COMPREHENSIVE INPUT:
{comprehensive_input}

BANNED PHRASE TAXONOMY:
{banned_phrases}

TASK: Analyze editorial compliance including:
1. Banned word/phrase detection
2. Tone penalty calculation
3. Editorial standards assessment
4. Context-aware flagging
5. Severity classification
6. Brand voice alignment evaluation

Focus on maintaining editorial standards without eliminating potentially valuable content.

RESPONSE FORMAT (JSON):
{
    "banned_terms": ["moon", "lambo", "trash"],
    "total_weight": 2.3,
    "tone_penalty": 0.46,
    "violation_categories": ["hype_language", "inappropriate_tone"],
    "severity_assessment": "moderate tone violations detected",
    "context_considerations": "terms used in legitimate context",
    "editorial_impact": "assessment of brand voice compliance",
    "preservation_recommendation": "content has value despite tone issues",
    "agent_score": 5.4,
    "detailed_reasoning": "Comprehensive editorial standards analysis..."
}
```

---

## 🤖 Original Multi-Agent System

### **Phase 1: Parallel Analysis Agents (10 Agents)**

#### **1. Summary Agent**
**Function**: Content summarization and key theme identification
```python
async def analyze_summary(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Title generation, abstract creation, content categorization
**API**: OpenAI GPT-4

#### **2. Input Preprocessor**
**Function**: Data quality assessment and normalization
```python
async def analyze_input_preprocessing(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Data cleansing, quality metrics, missing information identification
**API**: OpenAI GPT-4

#### **3. Context Evaluator**
**Function**: Contextual richness and source credibility assessment
```python
async def analyze_context(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Information completeness, source credibility, temporal relevance
**API**: OpenAI GPT-4

#### **4. Fact Checker**
**Function**: Factual accuracy verification and misinformation detection
```python
async def analyze_facts(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Factual claims verification, accuracy assessment, misinformation risk
**API**: OpenAI GPT-4

#### **5. Depth Analyzer**
**Function**: Content depth and analytical sophistication assessment
```python
async def analyze_depth(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Analysis depth, sophistication level, analytical value
**API**: OpenAI GPT-4

#### **6. Relevance Analyzer**
**Function**: Topic relevance and audience value assessment
```python
async def analyze_relevance(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Topic relevance, audience value, market relevance
**API**: OpenAI GPT-4

#### **7. Structure Analyzer**
**Function**: Content structure and presentation quality evaluation
```python
async def analyze_structure(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Content organization, presentation quality, readability
**API**: OpenAI GPT-4

#### **8. Reflective Agent**
**Function**: Meta-analysis and critical evaluation
```python
async def analyze_reflection(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Critical evaluation, perspective analysis, bias assessment
**API**: OpenAI GPT-4

#### **9. Metadata Ranking Agent**
**Function**: Author credibility and engagement metrics analysis
```python
async def analyze_metadata(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Author authority, engagement patterns, social proof
**API**: OpenAI GPT-4

#### **10. Consensus Agent**
**Function**: Cross-agent consensus building and consistency checking
```python
async def analyze_consensus(self, tweet: Tweet, run_id: str) -> AgentResponse
```

**Prompt Focus**: Agent agreement, consistency verification, consensus building
**API**: OpenAI GPT-4

### **Phase 2: Sequential Processing Agents (2 Agents)**

#### **11. Score Consolidator**
**Function**: Weighted score aggregation and final scoring
```python
async def analyze_score_consolidation(self, tweet: Tweet, run_id: str, all_responses: Dict[str, AgentResponse]) -> AgentResponse
```

**Prompt Focus**: Score aggregation, weighting methodology, final score calculation
**API**: OpenAI GPT-4

#### **12. Validator**
**Function**: Final quality assurance and validation
```python
async def analyze_validation(self, tweet: Tweet, run_id: str, all_responses: Dict[str, AgentResponse]) -> AgentResponse
```

**Prompt Focus**: Quality validation, completeness verification, error detection
**API**: OpenAI GPT-4

---

## 🔌 API & MCP Integrations

### **External APIs**

#### **1. OpenAI API**
- **Usage**: All 17 agents for LLM-powered analysis
- **Model**: GPT-4 for advanced reasoning and analysis
- **Volume**: 300+ calls per complete analysis
- **Configuration**:
  ```python
  client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
  ```

#### **2. Reddit API (PRAW)**
- **Usage**: Echo Mapper cross-platform detection
- **Features**: Subreddit searching, thread analysis, comment metrics
- **Configuration**:
  ```python
  reddit = praw.Reddit(
      client_id=os.getenv('REDDIT_CLIENT_ID'),
      client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
      user_agent='TwitterNewsClassifier/1.0'
  )
  ```

#### **3. Binance API**
- **Usage**: Real-time cryptocurrency price data
- **Features**: Price feeds, historical data, market timing
- **Endpoints**: `/api/v3/klines`, `/api/v3/ticker/price`
- **Configuration**:
  ```python
  headers = {'X-MBX-APIKEY': os.getenv('BINANCE_API_KEY')}
  ```

#### **4. Coinbase Developer Platform (CDP) API**
- **Usage**: Professional trading data and price feeds
- **Features**: Advanced trading data, institutional-grade APIs
- **Authentication**: API key + secret + passphrase
- **Configuration**:
  ```python
  auth_headers = {
      'CB-ACCESS-KEY': os.getenv('COINBASE_API_KEY'),
      'CB-ACCESS-SECRET': os.getenv('COINBASE_API_SECRET'),
      'CB-ACCESS-PASSPHRASE': os.getenv('COINBASE_API_PASSPHRASE')
  }
  ```

#### **5. Twitter API**
- **Usage**: High-quality tweet extraction
- **Features**: Real-time tweet data, user metadata, engagement metrics
- **Volume**: 50+ tweets per extraction from 20 verified accounts
- **Configuration**:
  ```python
  client = tweepy.Client(
      bearer_token=config.bearer_token,
      consumer_key=config.consumer_key,
      consumer_secret=config.consumer_secret,
      access_token=config.access_token,
      access_token_secret=config.access_token_secret,
      wait_on_rate_limit=True
  )
  ```

### **MCP (Model Context Protocol) Integrations**

#### **1. Context7 MCP**
- **Usage**: Documentation retrieval and library information
- **Functions**: 
  - `resolve-library-id`: Package name resolution
  - `get-library-docs`: Documentation fetching
- **Benefits**: Up-to-date technical documentation access

#### **2. GitHub MCP**
- **Usage**: Repository analysis and pull request information
- **Functions**:
  - `fetch_pull_request`: PR and commit analysis
  - Repository metadata extraction
- **Benefits**: Code change tracking and development insights

#### **3. Web Search MCP**
- **Usage**: Real-time information verification
- **Functions**: Current fact-checking and trend verification
- **Benefits**: Up-to-date information validation

### **Memory & Storage Systems**

#### **1. Shared Memory Store**
```python
memory_store: Dict[str, Any] = {}
```
- **Usage**: Inter-agent communication
- **Features**: Persistent data sharing, agent coordination
- **Scope**: Single analysis session

#### **2. File Repository**
```python
class FileRepository:
    def save_json(self, data: Dict, filepath: Path) -> bool
    def load_json(self, filepath: Path) -> Optional[Dict]
```
- **Usage**: Results persistence and data storage
- **Features**: JSON serialization, error handling
- **Location**: `results/` directory

---

## 📝 Agent Prompts Reference

### **Signal Integrity Agent Prompts**

#### **Sarcasm Sentinel Prompt**
```
You are a Sarcasm Sentinel Agent specialized in detecting sarcasm, irony, and tone-inverted phrasing in social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Detect sarcasm and ironic statements including:
1. Tone inversion detection (literal meaning vs. intended meaning)
2. Linguistic cue analysis (emojis, punctuation, phrasing patterns)
3. Context evaluation for ironic intent
4. Confidence assessment in sarcasm detection
5. Author style consideration
6. Contextual sarcasm reasoning

Focus on identifying tweets that use irony or sarcasm so they aren't misinterpreted as factual claims.

RESPONSE FORMAT (JSON):
{
    "is_sarcastic": true/false,
    "p_sarcasm": 0.85,
    "reason": "Uses irony and eye-roll emoji to convey opposite of literal text",
    "linguistic_cues": ["eye_roll_emoji", "exaggerated_praise", "contradictory_context"],
    "confidence_level": "high/medium/low",
    "context_analysis": "detailed analysis of contextual clues",
    "author_style_notes": "observations about author's typical tone",
    "agent_score": 8.5,
    "detailed_reasoning": "Comprehensive sarcasm detection analysis..."
}
```

#### **Echo Mapper Prompt**
```
You are an Echo Mapper Agent specialized in tracking cross-platform virality and discussion metrics.

COMPREHENSIVE INPUT:
{comprehensive_input}

CROSS-PLATFORM DATA:
{cross_platform_data}

TASK: Analyze cross-platform echo and virality including:
1. Reddit discussion volume analysis
2. Farcaster/social platform mention tracking
3. Echo velocity calculation
4. Viral trend identification
5. Platform-specific engagement patterns
6. Topic propagation assessment

Focus on measuring how widely the tweet's topic is being discussed across platforms.

RESPONSE FORMAT (JSON):
{
    "reddit_threads": 4,
    "farcaster_refs": 2,
    "discord_refs": 1,
    "echo_velocity": 0.75,
    "viral_indicators": ["trending_reddit", "multiple_platforms"],
    "platform_breakdown": {"reddit": 4, "farcaster": 2, "discord": 1},
    "trending_analysis": "assessment of viral potential",
    "topic_propagation": "how the topic is spreading",
    "agent_score": 7.8,
    "detailed_reasoning": "Comprehensive cross-platform echo analysis..."
}
```

#### **Latency Guard Prompt**
```
You are a Latency Guard Agent specialized in detecting temporal misalignment between tweets and market/on-chain events.

COMPREHENSIVE INPUT:
{comprehensive_input}

MARKET DATA:
{market_data}

TASK: Analyze temporal relationships including:
1. Price movement timing analysis
2. On-chain event correlation
3. News staleness detection
4. Market repricing identification
5. Temporal anomaly flagging
6. Front-running signal detection

Focus on identifying cases where news comes after market/on-chain reactions.

RESPONSE FORMAT (JSON):
{
    "repriced": true/false,
    "delta_seconds": 600,
    "price_change_pct": -4.5,
    "asset_symbol": "BTC",
    "temporal_analysis": "detailed timing relationship analysis",
    "market_indicators": ["price_drop_before_tweet", "volume_spike"],
    "on_chain_events": "relevant blockchain activity",
    "staleness_assessment": "evaluation of news timeliness",
    "agent_score": 6.2,
    "detailed_reasoning": "Comprehensive temporal analysis..."
}
```

#### **AI Slop Filter Prompt**
```
You are an AI Slop Filter Agent specialized in detecting low-effort, cliché-ridden, or AI-generated content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Analyze content quality and authenticity including:
1. Cliché and buzzword detection
2. AI-generated content identification
3. Repetitive pattern analysis
4. Content originality assessment
5. Formulaic writing detection
6. Content value evaluation

Focus on maintaining content quality while preserving valuable factual information.

RESPONSE FORMAT (JSON):
{
    "is_sloppy": true/false,
    "slop_score": 0.65,
    "cliche_count": 3,
    "detected_patterns": ["buzzword_heavy", "formulaic_structure"],
    "authenticity_indicators": ["unique_insight", "specific_details"],
    "quality_assessment": "assessment of overall content quality",
    "preservation_recommendation": "whether content should be preserved",
    "agent_score": 4.2,
    "detailed_reasoning": "Comprehensive content quality analysis..."
}
```

#### **Banned Phrase Skeptic Prompt**
```
You are a Banned Phrase Skeptic Agent specialized in detecting banned words/phrases and applying editorial tone penalties.

COMPREHENSIVE INPUT:
{comprehensive_input}

BANNED PHRASE TAXONOMY:
{banned_phrases}

TASK: Analyze editorial compliance including:
1. Banned word/phrase detection
2. Tone penalty calculation
3. Editorial standards assessment
4. Context-aware flagging
5. Severity classification
6. Brand voice alignment evaluation

Focus on maintaining editorial standards without eliminating potentially valuable content.

RESPONSE FORMAT (JSON):
{
    "banned_terms": ["moon", "lambo", "trash"],
    "total_weight": 2.3,
    "tone_penalty": 0.46,
    "violation_categories": ["hype_language", "inappropriate_tone"],
    "severity_assessment": "moderate tone violations detected",
    "context_considerations": "terms used in legitimate context",
    "editorial_impact": "assessment of brand voice compliance",
    "preservation_recommendation": "content has value despite tone issues",
    "agent_score": 5.4,
    "detailed_reasoning": "Comprehensive editorial standards analysis..."
}
```

### **Original Multi-Agent System Prompts**

#### **Summary Agent Prompt**
```
You are a Summary Agent specialized in generating comprehensive titles and abstracts for social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Generate an extensive summary analysis including:
1. A compelling, descriptive title that captures the content essence
2. A detailed abstract (100-150 words) summarizing key points
3. Key themes and topics identified
4. Content categorization (announcement, analysis, news, etc.)
5. Relevance assessment
6. Quality score (1-10)

Focus on identifying main topics, themes, and providing clear, engaging summaries.

RESPONSE FORMAT (JSON):
{
    "title": "Generated descriptive title",
    "abstract": "Detailed 100-150 word abstract",
    "key_themes": ["theme1", "theme2", "theme3"],
    "content_category": "category",
    "relevance_assessment": "detailed relevance assessment",
    "quality_indicators": {"clarity": 8, "focus": 9, "accuracy": 7},
    "agent_score": 8.5,
    "detailed_reasoning": "Comprehensive explanation of analysis..."
}
```

#### **Input Preprocessor Prompt**
```
You are an Input Preprocessor Agent specialized in data quality assessment and preprocessing for social media analysis.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Perform comprehensive input preprocessing including:
1. Data quality assessment and scoring
2. Missing information identification
3. Content normalization recommendations
4. Data consistency verification
5. Format standardization assessment
6. Input reliability scoring (1-10)

Focus on ensuring high-quality, consistent input for downstream analysis.

RESPONSE FORMAT (JSON):
{
    "normalized_text": "cleaned and normalized content",
    "data_quality_assessment": "overall data quality evaluation",
    "issues_identified": ["issue1", "issue2"],
    "missing_information": ["missing_field1", "missing_field2"],
    "preprocessing_applied": ["action1", "action2"],
    "quality_metrics": {"completeness": 8, "accuracy": 9, "consistency": 7},
    "agent_score": 8.2,
    "detailed_reasoning": "Comprehensive preprocessing analysis..."
}
```

#### **Context Evaluator Prompt**
```
You are a Context Evaluator Agent specialized in assessing contextual richness and information quality of social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Evaluate contextual dimensions including:
1. Information richness and depth assessment
2. Source credibility evaluation
3. Temporal relevance analysis
4. Contextual completeness verification
5. Background information adequacy
6. Context quality scoring (1-10)

Focus on understanding the broader context and information landscape.

RESPONSE FORMAT (JSON):
{
    "context_richness": "assessment of information depth",
    "information_completeness": "evaluation of available information",
    "source_credibility": "credibility assessment",
    "temporal_relevance": "timeliness evaluation",
    "quality_dimensions": {"depth": 7, "accuracy": 8, "relevance": 9, "clarity": 8},
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "agent_score": 7.8,
    "detailed_reasoning": "Comprehensive contextual analysis..."
}
```

#### **Fact Checker Prompt**
```
You are a Fact Checker Agent specialized in verifying factual accuracy and identifying potential misinformation in social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Perform comprehensive fact verification including:
1. Factual claims identification and verification
2. Misinformation risk assessment
3. Source reliability evaluation
4. Evidence quality assessment
5. Accuracy confidence scoring
6. Verification score (1-10)

Focus on identifying and verifying specific factual claims while assessing misinformation risk.

RESPONSE FORMAT (JSON):
{
    "factual_claims": ["claim1", "claim2"],
    "accuracy_assessment": "overall accuracy evaluation",
    "verification_status": "verification outcome",
    "credibility_indicators": ["indicator1", "indicator2"],
    "misinformation_risk": "risk level assessment",
    "confidence_level": "verification confidence",
    "accuracy_metrics": {"verifiability": 7, "consistency": 8, "reliability": 6},
    "agent_score": 7.5,
    "detailed_reasoning": "Comprehensive fact-checking analysis..."
}
```

#### **Depth Analyzer Prompt**
```
You are a Depth Analyzer Agent specialized in evaluating the analytical depth and sophistication of social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Analyze content depth including:
1. Analytical sophistication assessment
2. Insight quality evaluation
3. Complexity level analysis
4. Original thinking identification
5. Depth vs. surface-level distinction
6. Analytical depth scoring (1-10)

Focus on distinguishing between superficial and deeply analytical content.

RESPONSE FORMAT (JSON):
{
    "analytical_depth": "assessment of analysis sophistication",
    "insight_quality": "evaluation of insights provided",
    "complexity_level": "content complexity assessment",
    "original_contributions": ["contribution1", "contribution2"],
    "depth_indicators": ["indicator1", "indicator2"],
    "sophistication_metrics": {"analysis": 6, "insight": 7, "complexity": 5},
    "depth_category": "surface/moderate/deep",
    "agent_score": 6.8,
    "detailed_reasoning": "Comprehensive depth analysis..."
}
```

#### **Relevance Analyzer Prompt**
```
You are a Relevance Analyzer Agent specialized in evaluating topic relevance and audience value of social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Assess relevance dimensions including:
1. Topic relevance to cryptocurrency/finance domain
2. Audience value assessment
3. Market relevance evaluation
4. Timeliness and currency analysis
5. Interest level prediction
6. Relevance scoring (1-10)

Focus on determining how relevant and valuable the content is for the target audience.

RESPONSE FORMAT (JSON):
{
    "topic_relevance": "domain relevance assessment",
    "audience_value": "value proposition for audience",
    "market_relevance": "financial market relevance",
    "timeliness_assessment": "currency and timeliness evaluation",
    "interest_prediction": "predicted audience interest level",
    "relevance_metrics": {"domain": 8, "audience": 7, "market": 9, "timing": 6},
    "relevance_category": "high/medium/low",
    "agent_score": 7.6,
    "detailed_reasoning": "Comprehensive relevance analysis..."
}
```

#### **Structure Analyzer Prompt**
```
You are a Structure Analyzer Agent specialized in evaluating content organization, flow, and presentation quality.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Analyze structural elements including:
1. Content organization assessment
2. Information flow evaluation
3. Presentation quality analysis
4. Readability and clarity scoring
5. Structural coherence verification
6. Structure quality scoring (1-10)

Focus on how well the content is organized and presented for maximum impact.

RESPONSE FORMAT (JSON):
{
    "organization_quality": "content organization assessment",
    "information_flow": "logical flow evaluation",
    "presentation_assessment": "presentation quality analysis",
    "readability_score": "readability and clarity evaluation",
    "structural_strengths": ["strength1", "strength2"],
    "structural_weaknesses": ["weakness1", "weakness2"],
    "structure_metrics": {"organization": 8, "flow": 7, "clarity": 9, "coherence": 8},
    "agent_score": 8.1,
    "detailed_reasoning": "Comprehensive structural analysis..."
}
```

#### **Reflective Agent Prompt**
```
You are a Reflective Agent specialized in meta-analysis and critical evaluation of social media content and analysis process.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Provide reflective analysis including:
1. Critical evaluation of content and analysis
2. Perspective assessment and bias identification
3. Alternative viewpoint consideration
4. Analysis quality reflection
5. Improvement recommendations
6. Reflection quality scoring (1-10)

Focus on critical thinking and meta-analysis of both content and analytical process.

RESPONSE FORMAT (JSON):
{
    "critical_evaluation": "critical assessment of content",
    "perspective_analysis": "viewpoint and bias evaluation",
    "alternative_viewpoints": ["viewpoint1", "viewpoint2"],
    "analysis_reflection": "reflection on analysis quality",
    "bias_identification": ["bias1", "bias2"],
    "improvement_suggestions": ["suggestion1", "suggestion2"],
    "reflection_metrics": {"criticality": 7, "objectivity": 8, "depth": 6},
    "agent_score": 7.3,
    "detailed_reasoning": "Comprehensive reflective analysis..."
}
```

#### **Metadata Ranking Agent Prompt**
```
You are a Metadata Ranking Agent specialized in evaluating author authority, social proof, and engagement patterns.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Analyze metadata dimensions including:
1. Author authority and credibility assessment
2. Social proof evaluation (followers, verification)
3. Engagement pattern analysis
4. Influence metrics evaluation
5. Network effects assessment
6. Metadata quality scoring (1-10)

Focus on quantifying the social and authority signals around the content.

RESPONSE FORMAT (JSON):
{
    "author_authority": "authority level assessment",
    "social_proof_analysis": "social proof evaluation",
    "engagement_patterns": "engagement metrics analysis",
    "influence_assessment": "influence level evaluation",
    "network_effects": "network impact assessment",
    "credibility_indicators": ["indicator1", "indicator2"],
    "authority_metrics": {"expertise": 7, "influence": 8, "trust": 6},
    "agent_score": 7.4,
    "detailed_reasoning": "Comprehensive metadata analysis..."
}
```

#### **Consensus Agent Prompt**
```
You are a Consensus Agent specialized in building consensus across multiple analytical perspectives and identifying agreement patterns.

COMPREHENSIVE INPUT:
{comprehensive_input}

ALL AGENT RESPONSES:
{all_agent_responses}

TASK: Build analytical consensus including:
1. Cross-agent agreement identification
2. Disagreement pattern analysis
3. Consensus strength assessment
4. Conflicting viewpoint resolution
5. Unified perspective development
6. Consensus quality scoring (1-10)

Focus on synthesizing multiple analytical perspectives into a coherent consensus view.

RESPONSE FORMAT (JSON):
{
    "consensus_overview": "overall consensus assessment",
    "agreement_areas": ["area1", "area2"],
    "disagreement_points": ["point1", "point2"],
    "consensus_strength": "strength of agreement",
    "conflict_resolution": "resolution of conflicting views",
    "unified_perspective": "synthesized analytical view",
    "consensus_metrics": {"agreement": 8, "consistency": 7, "coherence": 9},
    "agent_score": 8.2,
    "detailed_reasoning": "Comprehensive consensus analysis..."
}
```

#### **Score Consolidator Prompt**
```
You are a Score Consolidator Agent specialized in aggregating and weighting scores from multiple analytical agents.

COMPREHENSIVE INPUT:
{comprehensive_input}

ALL AGENT RESPONSES:
{all_agent_responses}

TASK: Consolidate scoring including:
1. Individual agent score analysis
2. Weighted aggregation methodology
3. Score consistency verification
4. Outlier identification and handling
5. Final consolidated score calculation
6. Consolidation quality scoring (1-10)

Focus on creating a fair, weighted, and representative consolidated score.

RESPONSE FORMAT (JSON):
{
    "individual_scores": {"agent1": 8.2, "agent2": 7.5},
    "weighting_methodology": "explanation of weighting approach",
    "score_consistency": "consistency assessment across agents",
    "outlier_analysis": "identification of score outliers",
    "consolidated_score": 7.8,
    "confidence_level": "confidence in consolidated score",
    "scoring_metrics": {"consistency": 8, "representativeness": 9, "fairness": 8},
    "agent_score": 8.5,
    "detailed_reasoning": "Comprehensive score consolidation analysis..."
}
```

#### **Validator Prompt**
```
You are a Validator Agent specialized in final quality assurance and comprehensive validation of analytical results.

COMPREHENSIVE INPUT:
{comprehensive_input}

ALL AGENT RESPONSES:
{all_agent_responses}

TASK: Perform final validation including:
1. Analysis quality validation
2. Consistency check across agents
3. Completeness verification
4. Error detection and reporting
5. Final quality assurance
6. Validation score (1-10)

Ensure all analysis meets quality standards and identify any issues.

RESPONSE FORMAT (JSON):
{
    "analysis_quality": "validation of overall analysis quality",
    "consistency_check": "verification of consistency across agents",
    "completeness_verification": "assessment of analysis completeness",
    "error_detection": "identification of potential errors",
    "quality_assurance": "final quality assessment",
    "validation_metrics": {"quality": 9, "consistency": 8, "completeness": 9, "accuracy": 8},
    "validation_passed": true,
    "identified_issues": ["issue1", "issue2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "agent_score": 8.8,
    "detailed_reasoning": "Comprehensive validation analysis..."
}
```

---

*Last Updated: August 10, 2025*  
*Document Version: 1.0*  
*Total Agents Documented: 17*  
*Complete Function and Prompt Reference*