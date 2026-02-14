// Hop & Barley - ultra simple JavaScript
console.log('Hop & Barley JS loaded');

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready');
    
    // Make all cart buttons work
    var cartButtons = document.querySelectorAll('.btn-add-cart, .add-to-cart');
    console.log('Found ' + cartButtons.length + ' cart buttons');
    
    for (var i = 0; i < cartButtons.length; i++) {
        var button = cartButtons[i];
        button.style.cursor = 'pointer';
        
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Get product name
            var productCard = this.closest('.product-card');
            var productName = 'Product';
            if (productCard) {
                var title = productCard.querySelector('.product-title, h3, h4');
                if (title) {
                    productName = title.textContent.trim();
                }
            }
            
            console.log('Added to cart: ' + productName);
            alert(productName + ' added to cart!');
            
            // Visual feedback
            var originalText = this.innerHTML;
            this.innerHTML = 'Added!';
            this.disabled = true;
            
            setTimeout(function() {
                this.innerHTML = originalText;
                this.disabled = false;
            }.bind(this), 2000);
        });
    }
    
    // Make all buttons clickable
    var allButtons = document.querySelectorAll('button');
    for (var i = 0; i < allButtons.length; i++) {
        allButtons[i].style.cursor = 'pointer';
    }
    
    console.log('All buttons activated');
});

// Simple notification function
function showMessage(text) {
    alert(text);
}

// Global function for HTML onclick
window.addToCart = function(productId, productName) {
    alert(productName + ' added to cart!');
    return false;
};

console.log('JS initialization complete');
