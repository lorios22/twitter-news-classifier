#!/usr/bin/env python3
"""
🐦 EXTRACT REAL TWEETS SCRIPT
============================
Script to extract more real tweets from Twitter API and run full analysis.
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from infrastructure.adapters.twitter_api_adapter import TwitterApiAdapter, TwitterApiConfig
from domain.services.core_analysis.tweet_extraction_service import TweetExtractionService, ExtractionConfig
from infrastructure.repositories.file_repository import FileRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of crypto/finance Twitter accounts to extract from
CRYPTO_ACCOUNTS = [
    "whale_alert",
    "CoinMarketCap", 
    "cz_binance",
    "VitalikButerin",
    "elonmusk",
    "saylor",
    "APompliano",
    "RaoulGMI",
    "pentosh1",
    "WuBlockchain",
    "DocumentingBTC",
    "BitcoinMagazine",
    "aantonop",
    "naval",
    "balajis",
    "JustinSunTRX",
    "CRO_Community",
    "ethereum",
    "solana",
    "Polkadot",
    "avalancheavax",
    "Polygon",
    "Uniswap",
    "aave",
    "MakerDAO",
    "Chainlink",
    "CurveFinance",
    "SushiSwap",
    "1inch",
    "TokenSets",
    "Yearn_Finance",
    "synthetix_io",
    "graphprotocol",
    "ENS_Ethereum",
    "compoundfinance",
    "dydxprotocol",
    "LooksRare",
    "OpenSea",
    "SuperRare",
    "AsyncArt",
    "XCOPY",
    "beeple",
    "punk6529",
    "pranksy",
    "WhaleShark_Pro",
    "gmoney_eth",
    "deeze",
    "garyvee",
    "fallout_nft"
]

async def main():
    """Extract more real tweets and save them for analysis"""
    print("🐦 EXTRACTING REAL TWEETS FROM TWITTER API")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if Twitter API credentials are available
    twitter_credentials = {
        'TWITTER_API_KEY': os.getenv('TWITTER_API_KEY'),
        'TWITTER_API_SECRET': os.getenv('TWITTER_API_SECRET'),
        'TWITTER_ACCESS_TOKEN': os.getenv('TWITTER_ACCESS_TOKEN'),
        'TWITTER_ACCESS_TOKEN_SECRET': os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        'TWITTER_BEARER_TOKEN': os.getenv('TWITTER_BEARER_TOKEN')
    }
    
    missing_credentials = [key for key, value in twitter_credentials.items() if not value]
    
    if missing_credentials:
        print("❌ TWITTER API CREDENTIALS MISSING")
        print("Please configure the following environment variables:")
        for cred in missing_credentials:
            print(f"   - {cred}")
        print("\nTo get Twitter API credentials:")
        print("1. Go to https://developer.twitter.com/")
        print("2. Create a developer account")
        print("3. Create a new app")
        print("4. Generate API keys and tokens")
        print("5. Add them to your .env file")
        return
    
    try:
        # Initialize Twitter API adapter
        print("🔧 Initializing Twitter API connection...")
        twitter_adapter = TwitterApiAdapter.from_env()
        
        # Test connection
        print("🧪 Testing Twitter API connection...")
        if not twitter_adapter.test_connection():
            print("❌ Twitter API connection failed")
            return
        
        print("✅ Twitter API connection successful")
        
        # Initialize extraction service
        file_repository = FileRepository()
        extraction_service = TweetExtractionService(
            twitter_adapter=twitter_adapter,
            file_repository=file_repository
        )
        
        # Configure extraction
        config = ExtractionConfig(
            max_tweets=50,  # Extract more tweets
            hours_back=72,  # Look back 3 days
            accounts_list=CRYPTO_ACCOUNTS[:20],  # Use first 20 accounts
            enable_thread_extraction=True,
            enable_media_analysis=True,
            enable_url_extraction=True,
            output_directory="data/real_extraction",
            batch_size=5
        )
        
        print(f"📊 Extraction Configuration:")
        print(f"   🎯 Target tweets: {config.max_tweets}")
        print(f"   ⏰ Time window: {config.hours_back} hours")
        print(f"   👥 Accounts: {len(config.accounts_list)}")
        print(f"   📁 Output: {config.output_directory}")
        
        # Execute extraction
        print("\n🚀 Starting tweet extraction...")
        extraction_result = await extraction_service.extract_comprehensive_data(config)
        
        if extraction_result.status == 'success':
            print(f"✅ EXTRACTION SUCCESSFUL!")
            print(f"   📊 Tweets extracted: {extraction_result.total_tweets_extracted}")
            print(f"   👥 Accounts processed: {extraction_result.successful_accounts}")
            print(f"   📁 Output saved to: {extraction_result.output_file}")
            
            # Copy to sample_extraction for main.py to use
            if extraction_result.output_file and Path(extraction_result.output_file).exists():
                sample_dir = Path("data/sample_extraction")
                sample_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy the extracted data
                with open(extraction_result.output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                with open(sample_dir / "extracted_tweets.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"📁 Copied to: data/sample_extraction/extracted_tweets.json")
                print("\n🎯 Ready for analysis! Run: python3 main.py")
            
        else:
            print(f"❌ EXTRACTION FAILED: {extraction_result.status}")
            if extraction_result.error_details:
                for error in extraction_result.error_details:
                    print(f"   - {error}")
                    
    except Exception as e:
        logger.error(f"❌ Error during extraction: {str(e)}")
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())