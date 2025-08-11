# 🚀 Twitter News Classifier V2.0 - Input-Sovereign Classification System

## 🎯 Overview
Advanced **17-agent multi-agent system** for comprehensive Twitter content analysis in the cryptocurrency and financial news space. Features **5 Signal Integrity Agents** working alongside the original **12-agent system** to provide robust, input-sovereign classification.

## ✨ Key Features

### 🛰️ Signal Integrity Layer (NEW)
- **Sarcasm Sentinel**: Detects irony and tone inversion
- **Echo Mapper**: Cross-platform virality analysis with Reddit API
- **Latency Guard**: Market timing analysis with Binance/Coinbase APIs
- **AI Slop Filter**: Content quality and authenticity assessment  
- **Banned Phrase Skeptic**: Policy compliance with context-aware detection

### 🤖 Enhanced Multi-Agent Architecture
- **17 specialized agents** working in parallel and sequential phases
- **Real-time API integration** with OpenAI, Reddit, Binance, Coinbase
- **Comprehensive scoring system** (0-10 scale with quality mapping)
- **Intelligent human escalation** for edge cases
- **Domain-driven design** with clean architectural separation

### 📊 Advanced Analytics
- **High-quality tweet extraction** (25+ tweets from 20 verified accounts)
- **Complete metadata preservation** (user profiles, engagement metrics)
- **Real-time processing** with 100% success rate
- **Comprehensive JSON output** with detailed agent responses

## 🚀 Quick Start

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Python 3.8+ required
```

### Configuration
1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_key_here
   
   # Optional but recommended for full functionality
   TWITTER_API_KEY=your_twitter_key
   REDDIT_CLIENT_ID=your_reddit_id
   REDDIT_CLIENT_SECRET=your_reddit_secret
   BINANCE_API_KEY=your_binance_key
   COINBASE_API_KEY=your_coinbase_key
   COINBASE_API_SECRET=your_coinbase_secret
   ```

### Running the Complete Analysis
```bash
# Single command execution
python3 main.py

# Expected output:
# ✅ 25 tweets processed
# ✅ 17 agents analyzing each tweet  
# ✅ 100% success rate
# ✅ Results saved to results/twitter_analysis_results_YYYYMMDD_HHMMSS.json
```

## 🏗️ System Architecture

### Input-Sovereign Classification Pipeline
```
📡 Twitter API → 🛰️ Signal Integrity Layer → 🤖 Multi-Agent Analysis → 📊 Consolidated Output
     ↓                    ↓                        ↓                      ↓
  25+ tweets      5 specialized agents    12 analysis agents      JSON with scores
```

### Project Structure
```
├── main.py                          # Central execution entry point
├── domain/
│   ├── entities/                   # Core business objects (Tweet, AnalysisResult)
│   └── services/
│       ├── signal_integrity/      # 5 Signal Integrity Agents
│       ├── core_analysis/          # Original 12-agent system
│       ├── orchestration/          # System coordination
│       └── memory/                 # Memory management
├── infrastructure/
│   ├── adapters/                   # External API integrations
│   ├── repositories/               # Data persistence
│   └── prompts/                    # AI prompt management
└── results/                        # Analysis outputs
```

## 📊 Performance Metrics

### Latest System Performance
- ✅ **Tweets Processed**: 25/25 (100%)
- ✅ **Agent Success Rate**: 425/425 (100%)
- 🎯 **High-Quality Results**: 11/25 tweets scoring > 6.0 (44%)
- 🏆 **Top Score Achieved**: 7.654/10
- ⚡ **Processing Speed**: ~30-60 seconds per tweet
- 📈 **Quality Distribution**: 20% Excellent, 24% Good, 56% Average

### API Integration Status
- 🧠 **OpenAI API**: ✅ 300+ calls per analysis, 100% success
- 📱 **Reddit API**: ✅ Cross-platform detection active
- 💱 **Binance API**: ✅ Real-time price data for major cryptocurrencies
- 🏦 **Coinbase CDP**: ✅ Professional trading data access
- 🐦 **Twitter API**: ✅ High-quality tweet extraction from verified accounts

## 📄 Output Format

Each analysis generates a comprehensive JSON file containing:

