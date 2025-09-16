#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced Search Coordinator
Coordenador aprimorado de busca com foco em dados valiosos para marketing
"""

import os
import logging
import asyncio
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Imports dos serviços de busca
from services.real_search_orchestrator import real_search_orchestrator
from services.marketing_insights_extractor import marketing_insights_extractor
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class EnhancedSearchCoordinator:
    """Coordenador aprimorado de busca com foco em marketing"""

    def __init__(self):
        """Inicializa o coordenador"""
        self.search_orchestrator = real_search_orchestrator
        self.insights_extractor = marketing_insights_extractor
        
        # Configurações para agências de marketing
        self.marketing_focused_queries = [
            'estratégias marketing digital',
            'campanhas alta conversão',
            'anúncios que converteram',
            'cases sucesso marketing',
            'ROI campanhas digitais',
            'funil vendas otimizado',
            'landing pages alta conversão',
            'copy que converte',
            'segmentação audiência',
            'automação marketing',
            'growth hacking',
            'viral marketing',
            'influencer marketing ROI',
            'email marketing conversão',
            'social media engagement'
        ]
        
        self.target_content_size = 300 * 1024  # 300KB mínimo
        
        logger.info("🎯 Enhanced Search Coordinator inicializado para marketing")

    async def execute_marketing_focused_search(
        self,
        base_query: str,
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Executa busca focada em insights de marketing"""
        
        logger.info(f"🎯 Iniciando busca focada em marketing para: {base_query}")
        start_time = time.time()
        
        search_results = {
            'base_query': base_query,
            'session_id': session_id,
            'search_started': datetime.now().isoformat(),
            'marketing_queries_executed': [],
            'total_content_size': 0,
            'web_results': [],
            'social_results': [],
            'youtube_results': [],
            'viral_content': [],
            'marketing_insights': {},
            'statistics': {
                'queries_executed': 0,
                'total_sources': 0,
                'content_size_kb': 0,
                'marketing_insights_found': 0,
                'high_value_insights': 0
            }
        }
        
        try:
            # FASE 1: Busca base com query principal
            logger.info("🔍 FASE 1: Executando busca base")
            
            base_results = await self.search_orchestrator.execute_massive_real_search(
                query=base_query,
                context=context,
                session_id=session_id
            )
            
            if base_results:
                search_results['web_results'].extend(base_results.get('web_results', []))
                search_results['social_results'].extend(base_results.get('social_results', []))
                search_results['youtube_results'].extend(base_results.get('youtube_results', []))
                search_results['viral_content'].extend(base_results.get('viral_content', []))
                
                # Calcula tamanho do conteúdo
                content_size = self._calculate_content_size(base_results)
                search_results['total_content_size'] += content_size
                
                logger.info(f"✅ Busca base: {content_size/1024:.1f}KB coletados")
            
            # FASE 2: Buscas complementares focadas em marketing
            logger.info("🎯 FASE 2: Buscas complementares focadas em marketing")
            
            # Gera queries específicas baseadas no contexto
            marketing_queries = self._generate_marketing_queries(base_query, context)
            
            # Executa buscas complementares até atingir 300KB
            for query in marketing_queries:
                if search_results['total_content_size'] >= self.target_content_size:
                    logger.info(f"✅ Meta de 300KB atingida: {search_results['total_content_size']/1024:.1f}KB")
                    break
                
                try:
                    logger.info(f"🔍 Busca complementar: {query}")
                    
                    complementary_results = await self.search_orchestrator.execute_massive_real_search(
                        query=query,
                        context=context,
                        session_id=session_id
                    )
                    
                    if complementary_results:
                        # Adiciona resultados únicos (evita duplicatas)
                        new_web = self._filter_unique_results(
                            complementary_results.get('web_results', []),
                            search_results['web_results']
                        )
                        new_social = self._filter_unique_results(
                            complementary_results.get('social_results', []),
                            search_results['social_results']
                        )
                        new_youtube = self._filter_unique_results(
                            complementary_results.get('youtube_results', []),
                            search_results['youtube_results']
                        )
                        
                        search_results['web_results'].extend(new_web)
                        search_results['social_results'].extend(new_social)
                        search_results['youtube_results'].extend(new_youtube)
                        
                        # Atualiza tamanho
                        additional_size = self._calculate_content_size(complementary_results)
                        search_results['total_content_size'] += additional_size
                        
                        search_results['marketing_queries_executed'].append({
                            'query': query,
                            'results_count': len(new_web) + len(new_social) + len(new_youtube),
                            'content_size': additional_size
                        })
                        
                        logger.info(f"✅ Query '{query}': +{additional_size/1024:.1f}KB")
                    
                    # Pequena pausa entre buscas
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"❌ Erro na busca complementar '{query}': {e}")
                    continue
            
            # FASE 3: Extração de insights de marketing
            logger.info("💎 FASE 3: Extraindo insights de marketing")
            
            marketing_insights = await self.insights_extractor.extract_marketing_insights(
                search_results, session_id
            )
            
            search_results['marketing_insights'] = marketing_insights
            
            # FASE 4: Finalização e estatísticas
            search_duration = time.time() - start_time
            all_results = (search_results['web_results'] + 
                          search_results['social_results'] + 
                          search_results['youtube_results'])
            
            search_results['statistics'].update({
                'queries_executed': len(search_results['marketing_queries_executed']) + 1,
                'total_sources': len(all_results),
                'content_size_kb': search_results['total_content_size'] / 1024,
                'marketing_insights_found': marketing_insights.get('statistics', {}).get('total_insights', 0),
                'high_value_insights': marketing_insights.get('statistics', {}).get('high_value_count', 0),
                'search_duration': search_duration,
                'target_achieved': search_results['total_content_size'] >= self.target_content_size
            })
            
            # Salva resultados
            salvar_etapa("enhanced_search_results", search_results, categoria="busca_marketing")
            
            logger.info(f"✅ Busca focada em marketing concluída:")
            logger.info(f"📊 {stats['total_sources']} fontes coletadas")
            logger.info(f"📝 {stats['content_size_kb']:.1f}KB de conteúdo")
            logger.info(f"💎 {stats['marketing_insights_found']} insights de marketing")
            logger.info(f"⏱️ Duração: {search_duration:.2f}s")
            
            return search_results
            
        except Exception as e:
            logger.error(f"❌ Erro na busca focada em marketing: {e}")
            salvar_erro("enhanced_search_error", e, contexto={'query': base_query, 'session_id': session_id})
            raise

    def _generate_marketing_queries(self, base_query: str, context: Dict[str, Any]) -> List[str]:
        """Gera queries específicas para marketing baseadas no contexto"""
        
        segmento = context.get('segmento', '')
        produto = context.get('produto', '')
        
        # Queries específicas do segmento
        specific_queries = []
        
        if segmento and produto:
            specific_queries.extend([
                f"{segmento} {produto} marketing estratégias",
                f"{segmento} {produto} campanhas sucesso",
                f"{segmento} {produto} conversão alta",
                f"{segmento} {produto} ROI marketing",
                f"{segmento} {produto} cases sucesso",
                f"como vender {produto} {segmento}",
                f"marketing {produto} {segmento} Brasil",
                f"anúncios {produto} {segmento} converteram",
                f"funil vendas {produto} {segmento}",
                f"copy {produto} {segmento} alta conversão"
            ])
        
        # Combina com queries gerais de marketing
        all_queries = specific_queries + self.marketing_focused_queries
        
        # Remove duplicatas e limita
        unique_queries = list(dict.fromkeys(all_queries))
        
        return unique_queries[:15]  # Máximo 15 queries complementares

    def _filter_unique_results(self, new_results: List[Dict[str, Any]], existing_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filtra resultados únicos para evitar duplicatas"""
        
        existing_urls = set(r.get('url', '') for r in existing_results)
        unique_results = []
        
        for result in new_results:
            url = result.get('url', '')
            if url and url not in existing_urls:
                unique_results.append(result)
                existing_urls.add(url)
        
        return unique_results

    def _calculate_content_size(self, results: Dict[str, Any]) -> int:
        """Calcula tamanho total do conteúdo em bytes"""
        
        total_size = 0
        
        # Calcula tamanho de todos os resultados
        all_results = []
        all_results.extend(results.get('web_results', []))
        all_results.extend(results.get('social_results', []))
        all_results.extend(results.get('youtube_results', []))
        
        for result in all_results:
            # Soma tamanho de todos os campos de texto
            for field in ['title', 'snippet', 'content', 'description', 'text']:
                if field in result and result[field]:
                    total_size += len(str(result[field]))
        
        return total_size

    async def ensure_minimum_content_size(
        self,
        search_results: Dict[str, Any],
        session_id: str,
        target_size: int = None
    ) -> Dict[str, Any]:
        """Garante que o conteúdo atinja o tamanho mínimo"""
        
        if target_size is None:
            target_size = self.target_content_size
        
        current_size = search_results.get('total_content_size', 0)
        
        if current_size >= target_size:
            logger.info(f"✅ Meta de tamanho já atingida: {current_size/1024:.1f}KB")
            return search_results
        
        logger.info(f"📈 Expandindo busca: {current_size/1024:.1f}KB / {target_size/1024:.1f}KB")
        
        # Gera queries adicionais mais específicas
        additional_queries = self._generate_expansion_queries(search_results)
        
        for query in additional_queries:
            if search_results['total_content_size'] >= target_size:
                break
            
            try:
                logger.info(f"🔍 Busca de expansão: {query}")
                
                expansion_results = await self.search_orchestrator.execute_massive_real_search(
                    query=query,
                    context={'expansion': True},
                    session_id=session_id
                )
                
                if expansion_results:
                    # Adiciona resultados únicos
                    new_content_size = self._add_unique_results(search_results, expansion_results)
                    search_results['total_content_size'] += new_content_size
                    
                    logger.info(f"✅ Expansão: +{new_content_size/1024:.1f}KB")
                
                await asyncio.sleep(0.5)  # Pausa entre buscas
                
            except Exception as e:
                logger.error(f"❌ Erro na busca de expansão: {e}")
                continue
        
        final_size = search_results['total_content_size']
        logger.info(f"📊 Tamanho final: {final_size/1024:.1f}KB")
        
        return search_results

    def _generate_expansion_queries(self, search_results: Dict[str, Any]) -> List[str]:
        """Gera queries de expansão baseadas nos resultados atuais"""
        
        base_query = search_results.get('base_query', '')
        
        # Queries de expansão focadas em marketing
        expansion_queries = [
            f"{base_query} marketing digital",
            f"{base_query} estratégias vendas",
            f"{base_query} campanhas sucesso",
            f"{base_query} conversão alta",
            f"{base_query} ROI marketing",
            f"{base_query} growth hacking",
            f"{base_query} funil vendas",
            f"{base_query} automação marketing",
            f"{base_query} social media",
            f"{base_query} influencer marketing",
            f"{base_query} email marketing",
            f"{base_query} content marketing",
            f"{base_query} paid ads",
            f"{base_query} organic growth",
            f"{base_query} viral marketing"
        ]
        
        return expansion_queries

    def _add_unique_results(self, search_results: Dict[str, Any], new_results: Dict[str, Any]) -> int:
        """Adiciona resultados únicos e retorna tamanho adicionado"""
        
        added_size = 0
        
        # Processa cada tipo de resultado
        result_types = ['web_results', 'social_results', 'youtube_results']
        
        for result_type in result_types:
            existing_results = search_results.get(result_type, [])
            new_items = new_results.get(result_type, [])
            
            unique_new_items = self._filter_unique_results(new_items, existing_results)
            
            if unique_new_items:
                search_results[result_type].extend(unique_new_items)
                
                # Calcula tamanho adicionado
                for item in unique_new_items:
                    for field in ['title', 'snippet', 'content', 'description', 'text']:
                        if field in item and item[field]:
                            added_size += len(str(item[field]))
        
        return added_size

    async def extract_competitor_intelligence(
        self,
        search_results: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Extrai inteligência competitiva dos resultados"""
        
        logger.info("🕵️ Extraindo inteligência competitiva")
        
        competitor_data = {
            'competitors_identified': [],
            'strategies_found': [],
            'pricing_intelligence': [],
            'campaign_analysis': [],
            'market_positioning': []
        }
        
        try:
            all_content = []
            all_content.extend(search_results.get('web_results', []))
            all_content.extend(search_results.get('social_results', []))
            all_content.extend(search_results.get('youtube_results', []))
            
            # Processa cada item buscando inteligência competitiva
            for item in all_content:
                content_text = self._get_item_text(item)
                
                # Identifica menções de concorrentes
                competitors = self._identify_competitors(content_text, item)
                if competitors:
                    competitor_data['competitors_identified'].extend(competitors)
                
                # Extrai estratégias mencionadas
                strategies = self._extract_strategies(content_text, item)
                if strategies:
                    competitor_data['strategies_found'].extend(strategies)
                
                # Identifica dados de preços
                pricing = self._extract_pricing_data(content_text, item)
                if pricing:
                    competitor_data['pricing_intelligence'].extend(pricing)
                
                # Analisa campanhas mencionadas
                campaigns = self._analyze_mentioned_campaigns(content_text, item)
                if campaigns:
                    competitor_data['campaign_analysis'].extend(campaigns)
            
            # Salva inteligência competitiva
            salvar_etapa("competitor_intelligence", competitor_data, categoria="inteligencia_competitiva")
            
            logger.info(f"✅ Inteligência competitiva extraída:")
            logger.info(f"🏢 {len(competitor_data['competitors_identified'])} concorrentes identificados")
            logger.info(f"🎯 {len(competitor_data['strategies_found'])} estratégias encontradas")
            logger.info(f"💰 {len(competitor_data['pricing_intelligence'])} dados de preço")
            
            return competitor_data
            
        except Exception as e:
            logger.error(f"❌ Erro na extração de inteligência competitiva: {e}")
            return competitor_data

    def _get_item_text(self, item: Dict[str, Any]) -> str:
        """Extrai texto do item"""
        text_fields = ['content', 'description', 'snippet', 'text', 'caption', 'title']
        
        combined_text = ""
        for field in text_fields:
            if field in item and item[field]:
                combined_text += str(item[field]) + " "
        
        return combined_text.strip()

    def _identify_competitors(self, text: str, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica menções de concorrentes"""
        
        competitor_patterns = [
            r'empresa.*?líder.*?mercado',
            r'principal.*?concorrente',
            r'maior.*?player.*?setor',
            r'referência.*?mercado',
            r'benchmark.*?indústria'
        ]
        
        competitors = []
        
        for pattern in competitor_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                competitors.append({
                    'mention': match.group(0),
                    'context': text[max(0, match.start()-100):match.end()+100],
                    'source_url': item.get('url', ''),
                    'platform': item.get('platform', 'web'),
                    'confidence_score': 0.8
                })
        
        return competitors

    def _extract_strategies(self, text: str, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai estratégias mencionadas"""
        
        strategy_patterns = [
            r'estratégia.*?sucesso',
            r'método.*?funcionou',
            r'técnica.*?aumentou',
            r'abordagem.*?resultados',
            r'tática.*?conversão',
            r'framework.*?crescimento'
        ]
        
        strategies = []
        
        for pattern in strategy_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                strategies.append({
                    'strategy': match.group(0),
                    'description': text[max(0, match.start()-150):match.end()+150],
                    'source_url': item.get('url', ''),
                    'platform': item.get('platform', 'web'),
                    'value_score': 7
                })
        
        return strategies

    def _extract_pricing_data(self, text: str, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai dados de precificação"""
        
        pricing_patterns = [
            r'preço.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'valor.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'custa.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'investimento.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)',
            r'ticket.*?médio.*?R\$.*?(\d+(?:\.\d+)?(?:k|mil)?)'
        ]
        
        pricing_data = []
        
        for pattern in pricing_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                pricing_data.append({
                    'pricing_mention': match.group(0),
                    'value': match.group(1),
                    'context': text[max(0, match.start()-100):match.end()+100],
                    'source_url': item.get('url', ''),
                    'platform': item.get('platform', 'web'),
                    'value_score': 9  # Dados de preço são muito valiosos
                })
        
        return pricing_data

    def _analyze_mentioned_campaigns(self, text: str, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analisa campanhas mencionadas"""
        
        campaign_patterns = [
            r'campanha.*?(Facebook|Instagram|Google|YouTube)',
            r'anúncio.*?(Facebook|Instagram|Google|YouTube)',
            r'ad.*?(Facebook|Instagram|Google|YouTube)',
            r'publicidade.*?(Facebook|Instagram|Google|YouTube)',
            r'marketing.*?(Facebook|Instagram|Google|YouTube)'
        ]
        
        campaigns = []
        
        for pattern in campaign_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                campaigns.append({
                    'campaign_mention': match.group(0),
                    'platform': match.group(1).lower(),
                    'description': text[max(0, match.start()-200):match.end()+200],
                    'source_url': item.get('url', ''),
                    'value_score': 8
                })
        
        return campaigns

    def get_search_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do coordenador de busca"""
        
        return {
            'coordinator_status': 'active',
            'target_content_size_kb': self.target_content_size / 1024,
            'marketing_queries_available': len(self.marketing_focused_queries),
            'timestamp': datetime.now().isoformat()
        }

# Instância global
enhanced_search_coordinator = EnhancedSearchCoordinator()