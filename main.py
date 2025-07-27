#!/usr/bin/env python3
"""
🐦 TWITTER NEWS CLASSIFIER
=========================
Main entry point for comprehensive Twitter news content analysis.

This application uses a multi-agent AI system to analyze Twitter news content
from trusted crypto/blockchain accounts, providing comprehensive insights through 
12 specialized AI agents working in collaboration.

Domain-Driven Design Architecture:
- Domain: Core business entities and logic
- Application: Use cases and orchestration
- Infrastructure: External services and adapters
- Presentation: CLI interface

Features:
- Real Twitter API integration for crypto/blockchain news analysis
- 12 specialized AI agents for comprehensive content classification
- Thread detection and extraction for complete context
- Media content analysis (images, links) for rich information
- Weighted scoring system with importance prioritization
- Comprehensive reporting (JSON + Markdown) for actionable insights
- Clean DDD architecture with proper separation of concerns

Usage:
    python main.py

Environment Variables Required:
    - OPENAI_API_KEY: OpenAI API key for AI agents
    - TWITTER_BEARER_TOKEN: Twitter API Bearer Token
    - TWITTER_API_KEY: Twitter API Consumer Key  
    - TWITTER_API_SECRET: Twitter API Consumer Secret
    - TWITTER_ACCESS_TOKEN: Twitter API Access Token
    - TWITTER_ACCESS_TOKEN_SECRET: Twitter API Access Token Secret

Author: Twitter News Classifier System
Version: 4.0
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from application.use_cases.analyze_tweets_use_case import (
    AnalyzeTweetsUseCase, 
    AnalysisConfig
)


# Trusted crypto/blockchain accounts for analysis
TRUSTED_ACCOUNTS = [
    "BetMode_Barry", "PendleIntern", "1inchDAO", "PolkadotInsider", 
    "ASI_Alliance", "insider_sonic", "kaspaunchained", "ton_blockchain",
    "dydxfoundation", "0xPolygonEco", "pendle_fi", "GMX_IO", "algodevs",
    "arbitrum", "katana", "LidoFinance", "PancakeSwap", "SushiSwap",
    "Api3DAO", "0xPolygonFdn", "PolkadotDevs", "1inch", "fraxfinance",
    "AlgoFoundation", "avax", "Optimism", "veloprotocol", "NEARProtocol",
    "cosmoshub", "BandProtocol", "Uniswap", "SonicLabs", "solana",
    "Algorand", "0xPolygon", "Fetch_ai", "dYdX", "rendernetwork",
    "Rocket_Pool", "aave", "Cardano", "quant_network", "Cardano_CF",
    "StellarOrg", "ethereum", "Polkadot", "chainlink", "GamingOnAvax",
    "Ripple", "cosmos"
]


def setup_logging() -> logging.Logger:
    """Configure comprehensive logging system"""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File handler
    log_file = logs_dir / f"social_media_analyzer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler  
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s - %(message)s'
    ))
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logging.getLogger(__name__)


def validate_environment() -> bool:
    """Validate required environment variables"""
    
    required_vars = [
        'OPENAI_API_KEY',
        'TWITTER_BEARER_TOKEN', 
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📖 Please check the README.md for setup instructions.")
        return False
    
    return True


def print_banner():
    """Print application banner"""
    
    banner = """
🐦 TWITTER NEWS CLASSIFIER v4.0
===============================

🤖 12 Specialized AI Agents Working in Collaboration
📊 Comprehensive News Content Analysis & Classification
🐦 Real Twitter API Integration for Crypto/Blockchain News
🧵 Advanced Thread Detection & Context Extraction
🖼️ Deep Media Content Analysis for Rich Information
📈 Weighted Scoring with Accuracy & Relevance Prioritization
📋 Professional JSON & Markdown Reports for Actionable Insights
🏗️ Clean Domain-Driven Design Architecture

Starting comprehensive analysis of crypto/blockchain Twitter news content...
"""
    
    print(banner)


async def main():
    """Main application entry point"""
    
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    logger = setup_logging()
    
    # Print banner
    print_banner()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    logger.info("🐦 Starting Twitter News Classifier")
    logger.info(f"📊 Target accounts: {len(TRUSTED_ACCOUNTS)} crypto/blockchain accounts")
    
    try:
        # Create use case instance
        logger.info("🔧 Initializing multi-agent analysis system...")
        use_case = AnalyzeTweetsUseCase.create_from_env()
        
        # Configure analysis parameters
        config = AnalysisConfig(
            max_tweets=30,              # Analyze 30 tweets
            hours_back=24,              # From last 24 hours
            enable_thread_analysis=True,  # Enable thread detection
            enable_media_analysis=True,   # Enable media analysis
            output_format="json",        # JSON + Markdown output
            save_individual_results=True, # Save individual analyses
            generate_summary=True        # Generate summary report
        )
        
        logger.info(f"📋 Analysis Configuration:")
        logger.info(f"   • Max Tweets: {config.max_tweets}")
        logger.info(f"   • Time Range: {config.hours_back} hours")
        logger.info(f"   • Thread Analysis: {config.enable_thread_analysis}")
        logger.info(f"   • Media Analysis: {config.enable_media_analysis}")
        
        # Execute comprehensive analysis
        logger.info("🎯 Starting comprehensive multi-agent analysis...")
        
        result = await use_case.execute(
            account_usernames=TRUSTED_ACCOUNTS,
            config=config
        )
        
        # Display results
        print("\n" + "="*60)
        print("📊 ANALYSIS COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"🆔 Run ID: {result['run_id']}")
        print(f"⏱️  Execution Time: {result['execution_time']:.2f} seconds")
        print(f"🐦 Tweets Processed: {result['tweets_processed']}")
        print(f"✅ Successful Analyses: {result['successful_analyses']}")
        print(f"📈 Success Rate: {(result['successful_analyses']/result['tweets_processed']*100):.1f}%" 
              if result['tweets_processed'] > 0 else "N/A")
        print(f"📁 Results saved in: results/runs/{result['run_id']}")
        print("="*60)
        
        # Detailed results breakdown
        if result['tweets_processed'] > 0:
            print("\n📋 DETAILED BREAKDOWN:")
            print(f"   • Individual JSON reports: {result['successful_analyses']} files")
            print(f"   • Individual Markdown reports: {result['successful_analyses']} files") 
            print(f"   • Comprehensive summary report: 1 file")
            print(f"   • 12-agent analysis per tweet")
            print(f"   • Thread detection & extraction")
            print(f"   • Media content analysis")
            print(f"   • Weighted scoring consolidation")
        
        logger.info(f"🎉 Analysis workflow completed successfully: {result['run_id']}")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Analysis interrupted by user")
        print("\n⏹️ Analysis interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        print(f"\n❌ Analysis failed: {str(e)}")
        print("📖 Check the logs for detailed error information.")
        sys.exit(1)


if __name__ == "__main__":
    """
    Application entry point
    
    Runs the complete social media analysis workflow using asyncio
    for optimal performance with concurrent API calls and processing.
    """
    try:
        # Run main async function
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Application terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        sys.exit(1) 