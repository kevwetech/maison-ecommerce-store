"use strict"


const subtotal = parseFloat("{{ total }}");
const tax = parseFloat("{{ tax }}");

document.addEventListener('DOMContentLoaded', function() {
    const first = document.querySelector('input[name="delivery_option"]');
    if (first) {
        const price = parseFloat(first.getAttribute('data-price') || 0);
        const name = first.closest('.delivery-option').querySelector('.delivery-name').textContent;
        updateDelivery(price, name);
    }
});

function updateDelivery(price, name) {
    const shippingDisplay = document.getElementById('shipping-display');
    const totalDisplay = document.getElementById('total-display');
    const grandTotal = subtotal + tax + price;
    shippingDisplay.textContent = price === 0 ? 'Free' : '$' + price.toFixed(2);
    totalDisplay.textContent = '$' + grandTotal.toFixed(2);
}