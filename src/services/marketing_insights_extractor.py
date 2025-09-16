#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Marketing Insights Extractor
Extrator especializado de insights valiosos para agências de marketing
"""

import os
import logging
import asyncio
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class MarketingInsightsExtractor:
    """Extrator especializado para insights de marketing de alto valor"""

    def __init__(self):
        """Inicializa o extrator de insights"""
        self.viral_keywords = [
            'conversão', 'CTR', 'ROI', 'ROAS', 'engajamento', 'alcance',
            'impressões', 'cliques', 'leads', 'vendas', 'faturamento',
            'crescimento', 'estratégia', 'campanha', 'anúncio', 'ad',
            'funil', 'landing page', 'copy', 'headline', 'CTA',
            'segmentação', 'público-alvo', 'persona', 'jornada',
            'automação', 'email marketing', 'social media', 'influencer'
        ]
        
        self.high_value_patterns = [
            r'aumentou.*?(\d+)%',
            r'cresceu.*?(\d+)%',
            r'converteu.*?(\d+)%',
            r'CTR.*?(\d+(?:\.\d+)?)%',
            r'ROI.*?(\d+(?:\.\d+)?)x',
            r'ROAS.*?(\d+(?:\.\d+)?)x',
            r'R\$\s*(\d+(?:\.\d+)?(?:k|mil|milhão|milhões)?)',
            r'(\d+(?:\.\d+)?)x.*?mais.*?vendas',
            r'(\d+(?:\.\d+)?)x.*?mais.*?leads'
        ]
        
        logger.info("🎯 Marketing Insights Extractor inicializado")

    async def extract_marketing_insights(
        self,
        search_results: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Extrai insights valiosos para marketing dos resultados de busca"""
        
        logger.info(f"🎯 Extraindo insights de marketing para sessão: {session_id}")
        
        insights_data = {
            'session_id': session_id,
            'extraction_started': datetime.now().isoformat(),
            'high_value_insights': [],
            'conversion_data': [],
            'successful_campaigns': [],
            'viral_content_analysis': [],
            'audience_insights': [],
            'competitor_strategies': [],
            'pricing_insights': [],
            'funnel_optimization': [],
            'ad_performance_data': [],
            'engagement_patterns': [],
            'statistics': {
                'total_insights': 0,
                'high_value_count': 0,
                'conversion_cases': 0,
                'viral_content_found': 0
            }
        }
        
        try:
            # Processa todos os resultados coletados
            all_content = []
            
            # Web results
            web_results = search_results.get('web_results', [])
            all_content.extend(web_results)
            
            # YouTube results
            youtube_results = search_results.get('youtube_results', [])
            all_content.extend(youtube_results)
            
            # Social results
            social_results = search_results.get('social_results', [])
            all_content.extend(social_results)
            
            logger.info(f"📊 Processando {len(all_content)} itens de conteúdo")
            
            # Extrai insights de cada item
            for item in all_content:
                insights = await self._extract_item_insights(item)
                if insights:
                    insights_data['high_value_insights'].extend(insights.get('insights', []))
                    insights_data['conversion_data'].extend(insights.get('conversions', []))
                    insights_data['successful_campaigns'].extend(insights.get('campaigns', []))
                    insights_data['viral_content_analysis'].extend(insights.get('viral_analysis', []))
                    insights_data['audience_insights'].extend(insights.get('audience', []))
                    insights_data['competitor_strategies'].extend(insights.get('competitors', []))
                    insights_data['pricing_insights'].extend(insights.get('pricing', []))
                    insights_data['ad_performance_data'].extend(insights.get('ad_performance', []))
            
            # Analisa padrões de engajamento
            engagement_patterns = self._analyze_engagement_patterns(all_content)
            insights_data['engagement_patterns'] = engagement_patterns
            
            # Identifica oportunidades de funil
            funnel_opportunities = self._identify_funnel_opportunities(all_content)
            insights_data['funnel_optimization'] = funnel_opportunities
            
            # Calcula estatísticas finais
            insights_data['statistics'] = {
                'total_insights': len(insights_data['high_value_insights']),
                'high_value_count': len([i for i in insights_data['high_value_insights'] if i.get('value_score', 0) >= 8]),
                'conversion_cases': len(insights_data['conversion_data']),
                'viral_content_found': len(insights_data['viral_content_analysis']),
                'successful_campaigns': len(insights_data['successful_campaigns']),
                'audience_insights': len(insights_data['audience_insights']),
                'competitor_strategies': len(insights_data['competitor_strategies']),
                'pricing_insights': len(insights_data['pricing_insights']),
                'extraction_duration': (datetime.now() - datetime.fromisoformat(insights_data['extraction_started'])).total_seconds()
            }
            
            # Salva insights extraídos
            await self._save_marketing_insights(insights_data, session_id)
            
            logger.info(f"✅ Insights de marketing extraídos: {insights_data['statistics']['total_insights']} insights totais")
            
            return insights_data
            
        except Exception as e:
            logger.error(f"❌ Erro na extração de insights: {e}")
            raise

    async def _extract_item_insights(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrai insights de um item específico"""
        
        try:
            content_text = self._get_item_text(item)
            if not content_text or len(content_text) < 50:
                return None
            
            insights = {
                'insights': [],
                'conversions': [],
                'campaigns': [],
                'viral_analysis': [],
                'audience': [],
                'competitors': [],
                'pricing': [],
                'ad_performance': []
            }
            
            # Extrai dados de conversão
            conversion_data = self._extract_conversion_data(content_text, item)
            if conversion_data:
                insights['conversions'].append(conversion_data)
            
            # Identifica campanhas de sucesso
            campaign_data = self._identify_successful_campaigns(content_text, item)
            if campaign_data:
                insights['campaigns'].append(campaign_data)
            
            # Analisa conteúdo viral
            viral_analysis = self._analyze_viral_content(content_text, item)
            if viral_analysis:
                insights['viral_analysis'].append(viral_analysis)
            
            # Extrai insights de audiência
            audience_insights = self._extract_audience_insights(content_text, item)
            if audience_insights:
                insights['audience'].append(audience_insights)
            
            # Identifica estratégias de concorrentes
            competitor_strategies = self._extract_competitor_strategies(content_text, item)
            if competitor_strategies:
                insights['competitors'].append(competitor_strategies)
            
            # Extrai insights de precificação
            pricing_insights = self._extract_pricing_insights(content_text, item)
            if pricing_insights:
                insights['pricing'].append(pricing_insights)
            
            # Analisa performance de anúncios
            ad_performance = self._extract_ad_performance(content_text, item)
            if ad_performance:
                insights['ad_performance'].append(ad_performance)
            
            # Extrai insights gerais de alto valor
            general_insights = self._extract_high_value_insights(content_text, item)
            insights['insights'].extend(general_insights)
            
            return insights
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair insights do item: {e}")
            return None

    def _get_item_text(self, item: Dict[str, Any]) -> str:
        """Extrai texto do item de forma robusta"""
        text_fields = ['content', 'description', 'snippet', 'text', 'caption', 'title']
        
        combined_text = ""
        for field in text_fields:
            if field in item and item[field]:
                combined_text += str(item[field]) + " "
        
        return combined_text.strip()

    def _extract_conversion_data(self, text: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrai dados específicos de conversão"""
        
        conversion_patterns = [
            r'conversão.*?(\d+(?:\.\d+)?)%',
            r'converteu.*?(\d+(?:\.\d+)?)%',
            r'taxa.*?conversão.*?(\d+(?:\.\d+)?)%',
            r'CTR.*?(\d+(?:\.\d+)?)%',
            r'click.*?through.*?rate.*?(\d+(?:\.\d+)?)%'
        ]
        
        conversions_found = []
        
        for pattern in conversion_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                rate = float(match.group(1))
                if rate > 0:  # Só considera conversões positivas
                    conversions_found.append({
                        'rate': rate,
                        'context': text[max(0, match.start()-100):match.end()+100],
                        'metric_type': 'conversion_rate' if 'conversão' in match.group(0).lower() else 'ctr',
                        'source_url': item.get('url', ''),
                        'platform': item.get('platform', 'web')
                    })
        
        if conversions_found:
            # Retorna a melhor conversão encontrada
            best_conversion = max(conversions_found, key=lambda x: x['rate'])
            best_conversion['value_score'] = min(10, best_conversion['rate'] / 2)  # Score baseado na taxa
            return best_conversion
        
        return None

    def _identify_successful_campaigns(self, text: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Identifica campanhas de sucesso mencionadas"""
        
        success_indicators = [
            r'campanha.*?sucesso',
            r'estratégia.*?funcionou',
            r'resultado.*?incrível',
            r'crescimento.*?(\d+)%',
            r'aumentou.*?vendas.*?(\d+)%',
            r'ROI.*?(\d+(?:\.\d+)?)x',
            r'ROAS.*?(\d+(?:\.\d+)?)x'
        ]
        
        for pattern in success_indicators:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {
                    'campaign_description': text[max(0, match.start()-200):match.end()+200],
                    'success_metric': match.group(0),
                    'extracted_value': match.group(1) if match.groups() else None,
                    'source_url': item.get('url', ''),
                    'platform': item.get('platform', 'web'),
                    'value_score': 8,  # Campanhas de sucesso têm alto valor
                    'insight_type': 'successful_campaign'
                }
        
        return None

    def _analyze_viral_content(self, text: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analisa fatores de viralização do conteúdo"""
        
        viral_indicators = [
            r'viral',
            r'milhões.*?visualizações',
            r'(\d+)M.*?views',
            r'(\d+)k.*?likes',
            r'(\d+)k.*?compartilhamentos',
            r'trending',
            r'explodiu.*?redes',
            r'viralizou'
        ]
        
        viral_score = 0
        viral_factors = []
        
        for pattern in viral_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                viral_score += 1
                viral_factors.append(match.group(0))
        
        if viral_score > 0:
            return {
                'viral_score': min(10, viral_score * 2),
                'viral_factors': viral_factors,
                'content_analysis': text[:500],
                'source_url': item.get('url', ''),
                'platform': item.get('platform', 'web'),
                'value_score': min(10, viral_score * 1.5),
                'insight_type': 'viral_content'
            }
        
        return None

    def _extract_audience_insights(self, text: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrai insights sobre audiência e público-alvo"""
        
        audience_patterns = [
            r'público.*?(\d+).*?anos',
            r'audiência.*?(\d+)%.*?(masculino|feminino)',
            r'segmento.*?(A|B|C|D|E)',
            r'renda.*?R\$.*?(\d+(?:\.\d+)?k?)',
            r'comportamento.*?compra',
            r'jornada.*?cliente',
            r'persona.*?principal'
        ]
        
        audience_data = []
        
        for pattern in audience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                audience_data.append({
                    'insight': match.group(0),
                    'context': text[max(0, match.start()-100):match.end()+100],
                    'extracted_value': match.group(1) if match.groups() else None
                })
        
        if audience_data:
            return {
                'audience_insights': audience_data,
                'source_url': item.get('url', ''),
                'platform': item.get('platform', 'web'),
                'value_score': 7,  # Insights de audiência são valiosos
                'insight_type': 'audience_data'
            }
        
        return None

    def _extract_competitor_strategies(self, text: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrai estratégias de concorrentes"""
        
        competitor_patterns = [
            r'concorrente.*?estratégia',
            r'competidor.*?usando',
            r'líder.*?mercado.*?faz',
            r'empresa.*?X.*?cresceu',
            r'case.*?sucesso.*?(empresa|marca)',
            r'benchmarking',
            r'análise.*?competitiva'
        ]
        
        strategies_found = []
        
        for pattern in competitor_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                strategies_found.append({
                    'strategy_description': text[max(0, match.start()-150):match.end()+150],
                    'context': match.group(0),
                    'source_url': item.get('url', ''),
                    'platform': item.get('platform', 'web')
                })
        
        if strategies_found:
            return {
                'competitor_strategies': strategies_found,
                'value_score': 8,  # Estratégias de concorrentes são muito valiosas
                'insight_type': 'competitor_intelligence'
            }
        
        return None

    def _extract_pricing_insights(self, text: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrai insights de precificação"""
        
        pricing_patterns = [
            r'preço.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'valor.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'investimento.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'ticket.*?médio.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'LTV.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'CAC.*?R\$.*?(\d+(?:\.\d+)?)',
            r'margem.*?(\d+)%',
            r'markup.*?(\d+)%'
        ]
        
        pricing_data = []
        
        for pattern in pricing_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                pricing_data.append({
                    'pricing_info': match.group(0),
                    'value': match.group(1) if match.groups() else None,
                    'context': text[max(0, match.start()-100):match.end()+100],
                    'metric_type': self._classify_pricing_metric(match.group(0))
                })
        
        if pricing_data:
            return {
                'pricing_insights': pricing_data,
                'source_url': item.get('url', ''),
                'platform': item.get('platform', 'web'),
                'value_score': 9,  # Dados de preço são extremamente valiosos
                'insight_type': 'pricing_intelligence'
            }
        
        return None

    def _extract_ad_performance(self, text: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrai dados de performance de anúncios"""
        
        ad_patterns = [
            r'anúncio.*?converteu.*?(\d+(?:\.\d+)?)%',
            r'ad.*?performance.*?(\d+(?:\.\d+)?)%',
            r'campanha.*?Facebook.*?(\d+(?:\.\d+)?)%',
            r'Google.*?Ads.*?(\d+(?:\.\d+)?)%',
            r'Instagram.*?ad.*?(\d+(?:\.\d+)?)%',
            r'CPC.*?R\$.*?(\d+(?:\.\d+)?)',
            r'CPM.*?R\$.*?(\d+(?:\.\d+)?)',
            r'CPA.*?R\$.*?(\d+(?:\.\d+)?)'
        ]
        
        ad_data = []
        
        for pattern in ad_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                ad_data.append({
                    'ad_metric': match.group(0),
                    'performance_value': match.group(1) if match.groups() else None,
                    'context': text[max(0, match.start()-150):match.end()+150],
                    'platform': self._identify_ad_platform(match.group(0))
                })
        
        if ad_data:
            return {
                'ad_performance': ad_data,
                'source_url': item.get('url', ''),
                'platform': item.get('platform', 'web'),
                'value_score': 9,  # Performance de ads é extremamente valiosa
                'insight_type': 'ad_performance'
            }
        
        return None

    def _extract_high_value_insights(self, text: str, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai insights gerais de alto valor"""
        
        insights = []
        
        # Busca por padrões de alto valor
        for pattern in self.high_value_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value_score = self._calculate_insight_value(match.group(0), text)
                
                if value_score >= 6:  # Só insights de alto valor
                    insights.append({
                        'insight_text': match.group(0),
                        'context': text[max(0, match.start()-200):match.end()+200],
                        'extracted_value': match.group(1) if match.groups() else None,
                        'value_score': value_score,
                        'source_url': item.get('url', ''),
                        'platform': item.get('platform', 'web'),
                        'insight_type': 'high_value_metric'
                    })
        
        # Busca por palavras-chave de marketing
        marketing_score = 0
        for keyword in self.viral_keywords:
            if keyword.lower() in text.lower():
                marketing_score += 1
        
        if marketing_score >= 3:  # Conteúdo relevante para marketing
            insights.append({
                'insight_text': f'Conteúdo rico em marketing ({marketing_score} keywords)',
                'context': text[:300],
                'marketing_keywords': [kw for kw in self.viral_keywords if kw.lower() in text.lower()],
                'value_score': min(10, marketing_score),
                'source_url': item.get('url', ''),
                'platform': item.get('platform', 'web'),
                'insight_type': 'marketing_content'
            })
        
        return insights

    def _calculate_insight_value(self, insight_text: str, full_context: str) -> float:
        """Calcula o valor de um insight para agências de marketing"""
        
        score = 0
        insight_lower = insight_text.lower()
        
        # Métricas de conversão têm alto valor
        if any(word in insight_lower for word in ['conversão', 'ctr', 'roi', 'roas']):
            score += 3
        
        # Dados financeiros têm alto valor
        if any(word in insight_lower for word in ['r$', 'faturamento', 'receita', 'lucro']):
            score += 2
        
        # Percentuais específicos têm valor
        if re.search(r'\d+(?:\.\d+)?%', insight_text):
            score += 2
        
        # Multiplicadores têm valor
        if re.search(r'\d+(?:\.\d+)?x', insight_text):
            score += 2
        
        # Contexto de marketing aumenta valor
        marketing_context = sum(1 for kw in self.viral_keywords if kw.lower() in full_context.lower())
        score += min(3, marketing_context / 3)
        
        return min(10, score)

    def _analyze_engagement_patterns(self, all_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analisa padrões de engajamento"""
        
        patterns = []
        
        # Analisa por plataforma
        platform_engagement = {}
        
        for item in all_content:
            platform = item.get('platform', 'web')
            
            if platform not in platform_engagement:
                platform_engagement[platform] = {
                    'total_items': 0,
                    'high_engagement': 0,
                    'avg_viral_score': 0,
                    'engagement_metrics': []
                }
            
            platform_data = platform_engagement[platform]
            platform_data['total_items'] += 1
            
            viral_score = item.get('viral_score', 0)
            platform_data['avg_viral_score'] += viral_score
            
            if viral_score >= 7:
                platform_data['high_engagement'] += 1
            
            # Coleta métricas específicas
            if platform == 'youtube':
                views = item.get('view_count', 0)
                likes = item.get('like_count', 0)
                if views > 0:
                    engagement_rate = (likes / views) * 100
                    platform_data['engagement_metrics'].append(engagement_rate)
            
            elif platform in ['instagram', 'facebook']:
                likes = item.get('likes', 0)
                comments = item.get('comments', 0)
                if likes > 0:
                    comment_rate = (comments / likes) * 100
                    platform_data['engagement_metrics'].append(comment_rate)
        
        # Calcula médias e cria padrões
        for platform, data in platform_engagement.items():
            if data['total_items'] > 0:
                data['avg_viral_score'] /= data['total_items']
                data['high_engagement_rate'] = (data['high_engagement'] / data['total_items']) * 100
                
                if data['engagement_metrics']:
                    data['avg_engagement_rate'] = sum(data['engagement_metrics']) / len(data['engagement_metrics'])
                
                patterns.append({
                    'platform': platform,
                    'pattern_type': 'engagement_analysis',
                    'metrics': data,
                    'value_score': 8,
                    'insight_type': 'engagement_pattern'
                })
        
        return patterns

    def _identify_funnel_opportunities(self, all_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica oportunidades de otimização de funil"""
        
        opportunities = []
        
        funnel_keywords = [
            'funil', 'landing page', 'conversão', 'lead magnet',
            'isca digital', 'opt-in', 'squeeze page', 'checkout',
            'abandono carrinho', 'remarketing', 'retargeting'
        ]
        
        for item in all_content:
            text = self._get_item_text(item)
            
            funnel_mentions = 0
            mentioned_keywords = []
            
            for keyword in funnel_keywords:
                if keyword.lower() in text.lower():
                    funnel_mentions += 1
                    mentioned_keywords.append(keyword)
            
            if funnel_mentions >= 2:  # Conteúdo relevante para funil
                opportunities.append({
                    'opportunity_description': text[:400],
                    'funnel_keywords': mentioned_keywords,
                    'relevance_score': min(10, funnel_mentions * 2),
                    'source_url': item.get('url', ''),
                    'platform': item.get('platform', 'web'),
                    'value_score': min(10, funnel_mentions * 1.5),
                    'insight_type': 'funnel_opportunity'
                })
        
        return opportunities

    def _classify_pricing_metric(self, pricing_text: str) -> str:
        """Classifica o tipo de métrica de preço"""
        
        text_lower = pricing_text.lower()
        
        if 'ticket' in text_lower:
            return 'ticket_medio'
        elif 'ltv' in text_lower:
            return 'lifetime_value'
        elif 'cac' in text_lower:
            return 'customer_acquisition_cost'
        elif 'margem' in text_lower:
            return 'profit_margin'
        elif 'markup' in text_lower:
            return 'markup'
        else:
            return 'price_general'

    def _identify_ad_platform(self, ad_text: str) -> str:
        """Identifica a plataforma do anúncio"""
        
        text_lower = ad_text.lower()
        
        if 'facebook' in text_lower:
            return 'facebook'
        elif 'google' in text_lower:
            return 'google_ads'
        elif 'instagram' in text_lower:
            return 'instagram'
        elif 'youtube' in text_lower:
            return 'youtube'
        elif 'linkedin' in text_lower:
            return 'linkedin'
        else:
            return 'unknown'

    async def _save_marketing_insights(self, insights_data: Dict[str, Any], session_id: str):
        """Salva insights de marketing extraídos"""
        
        try:
            # Cria diretório da sessão
            session_dir = Path(f"analyses_data/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Salva insights completos
            insights_path = session_dir / "marketing_insights.json"
            with open(insights_path, 'w', encoding='utf-8') as f:
                json.dump(insights_data, f, ensure_ascii=False, indent=2)
            
            # Gera relatório de insights
            report = self._generate_insights_report(insights_data)
            report_path = session_dir / "marketing_insights_report.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"💾 Insights de marketing salvos: {insights_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar insights: {e}")

    def _generate_insights_report(self, insights_data: Dict[str, Any]) -> str:
        """Gera relatório detalhado dos insights de marketing"""
        
        stats = insights_data['statistics']
        
        report = f"""# INSIGHTS DE MARKETING - ARQV30 Enhanced v3.0

**Sessão:** {insights_data['session_id']}  
**Extração realizada em:** {insights_data['extraction_started']}  
**Total de Insights:** {stats['total_insights']}  
**Insights de Alto Valor:** {stats['high_value_count']}  
**Cases de Conversão:** {stats['conversion_cases']}  
**Conteúdo Viral:** {stats['viral_content_found']}

---

## RESUMO EXECUTIVO

### Insights Coletados:
- 🎯 **{stats['total_insights']}** insights totais extraídos
- 💎 **{stats['high_value_count']}** insights de alto valor (score ≥ 8)
- 📈 **{stats['conversion_cases']}** cases de conversão documentados
- 🔥 **{stats['viral_content_found']}** análises de conteúdo viral
- 🏆 **{stats['successful_campaigns']}** campanhas de sucesso identificadas
- 👥 **{stats['audience_insights']}** insights de audiência
- ⚔️ **{stats['competitor_strategies']}** estratégias de concorrentes
- 💰 **{stats['pricing_insights']}** insights de precificação

---

## TOP 10 INSIGHTS DE ALTO VALOR

"""
        
        # Adiciona top insights
        high_value_insights = [i for i in insights_data['high_value_insights'] if i.get('value_score', 0) >= 8]
        high_value_insights.sort(key=lambda x: x.get('value_score', 0), reverse=True)
        
        for i, insight in enumerate(high_value_insights[:10], 1):
            report += f"""### {i}. {insight.get('insight_type', 'Insight').replace('_', ' ').title()}

**Score de Valor:** {insight.get('value_score', 0):.1f}/10  
**Plataforma:** {insight.get('platform', 'N/A').title()}  
**Insight:** {insight.get('insight_text', 'N/A')}  
**URL:** {insight.get('source_url', 'N/A')}

**Contexto:**  
{insight.get('context', 'N/A')[:300]}...

---

"""
        
        # Adiciona dados de conversão
        if insights_data['conversion_data']:
            report += "\n## DADOS DE CONVERSÃO IDENTIFICADOS\n\n"
            
            for i, conv in enumerate(insights_data['conversion_data'][:5], 1):
                report += f"""### Conversão {i}

**Taxa:** {conv.get('rate', 0)}%  
**Tipo:** {conv.get('metric_type', 'N/A')}  
**Plataforma:** {conv.get('platform', 'N/A')}  
**Contexto:** {conv.get('context', 'N/A')[:200]}...

"""
        
        # Adiciona campanhas de sucesso
        if insights_data['successful_campaigns']:
            report += "\n## CAMPANHAS DE SUCESSO IDENTIFICADAS\n\n"
            
            for i, campaign in enumerate(insights_data['successful_campaigns'][:5], 1):
                report += f"""### Campanha {i}

**Métrica de Sucesso:** {campaign.get('success_metric', 'N/A')}  
**Valor Extraído:** {campaign.get('extracted_value', 'N/A')}  
**Descrição:** {campaign.get('campaign_description', 'N/A')[:300]}...

"""
        
        # Adiciona padrões de engajamento
        if insights_data['engagement_patterns']:
            report += "\n## PADRÕES DE ENGAJAMENTO\n\n"
            
            for pattern in insights_data['engagement_patterns']:
                platform = pattern.get('platform', 'N/A')
                metrics = pattern.get('metrics', {})
                
                report += f"""### {platform.title()}

**Total de Itens:** {metrics.get('total_items', 0)}  
**Alto Engajamento:** {metrics.get('high_engagement', 0)} ({metrics.get('high_engagement_rate', 0):.1f}%)  
**Score Viral Médio:** {metrics.get('avg_viral_score', 0):.2f}/10  
**Taxa de Engajamento Média:** {metrics.get('avg_engagement_rate', 0):.2f}%

"""
        
        report += f"\n---\n\n*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*"
        
        return report

# Instância global
marketing_insights_extractor = MarketingInsightsExtractor()