// Auto-refresh notification count every 30 seconds
document.addEventListener('DOMContentLoaded', function() {
    setInterval(function() {
        // Get the current page URL to construct the fetch URL
        const currentDomain = window.location.origin;
        const unreadCountUrl = currentDomain + '/users/unread-notification-count/';
        
        fetch(unreadCountUrl)
            .then(response => response.json())
            .then(data => {
                // Update notification badge in navbar if it exists
                const badge = document.querySelector('.notification-badge');
                if (badge) {
                    if (data.count > 0) {
                        badge.textContent = data.count;
                        badge.style.display = 'inline';
                    } else {
                        badge.style.display = 'none';
                    }
                }
            })
            .catch(error => console.error('Error fetching notification count:', error));
    }, 30000);
});
