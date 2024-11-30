// Speak Module
const SpeakModule = {
    elements: {
        elevenLabsWidget: null,
        callButton: null
    },

    // Initialize the speak module
    init() {
        this.initializeElements();
        this.attachEventListeners();
        this.initializeElevenLabs();
    },

    // Initialize DOM elements
    initializeElements() {
        this.elements.callButton = document.getElementById('callButton');
    },

    // Initialize ElevenLabs
    initializeElevenLabs() {
        // Create widget element
        const widget = document.createElement('elevenlabs-convai');
        widget.setAttribute('agent-id', 'FyamG7HPN1mpqH5gAcjK');
        widget.style.display = 'none'; // Hide initially
        document.body.appendChild(widget);

        // Load ElevenLabs script
        const script = document.createElement('script');
        script.src = 'https://elevenlabs.io/convai-widget/index.js';
        script.async = true;
        script.type = 'text/javascript';
        document.body.appendChild(script);

        this.elements.elevenLabsWidget = widget;
    },

    // Attach event listeners
    attachEventListeners() {
        // Call button
        this.elements.callButton.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default tel: behavior

            // Toggle widget visibility
            this.toggleCallWidget();
        });

        // Add click outside listener for widget
        document.addEventListener('click', (e) => {
            if (this.elements.elevenLabsWidget &&
                !this.elements.elevenLabsWidget.contains(e.target) &&
                !this.elements.callButton.contains(e.target)) {
                this.elements.elevenLabsWidget.style.display = 'none';
            }
        });
    },

    // Toggle widget visibility
    toggleCallWidget() {
        if (this.elements.elevenLabsWidget) {
            const isVisible = this.elements.elevenLabsWidget.style.display !== 'none';
            this.elements.elevenLabsWidget.style.display = isVisible ? 'none' : 'block';

            // Position the widget near the chat
            if (!isVisible) {
                const chatPopup = document.getElementById('chatPopup');
                const rect = chatPopup.getBoundingClientRect();

                this.elements.elevenLabsWidget.style.position = 'fixed';
                this.elements.elevenLabsWidget.style.top = `${rect.top}px`;
                this.elements.elevenLabsWidget.style.right = `${window.innerWidth - rect.right}px`;
                this.elements.elevenLabsWidget.style.zIndex = '1000';
            }
        }
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    SpeakModule.init();
});
