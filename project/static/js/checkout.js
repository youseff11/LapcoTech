// static/js/checkout.js

document.addEventListener('DOMContentLoaded', function() {
    // الحصول على CSRF token من meta tag أو حقل مخفي
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // الحصول على بيانات السلة من الـ script tag
    const cartDataElement = document.getElementById('cart-data');
    let cartData = null; // تهيئة cartData بـ null

    if (cartDataElement) {
        try {
            cartData = JSON.parse(cartDataElement.textContent);
            console.log("Cart Data from Django:", cartData);

            // تحديث إجمالي السعر المعروض في صفحة الدفع
            const checkoutGrandTotalElement = document.getElementById('checkoutGrandTotal');
            if (checkoutGrandTotalElement && cartData && !isNaN(parseFloat(cartData.total_price))) {
                checkoutGrandTotalElement.textContent = parseFloat(cartData.total_price).toFixed(0);
            }
        } catch (e) {
            console.error("Failed to parse cart data JSON:", e);
            // عرض رسالة خطأ للمستخدم إذا فشل تحليل بيانات السلة
            Swal.fire({
                icon: 'error',
                title: 'خطأ في تحميل السلة!',
                text: 'حدثت مشكلة أثناء تحميل معلومات السلة. يرجى محاولة تحديث الصفحة.',
                confirmButtonText: 'موافق'
            });
            // لا تتوقف عن التنفيذ هنا لأن النموذج قد لا يزال صالحًا لغير المستخدمين المسجلين
        }
    } else {
        console.error("Cart data script tag with ID 'cart-data' not found.");
        // إذا لم يتم العثور على العنصر، قد تكون هناك مشكلة في القالب
    }

    // الحصول على نموذج الشحن
    const shippingForm = document.getElementById('shippingForm');
    if (shippingForm) {
        shippingForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // منع الإرسال الافتراضي للنموذج

            const formData = new FormData(shippingForm);
            const shippingInfo = {};
            // جمع البيانات من حقول النموذج في كائن shippingInfo
            for (let [key, value] of formData.entries()) {
                // استبعاد csrfmiddlewaretoken من الـ shippingInfo لأنه يتم إرساله في الـ headers
                if (key !== 'csrfmiddlewaretoken') {
                    shippingInfo[key] = value;
                }
            }

            try {
                const response = await fetch('/cart/place_order/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // استخدام الـ CSRF token من الـ DOM
                    },
                    // إرسال shippingInfo إلى backend. cart_data غير ضرورية هنا لأن الـ backend يحصل عليها من الـ session/user
                    body: JSON.stringify({ shipping_info: shippingInfo }),
                });

                // التحقق من نوع المحتوى لضمان أنه JSON
                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    console.error('Expected JSON response from /cart/place_order/ but got:', await response.text());
                    throw new TypeError("Expected JSON response from server for place order.");
                }

                const data = await response.json(); // تحليل الاستجابة كـ JSON

                if (data.success) {
                    // عرض رسالة نجاح باستخدام SweetAlert
                    Swal.fire({
                        icon: 'success',
                        title: 'تم إتمام الطلب بنجاح!',
                        text: data.message,
                        showConfirmButton: false, // لا تظهر زر التأكيد
                        timer: 2000 // الرسالة ستختفي بعد 2 ثانية
                    }).then(() => {
                        // بعد إغلاق SweetAlert أو انتهاء المؤقت، قم بإعادة التوجيه
                        window.location.href = data.redirect_url;
                    });
                } else {
                    let errorMessage = data.message || 'حدث خطأ أثناء إتمام طلبك.';
                    // عرض أخطاء التحقق من النموذج تحت الحقول المناسبة
                    if (data.errors) {
                        // إزالة رسائل الأخطاء السابقة لمنع التكرار
                        document.querySelectorAll('.error-message').forEach(el => el.remove());

                        for (const field in data.errors) {
                            // البحث عن حقل الإدخال بالـ ID (مثال: 'id_first_name' لـ 'first_name')
                            const inputField = document.getElementById(`id_${field}`);
                            if (inputField) {
                                const errorElement = document.createElement('p');
                                errorElement.classList.add('error-message');
                                errorElement.style.color = 'red';
                                errorElement.textContent = data.errors[field].join(' '); // عرض جميع الأخطاء للحقل
                                // إدراج رسالة الخطأ بعد الحقل مباشرة
                                inputField.parentNode.insertBefore(errorElement, inputField.nextSibling);
                            } else {
                                // إذا لم يتم العثور على الحقل، أضف الخطأ إلى الرسالة العامة لـ SweetAlert
                                errorMessage += `\n${field}: ${data.errors[field].join(', ')}`;
                            }
                        }
                    }
                    // عرض رسالة خطأ عامة باستخدام SweetAlert
                    Swal.fire({
                        icon: 'error',
                        title: 'خطأ في الطلب!',
                        text: errorMessage,
                        confirmButtonText: 'حاول مرة أخرى'
                    });
                }
            } catch (error) {
                console.error('Error placing order:', error);
                // عرض رسالة خطأ للشبكة أو الأخطاء غير المتوقعة
                Swal.fire({
                    icon: 'error',
                    title: 'خطأ في الشبكة!',
                    text: 'تعذر الاتصال بالخادم أو حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.',
                    confirmButtonText: 'موافق'
                });
            }
        });
    } else {
        console.error("Shipping form with ID 'shippingForm' not found.");
    }
});