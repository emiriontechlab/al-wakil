// Al Wakil Interior Design - Local JavaScript

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Initialize particles animation
    // initParticles();
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Initialize mobile menu
    initMobileMenu();
});

// Particles animation for hero background
// function initParticles() {
//     const canvas = document.getElementById('particles-canvas');
//     if (!canvas) return;
    
//     const ctx = canvas.getContext('2d');
//     const particles = [];
//     const particleCount = 50;
    
//     // Set canvas size
//     function resizeCanvas() {
//         canvas.width = window.innerWidth;
//         canvas.height = window.innerHeight;
//     }
    
//     resizeCanvas();
//     window.addEventListener('resize', resizeCanvas);
    
//     // Particle class
//     class Particle {
//         constructor() {
//             this.x = Math.random() * canvas.width;
//             this.y = Math.random() * canvas.height;
//             this.vx = (Math.random() - 0.5) * 0.5;
//             this.vy = (Math.random() - 0.5) * 0.5;
//             this.size = Math.random() * 2 + 1;
//             this.opacity = Math.random() * 0.5 + 0.2;
//         }
        
//         update() {
//             this.x += this.vx;
//             this.y += this.vy;
            
//             // Wrap around edges
//             if (this.x < 0) this.x = canvas.width;
//             if (this.x > canvas.width) this.x = 0;
//             if (this.y < 0) this.y = canvas.height;
//             if (this.y > canvas.height) this.y = 0;
//         }
        
//         draw() {
//             ctx.beginPath();
//             ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
//             ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
//             ctx.fill();
//         }
//     }
    
//     // Create particles
//     for (let i = 0; i < particleCount; i++) {
//         particles.push(new Particle());
//     }
    
//     // Animation loop
//     function animate() {
//         ctx.clearRect(0, 0, canvas.width, canvas.height);
        
//         particles.forEach(particle => {
//             particle.update();
//             particle.draw();
//         });
        
//         requestAnimationFrame(animate);
//     }
    
//     animate();
// }

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.hero-title, .achievement, .cta-section, .section-header, .service-card, .announcement-text, .announcement-image');
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Mobile menu functionality
function initMobileMenu() {
    // Create mobile menu button
    const nav = document.querySelector('.main-nav');
    const navContainer = nav.querySelector('.nav-container');
    const navLinks = nav.querySelector('.nav-links');
    
    // Create hamburger button
    const menuButton = document.createElement('button');
    menuButton.className = 'mobile-menu-btn';
    menuButton.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;
    
    navContainer.appendChild(menuButton);
    
    // Toggle mobile menu
    menuButton.addEventListener('click', () => {
        nav.classList.toggle('mobile-menu-open');
    });
    
    // Close menu when clicking on links
    navLinks.addEventListener('click', (e) => {
        if (e.target.tagName === 'A') {
            nav.classList.remove('mobile-menu-open');
        }
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!nav.contains(e.target)) {
            nav.classList.remove('mobile-menu-open');
        }
    });
}

// Video play/pause functionality
document.addEventListener('DOMContentLoaded', function() {
    const video = document.querySelector('.video-section video');
    if (video) {
        // Pause video when not in view
        const videoObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    video.play();
                } else {
                    video.pause();
                }
            });
        }, { threshold: 0.5 });
        
        videoObserver.observe(video);
    }
});

// Form handling (if contact form is added)
function handleContactForm() {
    const form = document.querySelector('#contact-form');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Simple validation
        if (!data.name || !data.email || !data.message) {
            alert('Please fill in all required fields.');
            return;
        }
        
        // Here you would typically send the data to a server
        console.log('Form submitted:', data);
        alert('Thank you for your message! We will get back to you soon.');
        form.reset();
    });
}

// Initialize contact form if it exists
document.addEventListener('DOMContentLoaded', handleContactForm);

// Utility functions
function debounce(func, wait) {
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

// Scroll to top functionality
function addScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.className = 'scroll-to-top';
    scrollButton.innerHTML = '↑';
    scrollButton.setAttribute('aria-label', 'Scroll to top');
    
    document.body.appendChild(scrollButton);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', debounce(() => {
        if (window.pageYOffset > 300) {
            scrollButton.classList.add('visible');
        } else {
            scrollButton.classList.remove('visible');
        }
    }, 100));
    
    // Scroll to top when clicked
    scrollButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize scroll to top button
