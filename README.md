# 🐦 Twitter News Classifier v4.0

## 🎯 What Is This?

The **Twitter News Classifier** is an advanced AI-powered system designed to automatically analyze, classify, and score cryptocurrency and blockchain news content from trusted Twitter accounts. Using 12 specialized AI agents working in collaboration, it provides comprehensive insights into the quality, accuracy, and relevance of social media news content.

### 🚀 Key Features

- **🤖 12 Specialized AI Agents**: Each agent focuses on a specific aspect of content analysis (fact-checking, relevance, depth, etc.)
- **📊 Weighted Scoring System**: Prioritizes accuracy (18%) and relevance (15%) for reliable news classification
- **🐦 Real Twitter API Integration**: Extracts live data from 48 trusted crypto/blockchain accounts
- **🧵 Advanced Thread Analysis**: Captures complete conversation context and related tweets
- **🖼️ Rich Media Analysis**: Analyzes images, external links, and multimedia content
- **📈 Professional Reporting**: Generates both technical (JSON) and human-readable (Markdown) reports
- **🏗️ Domain-Driven Design**: Clean, maintainable architecture with proper separation of concerns

## 🎯 Who Is This For?

- **📊 Crypto Investors**: Stay informed about market-moving news with quality scoring
- **🔬 Researchers**: Analyze social media trends and sentiment in crypto/blockchain space
- **📰 Content Creators**: Find high-quality, verified information for content creation
- **💼 Financial Analysts**: Get comprehensive data about social media news impact
- **🏛️ Institutions**: Monitor trusted sources for investment and research decisions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Twitter API v2 access (Essential tier or higher)
- OpenAI API access with GPT-4 capabilities
- 8GB+ RAM for optimal performance

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/twitter-news-classifier.git
cd twitter-news-classifier
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-api-key

# Twitter API Configuration
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
```

4. **Run the analysis**:
```bash
python main.py
```

## 🏗️ System Architecture

### Domain-Driven Design Structure

The system follows clean DDD principles with four distinct layers:

```
📁 Project Structure:
├── main.py                          # 🚀 Application entry point
├── domain/                         # 🧠 Core business logic
│   ├── entities/                  # 📊 Business entities
│   │   ├── tweet.py              # 🐦 Tweet domain model
│   │   └── analysis_result.py    # 📋 Analysis result model
│   └── services/                 # ⚙️ Domain services
│       └── multi_agent_analyzer.py # 🤖 Multi-agent orchestration
├── application/                   # 🎯 Application layer
│   └── use_cases/               # 📋 Business use cases
│       └── analyze_tweets_use_case.py # 🔄 Main workflow
├── infrastructure/              # 🔧 Infrastructure layer
│   ├── adapters/               # 🔌 External service adapters
│   │   └── twitter_api_adapter.py # 🐦 Twitter API integration
│   ├── repositories/           # 💾 Data persistence
│   │   └── file_repository.py  # 📁 File-based storage
│   └── prompts/               # 📝 AI agent prompts
│       └── agent_prompts.py   # 🤖 Centralized prompt repository
└── results/                   # 📊 Analysis output storage
    └── runs/                 # 📅 Individual analysis runs
