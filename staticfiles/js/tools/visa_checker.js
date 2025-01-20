/**
 * Visa Requirements Checker
 * 
 * A comprehensive tool for checking visa requirements between countries.
 * Provides detailed visa information, requirements, and processing details.
 * 
 * Data Structure:
 * countries[] - Array of country objects containing:
 *   - code: ISO 2-letter country code
 *   - name: Full country name
 * 
 * Features:
 * - Country selection dropdowns
 * - Country swap functionality
 * - Real-time visa requirement checking
 * - Detailed visa status display
 * - Processing requirements display
 * - Document requirements listing
 * 
 * Required DOM Elements:
 * #fromCountry - Source country dropdown
 * #toCountry - Destination country dropdown
 * #swapCountries - Country swap button
 * #checkRequirements - Submit button
 * #resultsSection - Results container
 * #loadingState - Loading indicator
 * #resultsContent - Results content area
 * #visaStatus - Visa status display
 * #detailedRequirements - Requirements details
 * 
 * Visa Status Types:
 * - visa_required: Standard visa required
 * - visa_free: No visa needed
 * - visa_on_arrival: Visa available at entry
 * - e_visa: Electronic visa available
 * 
 * API Response Structure:
 * {
 *   status: string (visa status type),
 *   details: {
 *     processing_time: string,
 *     validity: string,
 *     cost: string,
 *     max_stay: string,
 *     entry_type: string,
 *     requirements: string[],
 *     additional_info: string[]
 *   }
 * }
 * 
 * Status Display Colors:
 * - visa_required: Red
 * - visa_free: Green
 * - visa_on_arrival: Blue
 * - e_visa: Yellow
 * 
 * Functions:
 * populateCountryDropdowns()
 * - Populates country selection dropdowns
 * - Sorts countries alphabetically
 * - Adds default option
 * 
 * getCookie(name)
 * - Retrieves CSRF token for form submission
 * - Required for POST requests
 * 
 * Error Handling:
 * - Empty country selection validation
 * - API error handling
 * - Network error handling
 * - User feedback display
 * 
 * Security:
 * - CSRF protection
 * - Input validation
 * - Secure form submission
 * 
 * UI Features:
 * - Loading states
 * - Error messages
 * - Dynamic content updates
 * - Responsive design
 * - Color-coded status display
 * 
 * Dependencies:
 * - Modern browser with Fetch API
 * - CSRF token implementation
 * - Tailwind CSS for styling
 * 
 * Browser Support:
 * - Modern browsers with ES6+ support
 * - FormData API support
 * - Fetch API support
 */

