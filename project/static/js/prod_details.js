// static/js/prod_details.js

document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.getElementById('csrf-token').value;

    const addToCartButton = document.querySelector('.btn-add-to-cart');

    if (addToCartButton) {
        addToCartButton.addEventListener('click', async function(e) {
            e.preventDefault(); // منع السلوك الافتراضي للزر (إذا كان داخل نموذج)

            const productId = this.dataset.productId;
            const quantity = 1; // هذه القيمة يمكن تعديلها لاحقاً إذا أضفت حقل للكمية

            try {
                const response = await fetch('/cart/add/', { // تأكد من أن هذا المسار صحيح في urls.py
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // إرسال الـ CSRF token في الـ header
                    },
                    body: JSON.stringify({ product_id: productId, quantity: quantity })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                if (data.success) {
                    // استخدام SweetAlert2 لتجربة مستخدم أفضل (تأكد من تضمين المكتبة في القالب)
                    Swal.fire({
                        icon: 'success',
                        title: 'Added to Cart!',
                        text: data.message,
                        showConfirmButton: false,
                        timer: 1500
                    });

                    // تحديث عدد المنتجات في سلة التسوق في شريط التنقل (إذا كانت الدالة موجودة)
                    // يجب أن تكون الدالة `updateCartCountBadge` معرفة عالمياً أو متوفرة في النطاق
                    const navCartCountBadge = document.getElementById('cart-count');
                    if (navCartCountBadge) {
                        navCartCountBadge.textContent = data.cart_items_count;
                        navCartCountBadge.classList.add('updated'); // لإضافة تأثير بصري مؤقت
                        setTimeout(() => {
                            navCartCountBadge.classList.remove('updated');
                        }, 300);
                    }

                    // *** تم إزالة السطر المسؤول عن إعادة التوجيه هنا ***
                    // window.location.href = '/cart/'; // هذا السطر هو الذي تم إزالته!

                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error!',
                        text: data.message || 'An error occurred while adding the product to the cart.',
                    });
                }
            } catch (error) {
                console.error('Error adding product to cart:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Unexpected Error!',
                    text: error.message || 'An unexpected error occurred. Please try again.',
                });
            }
        });
    }
});