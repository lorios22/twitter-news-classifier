#!/usr/bin/env python3
"""
🧪 TEST SCRIPT FOR OPTIONAL APIS
===============================
Test script to verify that optional APIs are working correctly.
"""

import os
import asyncio
from dotenv import load_dotenv

def test_reddit_api():
    """Test Reddit API connection"""
    try:
        import praw
        
        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        user_agent = os.getenv('REDDIT_USER_AGENT', 'TwitterNewsClassifier/1.0')
        
        if not client_id or not client_secret:
            print("⚠️ Reddit API: Credentials not configured")
            return False
        
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        # Test with a simple request
        subreddit = reddit.subreddit('cryptocurrency')
        posts = list(subreddit.hot(limit=1))
        
        print("✅ Reddit API: Connected successfully")
        print(f"   Test subreddit: r/cryptocurrency")
        print(f"   Sample post: {posts[0].title[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Reddit API: Failed - {e}")
        return False

def test_coinbase_api():
    """Test Coinbase CDP API connection"""
    try:
        import requests
        
        api_key = os.getenv('COINBASE_API_KEY')
        api_secret = os.getenv('COINBASE_API_SECRET') 
        
        if not api_key or not api_secret:
            print("⚠️ Coinbase API: Credentials not configured")
            return False
        
        # Test Coinbase CDP API (public endpoints)
        response = requests.get(
            'https://api.coinbase.com/v2/prices/BTC-USD/spot',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            price = float(data['data']['amount'])
            print("✅ Coinbase API: Connected successfully (CDP)")
            print(f"   BTC Price: ${price:,.2f}")
            return True
        else:
            print(f"❌ Coinbase API: HTTP {response.status_code}")
            if response.text:
                print(f"   Error: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ Coinbase API: Failed - {e}")
        return False

def test_binance_api():
    """Test Binance API connection"""
    try:
        import requests
        
        api_key = os.getenv('BINANCE_API_KEY')
        
        if not api_key:
            print("⚠️ Binance API: Credentials not configured")
            return False
        
        # Simple test - get BTC price (public endpoint)
        response = requests.get(
            'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Binance API: Connected successfully")
            print(f"   BTC Price: ${float(data['price']):.2f}")
            return True
        else:
            print(f"❌ Binance API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Binance API: Failed - {e}")
        return False

def test_enhanced_agents():
    """Test that enhanced agents can be imported and initialized"""
    try:
        # Test imports
        from domain.services.signal_integrity import (
            SarcasmSentinelAgent, EchoMapperAgent, LatencyGuardAgent,
            SlopFilterAgent, BannedPhraseSkepticAgent
        )
        
        print("✅ Enhanced Agents: All imports successful")
        
        # Test basic initialization
        memory_store = {}
        
        # Mock OpenAI client for testing
        class MockOpenAI:
            pass
        
        sarcasm_agent = SarcasmSentinelAgent(MockOpenAI(), memory_store)
        echo_agent = EchoMapperAgent(memory_store)
        latency_agent = LatencyGuardAgent(memory_store)
        slop_agent = SlopFilterAgent(memory_store)
        banned_agent = BannedPhraseSkepticAgent(memory_store)
        
        print("✅ Enhanced Agents: All agents initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Agents: Failed - {e}")
        return False

async def test_agent_functionality():
    """Test basic agent functionality"""
    try:
        from domain.services.signal_integrity import EchoMapperAgent, LatencyGuardAgent
        from datetime import datetime
        
        memory_store = {}
        
        # Test Echo Mapper
        reddit_config = None
        if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'):
            reddit_config = {
                'client_id': os.getenv('REDDIT_CLIENT_ID'),
                'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
                'user_agent': 'TwitterNewsClassifier/1.0'
            }
        
        echo_agent = EchoMapperAgent(memory_store, reddit_config)
        echo_result = await echo_agent.analyze_echo("Bitcoin price analysis", datetime.now())
        
        print("✅ Agent Functionality: Echo Mapper working")
        print(f"   Reddit threads found: {echo_result.reddit_threads}")
        print(f"   Echo velocity: {echo_result.echo_velocity:.2f}")
        
        # Test Latency Guard
        latency_agent = LatencyGuardAgent(memory_store)
        latency_result = await latency_agent.analyze_latency("Bitcoin price surge", datetime.now())
        
        print("✅ Agent Functionality: Latency Guard working")
        print(f"   Repriced: {latency_result.repriced}")
        print(f"   Price change: {latency_result.price_change_pct:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent Functionality: Failed - {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TESTING OPTIONAL APIS & ENHANCED AGENTS")
    print("=" * 50)
    
    load_dotenv()
    
    # Test APIs
    api_results = {
        'Reddit': test_reddit_api(),
        'Coinbase': test_coinbase_api(), 
        'Binance': test_binance_api()
    }
    
    # Test Enhanced Agents
    print("\n" + "=" * 50)
    print("🤖 TESTING ENHANCED AGENTS")
    print("=" * 50)
    
    agent_results = {
        'Enhanced Agents Import': test_enhanced_agents()
    }
    
    # Test Agent Functionality
    print("\n" + "=" * 50)
    print("⚡ TESTING AGENT FUNCTIONALITY")
    print("=" * 50)
    
    try:
        functionality_result = asyncio.run(test_agent_functionality())
        agent_results['Agent Functionality'] = functionality_result
    except Exception as e:
        print(f"❌ Agent Functionality Test: Failed - {e}")
        agent_results['Agent Functionality'] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RESULTS SUMMARY")
    print("=" * 50)
    
    working_apis = [name for name, status in api_results.items() if status]
    failed_apis = [name for name, status in api_results.items() if not status]
    
    working_agents = [name for name, status in agent_results.items() if status]
    failed_agents = [name for name, status in agent_results.items() if not status]
    
    print("🔌 APIs:")
    print(f"   ✅ Working: {', '.join(working_apis) if working_apis else 'None'}")
    print(f"   ❌ Failed: {', '.join(failed_apis) if failed_apis else 'None'}")
    
    print("\n🤖 Enhanced Agents:")
    print(f"   ✅ Working: {', '.join(working_agents) if working_agents else 'None'}")
    print(f"   ❌ Failed: {', '.join(failed_agents) if failed_agents else 'None'}")
    
    total_working = len(working_apis) + len(working_agents)
    total_tests = len(api_results) + len(agent_results)
    
    if total_working >= 4:  # At least Reddit/Binance + agents working
        print(f"\n🎉 {total_working}/{total_tests} components working!")
        print("Your enhanced system is ready to run with real data.")
    elif total_working >= 2:
        print(f"\n⚠️ {total_working}/{total_tests} components working.")
        print("System will work with limited functionality.")
    else:
        print(f"\n❌ Only {total_working}/{total_tests} components working.")
        print("Check your configuration and try again.")
    
    print("\n💡 To run the enhanced system:")
    print("   python3 demo_real_data_only.py")
    print("   python3 main_enhanced.py")

if __name__ == "__main__":
    main()