// Country data
const countries = [
    {code: 'AF', name: 'Afghanistan'},
    {code: 'AX', name: 'Aland Islands'},
    {code: 'AL', name: 'Albania'},
    {code: 'DZ', name: 'Algeria'},
    {code: 'AS', name: 'American Samoa'},
    {code: 'AD', name: 'Andorra'},
    {code: 'AO', name: 'Angola'},
    {code: 'AI', name: 'Anguilla'},
    {code: 'AQ', name: 'Antarctica'},
    {code: 'AG', name: 'Antigua and Barbuda'},
    {code: 'AR', name: 'Argentina'},
    {code: 'AM', name: 'Armenia'},
    {code: 'AW', name: 'Aruba'},
    {code: 'AU', name: 'Australia'},
    {code: 'AT', name: 'Austria'},
    {code: 'AZ', name: 'Azerbaijan'},
    {code: 'BS', name: 'Bahamas'},
    {code: 'BH', name: 'Bahrain'},
    {code: 'BD', name: 'Bangladesh'},
    {code: 'BB', name: 'Barbados'},
    {code: 'BY', name: 'Belarus'},
    {code: 'BE', name: 'Belgium'},
    {code: 'BZ', name: 'Belize'},
    {code: 'BJ', name: 'Benin'},
    {code: 'BM', name: 'Bermuda'},
    {code: 'BT', name: 'Bhutan'},
    {code: 'BO', name: 'Bolivia'},
    {code: 'BA', name: 'Bosnia and Herzegovina'},
    {code: 'BW', name: 'Botswana'},
    {code: 'BV', name: 'Bouvet Island'},
    {code: 'BR', name: 'Brazil'},
    {code: 'IO', name: 'British Indian Ocean Territory'},
    {code: 'BN', name: 'Brunei Darussalam'},
    {code: 'BG', name: 'Bulgaria'},
    {code: 'BF', name: 'Burkina Faso'},
    {code: 'BI', name: 'Burundi'},
    {code: 'KH', name: 'Cambodia'},
    {code: 'CM', name: 'Cameroon'},
    {code: 'CA', name: 'Canada'},
    {code: 'CV', name: 'Cape Verde'},
    {code: 'KY', name: 'Cayman Islands'},
    {code: 'CF', name: 'Central African Republic'},
    {code: 'TD', name: 'Chad'},
    {code: 'CL', name: 'Chile'},
    {code: 'CN', name: 'China'},
    {code: 'CX', name: 'Christmas Island'},
    {code: 'CC', name: 'Cocos (Keeling) Islands'},
    {code: 'CO', name: 'Colombia'},
    {code: 'KM', name: 'Comoros'},
    {code: 'CG', name: 'Congo'},
    {code: 'CD', name: 'Congo, Democratic Republic'},
    {code: 'CK', name: 'Cook Islands'},
    {code: 'CR', name: 'Costa Rica'},
    {code: 'CI', name: 'Cote D\'Ivoire'},
    {code: 'HR', name: 'Croatia'},
    {code: 'CU', name: 'Cuba'},
    {code: 'CY', name: 'Cyprus'},
    {code: 'CZ', name: 'Czech Republic'},
    {code: 'DK', name: 'Denmark'},
    {code: 'DJ', name: 'Djibouti'},
    {code: 'DM', name: 'Dominica'},
    {code: 'DO', name: 'Dominican Republic'},
    {code: 'EC', name: 'Ecuador'},
    {code: 'EG', name: 'Egypt'},
    {code: 'SV', name: 'El Salvador'},
    {code: 'GQ', name: 'Equatorial Guinea'},
    {code: 'ER', name: 'Eritrea'},
    {code: 'EE', name: 'Estonia'},
    {code: 'ET', name: 'Ethiopia'},
    {code: 'FK', name: 'Falkland Islands'},
    {code: 'FO', name: 'Faroe Islands'},
    {code: 'FJ', name: 'Fiji'},
    {code: 'FI', name: 'Finland'},
    {code: 'FR', name: 'France'},
    {code: 'GF', name: 'French Guiana'},
    {code: 'PF', name: 'French Polynesia'},
    {code: 'TF', name: 'French Southern Territories'},
    {code: 'GA', name: 'Gabon'},
    {code: 'GM', name: 'Gambia'},
    {code: 'GE', name: 'Georgia'},
    {code: 'DE', name: 'Germany'},
    {code: 'GH', name: 'Ghana'},
    {code: 'GI', name: 'Gibraltar'},
    {code: 'GR', name: 'Greece'},
    {code: 'GL', name: 'Greenland'},
    {code: 'GD', name: 'Grenada'},
    {code: 'GP', name: 'Guadeloupe'},
    {code: 'GU', name: 'Guam'},
    {code: 'GT', name: 'Guatemala'},
    {code: 'GG', name: 'Guernsey'},
    {code: 'GN', name: 'Guinea'},
    {code: 'GW', name: 'Guinea-Bissau'},
    {code: 'GY', name: 'Guyana'},
    {code: 'HT', name: 'Haiti'},
    {code: 'HM', name: 'Heard Island & Mcdonald Islands'},
    {code: 'VA', name: 'Holy See (Vatican City State)'},
    {code: 'HN', name: 'Honduras'},
    {code: 'HK', name: 'Hong Kong'},
    {code: 'HU', name: 'Hungary'},
    {code: 'IS', name: 'Iceland'},
    {code: 'IN', name: 'India'},
    {code: 'ID', name: 'Indonesia'},
    {code: 'IR', name: 'Iran'},
    {code: 'IQ', name: 'Iraq'},
    {code: 'IE', name: 'Ireland'},
    {code: 'IM', name: 'Isle Of Man'},
    {code: 'IL', name: 'Israel'},
    {code: 'IT', name: 'Italy'},
    {code: 'JM', name: 'Jamaica'},
    {code: 'JP', name: 'Japan'},
    {code: 'JE', name: 'Jersey'},
    {code: 'JO', name: 'Jordan'},
    {code: 'KZ', name: 'Kazakhstan'},
    {code: 'KE', name: 'Kenya'},
    {code: 'KI', name: 'Kiribati'},
    {code: 'KR', name: 'Korea'},
    {code: 'KW', name: 'Kuwait'},
    {code: 'KG', name: 'Kyrgyzstan'},
    {code: 'LA', name: 'Lao People\'s Democratic Republic'},
    {code: 'LV', name: 'Latvia'},
    {code: 'LB', name: 'Lebanon'},
    {code: 'LS', name: 'Lesotho'},
    {code: 'LR', name: 'Liberia'},
    {code: 'LY', name: 'Libyan Arab Jamahiriya'},
    {code: 'LI', name: 'Liechtenstein'},
    {code: 'LT', name: 'Lithuania'},
    {code: 'LU', name: 'Luxembourg'},
    {code: 'MO', name: 'Macao'},
    {code: 'MK', name: 'Macedonia'},
    {code: 'MG', name: 'Madagascar'},
    {code: 'MW', name: 'Malawi'},
    {code: 'MY', name: 'Malaysia'},
    {code: 'MV', name: 'Maldives'},
    {code: 'ML', name: 'Mali'},
    {code: 'MT', name: 'Malta'},
    {code: 'MH', name: 'Marshall Islands'},
    {code: 'MQ', name: 'Martinique'},
    {code: 'MR', name: 'Mauritania'},
    {code: 'MU', name: 'Mauritius'},
    {code: 'YT', name: 'Mayotte'},
    {code: 'MX', name: 'Mexico'},
    {code: 'FM', name: 'Micronesia'},
    {code: 'MD', name: 'Moldova'},
    {code: 'MC', name: 'Monaco'},
    {code: 'MN', name: 'Mongolia'},
    {code: 'ME', name: 'Montenegro'},
    {code: 'MS', name: 'Montserrat'},
    {code: 'MA', name: 'Morocco'},
    {code: 'MZ', name: 'Mozambique'},
    {code: 'MM', name: 'Myanmar'},
    {code: 'NA', name: 'Namibia'},
    {code: 'NR', name: 'Nauru'},
    {code: 'NP', name: 'Nepal'},
    {code: 'NL', name: 'Netherlands'},
    {code: 'AN', name: 'Netherlands Antilles'},
    {code: 'NC', name: 'New Caledonia'},
    {code: 'NZ', name: 'New Zealand'},
    {code: 'NI', name: 'Nicaragua'},
    {code: 'NE', name: 'Niger'},
    {code: 'NG', name: 'Nigeria'},
    {code: 'NU', name: 'Niue'},
    {code: 'NF', name: 'Norfolk Island'},
    {code: 'MP', name: 'Northern Mariana Islands'},
    {code: 'NO', name: 'Norway'},
    {code: 'OM', name: 'Oman'},
    {code: 'PK', name: 'Pakistan'},
    {code: 'PW', name: 'Palau'},
    {code: 'PS', name: 'Palestine'},
    {code: 'PA', name: 'Panama'},
    {code: 'PG', name: 'Papua New Guinea'},
    {code: 'PY', name: 'Paraguay'},
    {code: 'PE', name: 'Peru'},
    {code: 'PH', name: 'Philippines'},
    {code: 'PN', name: 'Pitcairn'},
    {code: 'PL', name: 'Poland'},
    {code: 'PT', name: 'Portugal'},
    {code: 'PR', name: 'Puerto Rico'},
    {code: 'QA', name: 'Qatar'},
    {code: 'RE', name: 'Reunion'},
    {code: 'RO', name: 'Romania'},
    {code: 'RU', name: 'Russian Federation'},
    {code: 'RW', name: 'Rwanda'},
    {code: 'BL', name: 'Saint Barthelemy'},
    {code: 'SH', name: 'Saint Helena'},
    {code: 'KN', name: 'Saint Kitts and Nevis'},
    {code: 'LC', name: 'Saint Lucia'},
    {code: 'MF', name: 'Saint Martin'},
    {code: 'PM', name: 'Saint Pierre and Miquelon'},
    {code: 'VC', name: 'Saint Vincent and Grenadines'},
    {code: 'WS', name: 'Samoa'},
    {code: 'SM', name: 'San Marino'},
    {code: 'ST', name: 'Sao Tome and Principe'},
    {code: 'SA', name: 'Saudi Arabia'},
    {code: 'SN', name: 'Senegal'},
    {code: 'RS', name: 'Serbia'},
    {code: 'SC', name: 'Seychelles'},
    {code: 'SL', name: 'Sierra Leone'},
    {code: 'SG', name: 'Singapore'},
    {code: 'SK', name: 'Slovakia'},
    {code: 'SI', name: 'Slovenia'},
    {code: 'SB', name: 'Solomon Islands'},
    {code: 'SO', name: 'Somalia'},
    {code: 'ZA', name: 'South Africa'},
    {code: 'GS', name: 'South Georgia and Sandwich Isl.'},
    {code: 'ES', name: 'Spain'},
    {code: 'LK', name: 'Sri Lanka'},
    {code: 'SD', name: 'Sudan'},
    {code: 'SR', name: 'Suriname'},
    {code: 'SJ', name: 'Svalbard and Jan Mayen'},
    {code: 'SZ', name: 'Swaziland'},
    {code: 'SE', name: 'Sweden'},
    {code: 'CH', name: 'Switzerland'},
    {code: 'SY', name: 'Syrian Arab Republic'},
    {code: 'TW', name: 'Taiwan'},
    {code: 'TJ', name: 'Tajikistan'},
    {code: 'TZ', name: 'Tanzania'},
    {code: 'TH', name: 'Thailand'},
    {code: 'TL', name: 'Timor-Leste'},
    {code: 'TG', name: 'Togo'},
    {code: 'TK', name: 'Tokelau'},
    {code: 'TO', name: 'Tonga'},
    {code: 'TT', name: 'Trinidad and Tobago'},
    {code: 'TN', name: 'Tunisia'},
    {code: 'TR', name: 'Turkey'},
    {code: 'TM', name: 'Turkmenistan'},
    {code: 'TC', name: 'Turks and Caicos Islands'},
    {code: 'TV', name: 'Tuvalu'},
    {code: 'UG', name: 'Uganda'},
    {code: 'UA', name: 'Ukraine'},
    {code: 'AE', name: 'United Arab Emirates'},
    {code: 'GB', name: 'United Kingdom'},
    {code: 'US', name: 'United States'},
    {code: 'UM', name: 'United States Outlying Islands'},
    {code: 'UY', name: 'Uruguay'},
    {code: 'UZ', name: 'Uzbekistan'},
    {code: 'VU', name: 'Vanuatu'},
    {code: 'VE', name: 'Venezuela'},
    {code: 'VN', name: 'Vietnam'},
    {code: 'VG', name: 'Virgin Islands, British'},
    {code: 'VI', name: 'Virgin Islands, U.S.'},
    {code: 'WF', name: 'Wallis and Futuna'},
    {code: 'EH', name: 'Western Sahara'},
    {code: 'YE', name: 'Yemen'},
    {code: 'ZM', name: 'Zambia'},
    {code: 'ZW', name: 'Zimbabwe'}
];

