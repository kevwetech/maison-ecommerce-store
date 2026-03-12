const cards = document.querySelectorAll('.category-card');

cards.forEach(card => card.classList.add('hidden'));

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.remove('hidden');
                entry.target.classList.add('visible');
            }, index * 100);
        }
    });
}, { threshold: 0.1 });

cards.forEach(card => observer.observe(card));