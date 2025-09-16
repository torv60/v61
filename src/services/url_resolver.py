#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - URL Resolver
Resolvedor de URLs com redirecionamentos e validação
"""

import logging
import requests
from typing import Optional
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)

class URLResolver:
    """Resolvedor de URLs com suporte a redirecionamentos"""

    def __init__(self):
        """Inicializa o resolvedor"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 15
        self.max_redirects = 10
        
        logger.info("🔗 URL Resolver inicializado")

    def resolve_redirect_url(self, url: str) -> str:
        """Resolve redirecionamentos de URL"""
        
        if not url or not url.startswith(('http://', 'https://')):
            return url
        
        try:
            # Faz HEAD request para seguir redirecionamentos
            response = self.session.head(
                url,
                allow_redirects=True,
                timeout=self.timeout,
                verify=False  # Para evitar problemas de SSL
            )
            
            final_url = response.url
            
            if final_url != url:
                logger.debug(f"🔄 URL resolvida: {url} -> {final_url}")
            
            return final_url
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Erro ao resolver URL {url}: {e}")
            return url
        except Exception as e:
            logger.warning(f"⚠️ Erro inesperado ao resolver URL {url}: {e}")
            return url

    def validate_url(self, url: str) -> bool:
        """Valida se uma URL é acessível"""
        
        if not url or not url.startswith(('http://', 'https://')):
            return False
        
        try:
            response = self.session.head(
                url,
                allow_redirects=True,
                timeout=self.timeout,
                verify=False
            )
            
            return response.status_code < 400
            
        except Exception as e:
            logger.warning(f"⚠️ URL inválida {url}: {e}")
            return False

    def normalize_url(self, url: str, base_url: str = None) -> str:
        """Normaliza URL (resolve URLs relativas)"""
        
        if not url:
            return ""
        
        # Se já é URL absoluta, retorna como está
        if url.startswith(('http://', 'https://')):
            return url
        
        # Se tem base_url, resolve URL relativa
        if base_url:
            try:
                return urljoin(base_url, url)
            except Exception as e:
                logger.warning(f"⚠️ Erro ao normalizar URL {url} com base {base_url}: {e}")
                return url
        
        return url

    def extract_domain(self, url: str) -> str:
        """Extrai domínio de uma URL"""
        
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except Exception as e:
            logger.warning(f"⚠️ Erro ao extrair domínio de {url}: {e}")
            return ""

    def is_social_media_url(self, url: str) -> bool:
        """Verifica se URL é de rede social"""
        
        social_domains = [
            'youtube.com', 'youtu.be',
            'instagram.com',
            'facebook.com', 'fb.com',
            'twitter.com', 'x.com',
            'tiktok.com',
            'linkedin.com',
            'pinterest.com',
            'snapchat.com'
        ]
        
        domain = self.extract_domain(url)
        return any(social_domain in domain for social_domain in social_domains)

    def is_news_url(self, url: str) -> bool:
        """Verifica se URL é de site de notícias"""
        
        news_domains = [
            'g1.globo.com', 'globo.com',
            'exame.com', 'valor.globo.com',
            'estadao.com.br', 'folha.uol.com.br',
            'infomoney.com.br', 'canaltech.com.br',
            'tecmundo.com.br', 'olhardigital.com.br',
            'uol.com.br', 'r7.com',
            'band.uol.com.br', 'sbt.com.br'
        ]
        
        domain = self.extract_domain(url)
        return any(news_domain in domain for news_domain in news_domains)

    def classify_url_type(self, url: str) -> str:
        """Classifica o tipo de URL"""
        
        if self.is_social_media_url(url):
            return 'social_media'
        elif self.is_news_url(url):
            return 'news'
        elif '.pdf' in url.lower():
            return 'pdf'
        elif any(ext in url.lower() for ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']):
            return 'document'
        elif any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            return 'image'
        elif any(ext in url.lower() for ext in ['.mp4', '.avi', '.mov', '.wmv']):
            return 'video'
        else:
            return 'web_page'

    def get_url_info(self, url: str) -> Dict[str, Any]:
        """Obtém informações completas sobre uma URL"""
        
        return {
            'original_url': url,
            'resolved_url': self.resolve_redirect_url(url),
            'domain': self.extract_domain(url),
            'url_type': self.classify_url_type(url),
            'is_valid': self.validate_url(url),
            'is_social_media': self.is_social_media_url(url),
            'is_news': self.is_news_url(url)
        }

# Instância global
url_resolver = URLResolver()