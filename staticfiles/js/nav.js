// static/js/nav.js

document.addEventListener('DOMContentLoaded', function() {

    // ... (Existing mobile menu and user dropdown logic) ...

    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('overlay');
    const closeMenu = document.getElementById('closeMenu');
    const hamburgerLines = document.querySelectorAll('.hamburger-line');
    const navItems = document.querySelectorAll('.mobile-nav-item');

    let isMenuOpen = false;

    function openMenu() {
        mobileMenu.classList.add('open');
        if (overlay) overlay.classList.add('active');
        menuToggle.setAttribute('aria-expanded', 'true');
        isMenuOpen = true;
    }

    function closeMenuHandler() {
        mobileMenu.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
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

        if (overlay) {
            overlay.addEventListener('click', closeMenuHandler);
        }

        navItems.forEach(item => {
            item.addEventListener('click', function() {
                // Prevent closing menu if it's a dropdown toggle itself
                if (this.textContent.includes('▼') || this.textContent.includes('+')) {
                    return;
                }
                closeMenuHandler();
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
            e.stopPropagation(); // Prevent the document click listener from immediately closing it
            userDropdownMenu.classList.toggle('active');
        });

        // Close user dropdown if clicked outside
        document.addEventListener('click', function(e) {
            if (!userMenuContainer.contains(e.target) && userDropdownMenu.classList.contains('active')) {
                userDropdownMenu.classList.remove('active');
            }
        });
    }

    const openCartBtn = document.getElementById('openCartBtn');
    const sideCart = document.getElementById('sideCart');
    const closeCartBtn = document.getElementById('closeCartBtn');
    const sideCartItems = document.getElementById('sideCartItems'); // Add this
    const cartTotalPrice = document.getElementById('cartTotalPrice'); // Add this
    const cartCountBadge = document.getElementById('cart-count'); // Add this
    const cartEmptyMessage = document.getElementById('cartEmptyMessage'); // Add this


    function openSideCart() {
        sideCart.classList.add('open');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when cart is open
        if (isMenuOpen) { // Close mobile menu if it's open when cart is opened
            closeMenuHandler();
        }
    }

    function closeSideCart() {
        sideCart.classList.remove('open');
        overlay.classList.remove('active');
        document.body.style.overflow = ''; // Re-enable scrolling
    }

    if (openCartBtn) {
        openCartBtn.addEventListener('click', openSideCart);
    }

    if (closeCartBtn) {
        closeCartBtn.addEventListener('click', closeSideCart);
    }

    if (overlay) {
        overlay.addEventListener('click', function() {
            closeSideCart();
            closeMenuHandler(); // Ensure mobile menu also closes
        });
    }

    // Close side cart and mobile menu with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeSideCart();
            closeMenuHandler();
        }
    });

    // NEW: Mobile Shop Dropdown Toggle
    const mobileDropbtn = document.querySelector('.mobile-dropbtn');
    const mobileDropdownContent = document.querySelector('.mobile-dropdown-content');

    if (mobileDropbtn && mobileDropdownContent) {
        mobileDropbtn.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            mobileDropdownContent.classList.toggle('show');

            // Change button text based on dropdown state
            if (mobileDropdownContent.classList.contains('show')) {
                mobileDropbtn.textContent = 'Shop -';
            } else {
                mobileDropbtn.textContent = 'Shop +';
            }
        });
    }

    // --- START Cart Logic for Navbar ---

    // Function to update cart display based on fetched data
    window.updateCartDisplay = function(cartData) { // Make it global for product_detail.js to use
        sideCartItems.innerHTML = ''; // Clear current content
        let total = 0;

        if (cartData && Object.keys(cartData).length > 0) {
            cartEmptyMessage.style.display = 'none'; // Hide "Your cart is empty" message
            for (const productId in cartData) {
                const item = cartData[productId];
                const itemElement = document.createElement('div');
                itemElement.classList.add('side-cart-item');
                itemElement.innerHTML = `
                    <img src="${item.image_url || '/static/images/placeholder.jpg'}" alt="${item.name}" class="side-cart-item-image">
                    <div class="side-cart-item-details">
                        <span class="side-cart-item-name">${item.name}</span>
                        <span class="side-cart-item-price">${item.qty} x ${item.price} EGP</span>
                    </div>
                    <button class="remove-item-btn" data-product-id="${productId}">×</button>
                `;
                sideCartItems.appendChild(itemElement);
                total += parseFloat(item.price) * item.qty;
            }
        } else {
            cartEmptyMessage.style.display = 'block'; // Show "Your cart is empty" message
        }

        cartTotalPrice.textContent = `${total.toFixed(0)} EGP`; // Update total price
        cartCountBadge.textContent = Object.keys(cartData).length; // Update product count

        // Add visual effect when count updates
        cartCountBadge.classList.add('updated');
        setTimeout(() => {
            cartCountBadge.classList.remove('updated');
        }, 300);

        // Add event listeners for "remove" buttons
        document.querySelectorAll('.remove-item-btn').forEach(button => {
            button.addEventListener('click', async function() {
                const productIdToRemove = this.dataset.productId;
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                try {
                    const response = await fetch(`/cart/remove/${productIdToRemove}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify({ product_id: productIdToRemove }),
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.message || 'Failed to remove item from cart.');
                    }

                    const data = await response.json();
                    if (data.success) {
                        console.log('Product removed from cart:', data.message);
                        updateCartDisplay(data.cart); // Update cart display with new data
                    } else {
                        console.error('Error removing from cart:', data.message);
                        alert('Failed to remove item: ' + data.message);
                    }

                } catch (error) {
                    console.error('Network or server error during removal:', error);
                    alert('An error occurred while removing from cart. Please try again.');
                }
            });
        });
    }

    // Function to fetch cart state from the backend
    async function fetchCartState() {
        try {
            const response = await fetch('/cart/summary_api/');
            if (!response.ok) {
                throw new Error('Failed to fetch cart state.');
            }
            const cartData = await response.json();
            updateCartDisplay(cartData);
        } catch (error) {
            console.error('Error fetching cart state:', error);
            // Optionally display an error message to the user
        }
    }

    // Fetch cart state when the nav.js script loads (on every page load)
    fetchCartState();

    // --- END Cart Logic for Navbar ---
});