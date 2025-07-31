/* Global JavaScript for Elden Ring Builds */

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Main app initialization
function initializeApp() {
    initializeTooltips();
    initializeModals();
    initializeImageLazyLoading();
    initializeFormValidation();
    initializeNotifications();
    
    console.log('Elden Ring Builds app initialized');
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize Bootstrap modals
function initializeModals() {
    const modalTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'));
    modalTriggerList.forEach(function(modalTriggerEl) {
        modalTriggerEl.addEventListener('click', function(e) {
            const targetModal = document.querySelector(this.getAttribute('data-bs-target'));
            if (targetModal) {
                const modal = new bootstrap.Modal(targetModal);
                modal.show();
            }
        });
    });
}

// Lazy loading for images
function initializeImageLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Form validation helpers
function initializeFormValidation() {
    // Add custom validation styles
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                }
            }
            
            form.classList.add('was-validated');
        });
    });
}

// Notification system
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Utility Functions
const EldenUtils = {
    // Show loading state
    showLoading: function(element) {
        if (element) {
            element.classList.add('loading');
            const originalText = element.textContent;
            element.dataset.originalText = originalText;
            element.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
        }
    },

    // Hide loading state
    hideLoading: function(element) {
        if (element && element.dataset.originalText) {
            element.classList.remove('loading');
            element.textContent = element.dataset.originalText;
            delete element.dataset.originalText;
        }
    },

    // Show toast notification
    showToast: function(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = toastContainer.lastElementChild;
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    },

    // Confirm dialog
    confirm: function(message, callback) {
        if (window.confirm(message)) {
            callback();
        }
    },

    // Copy to clipboard
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showToast('Copied to clipboard!', 'success');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('Copied to clipboard!', 'success');
        }
    },

    // Format numbers with commas
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },

    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// CSRF token helper for AJAX requests
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // In production, you might want to send this to a logging service
});

// Expose utilities globally
window.EldenUtils = EldenUtils;
