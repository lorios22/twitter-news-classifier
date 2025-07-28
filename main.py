#!/usr/bin/env python3
"""
🐦 TWITTER NEWS CLASSIFIER - SEPARATED WORKFLOW
===============================================
Main entry point for the separated two-phase Twitter analysis workflow.

This implementation provides:
- Phase 1: Comprehensive tweet extraction with metadata
- Phase 2: Multi-agent analysis of extracted data
- Robust error handling between phases
- Data preservation and recovery capabilities
- Independent processing with clean separation

Usage:
    python3 main_separated_workflow.py

Features:
- Two-phase processing for maximum reliability
- API failure recovery without data loss
- Comprehensive error handling and reporting
- Clean workflow management and orchestration
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv

from application.orchestrators.twitter_analysis_orchestrator import (
    TwitterAnalysisOrchestrator, 
    WorkflowConfig
)


# Updated trusted cryptocurrency and blockchain Twitter accounts list
TRUSTED_CRYPTO_ACCOUNTS = [
    "BetMode_Barry", "PendleIntern", "1inchDAO", "PolkadotInsider", "ASI_Alliance",
    "insider_sonic", "kaspaunchained", "ton_blockchain", "dydxfoundation", "0xPolygonEco",
    "pendle_fi", "GMX_IO", "algodevs", "arbitrum", "katana",
    "LidoFinance", "PancakeSwap", "SushiSwap", "Api3DAO", "0xPolygonFdn",
    "PolkadotDevs", "1inch", "fraxfinance", "AlgoFoundation", "avax",
    "Optimism", "veloprotocol", "NEARProtocol", "cosmoshub", "BandProtocol",
    "Uniswap", "SonicLabs", "solana", "Algorand", "0xPolygon",
    "Fetch_ai", "dYdX", "rendernetwork", "Rocket_Pool", "aave",
    "Cardano", "quant_network", "Cardano_CF", "StellarOrg", "ethereum",
    "Polkadot", "chainlink", "GamingOnAvax", "Ripple", "cosmos"
]


def setup_logging() -> logging.Logger:
    """Setup comprehensive logging configuration"""
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging
    log_filename = f"logs/twitter_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"📋 Logging configured - Log file: {log_filename}")
    
    return logger


def verify_environment_variables() -> bool:
    """Verify all required environment variables are set"""
    
    required_vars = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET', 
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET',
        'TWITTER_BEARER_TOKEN',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ ERROR: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please check your .env file and ensure all required variables are set.")
        print("   Refer to env_template.txt for the required format.")
        return False
    
    print("✅ All required environment variables found")
    return True


def print_application_banner():
    """Print application startup banner"""
    
    banner = """
🐦 TWITTER NEWS CLASSIFIER - SEPARATED WORKFLOW v4.0
====================================================

🎯 Two-Phase Processing Architecture:
   📡 Phase 1: Comprehensive Tweet Extraction
   🤖 Phase 2: Multi-Agent Analysis Pipeline

🔧 Enhanced Features:
   ✅ Independent phase processing
   ✅ Robust error handling and recovery
   ✅ Data preservation between phases
   ✅ API failure tolerance
   ✅ Comprehensive workflow management

🎨 Architecture:
   🏗️ Domain-Driven Design (DDD)
   📊 12 Specialized AI Agents
   🔄 Asynchronous Processing
   📈 Weighted Scoring System

