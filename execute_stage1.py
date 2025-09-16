#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar a Primeira Etapa - Coleta Massiva de Dados
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

async def execute_stage1():
    """Executa a primeira etapa - Coleta massiva de dados"""
    
    try:
        # Carrega variáveis de ambiente
        from services.environment_loader import environment_loader
        
        # Importa serviços necessários
        from services.enhanced_search_coordinator import enhanced_search_coordinator
        from services.content_size_monitor import content_size_monitor
        from services.marketing_insights_extractor import marketing_insights_extractor
        from services.social_media_content_analyzer import social_media_content_analyzer
        from services.auto_save_manager import salvar_etapa
        
        # Gera session_id único
        import time
        import uuid
        session_id = f"session_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
        
        logger.info(f"🚀 Executando PRIMEIRA ETAPA para sessão: {session_id}")
        
        # Contexto da análise (exemplo - ajuste conforme necessário)
        context = {
            "tema": "Patchwork e Costura",
            "segmento": "Artesanato e Costura Criativa",
            "publico_alvo": "Mulheres entre 35 e 80 anos, casadas e solteiras, donas de casa, aposentadas",
            "produto": "Grupo de whatsapp com dicas e video aulas de patchwork e costura criativa",
            "objetivo": "Patchwork Descomplicado - Patchwork e Costura"
        }
        
        # Query principal
        base_query = f"{context['tema']} {context['segmento']} Brasil"
        
        logger.info(f"🔍 Query principal: {base_query}")
        
        # FASE 1: Busca massiva focada em marketing
        logger.info("🎯 FASE 1: Executando busca massiva focada em marketing")
        
        search_results = await enhanced_search_coordinator.execute_marketing_focused_search(
            base_query=base_query,
            context=context,
            session_id=session_id
        )
        
        # FASE 2: Monitoramento de tamanho e qualidade
        logger.info("📏 FASE 2: Monitorando tamanho e qualidade do conteúdo")
        
        monitoring_data = content_size_monitor.monitor_content_collection(
            search_results=search_results,
            session_id=session_id
        )
        
        # FASE 3: Expansão se necessário
        if content_size_monitor.check_expansion_needed(monitoring_data):
            logger.info("📈 FASE 3: Expandindo busca para atingir meta de qualidade")
            
            expanded_results = await enhanced_search_coordinator.ensure_minimum_content_size(
                search_results=search_results,
                session_id=session_id
            )
            
            # Re-monitora após expansão
            final_monitoring = content_size_monitor.monitor_content_collection(
                search_results=expanded_results,
                session_id=session_id
            )
            
            search_results = expanded_results
            monitoring_data = final_monitoring
        
        # FASE 4: Análise especializada de redes sociais
        logger.info("📱 FASE 4: Análise especializada de redes sociais")
        
        social_results = search_results.get('social_results', []) + search_results.get('youtube_results', [])
        
        if social_results:
            social_analysis = await social_media_content_analyzer.analyze_social_content(
                social_results=social_results,
                session_id=session_id
            )
            
            search_results['social_media_analysis'] = social_analysis
        
        # FASE 5: Extração de inteligência competitiva
        logger.info("🕵️ FASE 5: Extraindo inteligência competitiva")
        
        competitor_intelligence = await enhanced_search_coordinator.extract_competitor_intelligence(
            search_results=search_results,
            session_id=session_id
        )
        
        search_results['competitor_intelligence'] = competitor_intelligence
        
        # FASE 6: Geração do relatório RES_BUSCA
        logger.info("📋 FASE 6: Gerando relatório RES_BUSCA")
        
        res_busca_data = {
            'session_id': session_id,
            'context': context,
            'search_results': search_results,
            'monitoring_data': monitoring_data,
            'competitor_intelligence': competitor_intelligence,
            'final_statistics': {
                'total_content_size_kb': monitoring_data['current_size_kb'],
                'target_achieved': monitoring_data['target_achieved'],
                'quality_score': monitoring_data['quality_score'],
                'total_sources': search_results.get('statistics', {}).get('total_sources', 0),
                'marketing_insights': search_results.get('marketing_insights', {}).get('statistics', {}).get('total_insights', 0),
                'viral_content': len(search_results.get('viral_content', [])),
                'screenshots_captured': len(search_results.get('screenshots_captured', []))
            }
        }
        
        # Salva RES_BUSCA
        produto_clean = context['produto'].replace(' ', '_').replace('/', '_')
        res_busca_path = f"analyses_data/RES_BUSCA_{produto_clean.upper()}.json"
        
        with open(res_busca_path, 'w', encoding='utf-8') as f:
            json.dump(res_busca_data, f, ensure_ascii=False, indent=2, default=str)
        
        # Gera relatório em markdown
        markdown_report = generate_res_busca_markdown(res_busca_data)
        markdown_path = f"analyses_data/{session_id}/RES_busca.md"
        
        os.makedirs(f"analyses_data/{session_id}", exist_ok=True)
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        
        # Salva etapa final
        salvar_etapa("primeira_etapa_concluida", res_busca_data, categoria="workflow")
        
        logger.info("✅ PRIMEIRA ETAPA CONCLUÍDA COM SUCESSO!")
        logger.info(f"📊 Tamanho final: {monitoring_data['current_size_kb']:.1f}KB")
        logger.info(f"📈 Qualidade: {monitoring_data['quality_score']:.2f}/10")
        logger.info(f"💎 Insights: {res_busca_data['final_statistics']['marketing_insights']}")
        logger.info(f"📁 RES_BUSCA salvo em: {res_busca_path}")
        logger.info(f"📋 Relatório salvo em: {markdown_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro crítico na primeira etapa: {e}")
        return False