document.addEventListener('DOMContentLoaded', addScrollToTop);

// Performance optimization: Lazy load images
function initLazyLoading() {
    const images = document.querySelectorAll('img[src]:not(.hero-slide)');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);

// FAQ Accordion functionality
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all other FAQ items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Toggle current item
            if (isActive) {
                item.classList.remove('active');
            } else {
                item.classList.add('active');
            }
        });
    });
}


//  alwakil scrolling image js
const sliders = document.querySelectorAll(".alwakil-image-row");

sliders.forEach((slider) => {
    let isPaused = false;
    let speed = 0.5;

    function autoScroll() {
        if (!isPaused) {
            slider.scrollLeft += speed;

            if (slider.scrollLeft >= slider.scrollWidth - slider.clientWidth) {
                slider.scrollLeft = 0;
            }
        }
        requestAnimationFrame(autoScroll);
    }

    autoScroll();

    const cards = slider.querySelectorAll(".alwakil-card");

    cards.forEach((card) => {
        card.addEventListener("mouseenter", () => {
            isPaused = true;
        });

        card.addEventListener("mouseleave", () => {
            isPaused = false;
        });
    });
});


// Initialize FAQ when DOM is loaded
document.addEventListener('DOMContentLoaded', initFAQ);

// Portfolio hover effects and text animation
function initPortfolioEffects() {
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const portfolioSection = document.querySelector('.portfolio');
    
    portfolioItems.forEach((item, index) => {
        const overlay = item.querySelector('.portfolio-overlay');
        
        // Set sequential delays so only one shows at a time
        // Each item gets 2.5s delay (25% of 10s total cycle)
        if (overlay) {
            overlay.style.animationDelay = `${index * 2}s`;
        }
        
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Pause animations when section is not visible for performance
    if (portfolioSection) {
        const portfolioObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const overlays = entry.target.querySelectorAll('.portfolio-overlay');
                if (entry.isIntersecting) {
                    overlays.forEach(overlay => {
                        overlay.style.animationPlayState = 'running';
                    });
                } else {
                    overlays.forEach(overlay => {
                        overlay.style.animationPlayState = 'paused';
                    });
                }
            });
        }, { threshold: 0.1 });
        
        portfolioObserver.observe(portfolioSection);
    }
}

// Initialize portfolio effects
document.addEventListener('DOMContentLoaded', initPortfolioEffects);

// Testimonials carousel (optional enhancement)
function initTestimonialsCarousel() {
    const testimonialsGrid = document.querySelector('.testimonials-grid');
    if (!testimonialsGrid) return;
    
    // Add touch/swipe support for mobile
    let startX = 0;
    let scrollLeft = 0;
    
    testimonialsGrid.addEventListener('touchstart', (e) => {
        startX = e.touches[0].pageX - testimonialsGrid.offsetLeft;
        scrollLeft = testimonialsGrid.scrollLeft;
    });
    
    testimonialsGrid.addEventListener('touchmove', (e) => {
        if (!startX) return;
        
        e.preventDefault();
        const x = e.touches[0].pageX - testimonialsGrid.offsetLeft;
        const walk = (x - startX) * 2;
        testimonialsGrid.scrollLeft = scrollLeft - walk;
    });
    
    testimonialsGrid.addEventListener('touchend', () => {
        startX = 0;
    });
}

// Initialize testimonials carousel
document.addEventListener('DOMContentLoaded', initTestimonialsCarousel);

// Enhanced scroll animations for new sections
function initEnhancedScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Special animations for specific elements
                if (entry.target.classList.contains('stat-item')) {
                    animateCounter(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observe new elements
    const newAnimateElements = document.querySelectorAll('.about-text, .about-image, .stat-item, .portfolio-item, .testimonial-item, .faq-item');
    
    newAnimateElements.forEach(el => {
        observer.observe(el);
    });
}

// Counter animation for statistics
function animateCounter(element) {
    const counter = element.querySelector('h3');
    if (!counter) return;
    
    const target = parseInt(counter.textContent);
    const duration = 2000; // 2 seconds
    const step = target / (duration / 16); // 60fps
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        // Format the number
        if (target >= 1000) {
            counter.textContent = Math.floor(current) + '+';
        } else {
            counter.textContent = Math.floor(current) + '+';
        }
    }, 16);
}

