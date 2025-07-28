# 🐦 Twitter News Classifier v4.0 - Separated Workflow

## 🎯 What Is This?

The **Twitter News Classifier** is an advanced AI-powered system designed to automatically analyze, classify, and score cryptocurrency and blockchain news content from trusted Twitter accounts. The system now features a **robust two-phase architecture** that separates tweet extraction from analysis for maximum reliability and error recovery.

## 🏗️ Two-Phase Architecture

### 📡 Phase 1: Tweet Extraction
- **Independent tweet data extraction** from Twitter API
- **Comprehensive metadata collection** (users, threads, media, URLs)
- **Error-resistant data persistence** - extracted data is preserved even if analysis fails
- **Thread detection and context extraction**
- **Media and URL content analysis**

### 🤖 Phase 2: Multi-Agent Analysis  
- **12 specialized AI agents** working in collaboration
- **Processes pre-extracted tweet data** with robust error handling
- **API failure recovery** with retry logic and batch processing
- **Weighted scoring consolidation** with importance prioritization
- **Comprehensive result integration**

## 🚀 Key Features

### ✅ Enhanced Reliability
- **Independent phase processing** - extraction and analysis run separately
- **Data preservation** - tweets remain saved even if analysis fails
- **API failure tolerance** - robust error handling with retry mechanisms
- **Workflow recovery** - can resume analysis from extracted data

### 🤖 AI-Powered Analysis
- **12 Specialized Agents**: Summary, Preprocessor, Context Evaluator, Fact Checker, Depth Analyzer, Relevance Analyzer, Structure Analyzer, Reflective Agent, Metadata Ranking, Consensus Agent, Score Consolidator, Validator
- **Weighted Scoring System** with importance prioritization
- **Real-time content analysis** with comprehensive scoring

### 🐦 Twitter Integration
- **Twitter API v2** with comprehensive field extraction
- **Real thread detection** and full context extraction
- **Media content analysis** (images, videos, GIFs)
- **URL extraction and content analysis**
- **User metadata and credibility assessment**

### 🏗️ Clean Architecture
- **Domain-Driven Design (DDD)** structure
- **Separation of concerns** with clear service boundaries
- **Comprehensive error handling** and logging
- **Modular and testable** codebase

## 📊 The 12 AI Agents

