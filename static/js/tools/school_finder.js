console.log("school finder page loaded");


document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const searchForm = document.getElementById('school-search-form');
    const resultsSection = document.getElementById('results-section');
    const schoolsContainer = document.getElementById('schools-container');
    const sortSelect = document.getElementById('sort-select');
    console.log("school finder");
    // Handle form submission
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Form submitted');
        
        // Show loading state
        resultsSection.classList.remove('hidden');
        schoolsContainer.innerHTML = '<div class="col-span-3 text-center py-8">Loading...</div>';
        
        // Get form data
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/tools/school-finder/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.status === 'success') {
                displayResults(data.schools);
            } else {
                displayNoResults(data.message || 'No schools found matching your criteria.');
            }
        } catch (error) {
            console.error('Error:', error);
            displayError('An error occurred while searching. Please try again.');
        }
    });

    // Handle sorting
    sortSelect.addEventListener('change', function() {
        const schools = Array.from(schoolsContainer.children);
        const sortValue = this.value;

        schools.sort((a, b) => {
            if (sortValue === 'tuition-low') {
                return getTuitionValue(a) - getTuitionValue(b);
            } else if (sortValue === 'tuition-high') {
                return getTuitionValue(b) - getTuitionValue(a);
            } else if (sortValue === 'ranking') {
                return getRankingValue(a) - getRankingValue(b);
            }
            return 0;
        });

        schoolsContainer.innerHTML = '';
        schools.forEach(school => schoolsContainer.appendChild(school));
    });

    // Display results function
    function displayResults(schools) {
        schoolsContainer.innerHTML = '';
        
        if (!schools.length) {
            displayNoResults('No schools found matching your criteria.');
            return;
        }

        schools.forEach(school => {
            const schoolCard = document.createElement('div');
            schoolCard.className = 'bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow';
            schoolCard.innerHTML = `
                <div class="p-6">
                    <div class="flex items-center mb-4">
                        <div>
                            <h3 class="text-lg font-semibold">${school.name}</h3>
                            <p class="text-sm text-gray-600">${school.location}</p>
                        </div>
                    </div>
                    <div class="space-y-3">
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-600">Tuition Fee:</span>
                            <span class="font-medium">$${school.tuition.toLocaleString()}/year</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-600">Programs:</span>
                            <span class="font-medium">${school.programs.join(', ')}</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-600">Scholarships:</span>
                            <span class="font-medium text-green-600">
                                ${school.scholarships_available ? 'Available' : 'Not Available'}
                            </span>
                        </div>
                    </div>
                    <div class="mt-6 space-y-3">
                        <a href="/tools/school-finder/details/${school.id}/" 
                           class="block text-center px-4 py-2 bg-[#1980e6] text-white rounded-full hover:bg-blue-700 transition-colors">
                            View Details
                        </a>
                        <a href="${school.website}" 
                           target="_blank"
                           class="block text-center px-4 py-2 border border-[#1980e6] text-[#1980e6] rounded-full hover:bg-blue-50 transition-colors">
                            Visit Website
                        </a>
                    </div>
                </div>
            `;
            schoolsContainer.appendChild(schoolCard);
        });
    }

    // Display no results message
    function displayNoResults(message) {
        schoolsContainer.innerHTML = `
            <div class="col-span-3 text-center py-8">
                <p class="text-gray-600">${message}</p>
                <button onclick="resetFilters()" class="mt-4 text-[#1980e6] hover:underline">
                    Reset Filters
                </button>
            </div>
        `;
    }

    // Display error message
    function displayError(message) {
        schoolsContainer.innerHTML = `
            <div class="col-span-3 text-center py-8">
                <p class="text-red-600">${message}</p>
                <button onclick="retrySearch()" class="mt-4 text-[#1980e6] hover:underline">
                    Try Again
                </button>
            </div>
        `;
    }

    // Helper functions
    function getTuitionValue(schoolCard) {
        const tuition = schoolCard.querySelector('.school-tuition').textContent;
        return parseInt(tuition.replace(/[^0-9]/g, '')) || 0;
    }

    function getRankingValue(schoolCard) {
        const ranking = schoolCard.querySelector('.school-ranking')?.textContent;
        return parseInt(ranking?.match(/\d+/)?.[0]) || 999;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Global functions
    window.resetFilters = function() {
        searchForm.reset();
        resultsSection.classList.add('hidden');
    }

    window.retrySearch = function() {
        searchForm.dispatchEvent(new Event('submit'));
    }

    // Auto-submit on filter changes
    const filterInputs = searchForm.querySelectorAll('select, input[type="checkbox"]');
    filterInputs.forEach(input => {
        input.addEventListener('change', () => {
            if (resultsSection.classList.contains('hidden')) return;
            searchForm.dispatchEvent(new Event('submit'));
        });
    });
});