// Initialize enhanced scroll animations
document.addEventListener('DOMContentLoaded', initEnhancedScrollAnimations);

// Smooth reveal animations for sections
function addSectionRevealAnimations() {
    const sections = document.querySelectorAll('section');
    
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        sectionObserver.observe(section);
    });
}

// Initialize section reveal animations
document.addEventListener('DOMContentLoaded', addSectionRevealAnimations);

// Professional Hero Slider with 3D effects
function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    const indicators = document.querySelectorAll('.indicator');
    const progressBar = document.querySelector('.progress-bar');
    
    if (!slides.length) return;

    let current = 0;
    let isTransitioning = false;
    let slideTimer = null;
    const slideInterval = 2000; // 2 seconds

    function updateSlider() {
        if (isTransitioning) return;
        isTransitioning = true;

        // Remove all classes
        slides.forEach((slide, index) => {
            slide.classList.remove('active', 'prev', 'next');
            indicators[index].classList.remove('active');
        });

        // Set current slide as active
        slides[current].classList.add('active');
        indicators[current].classList.add('active');

        // Set previous and next slides
        const prevIndex = current === 0 ? slides.length - 1 : current - 1;
        const nextIndex = current === slides.length - 1 ? 0 : current + 1;

        slides[prevIndex].classList.add('prev');
        slides[nextIndex].classList.add('next');

        // Reset progress bar animation
        if (progressBar) {
            progressBar.style.animation = 'none';
            progressBar.offsetHeight; // Trigger reflow
            progressBar.style.animation = `slideProgress ${slideInterval}ms linear`;
        }

        setTimeout(() => {
            isTransitioning = false;
        }, 1200); // Match CSS transition duration
    }

    function nextSlide() {
        current = (current + 1) % slides.length;
        updateSlider();
    }

    function goToSlide(index) {
        if (isTransitioning || index === current) return;
        current = index;
        updateSlider();
    }

    function startAutoSlide() {
        if (slideTimer) clearInterval(slideTimer);
        slideTimer = setInterval(nextSlide, slideInterval);
    }

    function stopAutoSlide() {
        if (slideTimer) clearInterval(slideTimer);
    }

    // Initialize slider
    updateSlider();
    startAutoSlide();

    // Indicator click handlers
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            stopAutoSlide();
            goToSlide(index);
            // Restart auto-advance after user interaction
            setTimeout(startAutoSlide, slideInterval);
        });
    });

    // Pause on hover
    const sliderContainer = document.querySelector('.hero-slider');
    if (sliderContainer) {
        sliderContainer.addEventListener('mouseenter', () => {
            stopAutoSlide();
            if (progressBar) progressBar.style.animationPlayState = 'paused';
        });

        sliderContainer.addEventListener('mouseleave', () => {
            startAutoSlide();
            if (progressBar) progressBar.style.animationPlayState = 'running';
        });
    }

    // Touch/swipe support for mobile
    let startX = 0;
    let endX = 0;

    if (sliderContainer) {
        sliderContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });

        sliderContainer.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            handleSwipe();
        });
    }

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = startX - endX;

        if (Math.abs(diff) > swipeThreshold) {
            stopAutoSlide();
            if (diff > 0) {
                // Swipe left - next slide
                nextSlide();
            } else {
                // Swipe right - previous slide
                current = current === 0 ? slides.length - 1 : current - 1;
                updateSlider();
            }
            // Restart auto-advance after swipe
            setTimeout(startAutoSlide, slideInterval);
        }
    }
}

document.addEventListener('DOMContentLoaded', initHeroSlider);

// Room Categories Grid functionality
function initRoomCategoriesGrid() {
    // Add click functionality
    document.querySelectorAll('.grid-item').forEach(item => {
        item.addEventListener('click', function() {
            const title = this.querySelector('.grid-item-title').textContent;
            console.log(`Clicked on: ${title}`);
            // You can add navigation or other functionality here
            // window.location.href = `/${title.toLowerCase()}.html`;
        });
    });

    // Add touch support for mobile
    document.querySelectorAll('.grid-item').forEach(item => {
        item.addEventListener('touchstart', function() {
            this.classList.add('touch-active');
        });
                     
        item.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('touch-active');
            }, 300);
        });
    });
}

// Initialize room categories grid
document.addEventListener('DOMContentLoaded', initRoomCategoriesGrid);
