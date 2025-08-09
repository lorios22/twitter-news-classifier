"""
🎼 ORCHESTRATION SERVICES
========================
Servicios de orquestación para coordinar múltiples agentes y consolidar resultados.

Módulos:
- EnhancedMultiAgentAnalyzer: Orquestador principal de agentes mejorados
- EnhancedScoreConsolidator: Consolidador de puntuaciones con nuevos agentes
"""

from .enhanced_multi_agent_analyzer import EnhancedMultiAgentAnalyzer, EnhancedAgentConfig
from .enhanced_score_consolidator import EnhancedScoreConsolidator

__all__ = [
    'EnhancedMultiAgentAnalyzer', 'EnhancedAgentConfig',
    'EnhancedScoreConsolidator'
]