// Sort countries by name
countries.sort((a, b) => a.name.localeCompare(b.name));

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const form = document.getElementById('visa-search-form');
    const fromCountry = document.getElementById('fromCountry');
    const toCountry = document.getElementById('toCountry');
    const visaFreeCheck = document.getElementById('visaFreeCheck');
    const etaCheck = document.getElementById('etaCheck');
    const checkRequirements = document.getElementById('checkRequirements');
    const loadingState = document.getElementById('loadingState');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    // Function to handle checkbox changes
    function handleCheckboxChange() {
        console.log('Checkbox change triggered'); // Debug log
        const isEitherChecked = visaFreeCheck.checked || etaCheck.checked;
        
        if (isEitherChecked) {
            toCountry.disabled = true;
            toCountry.value = '';
            toCountry.style.backgroundColor = '#F3F4F6';
            toCountry.style.cursor = 'not-allowed';
            toCountry.classList.add('opacity-50');
        } else {
            toCountry.disabled = false;
            toCountry.style.backgroundColor = '';
            toCountry.style.cursor = '';
            toCountry.classList.remove('opacity-50');
            
            // Ensure the dropdown is properly re-initialized
            if (!toCountry.options.length) {
                populateCountryDropdowns();
            }
        }
        console.log('Destination dropdown state:', {
            disabled: toCountry.disabled,
            value: toCountry.value,
            optionsLength: toCountry.options.length
        }); // Debug log
    }

    function handleCheckRequirements(e) {
        e.preventDefault();
        e.stopPropagation();  // Stop event bubbling
        console.log('Handling check requirements - single call');
        
        const fromCountryValue = fromCountry.value;
        const toCountryValue = toCountry.value;
        
        if (!fromCountryValue) {
            alert('Please select your nationality');
            return false;  // Prevent form submission
        }

        if (!toCountryValue && !visaFreeCheck.checked && !etaCheck.checked) {
            alert('Please select a destination country or search type');
            return false;  // Prevent form submission
        }

        // Show loading state
        loadingState.classList.remove('hidden');
        resultsSection.classList.remove('hidden');
        resultsContent.classList.add('hidden');

        // Prepare form data
        const formData = new FormData();
        formData.append('fromCountry', fromCountryValue);
        
        if (visaFreeCheck.checked) {
            formData.append('searchType', 'visa_free');
        } else if (etaCheck.checked) {
            formData.append('searchType', 'eta');
        } else {
            formData.append('searchType', 'specific');
            formData.append('toCountry', toCountryValue);
        }

        // Make API call
        fetch('/tools/visa-checker/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response received:', data);
            handleResponse(data);
        })
        .catch(error => {
            handleError(error);
            return false;  // Prevent form submission on error
        });

        return false;  // Prevent form submission in all cases
    }

    function handleResponse(data) {
        loadingState.classList.add('hidden');
        resultsContent.classList.remove('hidden');

        // Extract help banner to be reused
        const helpBanner = `
            <div class="bg-blue-50 border-l-4 border-blue-500 p-3 mb-3">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-blue-700">
                            Need help with your visa application or cheap tickets? Call us at <a href="tel:+6132408100" class="font-medium underline">+613 240 8100</a> or email us at <a href="mailto:info@traveltaf.com" class="font-medium underline">info@traveltaf.com</a>
                        </p>
                    </div>
                </div>
            </div>
        `;

        if (!data.success) {
            resultsContent.innerHTML = `
                ${helpBanner}
                <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-3">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                            </svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-yellow-700">
                                Visa information unavailable at the moment. Let our experts assist you with your visa application.
                            </p>
                        </div>
                    </div>
                </div>
            `;
            return;
        }

        const resultsHtml = data.results.map(result => `
            <div class="bg-white rounded-lg shadow-md p-3 mb-2">
                <div class="visa-status ${getStatusColorClass(result.visa_type)} p-2 rounded-lg text-center mb-2">
                    <h2 class="text-xl font-bold">${result.country_name}</h2>
                    <p class="text-sm mt-1">${result.visa_type}</p>
                </div>
                
                <div class="grid md:grid-cols-2 gap-3">
                    <!-- Processing Details Section -->
                    <div class="bg-gray-50 p-2 rounded">
                        <h3 class="font-semibold text-gray-700 mb-1">Processing Details</h3>
                        <div class="grid grid-cols-2 gap-1 text-sm">
                            ${result.processing_time ? `
                                <div class="text-gray-600">Processing Time:</div>
                                <div>${result.processing_time} days</div>
                            ` : ''}
                            
                            ${result.max_stay ? `
                                <div class="text-gray-600">Maximum Stay:</div>
                                <div>${result.max_stay} days</div>
                            ` : ''}
                            
                            <div class="text-gray-600">Multiple Entry:</div>
                            <div>${result.multiple_entry ? 'Yes' : 'No'}</div>
                            
                            ${result.fee ? `
                                <div class="text-gray-600">Fee:</div>
                                <div>${result.fee}</div>
                            ` : ''}
                        </div>
                    </div>

                    <!-- Required Documents Section -->
                    ${result.documents ? `
                        <div class="bg-gray-50 p-2 rounded">
                            <h3 class="font-semibold text-gray-700 mb-1">Required Documents</h3>
                            <div class="whitespace-pre-line text-sm">
                                ${result.documents}
                            </div>
                        </div>
                    ` : ''}
                </div>

                <!-- Additional Notes Section -->
                ${result.notes ? `
                    <div class="mt-2 bg-gray-50 p-2 rounded">
                        <h3 class="font-semibold text-gray-700 mb-1">Additional Notes</h3>
                        <div class="whitespace-pre-line text-sm">
                            ${result.notes}
                        </div>
                    </div>
                ` : ''}

                ${result.last_verified ? `
                    <div class="mt-2 text-xs text-gray-500 text-right">
                        Last verified: ${result.last_verified}
                    </div>
                ` : ''}
            </div>
        `).join('');

        resultsContent.innerHTML = `
            ${helpBanner}
            <div class="mb-2 text-center">
                <h1 class="text-2xl font-bold text-gray-800">${data.title}</h1>
            </div>
            ${resultsHtml}
        `;
    }

    function handleError(error) {
        console.error('Error:', error);
        loadingState.classList.add('hidden');
        resultsContent.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                An error occurred while processing your request.
            </div>
        `;
        resultsContent.classList.remove('hidden');
    }

    // Prevent traditional form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    });

    // Single click handler for the check requirements button
    checkRequirements?.addEventListener('click', handleCheckRequirements);

    visaFreeCheck?.addEventListener('change', function() {
        if (this.checked) {
            etaCheck.checked = false;
            toCountry.disabled = true;
        }
        handleCheckboxChange();
    });

    etaCheck?.addEventListener('change', function() {
        if (this.checked) {
            visaFreeCheck.checked = false;
            toCountry.disabled = true;
        }
        handleCheckboxChange();
    });

    // Initialize dropdowns
    populateCountryDropdowns();
});

// Populate dropdowns function
function populateCountryDropdowns() {
    // Create options HTML for fromCountry (Nigeria only)
    const fromCountryHtml = `
        <option value="">Select country</option>
        <option value="NG">Nigeria</option>
    `;
    
    // Create options HTML for destination countries (all countries)
    let toCountryHtml = '<option value="">Select country</option>';
    countries.sort((a, b) => a.name.localeCompare(b.name))
        .forEach(country => {
            toCountryHtml += `<option value="${country.code}">${country.name}</option>`;
        });
    
    // Set the options for both dropdowns
    fromCountry.innerHTML = fromCountryHtml;
    toCountry.innerHTML = toCountryHtml;
}

// Helper function to get CSRF token
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

function getStatusColorClass(status) {
    switch(status?.toLowerCase()) {
        case 'visa required':
            return 'bg-red-100 text-red-800';
        case 'visa free':
            return 'bg-green-100 text-green-800';
        case 'eta':
        case 'evisa':
            return 'bg-blue-100 text-blue-800';
        default:
            return 'bg-gray-100 text-gray-800';
    }
}