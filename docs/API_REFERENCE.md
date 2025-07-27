# 📖 Enhanced Social Media Multi-Agent Analyzer - API Reference

## Core Classes and Methods

### TwitterApiAdapter

#### Configuration
```python
@dataclass
class TwitterApiConfig:
    consumer_key: str           # Twitter API Consumer Key
    consumer_secret: str        # Twitter API Consumer Secret  
    access_token: str          # Twitter API Access Token
    access_token_secret: str   # Twitter API Access Token Secret
    bearer_token: str          # Twitter API Bearer Token
```

#### Methods

##### `extract_tweets_from_accounts(account_usernames, max_tweets=30, hours_back=24)`
**Purpose**: Extract tweets from specified Twitter accounts

**Parameters**:
- `account_usernames: List[str]` - List of Twitter usernames (without @)
- `max_tweets: int = 30` - Maximum number of tweets to extract
- `hours_back: int = 24` - How many hours back to search

**Returns**: `List[Tweet]` - List of Tweet entities

**API Fields Extracted**:
- **Tweet Fields**: id, text, created_at, author_id, conversation_id, in_reply_to_user_id, public_metrics, context_annotations, entities, geo, lang, possibly_sensitive, referenced_tweets, reply_settings, source, withheld
- **User Fields**: id, name, username, created_at, description, entities, location, pinned_tweet_id, profile_image_url, protected, public_metrics, url, verified, withheld
- **Media Fields**: duration_ms, height, media_key, preview_image_url, type, url, width, public_metrics, alt_text

##### `get_conversation_tweets(conversation_id, max_tweets=10)`
**Purpose**: Get tweets from a conversation thread

**Parameters**:
- `conversation_id: str` - Twitter conversation ID
- `max_tweets: int = 10` - Maximum tweets to retrieve

**Returns**: `List[Dict[str, Any]]` - List of tweet dictionaries

##### `test_connection()`
**Purpose**: Test Twitter API connection

**Returns**: `bool` - Connection success status

---

### MultiAgentAnalyzer

#### Configuration
```python
# Agent Weights for Score Consolidation
agent_weights = {
    'summary_agent': 0.10,          # 10% - Title and abstract quality
    'input_preprocessor': 0.05,     # 5% - Data quality
    'context_evaluator': 0.15,     # 15% - Context richness (high importance)
    'fact_checker': 0.18,          # 18% - Factual accuracy (highest importance)
    'depth_analyzer': 0.12,        # 12% - Analytical depth
    'relevance_analyzer': 0.15,    # 15% - Real-world relevance (high importance)
    'structure_analyzer': 0.08,    # 8% - Content organization
    'reflective_agent': 0.07,      # 7% - Critical evaluation
    'metadata_ranking_agent': 0.06, # 6% - User credibility
    'consensus_agent': 0.04,       # 4% - Agreement assessment
    'score_consolidator': 0.0,     # 0% - Meta-agent
    'validator': 0.0               # 0% - Meta-agent
}
```

#### Methods

##### `analyze_tweet(tweet, run_id)`
**Purpose**: Analyze a tweet using all 12 agents

**Parameters**:
- `tweet: Tweet` - Tweet entity to analyze
- `run_id: str` - Unique run identifier

**Returns**: `AnalysisResult` - Complete analysis result

**Processing Flow**:
1. Prepare comprehensive input for agents
2. Execute 12 agents sequentially
3. Calculate consolidated score using weighted system
4. Convert enums to strings for JSON serialization
5. Return complete analysis result

---

### AnalyzeTweetsUseCase

#### Configuration
```python
@dataclass
class AnalysisConfig:
    max_tweets: int = 30
    hours_back: int = 24
    enable_thread_analysis: bool = True
    enable_media_analysis: bool = True
    output_format: str = "json"
    save_individual_results: bool = True
    generate_summary: bool = True
```

#### Methods

##### `execute(account_usernames, config)`
**Purpose**: Execute complete tweet analysis workflow

**Parameters**:
- `account_usernames: List[str]` - List of Twitter account usernames
- `config: AnalysisConfig` - Analysis configuration parameters

**Returns**: `Dict[str, Any]` - Analysis execution summary

**Workflow Steps**:
1. Extract tweets from Twitter API
2. Analyze tweets using multi-agent system
3. Save individual results (JSON + Markdown)
4. Generate and save comprehensive summary
5. Return execution summary

---

### FileRepository

#### Methods

##### `save_analysis_result(result, run_id, filename, subfolder="individual_content")`
**Purpose**: Save analysis result as JSON file

**Parameters**:
- `result: AnalysisResult` - Analysis result to save
- `run_id: str` - Run identifier for directory organization
- `filename: str` - Name of the file to save
- `subfolder: str = "individual_content"` - Subfolder within run directory

**Returns**: `str` - Full path of saved file

##### `save_text_file(content, run_id, filename, subfolder="individual_content")`
**Purpose**: Save text content to file

**Parameters**:
- `content: str` - Text content to save
- `run_id: str` - Run identifier
- `filename: str` - File name
- `subfolder: str` - Subfolder name

**Returns**: `str` - Full path of saved file

##### `cleanup_old_runs(keep_latest=3)`
**Purpose**: Clean up old run directories

**Parameters**:
- `keep_latest: int = 3` - Number of latest runs to keep

**Returns**: `int` - Number of directories removed

---

## Data Entities

