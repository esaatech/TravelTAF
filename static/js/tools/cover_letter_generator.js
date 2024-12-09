document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('coverLetterForm');
    const results = document.getElementById('results');
    const coverLetterContent = document.getElementById('coverLetterContent');
    const manualEntrySection = document.getElementById('manual-entry-section');
    const uploadSection = document.getElementById('upload-section');
    const structuredJobSection = document.getElementById('structured-job-section');
    const unstructuredJobSection = document.getElementById('unstructured-job-section');
    
    // Toggle sections based on input method
    form.querySelectorAll('input[name="input_method"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'manual') {
                manualEntrySection.classList.remove('hidden');
                uploadSection.classList.add('hidden');
            } else {
                manualEntrySection.classList.add('hidden');
                uploadSection.classList.remove('hidden');
            }
        });
    });

    // Toggle job details sections based on input method
    document.querySelectorAll('input[name="job_input_method"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'structured') {
                structuredJobSection.classList.remove('hidden');
                unstructuredJobSection.classList.add('hidden');
                // Disable unstructured fields
                unstructuredJobSection.querySelectorAll('textarea').forEach(textarea => {
                    textarea.disabled = true;
                });
                // Enable structured fields
                structuredJobSection.querySelectorAll('input, textarea').forEach(input => {
                    input.disabled = false;
                });
            } else {
                structuredJobSection.classList.add('hidden');
                unstructuredJobSection.classList.remove('hidden');
                // Enable unstructured fields
                unstructuredJobSection.querySelectorAll('textarea').forEach(textarea => {
                    textarea.disabled = false;
                });
                // Disable structured fields
                structuredJobSection.querySelectorAll('input, textarea').forEach(input => {
                    input.disabled = true;
                });
            }
        });
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating...
        `;

        try {
            // Get form data
            const formData = new FormData(form);
            
            // Determine which endpoint to use based on input method
            const inputMethod = form.querySelector('input[name="input_method"]:checked').value;
            const endpoint = inputMethod === 'manual' ? '/tools/generate-cover-letter/' : '/tools/generate-cover-letter-raw/';

            // Send request to backend
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to generate cover letter');
            }

            const data = await response.json();

            // Display the generated cover letter
            coverLetterContent.innerHTML = data.cover_letter;
            results.classList.remove('hidden');
            results.scrollIntoView({ behavior: 'smooth' });

            // Setup copy button
            const copyButton = document.getElementById('copyButton');
            copyButton.addEventListener('click', () => {
                navigator.clipboard.writeText(coverLetterContent.textContent)
                    .then(() => {
                        copyButton.textContent = 'Copied!';
                        setTimeout(() => {
                            copyButton.textContent = 'Copy to Clipboard';
                        }, 2000);
                    });
            });

            // Setup edit button
            const editButton = document.getElementById('editButton');
            editButton.addEventListener('click', () => {
                const content = coverLetterContent.innerHTML;
                coverLetterContent.contentEditable = true;
                coverLetterContent.focus();
                editButton.textContent = 'Save Changes';
                editButton.onclick = () => {
                    coverLetterContent.contentEditable = false;
                    editButton.textContent = 'Edit Letter';
                    editButton.onclick = null;
                };
            });

        } catch (error) {
            console.error('Error:', error);
            showError('Failed to generate cover letter. Please try again.');
        } finally {
            // Reset button state
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
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

    // Helper function to show errors
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded';
        errorDiv.innerHTML = `
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-red-700">${message}</p>
                </div>
            </div>
        `;
        form.insertBefore(errorDiv, form.firstChild);
        setTimeout(() => errorDiv.remove(), 5000);
    }
});