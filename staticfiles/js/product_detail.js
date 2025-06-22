// static/js/product_detail.js

document.addEventListener('DOMContentLoaded', function() {
    const addToCartBtn = document.querySelector('.btn-add-to-cart');
    // Remove these lines as nav.js will handle them:
    // const sideCart = document.getElementById('sideCart');
    // const sideCartItems = document.getElementById('sideCartItems');
    // const cartTotalPrice = document.getElementById('cartTotalPrice');
    // const cartCountBadge = document.getElementById('cart-count');
    // const cartEmptyMessage = document.getElementById('cartEmptyMessage');
    // const openCartBtn = document.getElementById('openCartBtn');
    // const closeCartBtn = document.getElementById('closeCartBtn');
    // const overlay = document.getElementById('overlay');

    // These functions are now handled by nav.js, or will be called from global scope
    // function openSideCart() { /* ... */ }
    // function closeSideCart() { /* ... */ }
    // function updateCartDisplay(cartData) { /* ... */ }
    // async function fetchCartState() { /* ... */ }

    // Remove event listeners for opening/closing cart from here, nav.js handles them.
    // if (openCartBtn) { openCartBtn.addEventListener('click', openSideCart); }
    // if (closeCartBtn) { closeCartBtn.addEventListener('click', closeSideCart); }
    // if (overlay) { overlay.addEventListener('click', function() { /* ... */ }); }

    // No need to fetch cart state here, nav.js does it globally
    // fetchCartState();

    // Add product to cart
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', async function() {
            const productId = this.dataset.productId;

            // Ensure CSRF Token is present
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch('/cart/add/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ product_id: productId, quantity: 1 }), // You can modify quantity
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Failed to add product to cart: ${errorText}`);
                }

                const data = await response.json();

                if (data.success) {
                    console.log('Product added to cart:', data.message);
                    // Call the globally available updateCartDisplay from nav.js
                    if (window.updateCartDisplay) {
                        window.updateCartDisplay(data.cart);
                    }
                    // Open the side cart automatically (this function should also be available globally if needed,
                    // or triggered by updateCartDisplay in nav.js if you prefer)
                    const sideCart = document.getElementById('sideCart');
                    const overlay = document.getElementById('overlay');
                    if (sideCart && overlay) {
                        sideCart.classList.add('open');
                        overlay.classList.add('active');
                        document.body.style.overflow = 'hidden';
                    }
                } else {
                    console.error('Error adding to cart:', data.message);
                    alert('Failed to add product to cart: ' + data.message);
                }

            } catch (error) {
                console.error('Network or server error:', error);
                alert('An error occurred while adding to cart. Please try again.');
            }
        });
    }
});