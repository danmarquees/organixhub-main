// Simple filter plugin fallback
(function($) {
    'use strict';
    
    // Don't override jQuery's native filter - just add custom filtering
    window.filterProducts = function(category) {
        const products = document.querySelectorAll('.product-item');
        products.forEach(product => {
            if (category === 'all' || product.dataset.category === category) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    };
    
    // Custom product filter function
    $.fn.productFilter = function(options) {
        return this.each(function() {
            const $element = $(this);
            // Custom filter logic here
        });
    };
    
})(jQuery);
