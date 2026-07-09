// PWA and Modern UX Enhancements for OrganyxHub

class OrganyxPWA {
    constructor() {
        this.init();
    }

    init() {
        this.setupLazyLoading();
        this.setupInfiniteScroll();
        this.setupTouchGestures();
        this.setupPerformanceOptimizations();
        this.setupFocusManagement();
        this.setupProgressiveEnhancement();
        this.setupModernInteractions();
    }

    // Lazy Loading for Images
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.checkImageExists(img.dataset.src).then(exists => {
                            if (exists) {
                                img.src = img.dataset.src;
                                img.classList.remove('lazy');
                                img.classList.add('loaded');
                                observer.unobserve(img);
                            }
                        });
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // Infinite Scroll for Product Lists
    setupInfiniteScroll() {
        const productContainer = document.querySelector('.product-grid-4');
        if (!productContainer) return;

        let loading = false;
        let page = 1;

        const loadMoreProducts = async () => {
            if (loading) return;
            loading = true;

            try {
                const response = await fetch(`/api/products/?page=${page + 1}`);
                if (response.ok) {
                    const data = await response.json();
                    if (data.products && data.products.length > 0) {
                        this.appendProducts(data.products, productContainer);
                        page++;
                    }
                }
            } catch (error) {
                console.error('Error loading more products:', error);
            } finally {
                loading = false;
            }
        };

        const scrollObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                loadMoreProducts();
            }
        });

        const sentinel = document.createElement('div');
        sentinel.className = 'scroll-sentinel';
        productContainer.appendChild(sentinel);
        scrollObserver.observe(sentinel);
    }

    appendProducts(products, container) {
        products.forEach(product => {
            const productHTML = this.createProductCard(product);
            container.insertAdjacentHTML('beforeend', productHTML);
        });
    }

    createProductCard(product) {
        return `
            <div class="col-lg-3 col-md-4 col-12 col-sm-6 animate-fade-in-up">
                <div class="product-cart-wrap mb-30">
                    <div class="product-img-action-wrap">
                        <div class="product-img product-img-zoom">
                            <a href="/produto/${product.pid}/">
                                <img class="default-img lazy" data-src="${product.image}" alt="${product.title}" 
                                     style="aspect-ratio: 1/1; object-fit: cover;" />
                            </a>
                        </div>
                        <div class="product-action-1">
                            <a aria-label="Adicionar à Wishlist" class="action-btn add-to-wishlist interactive-element" 
                               data-product-item="${product.id}">
                                <i class="fi-rs-heart"></i>
                            </a>
                            <a aria-label="Visualização Rápida" class="action-btn interactive-element" 
                               href="/produto/${product.pid}/">
                                <i class="fi-rs-eye"></i>
                            </a>
                        </div>
                    </div>
                    <div class="product-content-wrap">
                        <h2><a href="/produto/${product.pid}/">${product.title}</a></h2>
                        <div class="product-price">
                            <span>R$ ${product.price}</span>
                        </div>
                        <button class="btn btn-primary add-to-cart-btn w-100" data-product-id="${product.id}">
                            <i class="fi-rs-shopping-cart"></i> Adicionar
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Touch Gestures for Mobile
    setupTouchGestures() {
        let startX, startY, endX, endY;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            this.handleSwipe(startX, startY, endX, endY);
        });
    }

    handleSwipe(startX, startY, endX, endY) {
        const deltaX = endX - startX;
        const deltaY = endY - startY;
        const minSwipeDistance = 50;

        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
            if (deltaX > 0) {
                // Swipe right - go back
                if (window.history.length > 1) {
                    window.history.back();
                }
            } else {
                // Swipe left - could trigger menu or other action
                this.toggleMobileMenu();
            }
        }
    }

    toggleMobileMenu() {
        const mobileMenu = document.querySelector('.mobile-header-wrapper-style');
        if (mobileMenu) {
            mobileMenu.classList.toggle('open');
        }
    }

    // Performance Optimizations
    setupPerformanceOptimizations() {
        // Debounced search
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.performSearch(e.target.value);
            }, 300));
        }

        // Preload critical resources
        this.preloadCriticalResources();

        // Optimize images
        this.optimizeImages();
    }

    debounce(func, wait) {
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

    async performSearch(query) {
        if (query.length < 2) return;

        try {
            const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
            if (response.ok) {
                const results = await response.json();
                this.displaySearchResults(results);
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    displaySearchResults(results) {
        // Implementation for displaying search results
        console.log('Search results:', results);
    }

    preloadCriticalResources() {
        const criticalResources = [
            '/static/assets/css/main.css',
            '/static/assets/js/main.js',
            '/static/assets/imgs/theme/logo.png'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            
            if (resource.endsWith('.css')) {
                link.as = 'style';
            } else if (resource.endsWith('.js')) {
                link.as = 'script';
            } else {
                link.as = 'image';
            }
            
            document.head.appendChild(link);
        });
    }

    supportsWebP() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }

    optimizeImages() {
        const images = document.querySelectorAll('img[src*=".jpg"], img[src*=".jpeg"], img[src*=".png"]');
        
        if (!this.supportsWebP()) return;

        // Process images with better error handling - no console spam
        const processImages = async () => {
            for (const img of images) {
                if (img.dataset.optimized) continue;
                
                try {
                    const originalSrc = img.src;
                    if (!originalSrc || originalSrc.includes('.webp')) continue;
                    
                    const webpSrc = originalSrc.replace(/\.(jpg|jpeg|png)$/i, '.webp');
                    
                    const webpExists = await this.checkImageExists(webpSrc);
                    if (webpExists) {
                        img.src = webpSrc;
                    }
                } catch (error) {
                    // Silently skip failed images to avoid console spam
                }
                
                img.dataset.optimized = 'true';
            }
        };

        processImages();
    }

    announce(message) {
        if (this.announcer) {
            this.announcer.textContent = message;
        }
    }

    setupFocusManagement() {
        // Trap focus in modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                const modal = document.querySelector('.modal.show');
                if (modal) {
                    this.trapFocus(e, modal);
                }
            }
        });
    }

    trapFocus(e, container) {
        const focusableElements = container.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
            if (document.activeElement === firstElement) {
                lastElement.focus();
                e.preventDefault();
            }
        } else {
            if (document.activeElement === lastElement) {
                firstElement.focus();
                e.preventDefault();
            }
        }
    }

    // Modern Interactions
    setupModernInteractions() {
        // Smooth scrolling
        this.setupSmoothScrolling();
        
        // Loading states
        this.setupLoadingStates();
        
        // Form validation
        this.setupFormValidation();
        
        // Enhanced cart functionality
        this.setupEnhancedCart();
    }

    setupSmoothScrolling() {
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
    }

    setupLoadingStates() {
        // Add loading states to buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-to-cart-btn')) {
                this.showButtonLoading(e.target);
            }
        });
    }

    showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adicionando...';
        button.disabled = true;

        // Simulate async operation
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-check"></i> Adicionado!';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 1000);
        }, 1000);
    }

    setupMicroAnimations() {
        // Add hover effects to interactive elements
        document.querySelectorAll('.interactive-element').forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.transform = 'scale(1.05)';
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'scale(1)';
            });
        });

        // Intersection Observer for animations
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                }
            });
        });

        document.querySelectorAll('.product-cart-wrap').forEach(element => {
            animationObserver.observe(element);
        });
    }

    setupProgressiveEnhancement() {
        // Enhanced form validation
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });

        // Enhanced cart functionality
        this.enhanceCartFunctionality();
    }

    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.showFieldError(field, 'Este campo é obrigatório');
                isValid = false;
            } else {
                this.clearFieldError(field);
            }
        });

        return isValid;
    }

    showFieldError(field, message) {
        field.classList.add('is-invalid');
        let errorElement = field.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains('invalid-feedback')) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }
        errorElement.textContent = message;
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorElement = field.nextElementSibling;
        if (errorElement && errorElement.classList.contains('invalid-feedback')) {
            errorElement.remove();
        }
    }

    enhanceCartFunctionality() {
        // Add quantity controls
        document.querySelectorAll('.qty-val').forEach(input => {
            this.addQuantityControls(input);
        });

        // Enhanced add to cart
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-to-cart-btn')) {
                this.enhancedAddToCart(e.target);
            }
        });
    }

    addQuantityControls(input) {
        const container = input.parentElement;
        const minusBtn = container.querySelector('.qty-down');
        const plusBtn = container.querySelector('.qty-up');

        if (minusBtn) {
            minusBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const currentValue = parseInt(input.value) || 1;
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }

        if (plusBtn) {
            plusBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const currentValue = parseInt(input.value) || 1;
                input.value = currentValue + 1;
                input.dispatchEvent(new Event('change'));
            });
        }
    }

    enhancedAddToCart(button) {
        // Add visual feedback
        const productCard = button.closest('.product-cart-wrap');
        if (productCard) {
            productCard.classList.add('adding-to-cart');
            
            // Create flying cart animation
            this.createFlyingCartAnimation(productCard);
            
            setTimeout(() => {
                productCard.classList.remove('adding-to-cart');
            }, 1000);
        }

        // Update cart counter with animation
        this.updateCartCounter();
    }

    createFlyingCartAnimation(productCard) {
        const productImg = productCard.querySelector('img');
        const cartIcon = document.querySelector('.mini-cart-icon');
        
        if (productImg && cartIcon) {
            const flyingImg = productImg.cloneNode();
            flyingImg.style.cssText = `
                position: fixed;
                z-index: 9999;
                width: 50px;
                height: 50px;
                pointer-events: none;
                transition: all 0.8s cubic-bezier(0.2, 1, 0.3, 1);
            `;
            
            const imgRect = productImg.getBoundingClientRect();
            const cartRect = cartIcon.getBoundingClientRect();
            
            flyingImg.style.left = imgRect.left + 'px';
            flyingImg.style.top = imgRect.top + 'px';
            
            document.body.appendChild(flyingImg);
            
            requestAnimationFrame(() => {
                flyingImg.style.left = cartRect.left + 'px';
                flyingImg.style.top = cartRect.top + 'px';
                flyingImg.style.transform = 'scale(0.1)';
                flyingImg.style.opacity = '0';
            });
            
            setTimeout(() => {
                flyingImg.remove();
            }, 800);
        }
    }

    updateCartCounter() {
        const counters = document.querySelectorAll('.cart-items-count');
        counters.forEach(counter => {
            counter.style.transform = 'scale(1.3)';
            setTimeout(() => {
                counter.style.transform = 'scale(1)';
            }, 200);
        });
    }
}

// Initialize PWA enhancements when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OrganyxPWA();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OrganyxPWA;
}
