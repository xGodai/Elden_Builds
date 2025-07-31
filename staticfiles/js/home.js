/* Home Page JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    initializeHomePage();
});

function initializeHomePage() {
    animateStats();
    initializeHeroAnimations();
    initializeBuildCards();
    
    console.log('Home page initialized');
}

// Animate statistics counters
function animateStats() {
    const statElements = document.querySelectorAll('.stat-item h3');
    
    const animateNumber = (element, target) => {
        const duration = 2000; // 2 seconds
        const start = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            
            const current = Math.floor(target * easeOutQuart);
            element.textContent = EldenUtils.formatNumber(current);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.textContent = EldenUtils.formatNumber(target);
            }
        };
        
        requestAnimationFrame(animate);
    };

    // Use Intersection Observer to trigger animation when stats come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.textContent);
                if (!isNaN(target)) {
                    animateNumber(entry.target, target);
                    observer.unobserve(entry.target);
                }
            }
        });
    }, { threshold: 0.5 });

    statElements.forEach(element => {
        observer.observe(element);
    });
}

// Initialize hero section animations
function initializeHeroAnimations() {
    const heroContent = document.querySelector('.hero-section .col-lg-6:first-child');
    const heroStats = document.querySelector('.hero-stats');
    
    if (heroContent) {
        heroContent.classList.add('fade-in');
    }
    
    if (heroStats) {
        setTimeout(() => {
            heroStats.classList.add('slide-in-left');
        }, 300);
    }
}

// Initialize build card interactions
function initializeBuildCards() {
    const buildCards = document.querySelectorAll('.build-card');
    
    buildCards.forEach(card => {
        // Add hover effect for better UX
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        // Add click tracking (for analytics if needed)
        card.addEventListener('click', function(e) {
            const buildTitle = this.querySelector('.card-title')?.textContent;
            console.log('Build card clicked:', buildTitle);
        });
    });
}

// Feature card animations on scroll
function initializeFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 200); // Stagger the animations
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}

// Call feature cards animation
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initializeFeatureCards, 500);
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Parallax effect for hero section (optional)
function initializeParallax() {
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        window.addEventListener('scroll', EldenUtils.debounce(function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        }, 10));
    }
}

// Initialize parallax if desired (uncomment to enable)
// initializeParallax();

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        animateStats,
        initializeHeroAnimations,
        initializeBuildCards,
        initializeFeatureCards
    };
}
