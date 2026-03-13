"use strict"


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

                const productName = btn.closest('.grid1')?.querySelector('p')?.textContent || 'Product';
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


// Scroll animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.15 });

document.querySelectorAll('.scroll-animate, .scroll-animate-left, .scroll-animate-right')
    .forEach(el => observer.observe(el));