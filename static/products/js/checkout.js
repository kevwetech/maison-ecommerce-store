"use strict"


const subtotal = {{ total|default:0 }};
const tax = {{ tax|default:0 }};

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
    shippingDisplay.textContent = price === 0 ? 'Free' : '₦' + price.toFixed(2);
    totalDisplay.textContent = '₦' + grandTotal.toFixed(2);
}



function updateDeliveryFromEvent(radio) {
    let price = parseFloat(radio.dataset.price || 0);
    const freeAbove = parseFloat(radio.dataset.freeAbove || 0);

    // Apply free shipping logic
    if (freeAbove && subtotal >= freeAbove) {
        price = 0;
    }

    const name = radio.closest('.delivery-option').querySelector('.delivery-name').textContent;

    const shippingDisplay = document.getElementById('shipping-display');
    const totalDisplay = document.getElementById('total-display');
    const grandTotal = subtotal + tax + price;

    shippingDisplay.textContent = price === 0 ? 'Free' : '₦' + price.toFixed(2);
    totalDisplay.textContent = '₦' + grandTotal.toFixed(2);
}