def generate_res_busca_markdown(res_busca_data: Dict[str, Any]) -> str:
    """Gera relatório RES_BUSCA em markdown"""
    
    context = res_busca_data['context']
    stats = res_busca_data['final_statistics']
    monitoring = res_busca_data['monitoring_data']
    
    report = f"""# RES_BUSCA - PRIMEIRA ETAPA CONCLUÍDA

**Sessão:** {res_busca_data['session_id']}  
**Tema:** {context['tema']}  
**Segmento:** {context['segmento']}  
**Público-Alvo:** {context['publico_alvo']}  
**Produto:** {context['produto']}

---

## RESUMO EXECUTIVO

### Coleta de Dados:
- **Tamanho Total:** {stats['total_content_size_kb']:.1f}KB
- **Meta Atingida:** {'✅ SIM' if stats['target_achieved'] else '❌ NÃO'}
- **Qualidade:** {stats['quality_score']:.2f}/10
- **Total de Fontes:** {stats['total_sources']}

### Insights Extraídos:
- **Marketing Insights:** {stats['marketing_insights']}
- **Conteúdo Viral:** {stats['viral_content']}
- **Screenshots:** {stats['screenshots_captured']}

---

## DADOS COLETADOS

### Por Tipo de Fonte:
"""
    
    # Adiciona breakdown do conteúdo
    content_breakdown = monitoring.get('content_breakdown', {})
    
    for content_type, data in content_breakdown.items():
        type_name = content_type.replace('_', ' ').title()
        report += f"""
#### {type_name}
- **Quantidade:** {data['count']} itens
- **Tamanho:** {data['size_kb']:.1f}KB
- **Participação:** {data['percentage_of_total']:.1f}%
"""
    
    # Adiciona recomendações
    recommendations = monitoring.get('recommendations', [])
    
    if recommendations:
        report += "\n## RECOMENDAÇÕES PARA PRÓXIMAS ETAPAS\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
    
    report += f"""

---

## PRÓXIMOS PASSOS

1. **Segunda Etapa:** Executar `python execute_stage2.py` para síntese com IA
2. **Terceira Etapa:** Executar `python execute_stage3.py` para geração de módulos
3. **Relatório Final:** Será compilado automaticamente na terceira etapa

---

*Primeira etapa concluída em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*
"""
    
    return report

if __name__ == "__main__":
    print("🚀 ARQV30 Enhanced v3.0 - PRIMEIRA ETAPA")
    print("=" * 50)
    
    # Executa primeira etapa
    success = asyncio.run(execute_stage1())
    
    if success:
        print("\n✅ PRIMEIRA ETAPA CONCLUÍDA COM SUCESSO!")
        print("🎯 Próximo passo: Execute a segunda etapa (síntese com IA)")
    else:
        print("\n❌ PRIMEIRA ETAPA FALHOU!")
        print("🔧 Verifique os logs para mais detalhes")