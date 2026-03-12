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
