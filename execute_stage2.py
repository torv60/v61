#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar a Segunda Etapa - Síntese com IA
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def execute_stage2():
    """Executa a segunda etapa - Síntese com IA"""
    
    try:
        # Carrega variáveis de ambiente
        from services.environment_loader import environment_loader
        
        # Importa o motor de síntese
        from services.enhanced_synthesis_engine import enhanced_synthesis_engine
        
        # Encontra a sessão mais recente
        analyses_dir = Path("analyses_data")
        session_dirs = [d for d in analyses_dir.iterdir() if d.is_dir() and d.name.startswith("session_")]
        
        if not session_dirs:
            logger.error("❌ Nenhuma sessão encontrada! Execute a primeira etapa primeiro.")
            return False
        
        # Ordena por timestamp (mais recente primeiro)
        session_dirs.sort(key=lambda x: x.name, reverse=True)
        latest_session = session_dirs[0]
        session_id = latest_session.name
        
        logger.info(f"🎯 Executando SEGUNDA ETAPA para sessão: {session_id}")
        
        # Verifica se existe relatório da primeira etapa
        relatorio_path = latest_session / "RES_busca.md"
        if not relatorio_path.exists():
            logger.error(f"❌ Relatório da primeira etapa não encontrado: {relatorio_path}")
            return False
        
        # Lê o relatório da primeira etapa
        with open(relatorio_path, 'r', encoding='utf-8') as f:
            relatorio_content = f.read()
        
        logger.info(f"📊 Relatório carregado: {len(relatorio_content)} caracteres")
        
        # Executa síntese com IA
        logger.info("🧠 Iniciando síntese com IA...")
        
        synthesis_result = await enhanced_synthesis_engine.execute_comprehensive_synthesis(
            session_id=session_id,
            collected_data=relatorio_content,
            context={
                "tema": "Patchwork e Costura",
                "publico_alvo": "Mulheres entre 35 e 80 anos, casadas e solteiras, donas de casa, aposentadas",
                "produto": "Grupo de whatsapp com dicas e video aulas de patchwork e costura criativa",
                "objetivo": "Patchwork Descomplicado - Patchwork e Costura"
            }
        )
        
        if synthesis_result and synthesis_result.get('success'):
            logger.info("✅ SEGUNDA ETAPA CONCLUÍDA COM SUCESSO!")
            logger.info(f"📋 Síntese salva em: {latest_session}/sintese_master.json")
            
            # Mostra resumo da síntese
            if 'synthesis_data' in synthesis_result:
                synthesis_data = synthesis_result['synthesis_data']
                logger.info(f"🎯 Insights principais: {len(synthesis_data.get('insights_principais', []))}")
                logger.info(f"🚀 Oportunidades identificadas: {len(synthesis_data.get('oportunidades_identificadas', []))}")
                logger.info(f"👥 Público-alvo refinado: {len(synthesis_data.get('publico_alvo_refinado', {}))}")
            
            return True
        else:
            logger.error("❌ Falha na síntese com IA")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro crítico na segunda etapa: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ARQV30 Enhanced v3.0 - SEGUNDA ETAPA")
    print("=" * 50)
    
    # Executa segunda etapa
    success = asyncio.run(execute_stage2())
    
    if success:
        print("\n✅ SEGUNDA ETAPA CONCLUÍDA COM SUCESSO!")
        print("🎯 Próximo passo: Execute a terceira etapa (módulos e relatório final)")
    else:
        print("\n❌ SEGUNDA ETAPA FALHOU!")
        print("🔧 Verifique os logs para mais detalhes")