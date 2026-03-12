"use strict"

// Search toggle
const icon = document.getElementById('searchIcon');
const box = document.querySelector('.search-toggle');

if (icon && box) {
    icon.addEventListener('click', () => {
        box.classList.toggle('active');
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // Search toggle
    const icon = document.getElementById('searchIcon');
    const box = document.querySelector('.search-toggle');

    if (icon && box) {
        icon.addEventListener('click', () => {
            box.classList.toggle('active');
        });
    }

    // Hamburger menu
    const menuToggle = document.getElementById('menuToggle');
    const menuPanel = document.getElementById('menuPanel');
    const menuClose = document.getElementById('menuClose');

    if (menuToggle && menuPanel) {
        menuToggle.addEventListener('click', () => {
            menuPanel.classList.toggle('active');
        });
    }

    if (menuClose && menuPanel) {
        menuClose.addEventListener('click', () => {
            menuPanel.classList.remove('active');
        });
    }
});

setTimeout(() => {
        document.querySelectorAll('.toast-message').forEach(toast => {
            toast.style.transition = 'opacity 0.3s ease';
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        });
    }, 4000);

