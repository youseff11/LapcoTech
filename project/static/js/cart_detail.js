// static/js/cart_detail.js

document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // الدالة الأصلية getCookie لم تعد ضرورية إذا كنت تحصل على الـ CSRF token من الـ DOM
    // ولكن نتركها هنا كمرجع إذا كانت مستخدمة في مكان آخر.
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const updateCartItemQuantity = async (itemId, quantityChange) => {
        // ****** إضافة: تحقق من itemId قبل المتابعة ******
        if (!itemId) {
            console.error('Error: Item ID is missing for quantity update.');
            alert('An error occurred: Item ID is missing. Please refresh the page.');
            return;
        }

        try {
            const response = await fetch('/cart/update_quantity/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ item_id: itemId, quantity_change: quantityChange }),
            });

            // تحقق إذا كانت الاستجابة JSON
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                console.error('Expected JSON response but got:', await response.text());
                throw new TypeError("Expected JSON response from server.");
            }

            const data = await response.json();

            if (data.success) {
                const itemElement = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
                if (itemElement) {
                    if (data.item_removed) {
                        itemElement.remove(); // Remove item from DOM if quantity <= 0
                        if (document.querySelectorAll('.cart-item').length === 0) {
                            // Show empty cart message if no items left
                            document.querySelector('.cart-items-container').innerHTML = '<p class="empty-cart-message">Your cart is empty. <a href="/shop/">Start shopping!</a></p>';
                            document.querySelector('.cart-summary').style.display = 'none'; // Hide summary
                        }
                    } else {
                        // Update quantity and total price for the item
                        itemElement.querySelector('.item-quantity').textContent = data.new_quantity;
                        // ****** تعديل: استخدم parseFloat وتأكد من القيمة قبل toFixed ******
                        const newTotalPriceItem = parseFloat(data.new_total_price_item);
                        if (!isNaN(newTotalPriceItem)) {
                            itemElement.querySelector('.item-total-price').textContent = newTotalPriceItem.toFixed(0);
                        } else {
                            console.warn(`Invalid new_total_price_item received: ${data.new_total_price_item}`);
                            itemElement.querySelector('.item-total-price').textContent = 'N/A'; // أو أي قيمة افتراضية
                        }
                    }
                    // Update overall cart summary
                    // ****** تعديل: استخدم parseFloat وتأكد من القيمة قبل toFixed ******
                    const totalCartPrice = parseFloat(data.total_cart_price);
                    if (!isNaN(totalCartPrice)) {
                        document.getElementById('summary-grand-total').textContent = totalCartPrice.toFixed(0);
                    } else {
                         console.warn(`Invalid total_cart_price received: ${data.total_cart_price}`);
                         document.getElementById('summary-grand-total').textContent = 'N/A';
                    }
                    
                    document.getElementById('summary-total-items').textContent = data.cart_items_count;


                    // Also update the navbar cart count badge if it exists
                    const navCartCountBadge = document.getElementById('cart-count');
                    if (navCartCountBadge) {
                        navCartCountBadge.textContent = data.cart_items_count;
                        navCartCountBadge.classList.add('updated');
                        setTimeout(() => {
                            navCartCountBadge.classList.remove('updated');
                        }, 300);
                    }
                }
                console.log(data.message);
            } else {
                alert(data.message); // يمكنك تغيير هذا إلى SweetAlert2 إذا أردت
            }
        } catch (error) {
            console.error('Error updating cart item quantity:', error);
            alert('An error occurred while updating the cart.'); // يمكنك تغيير هذا إلى SweetAlert2 إذا أردت
        }
    };

    const removeItemFromCart = async (itemId) => {
        // ****** إضافة: تحقق من itemId قبل المتابعة ******
        if (!itemId) {
            console.error('Error: Item ID is missing for remove action.');
            alert('An error occurred: Item ID is missing. Please refresh the page.');
            return;
        }

        if (!confirm('Are you sure you want to remove this item from your cart?')) {
            return; // User cancelled
        }
        try {
            const response = await fetch('/cart/remove/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ item_id: itemId }),
            });

            // تحقق إذا كانت الاستجابة JSON
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                console.error('Expected JSON response but got:', await response.text());
                throw new TypeError("Expected JSON response from server.");
            }

            const data = await response.json();

            if (data.success) {
                const itemElement = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
                if (itemElement) {
                    itemElement.remove(); // Remove item from DOM

                    if (document.querySelectorAll('.cart-item').length === 0) {
                        // Show empty cart message if no items left
                        document.querySelector('.cart-items-container').innerHTML = '<p class="empty-cart-message">Your cart is empty. <a href="/shop/">Start shopping!</a></p>';
                        document.querySelector('.cart-summary').style.display = 'none'; // Hide summary
                    }

                    // Update overall cart summary
                    document.getElementById('summary-total-items').textContent = data.cart_items_count;
                    // ****** تعديل: استخدم parseFloat وتأكد من القيمة قبل toFixed ******
                    const totalCartPrice = parseFloat(data.total_cart_price);
                    if (!isNaN(totalCartPrice)) {
                        document.getElementById('summary-grand-total').textContent = totalCartPrice.toFixed(0);
                    } else {
                         console.warn(`Invalid total_cart_price received: ${data.total_cart_price}`);
                         document.getElementById('summary-grand-total').textContent = 'N/A';
                    }


                    // Also update the navbar cart count badge if it exists
                    const navCartCountBadge = document.getElementById('cart-count');
                    if (navCartCountBadge) {
                        navCartCountBadge.textContent = data.cart_items_count;
                        navCartCountBadge.classList.add('updated');
                        setTimeout(() => {
                            navCartCountBadge.classList.remove('updated');
                        }, 300);
                    }
                }
                console.log(data.message);
            } else {
                alert(data.message); // يمكنك تغيير هذا إلى SweetAlert2 إذا أردت
            }
        } catch (error) {
            console.error('Error removing item from cart:', error);
            alert('An error occurred while removing the item.'); // يمكنك تغيير هذا إلى SweetAlert2 إذا أردت
        }
    };

    // Event listeners for quantity change buttons
    document.querySelectorAll('.quantity-minus').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            updateCartItemQuantity(itemId, -1);
        });
    });

    document.querySelectorAll('.quantity-plus').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            updateCartItemQuantity(itemId, 1);
        });
    });

    // Event listeners for remove item buttons
    document.querySelectorAll('.remove-item-btn').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            removeItemFromCart(itemId);
        });
    });

    // --- NEW: Event listener for "Proceed to Checkout" button ---
    const checkoutButton = document.querySelector('.btn-checkout');

    if (checkoutButton) {
        checkoutButton.addEventListener('click', async function() {
            try {
                const response = await fetch('/cart/check_auth/', { // استدعاء view للتحقق من تسجيل الدخول
                    method: 'GET', // يمكن أن يكون GET لأننا لا نرسل بيانات حساسة
                    headers: {
                        'X-CSRFToken': csrftoken, // لا يزال جيدًا إرسال CSRF حتى في GET إذا كان الـ view يستخدمه
                    },
                });

                // ****** إضافة: تحقق إذا كانت الاستجابة JSON قبل تحليلها ******
                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    console.error('Expected JSON response from /cart/check_auth/ but got:', await response.text());
                    throw new TypeError("Expected JSON response from server for authentication check.");
                }

                const data = await response.json();

                if (data.success && data.is_authenticated) {
                    // المستخدم مسجل الدخول، قم بإعادة التوجيه إلى صفحة الدفع
                    window.location.href = data.redirect_url;
                } else if (!data.is_authenticated) {
                    // المستخدم غير مسجل الدخول، أظهر رسالة SweetAlert2
                    Swal.fire({
                        icon: 'info',
                        title: 'Login Required',
                        text: data.message, // الرسالة من Django view
                        showCancelButton: true,
                        confirmButtonColor: '#0d6efd',
                        cancelButtonColor: '#6c757d',
                        confirmButtonText: 'Log In Now',
                        cancelButtonText: 'Cancel'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            // إذا نقر المستخدم على "Log In Now"، انتقل إلى صفحة تسجيل الدخول
                            window.location.href = data.redirect_url;
                        }
                    });
                } else {
                    // حالة خطأ غير متوقعة
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: data.message || 'An unexpected error occurred while checking authentication.',
                    });
                }
            } catch (error) {
                console.error('Error checking authentication:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Network Error',
                    text: 'Could not connect to the server. Please try again.',
                });
            }
        });
    }
});