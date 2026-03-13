"use strict"

document.addEventListener('DOMContentLoaded', function() {
    const qtyDisplay = document.getElementById('quantity');
    const qtyInput = document.getElementById('quantityInput');
    let qty = 1;

    document.getElementById('increaseBtn').addEventListener('click', () => {
        qty++;
        qtyDisplay.textContent = qty;
        qtyInput.value = qty;
    });

    document.getElementById('decreaseBtn').addEventListener('click', () => {
        if (qty > 1) {
            qty--;
            qtyDisplay.textContent = qty;
            qtyInput.value = qty;
        }
    });
});


const slides = document.querySelectorAll('.slide');
const thumbs = document.querySelectorAll('.thumb');
let current = 0;

function showSlide(index) {
    slides.forEach(s => s.classList.remove('active'));
    thumbs.forEach(t => t.classList.remove('active'));
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    thumbs[current].classList.add('active');
}

document.getElementById('prevBtn')?.addEventListener('click', () => showSlide(current - 1));
document.getElementById('nextBtn')?.addEventListener('click', () => showSlide(current + 1));

thumbs.forEach((thumb, i) => {
    thumb.addEventListener('click', () => showSlide(i));
});




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