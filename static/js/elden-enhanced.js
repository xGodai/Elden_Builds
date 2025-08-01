/**
 * Elden Ring Builds - Enhanced Interactions & Responsive Features
 * Custom JavaScript for improved user experience
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // RESPONSIVE NAVIGATION
    // ========================================
    
    // Auto-collapse mobile menu when clicking nav links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 992) { // Bootstrap lg breakpoint
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        });
    });
    
    // ========================================
    // CARD HOVER EFFECTS
    // ========================================
    
    // Enhanced card interactions
    const cards = document.querySelectorAll('.card, .build-card');
    
    cards.forEach(card => {
        // Add subtle rotation on hover for desktop
        card.addEventListener('mouseenter', function() {
            if (window.innerWidth >= 768) {
                this.style.transform = 'translateY(-6px) rotateX(2deg)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateX(0)';
        });
    });
    
    // ========================================
    // SMOOTH SCROLLING
    // ========================================
    
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ========================================
    // FORM ENHANCEMENTS
    // ========================================
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        // Set initial height
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
        
        // Resize on input
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
    
    // Enhanced form validation feedback (excluding authentication forms)
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        console.log(`Checking form: ${form.id}, action: ${form.action}, classes: ${form.className}`);
        
        // Skip authentication forms and build forms - let them submit normally
        if (form.classList.contains('er-form') || 
            form.action.includes('/login/') || 
            form.action.includes('/logout/') || 
            form.action.includes('/register/') ||
            form.id === 'build-form') {
            console.log(`Skipping form validation for: ${form.id}`);
            return;
        }
        
        console.log(`Adding validation to form: ${form.id}`);
        form.addEventListener('submit', function(e) {
            const invalidFields = form.querySelectorAll(':invalid');
            
            if (invalidFields.length > 0) {
                e.preventDefault();
                
                // Focus first invalid field
                invalidFields[0].focus();
                
                // Add shake animation to form
                form.classList.add('shake');
                setTimeout(() => form.classList.remove('shake'), 600);
            }
        });
    });
    
    // ========================================
    // IMAGE UPLOAD ENHANCEMENTS
    // ========================================
    
    // Drag and drop for image uploads
    const uploadAreas = document.querySelectorAll('.image-upload-area, [type="file"]');
    
    uploadAreas.forEach(area => {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, unhighlight, false);
        });
        
        // Handle dropped files
        area.addEventListener('drop', handleDrop, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        e.target.classList.add('dragover');
    }
    
    function unhighlight(e) {
        e.target.classList.remove('dragover');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        // Handle the files (this is a basic example)
        Array.from(files).forEach(file => {
            if (file.type.startsWith('image/')) {
                console.log('Dropped image file:', file.name);
                // You can add file preview logic here
            }
        });
    }
    
    // ========================================
    // LOADING STATES
    // ========================================
    
    // Show loading spinner on form submissions (excluding authentication forms)
    const submitButtons = document.querySelectorAll('[type="submit"]');
    
    submitButtons.forEach(button => {
        const form = button.closest('form');
        
        // Skip authentication forms - let them submit normally
        if (form && (form.classList.contains('er-form') || 
            form.action.includes('/login/') || 
            form.action.includes('/logout/') || 
            form.action.includes('/register/'))) {
            return;
        }
        
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                // Add loading state
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
                this.disabled = true;
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    this.disabled = false;
                    this.innerHTML = this.getAttribute('data-original-text') || 'Submit';
                }, 5000);
            }
        });
        
        // Store original text
        button.setAttribute('data-original-text', button.innerHTML);
    });
    
    // ========================================
    // NOTIFICATION SYSTEM
    // ========================================
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
    
    // ========================================
    // RESPONSIVE IMAGE LOADING
    // ========================================
    
    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    
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
    
    images.forEach(img => imageObserver.observe(img));
    
    // ========================================
    // VOTE BUTTONS (for comments/builds)
    // ========================================
    
    // Enhanced vote button interactions
    const voteButtons = document.querySelectorAll('.vote-btn');
    
    voteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            // Here you would typically make an AJAX call to update the vote
            // For now, just toggle the active state visually
            const isUpvote = this.classList.contains('upvote-btn');
            const isDownvote = this.classList.contains('downvote-btn');
            const parent = this.closest('.comment-vote-buttons');
            
            if (parent) {
                const upvoteBtn = parent.querySelector('.upvote-btn');
                const downvoteBtn = parent.querySelector('.downvote-btn');
                
                if (isUpvote) {
                    this.classList.toggle('active-upvote');
                    if (downvoteBtn) downvoteBtn.classList.remove('active-downvote');
                } else if (isDownvote) {
                    this.classList.toggle('active-downvote');
                    if (upvoteBtn) upvoteBtn.classList.remove('active-upvote');
                }
            }
        });
    });
    
    // ========================================
    // SEARCH ENHANCEMENTS
    // ========================================
    
    // Real-time search with debouncing
    const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
    
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            searchTimeout = setTimeout(() => {
                if (query.length >= 2) {
                    // Perform search (you would implement the actual search logic)
                    console.log('Searching for:', query);
                }
            }, 300); // 300ms debounce
        });
    });
    
    // ========================================
    // ACCESSIBILITY ENHANCEMENTS
    // ========================================
    
    // Keyboard navigation for dropdowns
    const dropdownToggles = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Focus management for modals
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const focusableElement = this.querySelector('input, button, textarea, select, a');
            if (focusableElement) {
                focusableElement.focus();
            }
        });
    });
    
    // ========================================
    // PERFORMANCE OPTIMIZATIONS
    // ========================================
    
    // Throttle scroll events
    let ticking = false;
    
    function updateScrollPosition() {
        const scrolled = window.pageYOffset;
        const navbar = document.querySelector('.navbar');
        
        if (scrolled > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScrollPosition);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
    
    // ========================================
    // DARK MODE TOGGLE (if needed)
    // ========================================
    
    // Theme switcher (optional feature)
    const themeToggle = document.querySelector('.theme-toggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('light-theme');
            
            // Save preference
            const isLight = document.body.classList.contains('light-theme');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
        });
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            document.body.classList.add('light-theme');
        }
    }
    
    // ========================================
    // RESPONSIVE UTILITIES
    // ========================================
    
    // Update viewport height for mobile browsers
    function updateViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    updateViewportHeight();
    window.addEventListener('resize', updateViewportHeight);
    
    // Touch device detection
    function addTouchClass() {
        if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
            document.body.classList.add('touch-device');
        }
    }
    
    addTouchClass();
    
    console.log('🔥 Elden Ring Builds - Enhanced interactions loaded successfully!');
});

// ========================================
// CSS ANIMATIONS STYLES
// ========================================

// Add CSS for shake animation
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
        20%, 40%, 60%, 80% { transform: translateX(4px); }
    }
    
    .shake {
        animation: shake 0.6s ease-in-out;
    }
    
    .navbar.scrolled {
        backdrop-filter: blur(20px);
        background: rgba(10, 10, 10, 0.95) !important;
    }
    
    .touch-device .card:hover {
        transform: none !important;
    }
    
    .light-theme {
        filter: invert(1) hue-rotate(180deg);
    }
    
    .light-theme img,
    .light-theme video,
    .light-theme iframe {
        filter: invert(1) hue-rotate(180deg);
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
`;

document.head.appendChild(style);
