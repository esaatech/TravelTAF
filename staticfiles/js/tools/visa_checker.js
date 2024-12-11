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
    const fromCountry = document.getElementById('fromCountry');
    const toCountry = document.getElementById('toCountry');
    
    // Populate dropdowns
    function populateCountryDropdowns() {
        const defaultOption = '<option value="">Select country</option>';
        const countryOptions = countries.map(country => 
            `<option value="${country.code}">${country.name}</option>`
        ).join('');
        
        fromCountry.innerHTML = defaultOption + countryOptions;
        toCountry.innerHTML = defaultOption + countryOptions;
    }

    // Initialize dropdowns
    populateCountryDropdowns();

    // Add swap functionality
    document.getElementById('swapCountries').addEventListener('click', function() {
        const temp = fromCountry.value;
        fromCountry.value = toCountry.value;
        toCountry.value = temp;
    });

    // Handle form submission
    document.getElementById('checkRequirements').addEventListener('click', function() {
        const fromCountry = document.getElementById('fromCountry').value;
        const toCountry = document.getElementById('toCountry').value;
        
        if (!fromCountry || !toCountry) {
            alert('Please select both countries');
            return;
        }

        // Show loading state
        document.getElementById('resultsSection').classList.remove('hidden');
        document.getElementById('loadingState').classList.remove('hidden');
        document.getElementById('resultsContent').classList.add('hidden');

        // Send request to backend
        const formData = new FormData();
        formData.append('fromCountry', fromCountry);
        formData.append('toCountry', toCountry);

        fetch('/tools/visa-checker/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                // Remove Content-Type header to let the browser set it with boundary
                // 'Content-Type': 'application/x-www-form-urlencoded'
            },
            credentials: 'same-origin' // Include cookies in the request
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data); // Debug log
            
            // Hide loading state
            document.getElementById('loadingState').classList.add('hidden');
            document.getElementById('resultsContent').classList.remove('hidden');

            // Update visa status
            const statusColors = {
                'visa_required': 'bg-red-100 text-red-800',
                'visa_free': 'bg-green-100 text-green-800',
                'visa_on_arrival': 'bg-blue-100 text-blue-800',
                'e_visa': 'bg-yellow-100 text-yellow-800'
            };

            const statusText = {
                'visa_required': 'Visa Required',
                'visa_free': 'Visa Free',
                'visa_on_arrival': 'Visa on Arrival',
                'e_visa': 'E-Visa Available'
            };

            document.getElementById('visaStatus').className = `p-4 rounded-lg text-center ${statusColors[data.status]}`;
            document.getElementById('visaStatus').innerHTML = `
                <h2 class="text-2xl font-bold">${statusText[data.status]}</h2>
            `;

            // Update detailed requirements
            document.getElementById('detailedRequirements').innerHTML = `
                <div class="grid md:grid-cols-2 gap-6">
                    <div>
                        <h3 class="font-bold mb-2">Processing Details</h3>
                        <ul class="space-y-2">
                            <li>Processing Time: ${data.details.processing_time}</li>
                            <li>Validity: ${data.details.validity}</li>
                            <li>Cost: ${data.details.cost}</li>
                            <li>Maximum Stay: ${data.details.max_stay}</li>
                            <li>Entry Type: ${data.details.entry_type}</li>
                        </ul>
                    </div>
                    <div>
                        <h3 class="font-bold mb-2">Required Documents</h3>
                        <ul class="list-disc pl-4 space-y-1">
                            ${data.details.requirements.map(req => `<li>${req}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                <div class="mt-6">
                    <h3 class="font-bold mb-2">Additional Information</h3>
                    <ul class="list-disc pl-4 space-y-1">
                        ${data.details.additional_info.map(info => `<li>${info}</li>`).join('')}
                    </ul>
                </div>
            `;
        })
        .catch(error => {
            console.error('Full error:', error); // Debug log
            document.getElementById('loadingState').classList.add('hidden');
            document.getElementById('resultsContent').innerHTML = `
                <div class="text-red-600 text-center">
                    <p>Error: ${error.message}</p>
                    <p class="text-sm mt-2">Please try again or contact support if this persists.</p>
                </div>
            `;
            document.getElementById('resultsContent').classList.remove('hidden');
        });
    });

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
});