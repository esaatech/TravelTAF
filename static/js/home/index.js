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



