function initializeSubscriptionForms() {
    const forms = document.querySelectorAll('form[data-subscription-form]');
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get the message div and button
            const messageDiv = this.nextElementSibling;
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            
            // Reset states at the start
            messageDiv.textContent = '';
            messageDiv.className = 'mt-4 text-sm hidden';
            submitButton.textContent = 'Subscribing...';
            submitButton.disabled = true;
            
            try {
                const formData = new FormData(this);
                
                // Ensure subscription type is set
                if (!formData.get('subscription_type')) {
                    formData.append('subscription_type', this.dataset.subscriptionType);
                }

                const response = await fetch('/subscribers/subscribe/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                const data = await response.json();
                
                // Check if the response was successful
                if (response.ok) {
                    messageDiv.textContent = data.message;
                    messageDiv.className = 'mt-4 text-sm text-green-600';
                    if (data.status === 'success') {
                        this.reset();
                        // Save subscription status in local storage
                        localStorage.setItem('newsletter_subscribed', 'true');
                    }
                } else {
                    messageDiv.textContent = data.message || 'An error occurred. Please try again.';
                    messageDiv.className = 'mt-4 text-sm text-red-600';
                }
                
            } catch (error) {
                console.error('Subscription error:', error);
                messageDiv.textContent = 'An error occurred. Please try again.';
                messageDiv.className = 'mt-4 text-sm text-red-600';
            } finally {
                // Always show message and reset button
                messageDiv.classList.remove('hidden');
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            }
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeSubscriptionForms); 