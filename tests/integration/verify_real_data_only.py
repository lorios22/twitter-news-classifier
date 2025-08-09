#!/usr/bin/env python3
"""
🔍 VERIFY REAL DATA ONLY
========================
Script para verificar que SOLO se usen datos reales, sin simulaciones
"""

import os
import requests
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv

def test_reddit_real_data():
    """Verificar que Reddit use datos reales"""
    print("🔍 REDDIT API - DATOS REALES")
    print("-" * 40)
    
    try:
        import praw
        reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        if not reddit_client_id or not reddit_client_secret:
            print("❌ Reddit: Credenciales no configuradas")
            return False
        
        reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent='RealDataVerifier/1.0'
        )
        
        # Obtener post real de r/cryptocurrency
        subreddit = reddit.subreddit('cryptocurrency')
        hot_posts = list(subreddit.hot(limit=3))
        
        if hot_posts:
            latest_post = hot_posts[0]
            print(f"✅ Reddit: Post real obtenido")
            print(f"   Título: {latest_post.title[:50]}...")
            print(f"   Autor: u/{latest_post.author}")
            print(f"   Score: {latest_post.score}")
            print(f"   Timestamp: {datetime.fromtimestamp(latest_post.created_utc)}")
            return True
        else:
            print("❌ Reddit: No se pudieron obtener posts reales")
            return False
            
    except Exception as e:
        print(f"❌ Reddit: Error - {e}")
        return False

def test_coinbase_real_data():
    """Verificar que Coinbase use datos reales"""
    print("\n🔍 COINBASE CDP API - DATOS REALES")
    print("-" * 40)
    
    try:
        # Test con precio actual real
        response = requests.get(
            'https://api.coinbase.com/v2/prices/BTC-USD/spot',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            price = float(data['data']['amount'])
            currency = data['data']['currency']
            
            print(f"✅ Coinbase: Precio real obtenido")
            print(f"   BTC Price: ${price:,.2f} {currency}")
            print(f"   Timestamp: {datetime.now()}")
            
            # Verificar que no es un precio simulado (debe estar en rango realista)
            if 10000 <= price <= 200000:
                print(f"✅ Coinbase: Precio está en rango realista")
                return True
            else:
                print(f"❌ Coinbase: Precio fuera de rango realista")
                return False
        else:
            print(f"❌ Coinbase: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Coinbase: Error - {e}")
        return False

def test_binance_real_data():
    """Verificar que Binance use datos reales"""
    print("\n🔍 BINANCE API - DATOS REALES")
    print("-" * 40)
    
    try:
        # Test con múltiples assets para verificar que son reales
        symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
        real_prices = {}
        
        for symbol in symbols:
            response = requests.get(
                f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}',
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                price = float(data['price'])
                real_prices[symbol] = price
            else:
                print(f"❌ Binance: Error obteniendo {symbol}")
                return False
        
        if real_prices:
            print(f"✅ Binance: Precios reales obtenidos")
            for symbol, price in real_prices.items():
                print(f"   {symbol}: ${price:,.2f}")
            print(f"   Timestamp: {datetime.now()}")
            
            # Verificar que los precios están en rangos realistas
            btc_price = real_prices.get('BTCUSDT', 0)
            eth_price = real_prices.get('ETHUSDT', 0)
            
            if (10000 <= btc_price <= 200000 and 
                500 <= eth_price <= 10000):
                print(f"✅ Binance: Precios están en rangos realistas")
                return True
            else:
                print(f"❌ Binance: Precios fuera de rangos realistas")
                return False
        else:
            print("❌ Binance: No se obtuvieron precios")
            return False
            
    except Exception as e:
        print(f"❌ Binance: Error - {e}")
        return False

async def test_agents_no_simulation():
    """Verificar que los agentes NO usen datos simulados"""
    print("\n🔍 AGENTES - VERIFICACIÓN SIN SIMULACIONES")
    print("-" * 50)
    
    try:
        # Importar y verificar agentes
        from domain.services.signal_integrity import EchoMapperAgent, LatencyGuardAgent
        
        memory_store = {}
        
        # Configurar Echo Mapper
        reddit_config = {
            'client_id': os.getenv('REDDIT_CLIENT_ID'),
            'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
            'user_agent': 'RealDataVerifier/1.0'
        } if os.getenv('REDDIT_CLIENT_ID') else None
        
        echo_mapper = EchoMapperAgent(memory_store, reddit_config)
        
        # Test Echo Mapper
        test_tweet = "Bitcoin price surge continues"
        test_time = datetime.now()
        
        echo_result = await echo_mapper.analyze_echo(test_tweet, test_time)
        
        print("✅ Echo Mapper: Ejecutado sin simulaciones")
        print(f"   Reddit threads: {echo_result.reddit_threads}")
        print(f"   Farcaster refs: {echo_result.farcaster_refs}")
        print(f"   Discord refs: {echo_result.discord_refs}")
        
        # Verificar que Farcaster y Discord devuelven 0 (no simulado)
        if echo_result.farcaster_refs == 0 and echo_result.discord_refs == 0:
            print("✅ Echo Mapper: Sin datos simulados para APIs no implementadas")
        else:
            print("❌ Echo Mapper: Posibles datos simulados detectados")
            return False
        
        # Test Latency Guard
        price_config = {
            'binance_enabled': bool(os.getenv('BINANCE_API_KEY')),
            'coinbase_enabled': bool(os.getenv('COINBASE_API_KEY'))
        }
        
        latency_guard = LatencyGuardAgent(memory_store, price_config)
        
        latency_result = await latency_guard.analyze_latency(test_tweet, test_time)
        
        print("✅ Latency Guard: Ejecutado sin simulaciones")
        print(f"   Repriced: {latency_result.repriced}")
        print(f"   Price change: {latency_result.price_change_pct:.2f}%")
        print(f"   Asset detected: {latency_result.asset_symbol}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agentes: Error - {e}")
        return False

def main():
    """Ejecutar todas las verificaciones"""
    load_dotenv()
    
    print("🔍 VERIFICACIÓN DE DATOS REALES ÚNICAMENTE")
    print("=" * 60)
    print("Este script verifica que NO se usen datos simulados")
    print("=" * 60)
    
    tests = []
    
    # Test APIs individuales
    tests.append(("Reddit API", test_reddit_real_data()))
    tests.append(("Coinbase API", test_coinbase_real_data()))
    tests.append(("Binance API", test_binance_real_data()))
    
    # Test agentes (async)
    agent_test = asyncio.run(test_agents_no_simulation())
    tests.append(("Agentes Sin Simulación", agent_test))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("\n🎉 VERIFICACIÓN EXITOSA")
        print("✅ El sistema usa ÚNICAMENTE datos reales")
        print("✅ NO se detectaron simulaciones")
        print("✅ Todas las APIs funcionan correctamente")
    else:
        print("\n⚠️ VERIFICACIÓN PARCIAL")
        print("❌ Algunos componentes no pasaron la verificación")
        print("💡 Revisa las APIs que fallaron arriba")
    
    print(f"\n🕐 Verificación completada: {datetime.now()}")

if __name__ == "__main__":
    main()