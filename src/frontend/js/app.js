// src/frontend/js/app.js

document.addEventListener('DOMContentLoaded', () => {
    // STATE
    let state = {
        products: [],
        cart: JSON.parse(localStorage.getItem('shop_cart')) || {}, // { product_id: quantity }
        user: { email: localStorage.getItem('user_email') || null },
        authMode: 'login' // 'login' or 'register'
    };

    // DOM ELEMENTS
    const els = {
        // App
        productsGrid: document.getElementById('products-grid'),
        loadingProducts: document.getElementById('loading-products'),
        emptyProducts: document.getElementById('products-empty'),
        toast: document.getElementById('toast'),
        toastMessage: document.getElementById('toast-message'),
        
        // Cart
        cartSidebar: document.getElementById('cart-sidebar'),
        cartToggleBtn: document.getElementById('cart-toggle'),
        cartCloseBtn: document.getElementById('cart-close'),
        backdrop: document.getElementById('backdrop'),
        cartBadge: document.getElementById('cart-badge'),
        cartItemsContainer: document.getElementById('cart-items'),
        cartTotal: document.getElementById('cart-total'),
        cartEmptyText: document.getElementById('cart-empty-text'),
        
        // Auth
        authSection: document.getElementById('auth-section'),
        userSection: document.getElementById('user-section'),
        userEmail: document.getElementById('user-email'),
        btnLoginModal: document.getElementById('btn-login-modal'),
        btnRegisterModal: document.getElementById('btn-register-modal'),
        btnLogout: document.getElementById('btn-logout'),
        
        // Auth MOdal
        authModal: document.getElementById('auth-modal'),
        authModalContent: document.getElementById('auth-modal-content'),
        modalClose: document.getElementById('modal-close'),
        modalTitle: document.getElementById('modal-title'),
        modalSubtitle: document.getElementById('modal-subtitle'),
        authForm: document.getElementById('auth-form'),
        authEmail: document.getElementById('auth-email'),
        authPassword: document.getElementById('auth-password'),
        btnAuthSubmitText: document.querySelector('#btn-auth-submit span'),
        authSpinner: document.getElementById('auth-spinner'),
        authError: document.getElementById('auth-error'),
        modalSwitchText: document.getElementById('modal-switch-text'),
        btnSwitchAuth: document.getElementById('btn-switch-auth'),
    };

    // ==========================================
    // INITIALIZATION
    // ==========================================
    init();

    async function init() {
        console.log("App initialization started...");
        try {
            updateNavbarAuth();
            bindEvents();
            console.log("Events bound successfully");
            await loadProducts();
            updateCartUI();
            console.log("App initialization complete");
        } catch (err) {
            console.error("Error during app initialization:", err);
            showToast('Initialization error: ' + err.message, true);
        }
    }

    // ==========================================
    // EVENTS BINDING
    // ==========================================
    function bindEvents() {
        // Auth modals
        els.btnLoginModal.addEventListener('click', () => openAuthModal('login'));
        els.btnRegisterModal.addEventListener('click', () => openAuthModal('register'));
        els.btnSwitchAuth.addEventListener('click', toggleAuthMode);
        els.modalClose.addEventListener('click', closeAuthModal);
        els.authForm.addEventListener('submit', handleAuthSubmit);
        els.btnLogout.addEventListener('click', logout);
        
        // Modal Backdrop auto-close
        els.authModal.addEventListener('click', (e) => {
            if (e.target === els.authModal) closeAuthModal();
        });

        // Cart
        els.cartToggleBtn.addEventListener('click', openCart);
        els.cartCloseBtn.addEventListener('click', closeCart);
        els.backdrop.addEventListener('click', () => { closeCart(); closeAuthModal(); });
    }

    // ==========================================
    // CATALOG & PRODUCTS LOGIC
    // ==========================================
    async function loadProducts() {
        els.loadingProducts.classList.remove('hidden');
        els.productsGrid.innerHTML = '';
        els.emptyProducts.classList.add('hidden');

        try {
            // Using our ApiService
            const response = await ApiService.getProducts();
            state.products = response.items || [];
            
            if (state.products.length === 0) {
                els.emptyProducts.classList.remove('hidden');
            } else {
                renderProducts();
            }
        } catch (error) {
            console.error("Error loading products:", error);
            showToast('Ошибка загрузки товаров: ' + error.message, true);
        } finally {
            els.loadingProducts.classList.add('hidden');
        }
    }

    function renderProducts() {
        els.productsGrid.innerHTML = state.products.map(product => `
            <div class="bg-card border border-gray-800 rounded-xl overflow-hidden hover:border-gray-600 transition group flex flex-col">
                <div class="h-48 bg-darker flex items-center justify-center p-4">
                    <div class="w-full h-full bg-gray-800/50 rounded flex items-center justify-center">
                        <span class="text-4xl">🛍️</span>
                    </div>
                </div>
                <div class="p-5 flex-1 flex flex-col justify-between">
                    <div>
                        <h3 class="text-lg font-bold text-white mb-1 line-clamp-1">${product.name}</h3>
                        <p class="text-sm text-gray-400 mb-4 line-clamp-2">${product.description || 'Не указано'}</p>
                    </div>
                    <div class="flex items-center justify-between mt-auto">
                        <span class="text-xl font-bold text-white">${product.price} ₽</span>
                        <button onclick="window.addToCart(${product.id})" class="h-10 w-10 bg-gray-800 hover:bg-primary text-white rounded-lg flex items-center justify-center transition group-hover:shadow-lg group-hover:shadow-primary/30">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // ==========================================
    // CART LOGIC
    // ==========================================
    window.addToCart = (productId) => {
        if (!state.cart[productId]) {
            state.cart[productId] = 1;
        } else {
            state.cart[productId]++;
        }
        saveCart();
        updateCartUI();
        
        const product = state.products.find(p => p.id === productId);
        showToast(`Добавлено: ${product?.name || 'Товар'}`);
    };

    window.removeFromCart = (productId) => {
        delete state.cart[productId];
        saveCart();
        updateCartUI();
    };

    window.updateCartQuantity = (productId, delta) => {
        if (!state.cart[productId]) return;
        state.cart[productId] += delta;
        if (state.cart[productId] <= 0) {
            delete state.cart[productId];
        }
        saveCart();
        updateCartUI();
    };

    function saveCart() {
        localStorage.setItem('shop_cart', JSON.stringify(state.cart));
    }

    function updateCartUI() {
        // Update badge count
        const totalItems = Object.values(state.cart).reduce((a, b) => a + b, 0);
        els.cartBadge.textContent = totalItems;
        
        // Determine cart content on frontend to avoid GET with body issue in JS fetch
        const cartProducts = Object.keys(state.cart).map(idStr => {
            const id = parseInt(idStr);
            const product = state.products.find(p => p.id === id);
            return {
                id,
                qty: state.cart[id],
                product
            };
        }).filter(item => item.product); // Filter out if products aren't loaded yet

        if (cartProducts.length === 0) {
            els.cartEmptyText.classList.remove('hidden');
            els.cartItemsContainer.innerHTML = '';
            els.cartTotal.textContent = '0 ₽';
            return;
        }

        els.cartEmptyText.classList.add('hidden');
        
        let html = '';
        let totalPrice = 0;

        cartProducts.forEach((item) => {
            const itemTotal = item.product.price * item.qty;
            totalPrice += itemTotal;
            html += `
                <div class="flex gap-4 p-3 bg-darker rounded-lg border border-gray-800">
                    <div class="flex-1">
                        <h4 class="text-white text-sm font-bold truncate">${item.product.name}</h4>
                        <p class="text-primary font-medium text-sm mt-1">${item.product.price} ₽</p>
                        
                        <div class="flex items-center gap-3 mt-3">
                            <button onclick="window.updateCartQuantity(${item.id}, -1)" class="w-6 h-6 bg-gray-800 hover:bg-gray-700 rounded flex items-center justify-center text-gray-300">-</button>
                            <span class="text-white text-sm w-4 text-center">${item.qty}</span>
                            <button onclick="window.updateCartQuantity(${item.id}, 1)" class="w-6 h-6 bg-gray-800 hover:bg-gray-700 rounded flex items-center justify-center text-gray-300">+</button>
                            <button onclick="window.removeFromCart(${item.id})" class="ml-auto text-xs text-red-500 hover:text-red-400">Удалить</button>
                        </div>
                    </div>
                </div>
            `;
        });

        els.cartItemsContainer.innerHTML = html;
        els.cartTotal.textContent = `${totalPrice} ₽`;
    }

    function openCart() {
        els.cartSidebar.classList.remove('translate-x-full');
        els.backdrop.classList.remove('hidden');
    }

    function closeCart() {
        els.cartSidebar.classList.add('translate-x-full');
        els.backdrop.classList.add('hidden');
    }

    // ==========================================
    // AUTH LOGIC
    // ==========================================
    function updateNavbarAuth() {
        if (state.user.email) {
            els.authSection.classList.add('hidden');
            els.userSection.classList.remove('hidden');
            els.userEmail.textContent = state.user.email;
        } else {
            els.authSection.classList.remove('hidden');
            els.userSection.classList.add('hidden');
            els.userEmail.textContent = '';
        }
    }

    function openAuthModal(mode) {
        state.authMode = mode;
        updateAuthModalUI();
        els.authModal.classList.remove('hidden');
        els.authError.classList.add('hidden');
        els.authEmail.value = '';
        els.authPassword.value = '';
    }

    function closeAuthModal() {
        els.authModal.classList.add('hidden');
    }

    function toggleAuthMode() {
        state.authMode = state.authMode === 'login' ? 'register' : 'login';
        updateAuthModalUI();
        els.authError.classList.add('hidden');
    }

    function updateAuthModalUI() {
        if (state.authMode === 'login') {
            els.modalTitle.textContent = 'Вход';
            els.modalSubtitle.textContent = 'Рады видеть вас снова!';
            els.btnAuthSubmitText.textContent = 'Войти';
            els.modalSwitchText.textContent = 'Нет аккаунта?';
            els.btnSwitchAuth.textContent = 'Регистрация';
        } else {
            els.modalTitle.textContent = 'Регистрация';
            els.modalSubtitle.textContent = 'Создайте новый аккаунт';
            els.btnAuthSubmitText.textContent = 'Зарегистрироваться';
            els.modalSwitchText.textContent = 'Уже есть аккаунт?';
            els.btnSwitchAuth.textContent = 'Войти';
        }
    }

    async function handleAuthSubmit(e) {
        e.preventDefault();
        const email = els.authEmail.value;
        const password = els.authPassword.value;

        // UI Loading state
        els.authSpinner.classList.remove('hidden');
        els.authError.classList.add('hidden');
        els.btnAuthSubmitText.parentElement.disabled = true;

        try {
            if (state.authMode === 'register') {
                await ApiService.register(email, password);
                showToast('Успешная регистрация! Выполняется вход...');
                // Auto-login after register
                const data = await ApiService.login(email, password);
                finalizeLogin(data.access_token, email);
            } else {
                const data = await ApiService.login(email, password);
                finalizeLogin(data.access_token, email);
            }
        } catch (error) {
            els.authError.textContent = error.message;
            els.authError.classList.remove('hidden');
        } finally {
            els.authSpinner.classList.add('hidden');
            els.btnAuthSubmitText.parentElement.disabled = false;
        }
    }

    function finalizeLogin(token, email) {
        localStorage.setItem('access_token', token);
        localStorage.setItem('user_email', email);
        state.user.email = email;
        
        updateNavbarAuth();
        closeAuthModal();
        showToast('Добро пожаловать!');
    }

    function logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_email');
        state.user.email = null;
        updateNavbarAuth();
        showToast('Вы успешно вышли из системы');
    }

    // ==========================================
    // UTILITIES
    // ==========================================
    let toastTimeout;
    function showToast(message, isError = false) {
        els.toastMessage.textContent = message;
        
        if (isError) {
            els.toast.classList.add('border-red-500', 'bg-red-900/50');
            els.toast.classList.remove('border-gray-700', 'bg-card');
        } else {
            els.toast.classList.add('border-gray-700', 'bg-card');
            els.toast.classList.remove('border-red-500', 'bg-red-900/50');
        }

        els.toast.classList.remove('translate-x-full', 'opacity-0');
        
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            els.toast.classList.add('translate-x-full', 'opacity-0');
        }, 3000);
    }
});
