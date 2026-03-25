// src/frontend/js/api.js

const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
    static getHeaders(isForm = false) {
        const token = localStorage.getItem('access_token');
        const headers = {};
        if (!isForm) {
            headers['Content-Type'] = 'application/json';
        }
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const response = await fetch(url, {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers
            }
        });
        
        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = { detail: response.statusText };
            }
            // Fix unhandled array details if validation error
            const detailMsg = Array.isArray(errorData.detail) 
                ? errorData.detail.map(e => e.msg).join(', ') 
                : errorData.detail || 'API request failed';
            throw new Error(detailMsg);
        }
        
        if (response.status === 204) return null;
        return response.json();
    }

    // AUTHENTICATION
    static async login(email, password) {
        const formData = new URLSearchParams();
        formData.append("username", email); // fastapi_users expects 'username' field, we use email
        formData.append("password", password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Неверный логин или пароль');
        }
        return response.json();
    }

    static async register(email, password) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, password, is_active: true, is_superuser: false, is_verified: false })
        });
    }

    // CATALOG
    static async getProducts() {
        return this.request('/products/');
    }

    static async getCategories() {
        return this.request('/categories/');
    }

    // CART
    static async getCart(cartData) {
        return this.request('/cart/cart', {
            method: 'POST',
            body: JSON.stringify(cartData || {})
        });
    }

    static async addToCart(productId, quantity, cartData) {
        return this.request('/cart/add', {
            method: 'POST',
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity,
                cart: cartData || {}
            })
        });
    }

    static async updateCart(productId, quantity, cartData) {
        return this.request('/cart/update', {
            method: 'PUT',
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity,
                cart: cartData || {}
            })
        });
    }

    static async removeFromCart(productId, cartData) {
        return this.request(`/cart/remove/${productId}`, {
            method: 'DELETE',
            body: JSON.stringify({
                cart: cartData || {}
            })
        });
    }
}
