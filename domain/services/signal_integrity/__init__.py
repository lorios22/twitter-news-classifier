"""
🛰️ SIGNAL INTEGRITY AGENTS
==========================
Agentes especializados en la integridad y filtrado de señales antes del análisis final.

Módulos:
- SarcasmSentinelAgent: Detección de sarcasmo e ironía
- EchoMapperAgent: Análisis de viralidad cross-platform  
- LatencyGuardAgent: Detección de noticias obsoletas/front-run
- SlopFilterAgent: Filtrado de contenido de baja calidad
- BannedPhraseSkepticAgent: Aplicación de penalizaciones tonales
"""

from .sarcasm_sentinel_agent import SarcasmSentinelAgent, SarcasmResult
from .echo_mapper_agent import EchoMapperAgent, EchoResult
from .latency_guard_agent import LatencyGuardAgent, LatencyResult
from .slop_filter_agent import SlopFilterAgent, SlopResult
from .banned_phrase_skeptic_agent import BannedPhraseSkepticAgent, BannedPhraseResult

__all__ = [
    'SarcasmSentinelAgent', 'SarcasmResult',
    'EchoMapperAgent', 'EchoResult', 
    'LatencyGuardAgent', 'LatencyResult',
    'SlopFilterAgent', 'SlopResult',
    'BannedPhraseSkepticAgent', 'BannedPhraseResult'
]