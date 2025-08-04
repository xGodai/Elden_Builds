document.addEventListener('DOMContentLoaded', function() {
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
    
    // Like button functionality
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const buildId = this.dataset.buildId;
            const originalText = this.innerHTML;
            
            // Add loading state
            this.innerHTML = '⏳';
            this.disabled = true;
            
            // Get CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]');
            if (!csrfToken) {
                alert('Error: Please refresh the page.');
                this.innerHTML = originalText;
                this.disabled = false;
                return;
            }
            
            // Create form data
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfToken.getAttribute('content'));
            
            // Make AJAX request
            fetch(`/build/${buildId}/like/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle the visual state
                    if (data.is_liked) {
                        this.classList.remove('btn-outline-danger');
                        this.classList.add('btn-danger');
                        this.title = 'Unlike this build';
                    } else {
                        this.classList.remove('btn-danger');
                        this.classList.add('btn-outline-danger');
                        this.title = 'Like this build';
                    }
                    
                    // Update like count in the stats
                    const statsContainer = this.closest('.card').querySelector('.d-flex.justify-content-between.text-muted');
                    if (statsContainer) {
                        const likeSpan = statsContainer.children[0];
                        likeSpan.textContent = `❤️ ${data.total_likes}`;
                    }
                } else {
                    alert('Failed to like/unlike build. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                // Restore button state
                this.innerHTML = originalText;
                this.disabled = false;
            });
        });
    });
});
