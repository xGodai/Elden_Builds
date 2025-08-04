// Elden Ring API Integration for Build Form
console.log('🎮 Build form JavaScript loaded!');

class EldenRingAutocomplete {
    constructor() {
        this.baseURL = 'https://eldenring.fanapis.com/api';
        this.cache = new Map();
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('🎮 DOM loaded, setting up autocomplete...');
            this.setupField('id_weapons', 'weapons');
            this.setupField('id_armor', 'armors');
            this.setupField('id_talismans', 'talismans');
            this.setupField('id_spells', 'incantations');
            
            // Also setup auto-resize for textareas
            this.setupTextareaResize();
        });
    }

    setupField(fieldId, apiEndpoint) {
        const field = document.getElementById(fieldId);
        if (!field) {
            console.warn(`❌ Field ${fieldId} not found`);
            return;
        }

        console.log(`✅ Setting up autocomplete for ${fieldId}`);

        // Create dropdown container
        const dropdown = this.createDropdown(field);
        let debounceTimer;

        field.addEventListener('input', (e) => {
            const currentValue = e.target.value;
            
            // Extract the current word being typed (after the last comma)
            const lastCommaIndex = currentValue.lastIndexOf(',');
            let query;
            
            if (lastCommaIndex >= 0) {
                // Get text after the last comma and trim whitespace
                query = currentValue.substring(lastCommaIndex + 1).trim();
            } else {
                // No comma found, use entire value
                query = currentValue.trim();
            }
            
            console.log(`🔍 Input detected: "${currentValue}"`);
            console.log(`🔍 Last comma at position: ${lastCommaIndex}`);
            console.log(`🔍 Extracted query: "${query}"`);
            console.log(`🔍 Query length: ${query.length}`);

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if (query.length >= 2) {
                    console.log(`🎯 Triggering search for: "${query}"`);
                    this.showSuggestions(query, apiEndpoint, dropdown, field);
                } else {
                    console.log(`❌ Query too short (${query.length}), hiding dropdown`);
                    this.hideDropdown(dropdown);
                }
            }, 300);
        });

        // Hide dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!field.contains(e.target) && !dropdown.contains(e.target)) {
                this.hideDropdown(dropdown);
            }
        });

        // Add helpful placeholder text
        const originalPlaceholder = field.placeholder;
        field.placeholder = originalPlaceholder + ' (separate multiple items with commas)';

        // Add visual feedback for debugging
        field.addEventListener('focus', () => {
            console.log(`🎯 Field focused: ${fieldId}, current value: "${field.value}"`);
        });

        field.addEventListener('blur', () => {
            console.log(`👋 Field blurred: ${fieldId}, final value: "${field.value}"`);
        });

        // Handle special keys
        field.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && dropdown.style.display === 'block') {
                e.preventDefault(); // Prevent form submission
                console.log('⏎ Enter pressed, selecting first suggestion');
                // Select first suggestion if available
                const firstSuggestion = dropdown.querySelector('div[style*="cursor: pointer"]');
                if (firstSuggestion) {
                    firstSuggestion.click();
                }
            } else if (e.key === 'Escape') {
                console.log('⎋ Escape pressed, hiding dropdown');
                this.hideDropdown(dropdown);
            }
        });
    }

    createDropdown(field) {
        const dropdown = document.createElement('div');
        dropdown.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 4px 4px;
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        `;

        // Make parent relative
        const parent = field.parentNode;
        if (getComputedStyle(parent).position === 'static') {
            parent.style.position = 'relative';
        }

        parent.appendChild(dropdown);
        return dropdown;
    }

    async fetchData(endpoint, limit = 100) {
        const cacheKey = `${endpoint}_${limit}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        try {
            // Try to get more data by making multiple requests if needed
            let allData = [];
            let page = 0;
            let hasMore = true;
            
            while (hasMore && allData.length < 500) { // Cap at 500 items to avoid too much data
                const url = `${this.baseURL}/${endpoint}?limit=100&page=${page}`;
                console.log(`🌐 Fetching page ${page}: ${url}`);
                
                const response = await fetch(url);
                if (!response.ok) {
                    if (page === 0) throw new Error('API request failed');
                    break; // If not first page, just stop fetching more
                }
                
                const data = await response.json();
                const items = data.data || [];
                
                if (items.length === 0) {
                    hasMore = false;
                } else {
                    allData = allData.concat(items);
                    page++;
                    
                    // If we got less than 100 items, probably no more pages
                    if (items.length < 100) {
                        hasMore = false;
                    }
                }
            }
            
            console.log(`📦 Got total of ${allData.length} items from ${endpoint}`);
            
            const result = { data: allData, success: true, count: allData.length };
            this.cache.set(cacheKey, result);
            return result;
        } catch (error) {
            console.error('❌ API Error:', error);
            return { data: [] };
        }
    }

    async showSuggestions(query, endpoint, dropdown, field) {
        // Show loading
        dropdown.innerHTML = '<div style="padding: 8px; color: #666;">🔍 Searching...</div>';
        dropdown.style.display = 'block';

        try {
            const result = await this.fetchData(endpoint);
            const items = result.data || [];

            // Enhanced filtering with multiple matching strategies
            const search = query.toLowerCase();
            const filteredItems = items.filter(item => {
                const name = item.name.toLowerCase();
                
                // Exact start match (highest priority)
                if (name.startsWith(search)) return true;
                
                // Contains match
                if (name.includes(search)) return true;
                
                // Word boundary match (for multi-word items)
                const words = name.split(/\s+/);
                if (words.some(word => word.startsWith(search))) return true;
                
                // Fuzzy match for common typos (optional)
                if (search.length >= 3) {
                    // Remove common prefixes/suffixes and try again
                    const cleanName = name.replace(/^(the\s+|a\s+)|(\s+of\s+.+)$/g, '');
                    if (cleanName.includes(search)) return true;
                }
                
                return false;
            })
            .sort((a, b) => {
                const aName = a.name.toLowerCase();
                const bName = b.name.toLowerCase();
                
                // Sort by relevance
                const aStarts = aName.startsWith(search) ? 0 : 1;
                const bStarts = bName.startsWith(search) ? 0 : 1;
                
                if (aStarts !== bStarts) return aStarts - bStarts;
                
                // Then by name length (shorter names first for exact matches)
                return aName.length - bName.length;
            })
            .slice(0, 15); // Show more results

            console.log(`🎯 Found ${filteredItems.length} matching items for "${query}" out of ${items.length} total`);

            if (filteredItems.length === 0) {
                dropdown.innerHTML = '<div style="padding: 8px; color: #999; text-align: center;">No matches found</div>';
                return;
            }

            this.renderSuggestions(filteredItems, dropdown, field);
        } catch (error) {
            console.error('❌ Error showing suggestions:', error);
            dropdown.innerHTML = '<div style="padding: 8px; color: #dc3545;">Error loading suggestions</div>';
        }
    }

    renderSuggestions(items, dropdown, field) {
        dropdown.innerHTML = '';

        items.forEach(item => {
            const suggestion = document.createElement('div');
            suggestion.style.cssText = `
                padding: 8px 12px;
                cursor: pointer;
                border-bottom: 1px solid #eee;
                display: flex;
                align-items: center;
                transition: background-color 0.2s;
            `;

            suggestion.innerHTML = `
                <div style="display: flex; align-items: center; width: 100%;">
                    ${item.image ? 
                        `<img src="${item.image}" alt="${item.name}" style="width: 24px; height: 24px; margin-right: 8px; object-fit: contain;">` : 
                        '<span style="width: 24px; margin-right: 8px;">⚔️</span>'
                    }
                    <div>
                        <div style="font-weight: bold;">${item.name}</div>
                        ${item.description ? `<small style="color: #666;">${item.description.substring(0, 80)}...</small>` : ''}
                    </div>
                </div>
            `;

            suggestion.addEventListener('mouseenter', () => {
                suggestion.style.backgroundColor = '#f8f9fa';
            });

            suggestion.addEventListener('mouseleave', () => {
                suggestion.style.backgroundColor = 'white';
            });

            suggestion.addEventListener('click', () => {
                this.selectItem(item, field, dropdown);
            });

            dropdown.appendChild(suggestion);
        });

        dropdown.style.display = 'block';
    }

    selectItem(item, field, dropdown) {
        const currentValue = field.value;
        const lastCommaIndex = currentValue.lastIndexOf(',');
        
        let newValue;
        if (lastCommaIndex >= 0) {
            // There are existing items, replace what's after the last comma
            const existingItems = currentValue.substring(0, lastCommaIndex + 1); // Keep everything up to and including the last comma
            newValue = existingItems + ' ' + item.name + ', '; // Add new item with trailing comma and space
        } else {
            // First item
            newValue = item.name + ', ';
        }
        
        field.value = newValue;
        this.hideDropdown(dropdown);
        
        // Position cursor at the end for next item
        field.focus();
        field.setSelectionRange(newValue.length, newValue.length);
        
        console.log(`✅ Selected: ${item.name} (final value: "${field.value}")`);
        field.dispatchEvent(new Event('change', { bubbles: true }));
    }

    hideDropdown(dropdown) {
        dropdown.style.display = 'none';
    }

    // Auto-resize textareas
    setupTextareaResize() {
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
            
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        });
    }
}

// Initialize autocomplete
const eldenRingAPI = new EldenRingAutocomplete();
