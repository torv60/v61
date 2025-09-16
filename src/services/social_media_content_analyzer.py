#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Social Media Content Analyzer
Analisador especializado de conteúdo de redes sociais para insights de marketing
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

class SocialMediaContentAnalyzer:
    """Analisador especializado de conteúdo de redes sociais"""

    def __init__(self):
        """Inicializa o analisador"""
        self.engagement_thresholds = {
            'youtube': {
                'viral_views': 100000,
                'high_engagement_rate': 5.0,
                'comment_engagement': 2.0
            },
            'instagram': {
                'viral_likes': 10000,
                'high_engagement_rate': 3.0,
                'comment_rate': 5.0
            },
            'facebook': {
                'viral_likes': 5000,
                'high_engagement_rate': 2.0,
                'share_rate': 1.0
            },
            'twitter': {
                'viral_retweets': 1000,
                'high_engagement_rate': 2.0,
                'reply_rate': 5.0
            },
            'tiktok': {
                'viral_views': 500000,
                'high_engagement_rate': 8.0,
                'share_rate': 3.0
            }
        }
        
        self.marketing_indicators = [
            'link na bio', 'swipe up', 'call to action', 'CTA',
            'compre agora', 'saiba mais', 'acesse o link',
            'promoção', 'desconto', 'oferta especial',
            'lançamento', 'novidade', 'exclusivo',
            'garanta já', 'últimas vagas', 'por tempo limitado'
        ]
        
        logger.info("📱 Social Media Content Analyzer inicializado")

    async def analyze_social_content(
        self,
        social_results: List[Dict[str, Any]],
        session_id: str
    ) -> Dict[str, Any]:
        """Analisa conteúdo de redes sociais para insights de marketing"""
        
        logger.info(f"📱 Analisando {len(social_results)} itens de redes sociais")
        
        analysis_results = {
            'session_id': session_id,
            'analysis_started': datetime.now().isoformat(),
            'platform_analysis': {},
            'viral_content_breakdown': [],
            'engagement_insights': [],
            'marketing_tactics_found': [],
            'content_themes': [],
            'hashtag_analysis': [],
            'influencer_insights': [],
            'ad_content_identified': [],
            'conversion_triggers': [],
            'audience_behavior': [],
            'statistics': {
                'total_analyzed': len(social_results),
                'viral_content': 0,
                'marketing_content': 0,
                'ad_content': 0,
                'high_engagement': 0
            }
        }
        
        try:
            # Agrupa por plataforma
            platform_groups = self._group_by_platform(social_results)
            
            # Analisa cada plataforma
            for platform, items in platform_groups.items():
                logger.info(f"📊 Analisando {platform}: {len(items)} itens")
                
                platform_analysis = await self._analyze_platform_content(platform, items)
                analysis_results['platform_analysis'][platform] = platform_analysis
                
                # Agrega resultados
                analysis_results['viral_content_breakdown'].extend(platform_analysis.get('viral_content', []))
                analysis_results['engagement_insights'].extend(platform_analysis.get('engagement_insights', []))
                analysis_results['marketing_tactics_found'].extend(platform_analysis.get('marketing_tactics', []))
                analysis_results['ad_content_identified'].extend(platform_analysis.get('ad_content', []))
            
            # Análise cross-platform
            cross_platform_insights = self._analyze_cross_platform_patterns(platform_groups)
            analysis_results['cross_platform_insights'] = cross_platform_insights
            
            # Extrai hashtags e tendências
            hashtag_analysis = self._analyze_hashtags(social_results)
            analysis_results['hashtag_analysis'] = hashtag_analysis
            
            # Identifica influenciadores
            influencer_insights = self._identify_influencers(social_results)
            analysis_results['influencer_insights'] = influencer_insights
            
            # Analisa gatilhos de conversão
            conversion_triggers = self._extract_conversion_triggers(social_results)
            analysis_results['conversion_triggers'] = conversion_triggers
            
            # Calcula estatísticas finais
            analysis_results['statistics'] = self._calculate_final_statistics(analysis_results)
            
            # Salva análise
            await self._save_social_analysis(analysis_results, session_id)
            
            logger.info(f"✅ Análise de redes sociais concluída:")
            logger.info(f"🔥 {analysis_results['statistics']['viral_content']} conteúdos virais")
            logger.info(f"📈 {analysis_results['statistics']['marketing_content']} conteúdos de marketing")
            logger.info(f"💰 {analysis_results['statistics']['ad_content']} anúncios identificados")
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"❌ Erro na análise de redes sociais: {e}")
            raise

    def _group_by_platform(self, social_results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Agrupa resultados por plataforma"""
        
        platform_groups = {}
        
        for item in social_results:
            platform = item.get('platform', 'unknown')
            
            if platform not in platform_groups:
                platform_groups[platform] = []
            
            platform_groups[platform].append(item)
        
        return platform_groups

    async def _analyze_platform_content(self, platform: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisa conteúdo específico de uma plataforma"""
        
        platform_analysis = {
            'platform': platform,
            'total_items': len(items),
            'viral_content': [],
            'engagement_insights': [],
            'marketing_tactics': [],
            'ad_content': [],
            'content_themes': [],
            'performance_metrics': {}
        }
        
        try:
            thresholds = self.engagement_thresholds.get(platform, {})
            
            for item in items:
                # Analisa viralidade
                viral_analysis = self._analyze_item_virality(item, platform, thresholds)
                if viral_analysis:
                    platform_analysis['viral_content'].append(viral_analysis)
                
                # Identifica táticas de marketing
                marketing_tactics = self._identify_marketing_tactics(item)
                if marketing_tactics:
                    platform_analysis['marketing_tactics'].extend(marketing_tactics)
                
                # Identifica conteúdo publicitário
                ad_content = self._identify_ad_content(item)
                if ad_content:
                    platform_analysis['ad_content'].append(ad_content)
                
                # Extrai insights de engajamento
                engagement_insight = self._extract_engagement_insight(item, platform)
                if engagement_insight:
                    platform_analysis['engagement_insights'].append(engagement_insight)
            
            # Calcula métricas de performance da plataforma
            platform_analysis['performance_metrics'] = self._calculate_platform_metrics(items, platform)
            
            return platform_analysis
            
        except Exception as e:
            logger.error(f"❌ Erro na análise da plataforma {platform}: {e}")
            return platform_analysis

    def _analyze_item_virality(self, item: Dict[str, Any], platform: str, thresholds: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analisa viralidade de um item específico"""
        
        try:
            viral_score = item.get('viral_score', 0)
            
            if viral_score >= 7.0:  # Threshold para conteúdo viral
                viral_factors = []
                
                # Analisa fatores específicos por plataforma
                if platform == 'youtube':
                    views = item.get('view_count', 0)
                    likes = item.get('like_count', 0)
                    comments = item.get('comment_count', 0)
                    
                    if views >= thresholds.get('viral_views', 100000):
                        viral_factors.append(f"Views virais: {views:,}")
                    
                    if views > 0 and likes > 0:
                        like_rate = (likes / views) * 100
                        if like_rate >= thresholds.get('high_engagement_rate', 5.0):
                            viral_factors.append(f"Alta taxa de likes: {like_rate:.2f}%")
                    
                    if views > 0 and comments > 0:
                        comment_rate = (comments / views) * 100
                        if comment_rate >= thresholds.get('comment_engagement', 2.0):
                            viral_factors.append(f"Alto engajamento comentários: {comment_rate:.2f}%")
                
                elif platform in ['instagram', 'facebook']:
                    likes = item.get('likes', 0)
                    comments = item.get('comments', 0)
                    shares = item.get('shares', 0)
                    
                    if likes >= thresholds.get('viral_likes', 10000):
                        viral_factors.append(f"Likes virais: {likes:,}")
                    
                    if likes > 0 and comments > 0:
                        comment_rate = (comments / likes) * 100
                        if comment_rate >= thresholds.get('comment_rate', 5.0):
                            viral_factors.append(f"Alta taxa comentários: {comment_rate:.2f}%")
                
                return {
                    'item_data': item,
                    'viral_score': viral_score,
                    'viral_factors': viral_factors,
                    'platform': platform,
                    'analysis_type': 'viral_content',
                    'value_score': viral_score
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise de viralidade: {e}")
            return None

    def _identify_marketing_tactics(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica táticas de marketing no conteúdo"""
        
        content_text = self._get_item_text(item)
        tactics_found = []
        
        for indicator in self.marketing_indicators:
            if indicator.lower() in content_text.lower():
                tactics_found.append({
                    'tactic': indicator,
                    'context': self._extract_context_around_phrase(content_text, indicator),
                    'platform': item.get('platform', 'unknown'),
                    'source_url': item.get('url', ''),
                    'value_score': 7
                })
        
        return tactics_found

    def _identify_ad_content(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Identifica conteúdo publicitário"""
        
        content_text = self._get_item_text(item)
        
        ad_indicators = [
            'patrocinado', 'sponsored', 'publicidade', 'anúncio',
            'promoção', 'oferta', 'desconto', 'compre agora',
            'saiba mais', 'acesse', 'clique aqui', 'link na bio'
        ]
        
        ad_score = 0
        found_indicators = []
        
        for indicator in ad_indicators:
            if indicator.lower() in content_text.lower():
                ad_score += 1
                found_indicators.append(indicator)
        
        if ad_score >= 2:  # Threshold para identificar como anúncio
            return {
                'ad_indicators': found_indicators,
                'ad_score': ad_score,
                'content_analysis': content_text[:400],
                'platform': item.get('platform', 'unknown'),
                'source_url': item.get('url', ''),
                'value_score': 8,  # Anúncios são valiosos para análise
                'analysis_type': 'ad_content'
            }
        
        return None

    def _extract_engagement_insight(self, item: Dict[str, Any], platform: str) -> Optional[Dict[str, Any]]:
        """Extrai insight de engajamento específico"""
        
        try:
            engagement_data = {}
            
            if platform == 'youtube':
                views = item.get('view_count', 0)
                likes = item.get('like_count', 0)
                comments = item.get('comment_count', 0)
                
                if views > 0:
                    engagement_data = {
                        'views': views,
                        'likes': likes,
                        'comments': comments,
                        'like_rate': (likes / views) * 100,
                        'comment_rate': (comments / views) * 100,
                        'engagement_rate': ((likes + comments) / views) * 100
                    }
            
            elif platform in ['instagram', 'facebook']:
                likes = item.get('likes', 0)
                comments = item.get('comments', 0)
                shares = item.get('shares', 0)
                
                if likes > 0:
                    engagement_data = {
                        'likes': likes,
                        'comments': comments,
                        'shares': shares,
                        'comment_rate': (comments / likes) * 100,
                        'share_rate': (shares / likes) * 100 if likes > 0 else 0,
                        'total_engagement': likes + comments + shares
                    }
            
            elif platform == 'twitter':
                likes = item.get('likes', 0)
                retweets = item.get('retweets', 0)
                replies = item.get('replies', 0)
                
                if likes > 0:
                    engagement_data = {
                        'likes': likes,
                        'retweets': retweets,
                        'replies': replies,
                        'retweet_rate': (retweets / likes) * 100,
                        'reply_rate': (replies / likes) * 100,
                        'total_engagement': likes + retweets + replies
                    }
            
            if engagement_data:
                # Calcula score de valor baseado no engajamento
                total_engagement = engagement_data.get('total_engagement', 0)
                engagement_rate = engagement_data.get('engagement_rate', 0)
                
                value_score = min(10, (total_engagement / 1000) + (engagement_rate / 2))
                
                return {
                    'platform': platform,
                    'engagement_metrics': engagement_data,
                    'content_title': item.get('title', ''),
                    'source_url': item.get('url', ''),
                    'value_score': value_score,
                    'analysis_type': 'engagement_insight'
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na extração de insight de engajamento: {e}")
            return None

    def _analyze_hashtags(self, social_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analisa hashtags para identificar tendências"""
        
        hashtag_data = {}
        
        for item in social_results:
            content_text = self._get_item_text(item)
            platform = item.get('platform', 'unknown')
            
            # Extrai hashtags
            hashtags = re.findall(r'#\w+', content_text)
            
            for hashtag in hashtags:
                hashtag_lower = hashtag.lower()
                
                if hashtag_lower not in hashtag_data:
                    hashtag_data[hashtag_lower] = {
                        'hashtag': hashtag,
                        'count': 0,
                        'platforms': set(),
                        'total_engagement': 0,
                        'examples': []
                    }
                
                data = hashtag_data[hashtag_lower]
                data['count'] += 1
                data['platforms'].add(platform)
                data['total_engagement'] += item.get('viral_score', 0)
                
                if len(data['examples']) < 3:
                    data['examples'].append({
                        'content': content_text[:200],
                        'platform': platform,
                        'url': item.get('url', '')
                    })
        
        # Converte para lista e ordena por relevância
        hashtag_analysis = []
        
        for hashtag_lower, data in hashtag_data.items():
            if data['count'] >= 2:  # Hashtags que aparecem pelo menos 2 vezes
                avg_engagement = data['total_engagement'] / data['count']
                
                hashtag_analysis.append({
                    'hashtag': data['hashtag'],
                    'frequency': data['count'],
                    'platforms': list(data['platforms']),
                    'avg_engagement': avg_engagement,
                    'examples': data['examples'],
                    'value_score': min(10, data['count'] + avg_engagement),
                    'analysis_type': 'hashtag_trend'
                })
        
        # Ordena por valor
        hashtag_analysis.sort(key=lambda x: x['value_score'], reverse=True)
        
        return hashtag_analysis[:20]  # Top 20 hashtags

    def _identify_influencers(self, social_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica influenciadores e criadores de conteúdo"""
        
        influencers = []
        
        for item in social_results:
            # Critérios para identificar influenciadores
            viral_score = item.get('viral_score', 0)
            platform = item.get('platform', 'unknown')
            
            # YouTube: canal com muitas views
            if platform == 'youtube':
                views = item.get('view_count', 0)
                channel = item.get('channel', '')
                
                if views >= 50000 and channel:  # Threshold para influenciador
                    influencers.append({
                        'name': channel,
                        'platform': platform,
                        'content_title': item.get('title', ''),
                        'metrics': {
                            'views': views,
                            'likes': item.get('like_count', 0),
                            'comments': item.get('comment_count', 0)
                        },
                        'viral_score': viral_score,
                        'source_url': item.get('url', ''),
                        'value_score': min(10, viral_score),
                        'analysis_type': 'influencer_content'
                    })
            
            # Instagram/Facebook: posts com alto engajamento
            elif platform in ['instagram', 'facebook']:
                likes = item.get('likes', 0)
                author = item.get('author', '')
                
                if likes >= 5000 and author:  # Threshold para influenciador
                    influencers.append({
                        'name': author,
                        'platform': platform,
                        'content_title': item.get('title', ''),
                        'metrics': {
                            'likes': likes,
                            'comments': item.get('comments', 0),
                            'shares': item.get('shares', 0)
                        },
                        'viral_score': viral_score,
                        'source_url': item.get('url', ''),
                        'value_score': min(10, viral_score),
                        'analysis_type': 'influencer_content'
                    })
        
        # Remove duplicatas por nome
        unique_influencers = []
        seen_names = set()
        
        for influencer in influencers:
            name = influencer['name'].lower()
            if name not in seen_names:
                seen_names.add(name)
                unique_influencers.append(influencer)
        
        return unique_influencers

    def _extract_conversion_triggers(self, social_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrai gatilhos de conversão do conteúdo social"""
        
        conversion_triggers = []
        
        trigger_patterns = [
            r'link.*?bio',
            r'swipe.*?up',
            r'stories.*?destaque',
            r'dm.*?info',
            r'whatsapp.*?link',
            r'compre.*?agora',
            r'acesse.*?link',
            r'saiba.*?mais',
            r'garanta.*?já',
            r'últimas.*?vagas',
            r'promoção.*?especial',
            r'desconto.*?exclusivo'
        ]
        
        for item in social_results:
            content_text = self._get_item_text(item)
            
            triggers_found = []
            
            for pattern in trigger_patterns:
                matches = re.finditer(pattern, content_text, re.IGNORECASE)
                for match in matches:
                    triggers_found.append({
                        'trigger': match.group(0),
                        'context': content_text[max(0, match.start()-50):match.end()+50],
                        'trigger_type': self._classify_trigger_type(match.group(0))
                    })
            
            if triggers_found:
                conversion_triggers.append({
                    'content_source': item,
                    'triggers_identified': triggers_found,
                    'trigger_count': len(triggers_found),
                    'platform': item.get('platform', 'unknown'),
                    'viral_score': item.get('viral_score', 0),
                    'value_score': min(10, len(triggers_found) * 2),
                    'analysis_type': 'conversion_triggers'
                })
        
        return conversion_triggers

    def _classify_trigger_type(self, trigger_text: str) -> str:
        """Classifica o tipo de gatilho de conversão"""
        
        text_lower = trigger_text.lower()
        
        if any(word in text_lower for word in ['link', 'bio', 'swipe', 'acesse']):
            return 'traffic_driver'
        elif any(word in text_lower for word in ['compre', 'garanta', 'últimas']):
            return 'urgency_trigger'
        elif any(word in text_lower for word in ['promoção', 'desconto', 'especial']):
            return 'offer_trigger'
        elif any(word in text_lower for word in ['dm', 'whatsapp', 'contato']):
            return 'contact_trigger'
        else:
            return 'general_cta'

    def _analyze_cross_platform_patterns(self, platform_groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Analisa padrões cross-platform"""
        
        cross_patterns = {
            'content_themes': {},
            'engagement_comparison': {},
            'viral_content_distribution': {},
            'marketing_tactics_by_platform': {}
        }
        
        # Analisa temas de conteúdo
        all_content_texts = []
        for platform, items in platform_groups.items():
            for item in items:
                content_text = self._get_item_text(item)
                all_content_texts.append({
                    'text': content_text,
                    'platform': platform,
                    'viral_score': item.get('viral_score', 0)
                })
        
        # Identifica temas comuns
        theme_keywords = [
            'dicas', 'tutorial', 'como fazer', 'passo a passo',
            'estratégia', 'segredo', 'truque', 'hack',
            'resultado', 'transformação', 'antes e depois',
            'case', 'história', 'experiência', 'depoimento'
        ]
        
        for keyword in theme_keywords:
            count = sum(1 for content in all_content_texts if keyword.lower() in content['text'].lower())
            if count >= 2:
                cross_patterns['content_themes'][keyword] = {
                    'frequency': count,
                    'avg_viral_score': sum(c['viral_score'] for c in all_content_texts if keyword.lower() in c['text'].lower()) / count
                }
        
        return cross_patterns

    def _calculate_platform_metrics(self, items: List[Dict[str, Any]], platform: str) -> Dict[str, Any]:
        """Calcula métricas de performance da plataforma"""
        
        if not items:
            return {}
        
        metrics = {
            'total_content': len(items),
            'avg_viral_score': 0,
            'high_performance_content': 0,
            'total_engagement': 0
        }
        
        total_viral_score = 0
        total_engagement = 0
        
        for item in items:
            viral_score = item.get('viral_score', 0)
            total_viral_score += viral_score
            
            if viral_score >= 7.0:
                metrics['high_performance_content'] += 1
            
            # Calcula engajamento total por plataforma
            if platform == 'youtube':
                engagement = item.get('like_count', 0) + item.get('comment_count', 0)
            elif platform in ['instagram', 'facebook']:
                engagement = item.get('likes', 0) + item.get('comments', 0) + item.get('shares', 0)
            elif platform == 'twitter':
                engagement = item.get('likes', 0) + item.get('retweets', 0) + item.get('replies', 0)
            else:
                engagement = 0
            
            total_engagement += engagement
        
        metrics['avg_viral_score'] = total_viral_score / len(items)
        metrics['total_engagement'] = total_engagement
        metrics['high_performance_rate'] = (metrics['high_performance_content'] / len(items)) * 100
        
        return metrics

    def _calculate_final_statistics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula estatísticas finais da análise"""
        
        stats = {
            'total_analyzed': analysis_results['statistics']['total_analyzed'],
            'viral_content': len(analysis_results['viral_content_breakdown']),
            'marketing_content': len(analysis_results['marketing_tactics_found']),
            'ad_content': len(analysis_results['ad_content_identified']),
            'high_engagement': len([i for i in analysis_results['engagement_insights'] if i.get('value_score', 0) >= 7]),
            'platforms_analyzed': len(analysis_results['platform_analysis']),
            'hashtags_trending': len(analysis_results['hashtag_analysis']),
            'influencers_identified': len(analysis_results['influencer_insights']),
            'conversion_triggers': len(analysis_results['conversion_triggers']),
            'analysis_duration': (datetime.now() - datetime.fromisoformat(analysis_results['analysis_started'])).total_seconds()
        }
        
        return stats

    def _extract_context_around_phrase(self, text: str, phrase: str) -> str:
        """Extrai contexto ao redor de uma frase"""
        
        try:
            phrase_index = text.lower().find(phrase.lower())
            if phrase_index == -1:
                return ""
            
            start = max(0, phrase_index - 100)
            end = min(len(text), phrase_index + len(phrase) + 100)
            
            return text[start:end]
            
        except Exception:
            return ""

    def _get_item_text(self, item: Dict[str, Any]) -> str:
        """Extrai texto do item"""
        text_fields = ['content', 'description', 'snippet', 'text', 'caption', 'title']
        
        combined_text = ""
        for field in text_fields:
            if field in item and item[field]:
                combined_text += str(item[field]) + " "
        
        return combined_text.strip()

    async def _save_social_analysis(self, analysis_results: Dict[str, Any], session_id: str):
        """Salva análise de redes sociais"""
        
        try:
            session_dir = Path(f"analyses_data/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Salva análise completa
            analysis_path = session_dir / "social_media_analysis.json"
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, ensure_ascii=False, indent=2, default=str)
            
            # Gera relatório
            report = self._generate_social_report(analysis_results)
            report_path = session_dir / "social_media_report.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"💾 Análise de redes sociais salva: {analysis_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar análise social: {e}")

    def _generate_social_report(self, analysis_results: Dict[str, Any]) -> str:
        """Gera relatório da análise de redes sociais"""
        
        stats = analysis_results['statistics']
        
        report = f"""# ANÁLISE DE REDES SOCIAIS - ARQV30 Enhanced v3.0

**Sessão:** {analysis_results['session_id']}  
**Análise realizada em:** {analysis_results['analysis_started']}  
**Conteúdo Analisado:** {stats['total_analyzed']} itens  
**Plataformas:** {stats['platforms_analyzed']}

---

## RESUMO EXECUTIVO

### Conteúdo Identificado:
- 🔥 **{stats['viral_content']}** conteúdos virais
- 📈 **{stats['marketing_content']}** conteúdos de marketing
- 💰 **{stats['ad_content']}** anúncios identificados
- ⚡ **{stats['high_engagement']}** conteúdos de alto engajamento
- 🏷️ **{stats['hashtags_trending']}** hashtags em tendência
- 👑 **{stats['influencers_identified']}** influenciadores identificados
- 🎯 **{stats['conversion_triggers']}** gatilhos de conversão

---

## ANÁLISE POR PLATAFORMA

"""
        
        # Adiciona análise por plataforma
        for platform, analysis in analysis_results['platform_analysis'].items():
            metrics = analysis.get('performance_metrics', {})
            
            report += f"""### {platform.title()}

**Total de Conteúdo:** {analysis['total_items']}  
**Conteúdo Viral:** {len(analysis['viral_content'])}  
**Score Viral Médio:** {metrics.get('avg_viral_score', 0):.2f}/10  
**Taxa de Alto Performance:** {metrics.get('high_performance_rate', 0):.1f}%  
**Engajamento Total:** {metrics.get('total_engagement', 0):,}

"""
        
        # Adiciona top hashtags
        if analysis_results['hashtag_analysis']:
            report += "\n## TOP HASHTAGS IDENTIFICADAS\n\n"
            
            for i, hashtag in enumerate(analysis_results['hashtag_analysis'][:10], 1):
                report += f"""### {i}. {hashtag['hashtag']}

**Frequência:** {hashtag['frequency']} menções  
**Plataformas:** {', '.join(hashtag['platforms'])}  
**Engajamento Médio:** {hashtag['avg_engagement']:.2f}/10  
**Score de Valor:** {hashtag['value_score']:.1f}/10

"""
        
        # Adiciona influenciadores
        if analysis_results['influencer_insights']:
            report += "\n## INFLUENCIADORES IDENTIFICADOS\n\n"
            
            for i, influencer in enumerate(analysis_results['influencer_insights'][:10], 1):
                metrics = influencer.get('metrics', {})
                
                report += f"""### {i}. {influencer['name']}

**Plataforma:** {influencer['platform'].title()}  
**Conteúdo:** {influencer['content_title'][:100]}...  
**Score Viral:** {influencer['viral_score']:.2f}/10  
**URL:** {influencer['source_url']}

**Métricas:**
"""
                
                for metric, value in metrics.items():
                    report += f"- {metric.title()}: {value:,}\n"
                
                report += "\n"
        
        report += f"\n---\n\n*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*"
        
        return report

# Instância global
enhanced_search_coordinator = EnhancedSearchCoordinator()