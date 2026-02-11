// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Кнопки добавления в корзину
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            alert('Товар добавлен в корзину!');
        });
    });
});