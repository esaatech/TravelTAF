document.addEventListener('DOMContentLoaded', function() {
    // Other existing code...
});

// FAQ Toggle Function
function toggleFAQ(button) {
    // Get the content div that follows the button
    const content = button.nextElementSibling;
    
    // Get the arrow icon
    const arrow = button.querySelector('svg');
    
    // Close all other FAQs
    const allFAQs = document.querySelectorAll('.border.rounded-lg.divide-y .p-4');
    allFAQs.forEach(faq => {
        if (faq !== button.parentElement) {
            const otherContent = faq.querySelector('div.hidden, div:not(.hidden)');
            const otherArrow = faq.querySelector('svg');
            if (otherContent && !otherContent.classList.contains('hidden')) {
                otherContent.classList.add('hidden');
                otherArrow.style.transform = 'rotate(0deg)';
            }
        }
    });
    
    // Toggle current FAQ
    content.classList.toggle('hidden');
    
    // Rotate arrow
    arrow.style.transform = content.classList.contains('hidden') 
        ? 'rotate(0deg)' 
        : 'rotate(180deg)';
}

// Optional: Add keyboard accessibility
document.addEventListener('DOMContentLoaded', function() {
    const faqButtons = document.querySelectorAll('.border.rounded-lg.divide-y button');
    
    faqButtons.forEach(button => {
        button.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleFAQ(button);
            }
        });
    });
});