```

## 🤖 The 12 AI Agents

### Scoring Weight Distribution

Our multi-agent system uses a carefully balanced scoring approach:

| Agent | Weight | Purpose |
|-------|--------|---------|
| **Fact Checker** | 18% | Accuracy verification and misinformation detection |
| **Context Evaluator** | 15% | Content richness and completeness assessment |
| **Relevance Analyzer** | 15% | Real-world importance and impact evaluation |
| **Depth Analyzer** | 12% | Content complexity and analytical depth |
| **Summary Agent** | 10% | Title generation and content summarization |
| **Structure Analyzer** | 8% | Organization and presentation quality |
| **Reflective Agent** | 7% | Critical thinking and bias detection |
| **Metadata Ranking** | 6% | Source credibility and authority assessment |
| **Input Preprocessor** | 5% | Data quality and normalization |
| **Consensus Agent** | 4% | Agreement and controversy evaluation |

### Agent Specializations

**🔍 Core Analysis Agents**:
- **Summary Agent**: Creates compelling titles and comprehensive abstracts
- **Fact Checker**: Verifies claims and identifies potential misinformation
- **Context Evaluator**: Assesses information completeness and context richness
- **Relevance Analyzer**: Evaluates real-world importance and practical impact

**📊 Quality Assessment Agents**:
- **Depth Analyzer**: Measures content complexity and analytical thoroughness
- **Structure Analyzer**: Evaluates organization and presentation clarity
- **Reflective Agent**: Provides critical thinking and alternative perspectives
- **Consensus Agent**: Identifies controversial topics and agreement levels

**🔧 Technical Agents**:
- **Input Preprocessor**: Cleans and normalizes data for better analysis
- **Metadata Ranking**: Assesses source credibility and author authority
- **Score Consolidator**: Combines individual scores using weighted formula
- **Validator**: Performs final quality assurance and error checking

## 📊 Analysis Process

### Step-by-Step Workflow

1. **🐦 Data Extraction (5-10 minutes)**
   - Connects to Twitter API v2
   - Monitors 48 trusted crypto/blockchain accounts
   - Extracts tweets with rich metadata, media, and thread context
   - Smart rate limiting to respect API constraints

2. **🔧 Content Preparation (1-2 minutes)**
   - Normalizes and cleans extracted data
   - Builds comprehensive context packages
   - Prepares structured input for AI agents

3. **🤖 Multi-Agent Analysis (15-20 minutes)**
   - Sequential processing through 12 specialized agents
   - Each agent provides detailed scoring and reasoning
   - Comprehensive evaluation from multiple perspectives

4. **📊 Score Consolidation (2-3 minutes)**
   - Weighted combination of individual agent scores
   - Final classification and quality assessment
   - Confidence interval calculation

5. **📋 Report Generation (1-2 minutes)**
   - Individual tweet analysis reports (JSON + Markdown)
   - Executive summary with key findings
   - Organized storage in timestamped directories

### Trusted Account Monitoring

The system monitors **48 carefully curated accounts** representing:

- **Protocol Foundations**: @ethereum, @solana, @chainlink, @cardano
- **DeFi Platforms**: @Uniswap, @aave, @SushiSwap, @PancakeSwap  
- **Infrastructure**: @Polygon, @arbitrum, @Optimism, @NEARProtocol
- **Analytics**: @dune, @defipulse, @coinmetrics
- **And 36 additional trusted crypto/blockchain sources**

## ⚙️ Configuration

### Analysis Parameters

Adjust parameters in the `AnalysisConfig` within `main.py`:
```python
config = AnalysisConfig(
    max_tweets=30,              # Number of tweets to analyze
    hours_back=24,              # Time range (hours)
    enable_thread_analysis=True, # Thread detection
    enable_media_analysis=True,  # Media content analysis
    save_individual_results=True # Individual reports
)
```

### API Configuration

**Twitter API v2 Requirements**:
- Essential tier or higher
- Full OAuth 2.0 credentials
- Rate limits: 300 user lookups, 75 timeline requests per 15 minutes

**OpenAI API Requirements**:
- GPT-4 model access (recommended) or GPT-3.5-turbo (fallback)
- Estimated usage: ~720,000 tokens per full analysis run
- Cost estimation: ~$43 per run (GPT-4) or ~$0.80 per run (GPT-3.5-turbo)

### Logging & Monitoring

Comprehensive logging is saved to `logs/` directory with detailed execution information including:
- Real-time processing status
- API rate limiting information
- Individual agent performance metrics
- Error handling and recovery actions

## 🛠️ Development & Customization

### Adding New Agents
1. Create agent prompt in `infrastructure/prompts/agent_prompts.py`
2. Add agent to the sequence in `domain/services/multi_agent_analyzer.py`
3. Configure weight in the scoring system

### Extending Analysis
- **New Data Structures**: Modify entities in `domain/entities/`
- **New Workflows**: Add use cases in `application/use_cases/`
- **External Services**: Create adapters in `infrastructure/adapters/`

### Custom Account Lists
Edit the `TRUSTED_ACCOUNTS` list in `main.py` to monitor different Twitter accounts or expand to new crypto/blockchain verticals.

## 📈 Performance & Monitoring

### System Performance
- **Processing Speed**: ~30 seconds per tweet (12 agents)
- **Total Analysis Time**: 20-35 minutes for 30 tweets
- **Success Rate**: >95% under normal conditions
- **Memory Usage**: ~500MB peak during processing
- **Storage**: ~50KB per analyzed tweet

### Cost Management
- **Development**: Use GPT-3.5-turbo for testing (~$0.80 per run)
- **Production**: GPT-4 for maximum accuracy (~$43 per run)
- **Optimization**: Adjust `max_tweets` parameter for budget control

## 🔒 Security & Privacy

### Data Protection
- **API Key Management**: Secure environment variable configuration
- **Rate Limiting**: Built-in Twitter API rate limit handling and respect
- **Error Isolation**: Individual agent failures don't compromise entire analysis
- **No Persistent Data**: Sensitive information is not stored long-term

### Privacy Considerations
- Only analyzes publicly available Twitter content
- No personal data storage beyond public tweet metadata
- Respects Twitter's Terms of Service and API usage policies

## 📋 Troubleshooting

### Common Issues

1. **Twitter API Errors**
   - ✅ Verify API credentials in `.env` file
   - ✅ Check API plan limits (Essential or higher required)
   - ✅ Ensure monitored accounts have recent activity

2. **OpenAI API Errors**
   - ✅ Verify API key validity and format
   - ✅ Check usage limits and billing status
   - ✅ Monitor rate limits during peak usage

3. **Performance Issues**
   - ✅ Install all requirements: `pip install -r requirements.txt`
   - ✅ Check Python version (3.8+ required)
   - ✅ Ensure adequate RAM (8GB+ recommended)

4. **Analysis Quality**
   - ✅ Use GPT-4 for best results
   - ✅ Verify account list contains active accounts
   - ✅ Check time range settings (24 hours default)

### Debug Information
- Check `logs/` directory for detailed execution logs
- Review individual agent outputs in results for debugging
- Monitor rate limiting messages for API optimization

## 🌟 Advanced Features

### Thread Analysis
- **Complete Context**: Extracts full conversation threads
- **Relationship Mapping**: Identifies reply chains and mentions
- **Context Preservation**: Maintains chronological order and relationships

### Media Content Analysis
- **Image Processing**: OCR and visual content analysis
- **Link Analysis**: External URL content extraction and evaluation
- **Rich Media Support**: Videos, documents, and multimedia content

### Quality Assurance
- **Multi-layer Validation**: Score consolidator and validator agents
- **Consistency Checking**: Cross-agent validation and error detection
- **Confidence Scoring**: Uncertainty quantification and reliability metrics

## 🤝 Contributing

We welcome contributions to improve the Twitter News Classifier:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-agent`
3. **Make your changes** with proper documentation
4. **Add tests** for new functionality
5. **Submit a pull request** with detailed description

### Development Guidelines
- Follow DDD principles and existing architecture
- Add comprehensive docstrings and comments
- Include unit tests for new components
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

### Upcoming Features
- **Real-time Stream Processing**: Live tweet analysis as they arrive
- **Sentiment Analysis Integration**: Advanced emotional sentiment scoring
- **Multi-language Support**: Analysis of non-English crypto content
- **API Service Mode**: REST API for integration with other systems
- **Custom Agent Framework**: User-defined analysis agents
- **Historical Trend Analysis**: Long-term pattern recognition and insights

---

**Twitter News Classifier v4.0** - Powered by AI collaboration for deep crypto/blockchain news insights.