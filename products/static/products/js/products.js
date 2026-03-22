"use strict"

// ── Price Range (Desktop) ────────────────
const range = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');

function setFill(el, display) {
    const percent = (el.value - el.min) / (el.max - el.min) * 100;
    el.style.setProperty('--fill', percent + '%');
    if (display) display.textContent = el.value;
}

if (range) {
    range.addEventListener('input', () => setFill(range, priceValue));
    setFill(range, priceValue);
    range.addEventListener('change', () => applyFilters());
}

// ── Price Range (Mobile) ─────────────────
const rangeMobile = document.getElementById('priceRangeMobile');
const priceValueMobile = document.getElementById('priceValueMobile');

if (rangeMobile) {
    rangeMobile.addEventListener('input', () => setFill(rangeMobile, priceValueMobile));
    setFill(rangeMobile, priceValueMobile);
}

// ── Category Filter (Desktop) ────────────
document.querySelectorAll('.cat-filter').forEach(radio => {
    radio.addEventListener('change', () => applyFilters());
});

// ── Search (Desktop) ─────────────────────
const searchInput = document.getElementById('searchInput');
let searchTimer;
if (searchInput) {
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => applyFilters(), 500);
    });
}

// ── Search (Mobile) ──────────────────────
const searchInputMobile = document.getElementById('searchInputMobile');
if (searchInputMobile) {
    searchInputMobile.addEventListener('input', () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => applyFilters(true), 500);
    });
}

// ── Apply Filters ─────────────────────────
function applyFilters(fromMobile = false) {
    const search = fromMobile
        ? searchInputMobile?.value
        : searchInput?.value || searchInputMobile?.value || '';

    const catDesktop = document.querySelector('.cat-filter:checked')?.value || '';
    const catMobile = document.querySelector('.cat-filter-mobile:checked')?.value || '';
    const category = catDesktop || catMobile;

    const maxPrice = fromMobile
        ? (rangeMobile?.value || 2000)
        : (range?.value || 2000);

    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (category) params.set('category', category);
    if (maxPrice && maxPrice != 2000) params.set('max_price', maxPrice);

    window.location.href = `${window.location.pathname}?${params.toString()}`;
}

// ── Mobile Drawer ─────────────────────────
const filterToggle = document.getElementById('filterToggle');
const filterDrawer = document.getElementById('filterDrawer');
const drawerOverlay = document.getElementById('drawerOverlay');
const drawerClose = document.getElementById('drawerClose');
const applyFiltersBtn = document.getElementById('applyFilters');

function openDrawer() {
    filterDrawer.classList.add('open');
    drawerOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
}

function closeDrawer() {
    filterDrawer.classList.remove('open');
    drawerOverlay.classList.remove('open');
    document.body.style.overflow = '';
}

if (filterToggle) filterToggle.addEventListener('click', openDrawer);
if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);
if (applyFiltersBtn) applyFiltersBtn.addEventListener('click', () => applyFilters(true));

// ── Add to Cart (AJAX) ────────────────────
document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const form = this.closest('form');
        if (!form) return;
        const url = form.action;
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(res => res.json())
        .then(data => {
           if (data.success) {
           const cartCount = document.getElementById('cart-count');
           if (cartCount) {
                cartCount.textContent = data.cart_count;
                cartCount.style.display = 'flex';
            }
            btn.innerHTML = '<i class="fa-solid fa-check"></i> Added!';
            setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-bag-shopping"></i> Add to Cart';
            }, 1500);

        // ← Add this toast notification
            const productName = btn.closest('.product-card')?.querySelector('h4')?.textContent || 'Product';
            showToast(`✓ ${productName} added to cart!`);
           }
        });
    });
});

function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: #1a1a1a;
        color: #fff;
        padding: 14px 20px;
        border-radius: 10px;
        font-size: 14px;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.3s ease;
        font-family: 'Inter', sans-serif;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.style.opacity = '1', 10);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


// Scroll animations for product cards
const cards = document.querySelectorAll('.product-card');

// First hide them via JS, then animate in
cards.forEach(card => card.classList.add('hidden'));

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.remove('hidden');
                entry.target.classList.add('visible');
            }, index * 80);
        }
    });
}, { threshold: 0.1 });

cards.forEach(card => observer.observe(card));



function toggleWishlist(productId, btn) {
    fetch(`/products/wishlist/toggle/${productId}/`, {
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
    })
    .then(res => res.json())
    .then(data => {
        const icon = btn.querySelector('i');
        if (data.status === 'added') {
            icon.classList.remove('fa-regular');
            icon.classList.add('fa-solid');
        } else {
            icon.classList.remove('fa-solid');
            icon.classList.add('fa-regular');
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}