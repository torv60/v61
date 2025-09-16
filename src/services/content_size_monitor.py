#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Content Size Monitor
Monitor de tamanho de conteúdo para garantir 300KB mínimo
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class ContentSizeMonitor:
    """Monitor de tamanho de conteúdo para garantir qualidade"""

    def __init__(self):
        """Inicializa o monitor"""
        self.target_size_kb = 300
        self.target_size_bytes = self.target_size_kb * 1024
        self.minimum_quality_threshold = 0.7
        
        logger.info(f"📏 Content Size Monitor inicializado - Meta: {self.target_size_kb}KB")

    def monitor_content_collection(
        self,
        search_results: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Monitora coleta de conteúdo e garante qualidade"""
        
        logger.info(f"📏 Monitorando tamanho de conteúdo para sessão: {session_id}")
        
        monitoring_data = {
            'session_id': session_id,
            'monitoring_started': datetime.now().isoformat(),
            'target_size_kb': self.target_size_kb,
            'current_size_kb': 0,
            'current_size_bytes': 0,
            'quality_score': 0,
            'content_breakdown': {},
            'size_by_source': {},
            'quality_metrics': {},
            'recommendations': [],
            'target_achieved': False
        }
        
        try:
            # Calcula tamanho atual
            current_size = self._calculate_total_size(search_results)
            monitoring_data['current_size_bytes'] = current_size
            monitoring_data['current_size_kb'] = current_size / 1024
            
            # Analisa breakdown por tipo de conteúdo
            content_breakdown = self._analyze_content_breakdown(search_results)
            monitoring_data['content_breakdown'] = content_breakdown
            
            # Analisa tamanho por fonte
            size_by_source = self._analyze_size_by_source(search_results)
            monitoring_data['size_by_source'] = size_by_source
            
            # Calcula métricas de qualidade
            quality_metrics = self._calculate_quality_metrics(search_results)
            monitoring_data['quality_metrics'] = quality_metrics
            monitoring_data['quality_score'] = quality_metrics.get('overall_quality', 0)
            
            # Verifica se meta foi atingida
            monitoring_data['target_achieved'] = current_size >= self.target_size_bytes
            
            # Gera recomendações
            recommendations = self._generate_recommendations(monitoring_data, search_results)
            monitoring_data['recommendations'] = recommendations
            
            # Salva dados de monitoramento
            self._save_monitoring_data(monitoring_data, session_id)
            
            # Log do status
            status = "✅ META ATINGIDA" if monitoring_data['target_achieved'] else "⚠️ ABAIXO DA META"
            logger.info(f"{status}: {monitoring_data['current_size_kb']:.1f}KB / {self.target_size_kb}KB")
            logger.info(f"📊 Qualidade: {monitoring_data['quality_score']:.2f}/10")
            
            return monitoring_data
            
        except Exception as e:
            logger.error(f"❌ Erro no monitoramento: {e}")
            raise

    def _calculate_total_size(self, search_results: Dict[str, Any]) -> int:
        """Calcula tamanho total do conteúdo coletado"""
        
        total_size = 0
        
        # Tipos de resultados para analisar
        result_types = ['web_results', 'social_results', 'youtube_results', 'viral_content']
        
        for result_type in result_types:
            results = search_results.get(result_type, [])
            
            for result in results:
                # Campos de texto para contar
                text_fields = ['title', 'snippet', 'content', 'description', 'text', 'caption']
                
                for field in text_fields:
                    if field in result and result[field]:
                        total_size += len(str(result[field]))
        
        return total_size

    def _analyze_content_breakdown(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa breakdown do conteúdo por tipo"""
        
        breakdown = {}
        
        result_types = ['web_results', 'social_results', 'youtube_results', 'viral_content']
        
        for result_type in result_types:
            results = search_results.get(result_type, [])
            
            type_size = 0
            type_count = len(results)
            
            for result in results:
                text_fields = ['title', 'snippet', 'content', 'description', 'text', 'caption']
                
                for field in text_fields:
                    if field in result and result[field]:
                        type_size += len(str(result[field]))
            
            breakdown[result_type] = {
                'count': type_count,
                'size_bytes': type_size,
                'size_kb': type_size / 1024,
                'avg_size_per_item': type_size / type_count if type_count > 0 else 0,
                'percentage_of_total': 0  # Será calculado depois
            }
        
        # Calcula percentuais
        total_size = sum(b['size_bytes'] for b in breakdown.values())
        
        if total_size > 0:
            for result_type in breakdown:
                breakdown[result_type]['percentage_of_total'] = (breakdown[result_type]['size_bytes'] / total_size) * 100
        
        return breakdown

    def _analyze_size_by_source(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa tamanho por fonte/provedor"""
        
        size_by_source = {}
        
        # Coleta todos os resultados
        all_results = []
        all_results.extend(search_results.get('web_results', []))
        all_results.extend(search_results.get('social_results', []))
        all_results.extend(search_results.get('youtube_results', []))
        
        for result in all_results:
            source = result.get('source', 'unknown')
            
            if source not in size_by_source:
                size_by_source[source] = {
                    'count': 0,
                    'size_bytes': 0,
                    'size_kb': 0
                }
            
            # Calcula tamanho do item
            item_size = 0
            text_fields = ['title', 'snippet', 'content', 'description', 'text', 'caption']
            
            for field in text_fields:
                if field in result and result[field]:
                    item_size += len(str(result[field]))
            
            size_by_source[source]['count'] += 1
            size_by_source[source]['size_bytes'] += item_size
            size_by_source[source]['size_kb'] = size_by_source[source]['size_bytes'] / 1024
        
        return size_by_source

    def _calculate_quality_metrics(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas de qualidade do conteúdo"""
        
        quality_metrics = {
            'content_diversity': 0,
            'source_reliability': 0,
            'marketing_relevance': 0,
            'viral_content_ratio': 0,
            'engagement_quality': 0,
            'overall_quality': 0
        }
        
        try:
            # Diversidade de conteúdo (quantos tipos diferentes)
            content_types = set()
            all_results = []
            all_results.extend(search_results.get('web_results', []))
            all_results.extend(search_results.get('social_results', []))
            all_results.extend(search_results.get('youtube_results', []))
            
            for result in all_results:
                platform = result.get('platform', 'web')
                source = result.get('source', 'unknown')
                content_types.add(f"{platform}_{source}")
            
            quality_metrics['content_diversity'] = min(10, len(content_types))
            
            # Confiabilidade das fontes (baseado em domínios conhecidos)
            reliable_domains = [
                'g1.globo.com', 'exame.com', 'valor.globo.com',
                'estadao.com.br', 'folha.uol.com.br', 'infomoney.com.br',
                'youtube.com', 'instagram.com', 'facebook.com'
            ]
            
            reliable_sources = 0
            total_sources = len(all_results)
            
            for result in all_results:
                url = result.get('url', '')
                if any(domain in url for domain in reliable_domains):
                    reliable_sources += 1
            
            quality_metrics['source_reliability'] = (reliable_sources / total_sources * 10) if total_sources > 0 else 0
            
            # Relevância para marketing (baseado em keywords)
            marketing_keywords = [
                'marketing', 'vendas', 'conversão', 'ROI', 'campanha',
                'anúncio', 'publicidade', 'estratégia', 'funil'
            ]
            
            marketing_relevant = 0
            
            for result in all_results:
                content_text = self._get_item_text(result).lower()
                if any(keyword in content_text for keyword in marketing_keywords):
                    marketing_relevant += 1
            
            quality_metrics['marketing_relevance'] = (marketing_relevant / total_sources * 10) if total_sources > 0 else 0
            
            # Ratio de conteúdo viral
            viral_content = search_results.get('viral_content', [])
            quality_metrics['viral_content_ratio'] = (len(viral_content) / total_sources * 10) if total_sources > 0 else 0
            
            # Qualidade de engajamento
            high_engagement_count = 0
            
            for result in all_results:
                viral_score = result.get('viral_score', 0)
                if viral_score >= 7.0:
                    high_engagement_count += 1
            
            quality_metrics['engagement_quality'] = (high_engagement_count / total_sources * 10) if total_sources > 0 else 0
            
            # Qualidade geral (média ponderada)
            weights = {
                'content_diversity': 0.2,
                'source_reliability': 0.25,
                'marketing_relevance': 0.3,
                'viral_content_ratio': 0.15,
                'engagement_quality': 0.1
            }
            
            overall_quality = sum(
                quality_metrics[metric] * weight
                for metric, weight in weights.items()
            )
            
            quality_metrics['overall_quality'] = overall_quality
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"❌ Erro no cálculo de qualidade: {e}")
            return quality_metrics

    def _generate_recommendations(
        self,
        monitoring_data: Dict[str, Any],
        search_results: Dict[str, Any]
    ) -> List[str]:
        """Gera recomendações baseadas no monitoramento"""
        
        recommendations = []
        
        current_size_kb = monitoring_data['current_size_kb']
        quality_score = monitoring_data['quality_score']
        target_achieved = monitoring_data['target_achieved']
        
        # Recomendações de tamanho
        if not target_achieved:
            deficit_kb = self.target_size_kb - current_size_kb
            recommendations.append(f"📈 EXPANDIR BUSCA: Faltam {deficit_kb:.1f}KB para atingir meta de {self.target_size_kb}KB")
            recommendations.append("🔍 Sugestão: Executar buscas complementares com queries específicas do nicho")
        else:
            recommendations.append(f"✅ META ATINGIDA: {current_size_kb:.1f}KB coletados (meta: {self.target_size_kb}KB)")
        
        # Recomendações de qualidade
        if quality_score < 7.0:
            recommendations.append(f"⚠️ QUALIDADE BAIXA: Score {quality_score:.1f}/10 - Buscar fontes mais confiáveis")
            
            # Recomendações específicas baseadas nas métricas
            quality_metrics = monitoring_data.get('quality_metrics', {})
            
            if quality_metrics.get('marketing_relevance', 0) < 6:
                recommendations.append("🎯 Aumentar relevância: Focar em queries específicas de marketing")
            
            if quality_metrics.get('viral_content_ratio', 0) < 5:
                recommendations.append("🔥 Buscar mais conteúdo viral: Expandir busca em redes sociais")
            
            if quality_metrics.get('source_reliability', 0) < 6:
                recommendations.append("🏢 Melhorar fontes: Priorizar domínios confiáveis e autoridades do setor")
        
        else:
            recommendations.append(f"✅ QUALIDADE ALTA: Score {quality_score:.1f}/10 - Conteúdo de excelente qualidade")
        
        # Recomendações de diversidade
        content_breakdown = monitoring_data.get('content_breakdown', {})
        
        web_percentage = content_breakdown.get('web_results', {}).get('percentage_of_total', 0)
        social_percentage = content_breakdown.get('social_results', {}).get('percentage_of_total', 0)
        
        if web_percentage > 80:
            recommendations.append("📱 DIVERSIFICAR: Muito conteúdo web - Aumentar coleta de redes sociais")
        elif social_percentage > 70:
            recommendations.append("🌐 EQUILIBRAR: Muito conteúdo social - Adicionar mais fontes web")
        else:
            recommendations.append("⚖️ BOA DIVERSIDADE: Conteúdo bem distribuído entre fontes")
        
        # Recomendações específicas para marketing
        marketing_insights = search_results.get('marketing_insights', {})
        if marketing_insights:
            insights_count = marketing_insights.get('statistics', {}).get('total_insights', 0)
            
            if insights_count < 20:
                recommendations.append("💎 AUMENTAR INSIGHTS: Buscar mais conteúdo específico de marketing e conversão")
            else:
                recommendations.append(f"💎 INSIGHTS RICOS: {insights_count} insights de marketing identificados")
        
        return recommendations

    def _calculate_total_size(self, search_results: Dict[str, Any]) -> int:
        """Calcula tamanho total em bytes"""
        
        total_size = 0
        
        # Tipos de resultados
        result_types = ['web_results', 'social_results', 'youtube_results', 'viral_content']
        
        for result_type in result_types:
            results = search_results.get(result_type, [])
            
            for result in results:
                # Campos de texto
                text_fields = ['title', 'snippet', 'content', 'description', 'text', 'caption']
                
                for field in text_fields:
                    if field in result and result[field]:
                        total_size += len(str(result[field]))
        
        return total_size

    def generate_size_report(self, monitoring_data: Dict[str, Any]) -> str:
        """Gera relatório de tamanho e qualidade"""
        
        current_size_kb = monitoring_data['current_size_kb']
        target_size_kb = monitoring_data['target_size_kb']
        quality_score = monitoring_data['quality_score']
        target_achieved = monitoring_data['target_achieved']
        
        status_emoji = "✅" if target_achieved else "⚠️"
        status_text = "META ATINGIDA" if target_achieved else "ABAIXO DA META"
        
        report = f"""# RELATÓRIO DE TAMANHO E QUALIDADE - ARQV30 Enhanced v3.0

**Sessão:** {monitoring_data['session_id']}  
**Monitoramento realizado em:** {monitoring_data['monitoring_started']}  
**Status:** {status_emoji} {status_text}

---

## RESUMO EXECUTIVO

### Tamanho do Conteúdo:
- **Atual:** {current_size_kb:.1f}KB
- **Meta:** {target_size_kb}KB
- **Progresso:** {(current_size_kb/target_size_kb*100):.1f}%
- **Status:** {'✅ Atingido' if target_achieved else f'❌ Faltam {target_size_kb-current_size_kb:.1f}KB'}

### Qualidade do Conteúdo:
- **Score Geral:** {quality_score:.2f}/10
- **Classificação:** {self._classify_quality_score(quality_score)}

---

## BREAKDOWN POR TIPO DE CONTEÚDO

"""
        
        # Adiciona breakdown
        content_breakdown = monitoring_data.get('content_breakdown', {})
        
        for content_type, data in content_breakdown.items():
            type_name = content_type.replace('_', ' ').title()
            
            report += f"""### {type_name}

**Quantidade:** {data['count']} itens  
**Tamanho:** {data['size_kb']:.1f}KB ({data['percentage_of_total']:.1f}% do total)  
**Tamanho Médio por Item:** {data['avg_size_per_item']:.0f} bytes

"""
        
        # Adiciona análise por fonte
        size_by_source = monitoring_data.get('size_by_source', {})
        
        if size_by_source:
            report += "## ANÁLISE POR FONTE\n\n"
            
            # Ordena por tamanho
            sorted_sources = sorted(size_by_source.items(), key=lambda x: x[1]['size_kb'], reverse=True)
            
            for source, data in sorted_sources:
                report += f"""### {source.upper()}

**Itens:** {data['count']}  
**Tamanho:** {data['size_kb']:.1f}KB  
**Contribuição:** {(data['size_kb']/current_size_kb*100):.1f}% do total

"""
        
        # Adiciona métricas de qualidade
        quality_metrics = monitoring_data.get('quality_metrics', {})
        
        if quality_metrics:
            report += "## MÉTRICAS DE QUALIDADE\n\n"
            
            metrics_labels = {
                'content_diversity': 'Diversidade de Conteúdo',
                'source_reliability': 'Confiabilidade das Fontes',
                'marketing_relevance': 'Relevância para Marketing',
                'viral_content_ratio': 'Ratio de Conteúdo Viral',
                'engagement_quality': 'Qualidade de Engajamento'
            }
            
            for metric, value in quality_metrics.items():
                if metric in metrics_labels:
                    label = metrics_labels[metric]
                    score_bar = "█" * int(value) + "░" * (10 - int(value))
                    report += f"**{label}:** {value:.1f}/10 `{score_bar}`\n\n"
        
        # Adiciona recomendações
        recommendations = monitoring_data.get('recommendations', [])
        
        if recommendations:
            report += "## RECOMENDAÇÕES\n\n"
            
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"
        
        report += f"\n---\n\n*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*"
        
        return report

    def _classify_quality_score(self, score: float) -> str:
        """Classifica score de qualidade"""
        
        if score >= 9.0:
            return "🏆 EXCELENTE"
        elif score >= 8.0:
            return "✅ MUITO BOM"
        elif score >= 7.0:
            return "👍 BOM"
        elif score >= 6.0:
            return "⚠️ REGULAR"
        elif score >= 5.0:
            return "❌ BAIXO"
        else:
            return "💀 CRÍTICO"

    def _save_monitoring_data(self, monitoring_data: Dict[str, Any], session_id: str):
        """Salva dados de monitoramento"""
        
        try:
            session_dir = Path(f"analyses_data/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Salva dados de monitoramento
            monitoring_path = session_dir / "content_size_monitoring.json"
            with open(monitoring_path, 'w', encoding='utf-8') as f:
                json.dump(monitoring_data, f, ensure_ascii=False, indent=2)
            
            # Gera e salva relatório
            report = self.generate_size_report(monitoring_data)
            report_path = session_dir / "content_size_report.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"💾 Dados de monitoramento salvos: {monitoring_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar monitoramento: {e}")

    def _get_item_text(self, item: Dict[str, Any]) -> str:
        """Extrai texto do item"""
        text_fields = ['content', 'description', 'snippet', 'text', 'caption', 'title']
        
        combined_text = ""
        for field in text_fields:
            if field in item and item[field]:
                combined_text += str(item[field]) + " "
        
        return combined_text.strip()

    def check_expansion_needed(self, monitoring_data: Dict[str, Any]) -> bool:
        """Verifica se é necessário expandir a busca"""
        
        target_achieved = monitoring_data.get('target_achieved', False)
        quality_score = monitoring_data.get('quality_score', 0)
        
        # Precisa expandir se não atingiu meta ou qualidade baixa
        return not target_achieved or quality_score < self.minimum_quality_threshold

    def get_expansion_suggestions(self, monitoring_data: Dict[str, Any]) -> List[str]:
        """Retorna sugestões para expansão da busca"""
        
        suggestions = []
        
        content_breakdown = monitoring_data.get('content_breakdown', {})
        
        # Sugere expandir tipos com pouco conteúdo
        for content_type, data in content_breakdown.items():
            if data['count'] < 5:  # Poucos itens
                type_name = content_type.replace('_', ' ')
                suggestions.append(f"Expandir {type_name}: apenas {data['count']} itens coletados")
        
        # Sugere melhorar qualidade
        quality_metrics = monitoring_data.get('quality_metrics', {})
        
        if quality_metrics.get('marketing_relevance', 0) < 6:
            suggestions.append("Buscar mais conteúdo específico de marketing e vendas")
        
        if quality_metrics.get('viral_content_ratio', 0) < 5:
            suggestions.append("Aumentar coleta de conteúdo viral em redes sociais")
        
        return suggestions

# Instância global
content_size_monitor = ContentSizeMonitor()