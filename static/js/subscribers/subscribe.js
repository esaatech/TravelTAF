function initializeSubscriptionForms() {
    const forms = document.querySelectorAll('form[data-subscription-form]');
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const messageDiv = this.nextElementSibling;
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            
            // Disable the submit button and show loading state
            submitButton.disabled = true;
            submitButton.textContent = 'Subscribing...';
            
            try {
                const formData = new FormData(this);
                // Add subscription type based on form data attribute
                formData.append('subscription_type', this.dataset.subscriptionType);

                const response = await fetch('/subscribers/subscribe/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                const data = await response.json();
                
                messageDiv.textContent = data.message;
                messageDiv.className = data.status === 'success' 
                    ? 'mt-4 text-sm text-green-600' 
                    : 'mt-4 text-sm text-red-600';
                
                if (data.status === 'success') {
                    this.reset();
                }
                
                // Show the message div
                messageDiv.classList.remove('hidden');
                
            } catch (error) {
                messageDiv.textContent = 'An error occurred. Please try again.';
                messageDiv.className = 'mt-4 text-sm text-red-600';
                messageDiv.classList.remove('hidden');
            } finally {
                // Re-enable the submit button and restore original text
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', initializeSubscriptionForms); 