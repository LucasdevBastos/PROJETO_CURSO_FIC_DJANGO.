/**
 * Auto Translator - Sistema de Tradução Automática EN -> PT-BR
 * 
 * Este script detecta e traduz automaticamente textos em inglês
 * para português brasileiro em toda a página.
 * 
 * Funcionalidades:
 * - Tradução automática ao carregar a página
 * - Cache local para melhor performance
 * - Tradução em lote para otimização
 * - Ignora elementos essenciais (IDs, classes, scripts, etc.)
 */

class AutoTranslator {
    constructor() {
        this.apiUrl = '/core/api/translate/';
        this.cache = new Map();
        this.loadCache();
        this.batchSize = 50; // Traduz 50 textos por vez
        this.processingQueue = [];
        this.isProcessing = false;
        
        // Seletores de elementos a ignorar
        this.ignoredSelectors = [
            'script',
            'style',
            'code',
            'pre',
            '[translate="no"]',
            '[data-no-translate]',
            '.no-translate'
        ];
        
        // Atributos que não devem ser traduzidos
        this.ignoredAttributes = [
            'id',
            'class',
            'href',
            'src',
            'data-',
            'aria-',
            'role',
            'type',
            'name',
            'value'
        ];
    }

    /**
     * Carrega cache do localStorage
     */
    loadCache() {
        try {
            const cached = localStorage.getItem('translation_cache');
            if (cached) {
                const data = JSON.parse(cached);
                this.cache = new Map(Object.entries(data));
            }
        } catch (e) {
            console.warn('Erro ao carregar cache de traduções:', e);
        }
    }

    /**
     * Salva cache no localStorage
     */
    saveCache() {
        try {
            const data = Object.fromEntries(this.cache);
            localStorage.setItem('translation_cache', JSON.stringify(data));
        } catch (e) {
            console.warn('Erro ao salvar cache de traduções:', e);
        }
    }

    /**
     * Verifica se um texto está em inglês
     */
    isEnglish(text) {
        if (!text || text.trim().length < 3) return false;
        
        // Remove números e caracteres especiais
        const cleanText = text.replace(/[0-9\s\.\,\!\?\-\(\)\[\]\{\}]/g, '');
        if (cleanText.length < 3) return false;
        
        // Palavras comuns em inglês que indicam que o texto deve ser traduzido
        const englishKeywords = [
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one',
            'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old',
            'see', 'time', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she',
            'too', 'use', 'episode', 'episodes', 'season', 'seasons', 'genre', 'genres', 'studio',
            'status', 'ongoing', 'completed', 'airing', 'aired', 'score', 'rank', 'popularity',
            'members', 'favorites', 'synopsis', 'background', 'premiered', 'broadcast', 'producer',
            'licensor', 'source', 'duration', 'rating', 'action', 'adventure', 'comedy', 'drama',
            'fantasy', 'horror', 'mystery', 'romance', 'sci-fi', 'slice', 'life', 'sports',
            'supernatural', 'thriller', 'currently', 'finished', 'winter', 'spring', 'summer', 'fall',
            'opening', 'ending', 'theme', 'character', 'characters', 'voice', 'actor', 'staff'
        ];
        
        const lowerText = text.toLowerCase();
        return englishKeywords.some(keyword => {
            const regex = new RegExp('\\b' + keyword + '\\b');
            return regex.test(lowerText);
        });
    }

    /**
     * Verifica se um elemento deve ser ignorado
     */
    shouldIgnoreElement(element) {
        // Ignora elementos específicos
        if (this.ignoredSelectors.some(selector => element.matches(selector))) {
            return true;
        }
        
        // Ignora elementos invisíveis
        if (element.offsetParent === null && element.tagName !== 'BODY') {
            return true;
        }
        
        return false;
    }