### Tweet Entity
```python
@dataclass
class Tweet:
    # Core tweet data
    tweet_id: str
    text: str
    created_at: datetime
    author_username: str
    author_id: str
    
    # Engagement metrics
    like_count: int = 0
    retweet_count: int = 0
    reply_count: int = 0
    quote_count: int = 0
    
    # Rich metadata
    user_metadata: Optional[UserMetadata] = None
    media_attachments: Optional[MediaAttachment] = None
    external_links: List[str] = field(default_factory=list)
    thread_context: Optional[ThreadContext] = None
    conversation_context: Optional[Dict[str, Any]] = None
    
    # Analysis metadata
    content_type: Optional[ContentType] = None
    processing_timestamp: Optional[datetime] = None
    
    # Computed properties
    @property
    def engagement_score(self) -> float
    @property
    def has_media(self) -> bool
    @property
    def is_thread_tweet(self) -> bool
```

### AnalysisResult Entity
```python
@dataclass
class AnalysisResult:
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
    
    # Computed properties
    @property
    def success_rate(self) -> float
    @property
    def average_agent_score(self) -> float
    @property
    def has_media_analysis(self) -> bool
    @property
    def has_thread_analysis(self) -> bool
```

### UserMetadata Entity
```python
@dataclass
class UserMetadata:
    user_id: str
    username: str
    display_name: str
    created_at: datetime
    description: str
    verified: bool
    profile_image_url: str
    public_metrics: Dict[str, int]  # followers_count, following_count, tweet_count, listed_count
```

### MediaAttachment Entity
```python
@dataclass
class MediaAttachment:
    links_analyzed: List[Dict[str, Any]] = field(default_factory=list)
    images_analyzed: List[Dict[str, Any]] = field(default_factory=list)
    total_processing_time: float = 0.0
    summary: Dict[str, Any] = field(default_factory=dict)
```

### ThreadContext Entity
```python
@dataclass
class ThreadContext:
    conversation_id: Optional[str] = None
    is_thread: bool = False
    in_reply_to_user_id: Optional[str] = None
    thread_position: Optional[int] = None
```

---

## Error Handling

### Exception Types
```python
# Twitter API Errors
400 Bad Request         # Parameter validation errors
401 Unauthorized       # Authentication failures
403 Forbidden         # Access permission issues
429 Too Many Requests # Rate limit exceeded
500 Server Error      # Twitter service issues

# OpenAI API Errors
InvalidRequestError    # Request parameter issues
RateLimitError        # API rate limit exceeded
AuthenticationError   # API key issues
ServiceUnavailableError # Service downtime

# Application Errors
JSONDecodeError       # JSON parsing failures
ValidationError       # Data validation issues
FileNotFoundError     # File system issues
TimeoutError         # Network timeout issues
```

### Error Recovery Strategies
```python
# JSON Parsing Fallback
1. Direct JSON parsing
2. Extract from ```json code blocks
3. Extract from curly braces
4. Fallback response with default values

# Rate Limiting Strategy
1. Automatic wait_on_rate_limit=True
2. Custom pause every 10 accounts
3. TooManyRequests exception handling
4. Graceful degradation

# Network Error Recovery
1. Exponential backoff retry
2. Circuit breaker pattern
3. Fallback to cached data
4. Graceful service degradation
```

---

## Configuration Reference

### Environment Variables
```bash
# Required API Keys
OPENAI_API_KEY=sk-proj-your-openai-api-key
TWITTER_BEARER_TOKEN=your-twitter-bearer-token
TWITTER_API_KEY=your-twitter-consumer-key
TWITTER_API_SECRET=your-twitter-consumer-secret  
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret

# Optional Configuration
MAX_TWEETS=30
HOURS_BACK=24
ENABLE_THREAD_ANALYSIS=true
ENABLE_MEDIA_ANALYSIS=true
LOG_LEVEL=INFO
```

### OpenAI Configuration
```python
OpenAI_CONFIG = {
    "model": "gpt-4",
    "max_tokens": 2000,
    "temperature": 0.3,
    "system_message": "You are a specialized AI agent for social media content analysis. Always respond with valid JSON format as specified in the prompt."
}
```

### Analysis Configuration
```python
ANALYSIS_CONFIG = {
    "target_accounts": 48,
    "tweets_per_account": "5-10 (smart distribution)",
    "total_target_tweets": 30,
    "time_range_hours": 24,
    "exclude_content": ["retweets", "replies"],
    "include_expansions": True,
    "enable_thread_detection": True,
    "enable_media_analysis": True
}
```

---

## Performance Specifications

### Processing Metrics
```python
PERFORMANCE_METRICS = {
    "time_per_tweet": "~30 seconds (12 agents × 2.5s avg)",
    "total_processing_time": "~15 minutes for 30 tweets",
    "success_rate": ">95% under normal conditions",
    "memory_usage": "~500MB peak during processing",
    "api_requests_per_run": "~360 OpenAI + ~150 Twitter",
    "storage_per_tweet": "~50KB (JSON + Markdown)",
    "cost_per_run": "~$10-15 (GPT-4 pricing)"
}
```

### Rate Limits
```python
RATE_LIMITS = {
    "twitter_user_lookup": "300 requests per 15 minutes",
    "twitter_timeline": "75 requests per 15 minutes", 
    "openai_gpt4": "10,000 requests per minute",
    "openai_tokens": "150,000 tokens per minute",
    "file_operations": "No limits (local filesystem)"
}
```

This API reference provides comprehensive documentation for all classes, methods, and configuration options in the Enhanced Social Media Multi-Agent Analyzer system. 