Starting comprehensive analysis of crypto/blockchain Twitter content...
"""
    
    print(banner)


async def main():
    """Main execution function"""
    
    # Setup logging
    logger = setup_logging()
    
    try:
        # Print application banner
        print_application_banner()
        
        # Load environment variables
        load_dotenv()
        
        # Verify environment setup
        if not verify_environment_variables():
            sys.exit(1)
        
        logger.info("🚀 Starting Twitter News Classifier - Separated Workflow")
        logger.info(f"📊 Target accounts: {len(TRUSTED_CRYPTO_ACCOUNTS)} crypto/blockchain accounts")
        
        # Initialize orchestrator with API credentials
        orchestrator = TwitterAnalysisOrchestrator(
            twitter_api_key=os.getenv('TWITTER_API_KEY'),
            twitter_api_secret=os.getenv('TWITTER_API_SECRET'),
            twitter_access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            twitter_access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            twitter_bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Configure workflow
        workflow_config = WorkflowConfig(
            max_tweets=30,
            hours_back=24,
            trusted_accounts=TRUSTED_CRYPTO_ACCOUNTS,
            max_retries=3,
            retry_delay=30,
            batch_size=5,
            continue_on_api_failure=True,
            output_base_directory="data/workflow_runs",
            cleanup_old_runs=True,
            max_old_runs_to_keep=5,
            enable_extraction_recovery=True,
            enable_analysis_recovery=True,
            save_intermediate_results=True
        )
        
        logger.info("🎯 Workflow Configuration:")
        logger.info(f"   📊 Max tweets: {workflow_config.max_tweets}")
        logger.info(f"   ⏰ Time window: {workflow_config.hours_back} hours")
        logger.info(f"   👥 Accounts: {len(workflow_config.trusted_accounts)}")
        logger.info(f"   🔄 Max retries: {workflow_config.max_retries}")
        logger.info(f"   ⚡ Batch size: {workflow_config.batch_size}")
        logger.info(f"   🛡️ Error recovery: {workflow_config.continue_on_api_failure}")
        
        # Execute complete workflow
        logger.info("🚀 Executing complete two-phase workflow...")
        
        result = await orchestrator.execute_complete_workflow(workflow_config)
        
        # Print final results
        print("\n" + "=" * 60)
        print("📊 WORKFLOW EXECUTION COMPLETED")
        print("=" * 60)
        print(f"🆔 Workflow ID: {result.workflow_id}")
        print(f"⏱️  Total Processing Time: {result.total_processing_time:.2f} seconds")
        print(f"📈 Overall Status: {result.overall_status.upper()}")
        print(f"🏁 Phases Completed: {result.phase_completed}")
        print(f"💾 Data Preserved: {'YES' if result.data_preserved else 'NO'}")
        
        if result.extraction_result:
            print(f"📡 Tweets Extracted: {result.extraction_result.total_tweets_extracted}")
            if result.extraction_result.tweets_file_path:
                print(f"📂 Extraction Data: {result.extraction_result.tweets_file_path}")
        
        if result.analysis_result:
            print(f"🤖 Successful Analyses: {result.analysis_result.successful_analyses}")
            print(f"❌ Failed Analyses: {result.analysis_result.failed_analyses}")
            if result.analysis_result.results_file_path:
                print(f"📂 Analysis Results: {result.analysis_result.results_file_path}")
        
        if result.error_summary:
            print(f"⚠️ Total Errors: {len(result.error_summary)}")
        
        print("=" * 60)
        
        # Print recommendations
        if result.recommendations:
            print("💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"   {rec}")
            print("=" * 60)
        
        # Print workflow statistics
        stats = orchestrator.get_workflow_stats()
        print("📈 WORKFLOW STATISTICS:")
        print(f"   🔄 Total workflows executed: {stats['workflows_executed']}")
        print(f"   ✅ Successful extractions: {stats['successful_extractions']}")
        print(f"   🤖 Successful analyses: {stats['successful_analyses']}")
        print(f"   🐦 Total tweets processed: {stats['total_tweets_processed']}")
        print(f"   ❌ Total errors: {stats['total_errors']}")
        print("=" * 60)
        
        # Log success
        if result.overall_status == 'success':
            logger.info("🎉 Complete workflow executed successfully!")
        elif result.overall_status == 'analysis_failed':
            logger.warning("⚠️ Extraction successful but analysis failed - data preserved for retry")
        else:
            logger.error("❌ Workflow failed - check logs for details")
        
        return 0 if result.overall_status in ['success', 'analysis_failed'] else 1
        
    except KeyboardInterrupt:
        logger.info("⏹️ Workflow interrupted by user")
        print("\n⏹️ Workflow interrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}", exc_info=True)
        print(f"\n💥 Fatal error: {str(e)}")
        print("Check the log file for detailed error information.")
        return 1


if __name__ == "__main__":
    print("🐦 Twitter News Classifier - Separated Workflow")
    print("=" * 50)
    
    try:
        # Run the async main function
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n⏹️ Application interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Application failed to start: {str(e)}")
        sys.exit(1) 