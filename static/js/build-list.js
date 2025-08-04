document.addEventListener('DOMContentLoaded', function() {
    console.log('🎮 Build list JavaScript loaded!');
    
    // Filter and Sort functionality
    const categorySelect = document.getElementById('category-select');
    const sortSelect = document.getElementById('sort-select');
    const searchInput = document.querySelector('.search-input');
    
    function updateBuilds() {
        const currentUrl = new URL(window.location);
        
        // Update category parameter
        if (categorySelect.value) {
            currentUrl.searchParams.set('category', categorySelect.value);
        } else {
            currentUrl.searchParams.delete('category');
        }
        
        // Update sort parameter
        if (sortSelect.value) {
            currentUrl.searchParams.set('sort', sortSelect.value);
        } else {
            currentUrl.searchParams.delete('sort');
        }
        
        // Update search parameter
        if (searchInput.value.trim()) {
            currentUrl.searchParams.set('search', searchInput.value.trim());
        } else {
            currentUrl.searchParams.delete('search');
        }
        
        // Remove page parameter when filtering
        currentUrl.searchParams.delete('page');
        
        window.location.href = currentUrl.toString();
    }
    
    // Add event listeners
    if (categorySelect) {
        categorySelect.addEventListener('change', updateBuilds);
    }
    
    if (sortSelect) {
        sortSelect.addEventListener('change', updateBuilds);
    }
    
    // Search with debouncing
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(updateBuilds, 500);
        });
        
        // Set initial search value if present in URL
        const urlParams = new URLSearchParams(window.location.search);
        const searchParam = urlParams.get('search');
        if (searchParam) {
            searchInput.value = searchParam;
        }
    }
    
    console.log('🎮 Build list JavaScript setup complete!');
});
