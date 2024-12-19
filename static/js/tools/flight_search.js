// Utility class for handling flight search results
class FlightResultsManager {
    constructor(options = {}) {
        // Initialize configuration
        this.config = {
            resultsPerPage: options.resultsPerPage || 10,
            sortField: options.sortField || 'price',
            sortOrder: options.sortOrder || 'asc',
            container: options.container || document.getElementById('resultsGrid'),
            paginationContainer: options.paginationContainer || document.getElementById('paginationContainer')
        };

        // Initialize state
        this.state = {
            currentPage: 1,
            allResults: [],
            filteredResults: []
        };

        // Bind methods
        this.handleSort = this.handleSort.bind(this);
        this.handlePageChange = this.handlePageChange.bind(this);
    }

    // Set new results and reset pagination
    setResults(results) {
        this.state.allResults = results;
        this.state.filteredResults = [...results];
        this.state.currentPage = 1;
        this.sortResults();
        this.render();
    }

    // Sort results based on current configuration
    sortResults() {
        this.state.filteredResults.sort((a, b) => {
            const aValue = a[this.config.sortField];
            const bValue = b[this.config.sortField];

            if (this.config.sortField === 'duration') {
                // Special handling for duration
                return this.config.sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
            }

            if (this.config.sortField === 'price') {
                return this.config.sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
            }

            // Default string comparison
            return this.config.sortOrder === 'asc' ? 
                aValue.localeCompare(bValue) : 
                bValue.localeCompare(aValue);
        });
    }

    // Handle sort change
    handleSort(field, order) {
        this.config.sortField = field;
        this.config.sortOrder = order;
        this.sortResults();
        this.render();
    }

    // Handle page change
    handlePageChange(page) {
        this.state.currentPage = page;
        this.renderResults();
        window.scrollTo({
            top: this.config.container.offsetTop - 100,
            behavior: 'smooth'
        });
    }

    // Render pagination controls
    renderPagination() {
        const totalPages = Math.ceil(this.state.filteredResults.length / this.config.resultsPerPage);
        const pagination = document.createElement('div');
        pagination.className = 'flex justify-center space-x-2 mt-6';

        // Previous button
        if (this.state.currentPage > 1) {
            const prevButton = this.createPaginationButton('Previous', this.state.currentPage - 1);
            pagination.appendChild(prevButton);
        }

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = this.createPaginationButton(i.toString(), i, i === this.state.currentPage);
            pagination.appendChild(pageButton);
        }

        // Next button
        if (this.state.currentPage < totalPages) {
            const nextButton = this.createPaginationButton('Next', this.state.currentPage + 1);
            pagination.appendChild(nextButton);
        }

        this.config.paginationContainer.innerHTML = '';
        this.config.paginationContainer.appendChild(pagination);
    }

    // Create pagination button element
    createPaginationButton(text, page, isActive = false) {
        const button = document.createElement('button');
        button.className = `px-4 py-2 rounded ${isActive ? 
            'bg-blue-600 text-white' : 
            'bg-white text-gray-700 hover:bg-gray-50 border'}`;
        button.textContent = text;
        button.addEventListener('click', () => this.handlePageChange(page));
        return button;
    }

    // Render a single result card
    renderResultCard(result) {
        return `
            <div class="bg-white rounded-lg shadow-sm p-6 border hover:shadow-md transition-shadow">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <div class="flex items-center space-x-4 mb-4">
                            <span class="text-lg font-semibold">${result.destination}</span>
                            <div class="flex items-center text-gray-500">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M10.293 15.707a1 1 0 010-1.414L12.586 12H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
                            <div>
                                <p class="font-medium">Departure</p>
                                <p>${new Date(result.departure_date).toLocaleDateString()}</p>
                            </div>
                            ${result.return_date ? `
                                <div>
                                    <p class="font-medium">Return</p>
                                    <p>${new Date(result.return_date).toLocaleDateString()}</p>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-2xl font-bold text-[#1980e6]">€${result.price}</div>
                    </div>
                </div>
            </div>
        `;
    }

    // Render current page results
    renderResults() {
        const startIndex = (this.state.currentPage - 1) * this.config.resultsPerPage;
        const endIndex = startIndex + this.config.resultsPerPage;
        const pageResults = this.state.filteredResults.slice(startIndex, endIndex);

        this.config.container.innerHTML = pageResults
            .map(result => this.renderResultCard(result))
            .join('');
    }

    // Render everything (results and pagination)
    render() {
        this.renderResults();
        this.renderPagination();
    }
}
