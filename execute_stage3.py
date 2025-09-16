#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar a Terceira Etapa - Geração de Módulos e Relatório Final
"""

import os
import sys
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

async def execute_stage3():
    """Executa a terceira etapa - Geração de módulos e relatório final"""
    
    try:
        # Carrega variáveis de ambiente
        from services.environment_loader import environment_loader
        
        # Importa serviços necessários
        from services.enhanced_module_processor import enhanced_module_processor
        from services.comprehensive_report_generator_v3 import comprehensive_report_generator_v3
        
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
        
        logger.info(f"🎯 Executando TERCEIRA ETAPA para sessão: {session_id}")
        
        # Verifica se existe síntese da segunda etapa
        sintese_path = latest_session / "resumo_sintese.json"
        if not sintese_path.exists():
            logger.warning(f"⚠️ Síntese da segunda etapa não encontrada: {sintese_path}")
            logger.info("🔄 Continuando com dados disponíveis da primeira etapa")
        
        # FASE 1: Geração dos 16 módulos especializados
        logger.info("📝 FASE 1: Gerando 16 módulos especializados")
        
        modules_result = await enhanced_module_processor.generate_all_modules(session_id)
        
        if not modules_result.get('successful_modules'):
            logger.error("❌ Falha na geração de módulos")
            return False
        
        logger.info(f"✅ Módulos gerados: {modules_result['successful_modules']}/{modules_result['total_modules']}")
        
        # FASE 2: Compilação do relatório final
        logger.info("📋 FASE 2: Compilando relatório final")
        
        final_report_result = comprehensive_report_generator_v3.compile_final_markdown_report(session_id)
        
        if not final_report_result.get('success'):
            logger.error("❌ Falha na compilação do relatório final")
            return False
        
        logger.info(f"✅ Relatório final compilado: {final_report_result['report_path']}")
        
        # FASE 3: Geração de estatísticas finais
        logger.info("📊 FASE 3: Gerando estatísticas finais")
        
        final_statistics = {
            'session_id': session_id,
            'workflow_completed': True,
            'modules_generated': modules_result['successful_modules'],
            'modules_failed': modules_result['failed_modules'],
            'total_modules': modules_result['total_modules'],
            'success_rate': (modules_result['successful_modules'] / modules_result['total_modules']) * 100,
            'final_report_path': final_report_result['report_path'],
            'report_statistics': final_report_result.get('estatisticas_relatorio', {}),
            'completion_timestamp': datetime.now().isoformat()
        }
        
        # Salva estatísticas finais
        from services.auto_save_manager import salvar_etapa
        salvar_etapa("terceira_etapa_concluida", final_statistics, categoria="workflow")
        
        # Salva também na pasta da sessão
        stats_path = latest_session / "workflow_final_statistics.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(final_statistics, f, ensure_ascii=False, indent=2)
        
        logger.info("✅ TERCEIRA ETAPA CONCLUÍDA COM SUCESSO!")
        logger.info(f"📊 Taxa de sucesso: {final_statistics['success_rate']:.1f}%")
        logger.info(f"📋 Relatório final: {final_report_result['report_path']}")
        logger.info(f"📈 Estatísticas: {stats_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro crítico na terceira etapa: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ARQV30 Enhanced v3.0 - TERCEIRA ETAPA")
    print("=" * 50)
    
    # Executa terceira etapa
    success = asyncio.run(execute_stage3())
    
    if success:
        print("\n✅ TERCEIRA ETAPA CONCLUÍDA COM SUCESSO!")
        print("🎉 WORKFLOW COMPLETO - Todos os módulos e relatório final gerados!")
    else:
        print("\n❌ TERCEIRA ETAPA FALHOU!")
        print("🔧 Verifique os logs para mais detalhes")