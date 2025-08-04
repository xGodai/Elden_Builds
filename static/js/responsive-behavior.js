/**
 * Responsive Behavior JavaScript - Elden Ring Builds
 * Handles viewport management, responsive updates, and navigation behavior
 */

// Immediate viewport and responsive setup (IIFE)
(function() {
  // Force proper viewport immediately
  const viewport = document.querySelector('meta[name="viewport"]');
  if (viewport) {
    viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, shrink-to-fit=no, user-scalable=yes');
  }
  
  // Prevent layout shifts by setting body to loaded state
  function setLoaded() {
    document.body.classList.add('loaded');
  }
  
  // Set loaded state as soon as possible
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setLoaded);
  } else {
    setLoaded();
  }
})();

// Enhanced responsive behavior on page load and navigation
document.addEventListener('DOMContentLoaded', function() {
  // Force viewport recalculation and responsive classes
  function forceResponsiveUpdate() {
    const viewport = document.querySelector('meta[name="viewport"]');
    if (viewport) {
      // Temporarily change and restore viewport to force recalculation
      const originalContent = viewport.getAttribute('content');
      viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, shrink-to-fit=no');
      
      // Force reflow
      document.body.offsetHeight;
      
      setTimeout(() => {
        viewport.setAttribute('content', originalContent);
        
        // Trigger Bootstrap responsive recalculation
        if (window.bootstrap) {
          // Re-initialize any Bootstrap components that depend on viewport
          const modals = document.querySelectorAll('.modal');
          modals.forEach(modal => {
            if (bootstrap.Modal.getInstance(modal)) {
              bootstrap.Modal.getInstance(modal).handleUpdate();
            }
          });
        }
      }, 10);
    }
  }
  
  // Initial responsive update
  forceResponsiveUpdate();
  
  // Handle window resize with debouncing
  let resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      forceResponsiveUpdate();
      
      // Force responsive class updates
      document.body.classList.add('resize-event');
      setTimeout(() => {
        document.body.classList.remove('resize-event');
      }, 100);
    }, 150);
  });
  
  // Handle page visibility changes (when switching tabs/windows)
  document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
      setTimeout(forceResponsiveUpdate, 100);
    }
  });
  
  // Enhanced navbar collapse functionality
  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarCollapse = document.querySelector('.navbar-collapse');
  
  if (navbarToggler && navbarCollapse) {
    // Ensure proper mobile navbar behavior
    function updateNavbarBehavior() {
      const isMobile = window.innerWidth < 992;
      
      if (isMobile) {
        navbarCollapse.classList.add('mobile-nav');
      } else {
        navbarCollapse.classList.remove('mobile-nav');
        // Auto-close mobile nav when switching to desktop
        if (navbarCollapse.classList.contains('show')) {
          const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
          if (bsCollapse) {
            bsCollapse.hide();
          }
        }
      }
    }
    
    // Initial navbar setup
    updateNavbarBehavior();
    
    // Update on resize
    window.addEventListener('resize', updateNavbarBehavior);
    
    // Close navbar when clicking outside on mobile
    document.addEventListener('click', function(event) {
      const isClickInsideNav = navbarCollapse.contains(event.target) || navbarToggler.contains(event.target);
      const isNavOpen = navbarCollapse.classList.contains('show');
      const isMobile = window.innerWidth < 992;
      
      if (!isClickInsideNav && isNavOpen && isMobile) {
        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
        if (bsCollapse) {
          bsCollapse.hide();
        }
      }
    });
  }
  
  // Ensure body is visible after all setup
  document.body.classList.add('loaded');
});

// Handle page navigation (for SPAs or AJAX navigation)
window.addEventListener('popstate', function() {
  setTimeout(() => {
    document.body.classList.add('loaded');
    // Force responsive recalculation on navigation
    window.dispatchEvent(new Event('resize'));
  }, 50);
});

// Export functions for potential use by other scripts
window.ResponsiveBehavior = {
  forceUpdate: function() {
    window.dispatchEvent(new Event('resize'));
  },
  
  setLoaded: function() {
    document.body.classList.add('loaded');
  },
  
  checkMobile: function() {
    return window.innerWidth < 992;
  }
};