    /**
     * Coleta todos os textos que precisam ser traduzidos
     */
    collectTexts(rootElement = document.body) {
        const textsToTranslate = [];
        const walker = document.createTreeWalker(
            rootElement,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: (node) => {
                    if (!node.textContent.trim()) return NodeFilter.FILTER_REJECT;
                    if (this.shouldIgnoreElement(node.parentElement)) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let node;
        while (node = walker.nextNode()) {
            const text = node.textContent.trim();
            if (this.isEnglish(text)) {
                textsToTranslate.push({
                    node: node,
                    text: text
                });
            }
        }

        return textsToTranslate;
    }

    /**
     * Traduz textos em lote via API
     */
    async translateBatch(texts) {
        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ texts: texts })
            });

            if (!response.ok) {
                throw new Error(`Erro na tradução: ${response.status}`);
            }

            const data = await response.json();
            return data.translations;
        } catch (error) {
            console.error('Erro ao traduzir:', error);
            return texts; // Retorna textos originais em caso de erro
        }
    }

    /**
     * Processa fila de tradução
     */
    async processQueue() {
        if (this.isProcessing || this.processingQueue.length === 0) {
            return;
        }

        this.isProcessing = true;

        // Separa textos que já estão no cache dos que precisam ser traduzidos
        const needsTranslation = [];
        const cached = [];

        for (const item of this.processingQueue) {
            if (this.cache.has(item.text)) {
                cached.push({
                    node: item.node,
                    translation: this.cache.get(item.text)
                });
            } else {
                needsTranslation.push(item);
            }
        }

        // Aplica traduções do cache
        cached.forEach(item => {
            item.node.textContent = item.translation;
        });

        // Traduz novos textos em lotes
        while (needsTranslation.length > 0) {
            const batch = needsTranslation.splice(0, this.batchSize);
            const texts = batch.map(item => item.text);
            
            const translations = await this.translateBatch(texts);
            
            // Aplica traduções e salva no cache
            batch.forEach((item, index) => {
                const translation = translations[index];
                item.node.textContent = translation;
                this.cache.set(item.text, translation);
            });
        }

        this.saveCache();
        this.processingQueue = [];
        this.isProcessing = false;
    }

    /**
     * Traduz atributos específicos (como title, alt, placeholder)
     */
    translateAttributes(element) {
        const attributesToTranslate = ['title', 'alt', 'placeholder', 'aria-label'];
        
        attributesToTranslate.forEach(attr => {
            const value = element.getAttribute(attr);
            if (value && this.isEnglish(value)) {
                if (this.cache.has(value)) {
                    element.setAttribute(attr, this.cache.get(value));
                } else {
                    // Adiciona à fila para traduzir depois
                    this.translateBatch([value]).then(translations => {
                        const translation = translations[0];
                        element.setAttribute(attr, translation);
                        this.cache.set(value, translation);
                        this.saveCache();
                    });
                }
            }
        });
    }

    /**
     * Inicia tradução automática
     */
    async start() {
        console.log('🌐 Iniciando tradução automática...');
        
        // Coleta textos
        const items = this.collectTexts();
        
        if (items.length === 0) {
            console.log('✓ Nenhum texto em inglês encontrado');
            return;
        }

        console.log(`🔄 Traduzindo ${items.length} textos...`);
        
        // Adiciona à fila
        this.processingQueue = items;
        
        // Processa fila
        await this.processQueue();
        
        // Traduz atributos
        document.querySelectorAll('[title], [alt], [placeholder], [aria-label]').forEach(el => {
            if (!this.shouldIgnoreElement(el)) {
                this.translateAttributes(el);
            }
        });
        
        console.log('✓ Tradução concluída!');
    }

    /**
     * Observa mudanças no DOM para traduzir conteúdo dinâmico
     */
    observeDOMChanges() {
        const observer = new MutationObserver((mutations) => {
            let hasNewContent = false;
            
            for (const mutation of mutations) {
                if (mutation.addedNodes.length > 0) {
                    hasNewContent = true;
                    break;
                }
            }
            
            if (hasNewContent) {
                // Aguarda 500ms antes de traduzir para evitar múltiplas traduções
                clearTimeout(this.domChangeTimeout);
                this.domChangeTimeout = setTimeout(() => {
                    this.start();
                }, 500);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Limpa cache (útil para desenvolvimento)
     */
    clearCache() {
        this.cache.clear();
        localStorage.removeItem('translation_cache');
        console.log('Cache de traduções limpo!');
    }
}

// Inicializa tradutor automaticamente
const translator = new AutoTranslator();

// Aguarda DOM carregar completamente
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        translator.start();
        translator.observeDOMChanges();
    });
} else {
    translator.start();
    translator.observeDOMChanges();
}

// Expõe globalmente para acesso via console (debug)
window.translator = translator;