### Complete Tweet Analysis
```json
{
  "analysis_metadata": {
    "timestamp": "2025-08-10T15:27:35.496618",
    "total_tweets": 25,
    "agents_count": 17,
    "language": "English"
  },
  "tweets_analysis": [
    {
      "tweet_metadata": { /* Complete tweet and user data */ },
      "signal_integrity_analysis": { /* 5 agent responses */ },
      "original_multi_agent_analysis": { /* 12 agent responses */ },
      "consolidated_scoring": {
        "final_score": 7.654,
        "qualitative_assessment": "Excellent",
        "recommendation": "Approve"
      },
      "human_escalation_assessment": { /* Routing logic */ }
    }
  ],
  "analysis_summary": {
    "total_tweets_processed": 25,
    "successful_analyses": 25,
    "success_rate_percentage": 100.0,
    "system_performance": "Excellent"
  }
}
```

## 🔧 Configuration Options

### Tweet Extraction Settings
- **Volume**: 25+ tweets per analysis (configurable in `main.py`)
- **Sources**: 20 verified crypto/finance accounts
- **Quality Filter**: 100+ likes, verified engagement
- **Time Window**: 72 hours (configurable)

### Agent Configuration
- **Signal Integrity**: All 5 agents enabled by default
- **Original System**: All 12 agents active
- **Scoring**: 0-10 scale with qualitative mapping
- **Escalation**: Configurable thresholds for human review

## 📚 Documentation

### Technical Documentation
- 📋 **[System Architecture V2.0](SYSTEM_ARCHITECTURE_V2.md)**: Comprehensive technical overview
- 📝 **[Implementation Changelog](IMPLEMENTATION_CHANGELOG.md)**: Detailed change tracking
- 🤖 **[Agent Reference Guide](AGENT_REFERENCE_GUIDE.md)**: Complete agent functions, APIs, and prompts
- 🔧 **[API Reference](docs/API_REFERENCE.md)**: Complete method documentation

### Architectural Diagrams
- 🏗️ **System Flow Diagram**: Visual representation of the 17-agent pipeline
- 📊 **Data Flow**: Input processing through output generation
- 🔌 **API Integration**: External service dependencies and connections

## 🎯 Use Cases

### Financial Analysis
- **Market Sentiment**: Real-time crypto market sentiment analysis
- **News Verification**: Fact-checking and source credibility assessment
- **Trend Detection**: Cross-platform virality and echo pattern analysis

### Content Moderation
- **Quality Control**: AI-generated content detection and filtering
- **Policy Compliance**: Banned phrase detection with context awareness
- **Escalation Management**: Intelligent routing for human review

### Research & Analytics
- **Academic Research**: Comprehensive dataset for social media analysis
- **Business Intelligence**: Market trends and influencer impact assessment
- **Risk Assessment**: Market manipulation and misinformation detection

## 🔮 Future Roadmap

### Immediate Enhancements
- 🔄 **Async PRAW Integration**: Improved Reddit API performance
- 📈 **Enhanced Crypto Detection**: Support for more exchanges and assets
- 📊 **Performance Dashboard**: Real-time monitoring and analytics

### Advanced Features
- 🤖 **ML Model Integration**: Pattern recognition and anomaly detection
- 🌍 **Multi-language Support**: Global content analysis capabilities
- 📡 **Real-time Streaming**: Live tweet analysis and alerting

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd twitter-news-classifier

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API keys

# Run analysis
python3 main.py
```

### Testing
```bash
# Run test suite (when available)
python3 -m pytest tests/

# Lint code
flake8 domain/ infrastructure/

# Type checking
mypy domain/ infrastructure/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Achievements

- ✅ **100% Success Rate**: All 25 tweets processed without failures
- 🎯 **Quality Target Met**: 44% of tweets achieving scores > 6.0
- 🚀 **Real-time Processing**: Zero simulated data, all real-time APIs
- 🏗️ **Clean Architecture**: Domain-driven design with 17-agent orchestration
- 📊 **Comprehensive Output**: Complete analysis results with detailed reasoning

---

*Version: 2.0*  
*Last Updated: August 10, 2025*  
*System Status: Operational (100% success rate)*  
*Architecture: 17-Agent Input-Sovereign Classification*