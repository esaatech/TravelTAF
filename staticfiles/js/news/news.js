import Dialog from '../utils/dialog.js';

class NewsSubscriptionManager {
    constructor() {
        this.storageKey = 'newsletter_subscribed';
        
        // Fix: Look for the data attribute in the container div instead of body
        const container = document.querySelector('.container[data-user-logged-in]');
        
        // Debug log to check the value
        console.log('Data attribute value:', container?.dataset.userLoggedIn);
        
        // Fix: Convert string 'true'/'false' to actual boolean
        this.isUserLoggedIn = container?.dataset.userLoggedIn === 'true';
        
        // Debug log to check the converted boolean
        console.log('Is user logged in?:', this.isUserLoggedIn);
        
        this.hasCheckedSubscription = false;

        // Get dialog content from data attributes
        this.dialogTitle = container?.dataset.dialogTitle || "Stay Updated with Our Latest News";
        this.dialogBody = container?.dataset.dialogBody || "Subscribe to our newsletter and never miss important updates!";
        
        console.log('Dialog Title:', this.dialogTitle);
        console.log('Dialog Body:', this.dialogBody);
    }

    /**
     * Initialize the subscription manager
     */
    init() {
        // Don't show subscription dialog immediately
        // Wait for some user engagement
        setTimeout(() => this.checkAndShowSubscription(), 5000);
    }

    /**
     * Check if user should see subscription dialog
     * @returns {boolean}
     */
    shouldShowSubscription() {
       
        // Don't show if already checked in this session
        if (this.hasCheckedSubscription) return false;

        // Don't show if user is logged in (assumed subscribed)
        if (this.isUserLoggedIn) return false;

        // Don't show if user previously subscribed
        if (this.isSubscribed()) return false;

        return true;
    }

    /**
     * Check localStorage for subscription status
     * @returns {boolean}
     */
    isSubscribed() {
        return localStorage.getItem(this.storageKey) === 'true';
    }

    /**
     * Mark user as subscribed in localStorage
     */
    markAsSubscribed() {
        localStorage.setItem(this.storageKey, 'true');
        this.hasCheckedSubscription = true;
    }

    /**
     * Validate email format
     * @param {string} email
     * @returns {boolean}
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Handle subscription form submission
     * @param {string} email
     * @returns {Promise}
     */
    async handleSubscribe(email) {
        if (!this.isValidEmail(email)) {
            throw new Error('Please enter a valid email address');
        }

        try {
            // Create form data
            const formData = new FormData();
            formData.append('email', email);
            formData.append('subscription_type', 'news');  // Set subscription type as required by your view

            // Make API call to your backend
            const response = await fetch('/subscribers/subscribe/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Subscription failed');
            }

            // If successful, mark as subscribed
            this.markAsSubscribed();
            return data;
        } catch (error) {
            console.error('Subscription error:', error);
            throw error;
        }
    }

    /**
     * Get CSRF token from cookie
     * @returns {string}
     */
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    /**
     * Show subscription dialog
     */
    showSubscriptionDialog() {
        const dialog = new Dialog({
            title: this.dialogTitle,
            content: `
                <div class="text-center">
                    <p class="text-gray-600 mb-4">${this.dialogBody}</p>
                    <form id="subscribeForm" class="space-y-4">
                        <input type="email" 
                               name="email"
                               required
                               placeholder="Enter your email" 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <p class="error-message text-red-500 mt-2 hidden"></p>
                    </form>
                </div>
            `,
            primaryButtonText: 'Subscribe',
            secondaryButtonText: 'Maybe Later',
            onPrimaryClick: async (dialogInstance) => {
                const form = dialogInstance.element.querySelector('#subscribeForm');
                const emailInput = form.querySelector('input[name="email"]');
                const errorMessage = form.querySelector('.error-message');
                
                try {
                    const result = await this.handleSubscribe(emailInput.value);
                    dialogInstance.close();
                    this.showSuccessMessage(result.message);
                } catch (error) {
                    errorMessage.textContent = error.message;
                    errorMessage.classList.remove('hidden');
                }
            }
        });

        dialog.show();
    }

    /**
     * Show success message after subscription
     */
    showSuccessMessage() {
        const successDialog = new Dialog({
            title: 'Thank You!',
            content: '<p class="text-center text-gray-600">You have successfully subscribed to our newsletter.</p>',
            primaryButtonText: 'OK',
            showClose: false
        });
        successDialog.show();
    }

    /**
     * Check conditions and show subscription dialog if needed
     */
    checkAndShowSubscription() {
        if (this.shouldShowSubscription()) {
            this.showSubscriptionDialog();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const subscriptionManager = new NewsSubscriptionManager();
    subscriptionManager.init();
});