document.addEventListener('DOMContentLoaded', function() {
    console.log('🎮 Build list JavaScript loaded!');
    
    // Get CSRF token
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
               document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }
    
    // Grace button functionality
    document.addEventListener('click', function(e) {
        console.log('Click detected on:', e.target.className);
        
        if (e.target.classList.contains('grace-btn')) {
            console.log('Grace button clicked!');
            e.preventDefault();
            e.stopPropagation();
            
            const button = e.target;
            const buildId = button.getAttribute('data-build-id');
            const isLiked = button.getAttribute('data-liked') === 'true';
            
            console.log('Grace button clicked:', { buildId, isLiked });
            
            // Disable button during request
            button.disabled = true;
            
            // Create form data
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', getCSRFToken());
            
            // Make AJAX request
            fetch(`/builds/build/${buildId}/like/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.success) {
                    // Update button appearance
                    if (data.is_liked) {
                        button.classList.add('bg-danger', 'text-white');
                        button.setAttribute('data-liked', 'true');
                        button.title = 'Remove Grace from this build';
                    } else {
                        button.classList.remove('bg-danger', 'text-white');
                        button.setAttribute('data-liked', 'false');
                        button.title = 'Grace this build';
                    }
                    
                    // Update Grace count in the stats section
                    const buildCard = button.closest('.card');
                    const graceCountElement = buildCard.querySelector('[data-grace-count]');
                    if (graceCountElement) {
                        graceCountElement.textContent = `⚡ ${data.total_likes} Grace`;
                    }
                    
                    console.log('Grace button updated successfully');
                } else {
                    console.error('Server returned success=false');
                }
            })
            .catch(error => {
                console.error('Error toggling grace:', error);
                alert('Failed to update Grace. Please try again.');
            })
            .finally(() => {
                // Re-enable button
                button.disabled = false;
            });
        }
    });
    
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
        
        // Set initial category value if present in URL
        const urlParams = new URLSearchParams(window.location.search);
        const categoryParam = urlParams.get('category');
        if (categoryParam) {
            categorySelect.value = categoryParam;
        }
    }
    
    if (sortSelect) {
        sortSelect.addEventListener('change', updateBuilds);
        
        // Set initial sort value if present in URL
        const urlParams = new URLSearchParams(window.location.search);
        const sortParam = urlParams.get('sort');
        if (sortParam) {
            sortSelect.value = sortParam;
        } else {
            sortSelect.value = 'newest'; // Default value
        }
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