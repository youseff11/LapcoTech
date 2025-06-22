document.addEventListener('DOMContentLoaded', function() {

    const csrftoken = document.getElementById('csrf-token') ? document.getElementById('csrf-token').value : null;

    const shopProductListUrl = typeof window.shopProductListUrl !== 'undefined' ? window.shopProductListUrl : '/shop/';

    const cartItemsContainer = document.querySelector('.cart-items-container');
    const cartTotalValueElement = document.getElementById('cart-total-value');
    let emptyCartMessage = document.getElementById('empty-cart-message');
    const cartTotalSection = document.querySelector('.cart-total');

    function updateNavbarCartCount(newCount) {
        const cartBadgeElement = document.querySelector('.cart-count-badge');
        if (cartBadgeElement) {
            cartBadgeElement.textContent = newCount;
            cartBadgeElement.classList.add('updated');
            setTimeout(() => {
                cartBadgeElement.classList.remove('updated');
            }, 300);
        }
    }

    async function updateCartOnServer(productId, quantity, actionType) {
        let url;
        let bodyData = { 'product_id': productId };

        if (actionType === 'update_quantity') {
            url = '/cart/update-item/';
            bodyData.quantity = quantity;
        } else if (actionType === 'remove_item') {
            url = '/cart/remove-item/';
        } else {
            console.error('Invalid action type for cart update:', actionType);
            return;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(bodyData)
            });

            const contentType = response.headers.get("content-type");
            if (!contentType || contentType.indexOf("application/json") === -1) {
                const errorText = await response.text();
                console.error("Server responded with non-JSON content:", errorText);
                throw new Error("Received non-JSON response from server.");
            }

            const data = await response.json();

            if (data.success) {
                const itemSubtotalSpan = document.getElementById(`subtotal-${productId}`);
                if (itemSubtotalSpan && actionType === 'update_quantity') {
                    itemSubtotalSpan.textContent = parseFloat(data.item_subtotal).toFixed(0); 
                }

                if (cartTotalValueElement) {
                    cartTotalValueElement.textContent = `EGP ${parseFloat(data.cart_total).toFixed(2)}`;
                }

                updateNavbarCartCount(data.cart_item_count);

                if (actionType === 'remove_item' || (actionType === 'update_quantity' && data.quantity === 0)) {
                    const itemElement = document.getElementById(`cart-item-${productId}`);
                    if (itemElement) {
                        itemElement.remove();
                    }
                }
                
                checkCartDisplay();
            } else {
                alert('Error processing cart request: ' + data.message);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('An error occurred: ' + error.message);
            const quantityInput = document.querySelector(`.quantity-input[data-product-id="${productId}"]`);
            if (quantityInput && actionType === 'update_quantity') {
                quantityInput.value = quantityInput.dataset.previousQuantity || 1;
            }
        }
    }

    if (cartItemsContainer) {
        cartItemsContainer.addEventListener('click', async function(event) {
            const target = event.target;

            if (target.classList.contains('quantity-btn')) {
                const productId = target.dataset.productId;
                const action = target.dataset.action;
                const quantityInput = target.closest('.cart-item-details').querySelector('.quantity-input');
                let currentQuantity = parseInt(quantityInput.value);

                quantityInput.dataset.previousQuantity = currentQuantity;

                if (action === 'increase') {
                    currentQuantity++;
                    quantityInput.value = currentQuantity;
                    await updateCartOnServer(productId, currentQuantity, 'update_quantity');
                } else if (action === 'decrease') {
                    if (currentQuantity > 1) {
                        currentQuantity--;
                        quantityInput.value = currentQuantity;
                        await updateCartOnServer(productId, currentQuantity, 'update_quantity');
                    } else {
                        if (confirm('Are you sure you want to remove this product from your cart?')) {
                            await updateCartOnServer(productId, 0, 'remove_item');
                        } else {
                            quantityInput.value = 1;
                        }
                    }
                }

            } else if (target.classList.contains('btn-remove-item')) {
                const productId = target.dataset.productId;
                if (confirm('Are you sure you want to remove this product from your cart?')) {
                    await updateCartOnServer(productId, 0, 'remove_item');
                }
            }
        });

        cartItemsContainer.addEventListener('change', async function(event) {
            const target = event.target;
            if (target.classList.contains('quantity-input')) {
                const productId = target.dataset.productId;
                let newQuantity = parseInt(target.value);
                
                target.dataset.previousQuantity = newQuantity; 

                if (isNaN(newQuantity) || newQuantity < 0) {
                    alert('Please enter a valid quantity (0 or more).');
                    target.value = target.dataset.previousQuantity || 1;
                    return;
                }
                
                if (newQuantity === 0) {
                    if (confirm('Setting the quantity to 0 will remove this item. Are you sure?')) {
                        await updateCartOnServer(productId, 0, 'remove_item');
                    } else {
                        target.value = target.dataset.previousQuantity || 1;
                    }
                } else {
                    await updateCartOnServer(productId, newQuantity, 'update_quantity');
                }
            }
        });
    }

    const confirmOrderBtn = document.querySelector('.btn-checkout');
    if (confirmOrderBtn) {
        confirmOrderBtn.addEventListener('click', async function() {
            const currentTotalText = cartTotalValueElement ? cartTotalValueElement.textContent : 'EGP 0.00';
            const total = parseFloat(currentTotalText.replace('EGP', '').replace(',', '').trim()); 

            if (total <= 0) {
                alert("Your cart is empty or the total is zero. Please add items before confirming your order.");
                return;
            }

            confirmOrderBtn.disabled = true;
            confirmOrderBtn.textContent = 'Processing...';

            try {
                const response = await fetch('/process-order/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({})
                });

                const contentType = response.headers.get("content-type");
                if (contentType && contentType.indexOf("application/json") !== -1) {
                    const data = await response.json();

                    if (data.success) {
                        alert('Order placed successfully! Order ID: ' + data.order_id);
                        cartItemsContainer.innerHTML = '';
                        if (cartTotalValueElement) {
                             cartTotalValueElement.textContent = 'EGP 0.00';
                        }
                        updateNavbarCartCount(0);
                        checkCartDisplay();
                        window.location.href = data.redirect_url || '/';
                    } else {
                        alert('Order submission error: ' + data.message);
                    }
                } else {
                    const errorText = await response.text();
                    console.error("Server responded with non-JSON content:", errorText);
                    alert('Received unexpected response from the server. Please try again or contact support.');
                }
            } catch (error) {
                console.error('Fetch error during order processing:', error);
                alert('An error occurred while placing your order: ' + error.message + '. Please check your connection and try again.');
            } finally {
                confirmOrderBtn.disabled = false;
                confirmOrderBtn.textContent = 'Confirm Order';
            }
        });
    }

    function checkCartDisplay() {
        const actualCartItems = Array.from(cartItemsContainer.children).filter(child => child.classList && child.classList.contains('cart-item'));
        
        if (actualCartItems.length === 0) {
            if (!emptyCartMessage || !document.contains(emptyCartMessage)) {
                emptyCartMessage = document.createElement('p');
                emptyCartMessage.id = 'empty-cart-message';
                emptyCartMessage.style.textAlign = 'center';
                emptyCartMessage.innerHTML = `Your cart is empty. <a href="${shopProductListUrl}">Start shopping!</a>`;
                cartItemsContainer.appendChild(emptyCartMessage);
            }
            emptyCartMessage.style.display = 'block';

            if (cartTotalSection) {
                cartTotalSection.style.display = 'none';
            }
        } else {
            if (emptyCartMessage) {
                emptyCartMessage.style.display = 'none';
            }
            if (cartTotalSection) {
                cartTotalSection.style.display = 'block';
            }
        }
    }

    checkCartDisplay();
});