| Agent | Weight | Purpose |
|-------|--------|---------|
| **Summary Agent** | 10% | Title and abstract generation |
| **Input Preprocessor** | 5% | Data quality and normalization |
| **Context Evaluator** | 15% | Content context and richness assessment |
| **Fact Checker** | 18% | Accuracy verification (highest importance) |
| **Depth Analyzer** | 12% | Content complexity and analytical depth |
| **Relevance Analyzer** | 15% | Real-world importance assessment |
| **Structure Analyzer** | 8% | Content organization evaluation |
| **Reflective Agent** | 7% | Meta-analysis and critical evaluation |
| **Metadata Ranking Agent** | 6% | User credibility assessment |
| **Consensus Agent** | 4% | Agreement and consensus evaluation |
| **Score Consolidator** | 0% | Aggregated results calculation (meta-agent) |
| **Validator** | 0% | Final validation and quality assurance (meta-agent) |

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd twitter-news-classifier

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp env_template.txt .env
# Edit .env with your API keys
```

### 2. Required API Keys

Create a `.env` file with:

```env
# Twitter API v2 Credentials
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
```

### 3. Run Analysis

```bash
# Execute the complete two-phase workflow
python main.py
```

## 🎯 How the System Works

### Phase 1: Tweet Extraction
1. **API Connection**: Connects to Twitter API v2 with comprehensive field extraction
2. **Account Processing**: Processes 48 trusted crypto/blockchain accounts
3. **Data Enhancement**: Adds thread context, media analysis, and URL extraction  
4. **Data Persistence**: Saves all extracted data to JSON files with metadata
5. **Error Handling**: Preserves data even if extraction encounters issues

### Phase 2: Multi-Agent Analysis
1. **Data Loading**: Loads pre-extracted tweet data from JSON files
2. **Batch Processing**: Processes tweets in configurable batches
3. **Agent Execution**: Each of 12 agents analyzes the content independently
4. **Error Recovery**: Implements retry logic for API failures
5. **Score Consolidation**: Combines agent scores using weighted importance
6. **Result Integration**: Merges analysis results with original tweet data

## 📂 Architecture Overview

```
twitter-news-classifier/
├── main.py                          # Main entry point (separated workflow)
├── domain/                          # Core business logic
│   ├── entities/                    # Business entities
│   │   ├── tweet.py                # Tweet entity with full metadata
│   │   └── analysis_result.py      # Analysis result structures
│   └── services/                    # Domain services
│       ├── tweet_extraction_service.py        # Phase 1: Tweet extraction
│       ├── multi_agent_analysis_service.py    # Phase 2: Analysis processing
│       └── multi_agent_analyzer.py            # Core multi-agent engine
├── application/                     # Application layer
│   └── orchestrators/              # Workflow orchestration
│       └── twitter_analysis_orchestrator.py   # Main workflow manager
├── infrastructure/                 # External integrations
│   ├── adapters/                   # External service adapters
│   │   └── twitter_api_adapter.py  # Twitter API integration
│   ├── repositories/               # Data persistence
│   │   └── file_repository.py      # File-based data storage
│   └── prompts/                    # AI agent prompts
│       └── agent_prompts.py        # Centralized agent prompts
├── data/                           # Data directory
│   └── workflow_runs/              # Workflow execution results
├── logs/                           # Execution logs
└── docs/                           # Documentation
```

## 📊 Sample Output Structure

### Workflow Results
```
data/workflow_runs/WORKFLOW_20241127_143022/
├── extraction/                     # Phase 1 results
│   ├── EXTRACTION_20241127_143022/
│   │   ├── extracted_tweets.json   # All tweet data with metadata
│   │   └── extraction_metadata.json # Extraction statistics
├── analysis/                       # Phase 2 results  
│   ├── ANALYSIS_20241127_143535/
│   │   ├── integrated_analysis_results.json # Full analysis results
│   │   ├── analysis_summary.json           # Analysis summary
│   │   └── intermediate/                   # Individual tweet analyses
└── workflow_result.json            # Complete workflow summary
```

## 🔧 Configuration Options

### Workflow Configuration
- **max_tweets**: Maximum tweets to extract (default: 30)
- **hours_back**: Time window for extraction (default: 24 hours)  
- **max_retries**: API failure retry attempts (default: 3)
- **batch_size**: Analysis batch size (default: 5)
- **continue_on_api_failure**: Whether to continue on errors (default: true)

### Error Handling Features
- **Independent phase processing** - extraction failure doesn't affect saved data
- **Retry logic** with configurable delays and maximum attempts
- **Data preservation** - extracted tweets saved regardless of analysis success
- **Comprehensive logging** for debugging and monitoring

## 🎯 Trusted Accounts

The system analyzes content from 48 carefully selected crypto/blockchain Twitter accounts:

**Key Figures**: VitalikButerin, naval, elonmusk, APompliano, aantonop
**News Sources**: CoinDesk, cointelegraph, bitcoinmagazine  
**Projects**: ethereum, solana, chainlink, Uniswap, aaveaave, MakerDAO
**Analysts**: TheCryptoDog, DocumentingBTC, lopp, ErikVoorhees
**Exchanges**: changpeng_cz, brian_armstrong, SBF_FTX
**And many more trusted voices in the crypto/blockchain space**

## 🛡️ Error Handling & Recovery

### Extraction Phase Recovery
- Twitter API rate limit handling
- Network error resilience  
- Partial data preservation
- Comprehensive error logging

### Analysis Phase Recovery
- OpenAI API failure handling
- Individual tweet retry logic
- Batch processing with failure isolation
- Intermediate result saving

## 🔍 Monitoring & Logging

- **Comprehensive logging** to `logs/` directory
- **Real-time progress tracking** with detailed status updates
- **Performance metrics** and execution statistics
- **Error analysis** and debugging information
- **Workflow summaries** with recommendations

## 📈 Performance Characteristics

- **Extraction**: ~2-5 minutes for 30 tweets (depending on API response times)
- **Analysis**: ~15-30 minutes for 30 tweets (depending on OpenAI API response times)
- **Total Workflow**: ~20-35 minutes for complete processing
- **Error Recovery**: Automatic retry with exponential backoff
- **Data Persistence**: All intermediate results saved for recovery

## 🚨 Troubleshooting

### Common Issues

1. **Twitter API Errors**
   - Verify API credentials in `.env`
   - Check API usage limits and quotas
   - Ensure account has proper permissions

2. **OpenAI API Errors**  
   - Verify OpenAI API key format
   - Check account billing and usage limits
   - Monitor rate limiting

3. **Extraction Successful, Analysis Failed**
   - Check OpenAI API key and billing
   - Review extracted data in `data/workflow_runs/`
   - Re-run analysis phase with saved extraction data

4. **No Tweets Extracted**
   - Verify Twitter account usernames
   - Check time window (hours_back parameter)
   - Review API permissions

## 🔮 Roadmap

- [ ] **Real-time Processing**: Live tweet stream analysis
- [ ] **Enhanced Media Analysis**: Advanced image and video content analysis  
- [ ] **Sentiment Tracking**: Historical sentiment analysis and trending
- [ ] **Custom Agent Configuration**: User-defined agent weights and prompts
- [ ] **API Rate Optimization**: Intelligent rate limiting and request batching
- [ ] **Dashboard Interface**: Web-based monitoring and results visualization

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests for any improvements.

---

**🐦 Twitter News Classifier v4.0** - Separating extraction from analysis for maximum reliability and error recovery.