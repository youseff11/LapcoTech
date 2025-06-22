// static/js/navv.js

document.addEventListener('DOMContentLoaded', function() {

    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeMenu = document.getElementById('closeMenu');

    let isMenuOpen = false;

    function openMenu() {
        mobileMenu.classList.add('open');
        document.body.style.overflow = 'hidden';
        isMenuOpen = true;
    }

    function closeMenuHandler() {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
        isMenuOpen = false;
    }

    if (menuToggle && mobileMenu && closeMenu) {
        menuToggle.addEventListener('click', function() {
            if (!isMenuOpen) {
                openMenu();
            } else {
                closeMenuHandler();
            }
        });

        closeMenu.addEventListener('click', closeMenuHandler);

        document.querySelectorAll('.mobile-dropdown .mobile-nav-item').forEach(item => {
            item.addEventListener('click', function(e) {
                if (this.classList.contains('mobile-dropbtn')) {
                    e.stopPropagation();
                } else {
                    closeMenuHandler();
                }
            });
        });

        window.addEventListener('resize', function() {
            if (window.innerWidth > 768 && isMenuOpen) {
                closeMenuHandler();
            }
        });

        menuToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });

        closeMenu.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    }

    const userMenuContainer = document.querySelector('.user-menu-container');
    const userIconTrigger = document.querySelector('.user-icon-trigger');
    const userDropdownMenu = document.querySelector('.user-dropdown-menu');

    if (userIconTrigger && userDropdownMenu && userMenuContainer) {
        userIconTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            userDropdownMenu.classList.toggle('active');
        });

        document.addEventListener('click', function(e) {
            if (!userMenuContainer.contains(e.target) && userDropdownMenu.classList.contains('active')) {
                userDropdownMenu.classList.remove('active');
            }
        });
    }

    const cartCountBadge = document.getElementById('cart-count');
    const openCartBtn = document.getElementById('openCartBtn'); // Get the cart link element

    // هذه الدالة تقوم بتحديث عداد العربة بصريًا
    window.updateCartCountBadge = function(count) {
        if (cartCountBadge) {
            cartCountBadge.textContent = count;
            // إضافة وإزالة كلاس 'updated' لتحريك العداد أو إعطاء تأثير بصري
            cartCountBadge.classList.add('updated');
            setTimeout(() => {
                cartCountBadge.classList.remove('updated');
            }, 300);
        }
    };

    // عند تحميل الصفحة، احصل على العدد الأولي لعناصر العربة من السمة data-initial-cart-count
    // هذه القيمة يجب أن يتم توفيرها بشكل ديناميكي بواسطة الخادم في كل مرة يتم فيها عرض الصفحة.
    if (openCartBtn && cartCountBadge) {
        const initialCount = parseInt(openCartBtn.dataset.initialCartCount || '0');
        window.updateCartCountBadge(initialCount);
    }
});