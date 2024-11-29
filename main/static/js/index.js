document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.querySelector('input[placeholder="Enter a country or region"]');
    const searchButton = document.querySelector('button span.truncate').closest('button');
    
    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value;
        // Add your search logic here
        console.log('Searching for:', searchTerm);
    });

    // Comparison button functionality
    const compareButton = document.querySelector('button span.truncate:last-of-type').closest('button');
    compareButton.addEventListener('click', function() {
        // Add your comparison logic here
        console.log('Starting comparison');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chatToggle');
    const chatPopup = document.getElementById('chatPopup');
    const chatClose = document.getElementById('chatClose');

    chatToggle.addEventListener('click', () => {
        chatPopup.classList.add('active');
    });

    chatClose.addEventListener('click', () => {
        chatPopup.classList.remove('active');
    });

    // Close chat when clicking outside
    document.addEventListener('click', (e) => {
        if (!chatPopup.contains(e.target) && !chatToggle.contains(e.target)) {
            chatPopup.classList.remove('active');
        }
    });
});
