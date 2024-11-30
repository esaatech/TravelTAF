// Speak Module
const SpeakModule = {
    elements: {
        elevenLabsWidget: null,
        callButton: null
    },

    init() {
        console.log('1. SpeakModule.init() called');
        this.initializeElements();
        this.attachEventListeners();
        this.initializeElevenLabs();
        console.log('4. SpeakModule initialization complete');
    },

    initializeElements() {
        console.log('2. Initializing elements');
        this.elements.callButton = document.getElementById('callButton');
        console.log('Found call button:', this.elements.callButton);
    },

    initializeElevenLabs() {
        console.log('3. Initializing ElevenLabs');
        const widget = document.createElement('elevenlabs-convai');
        widget.setAttribute('agent-id', 'FyamG7HPN1mpqH5gAcjK');
        widget.style.display = 'none';
        widget.style.width = '100px';
        widget.style.height = '100px';
        widget.style.backgroundColor = 'white';
        widget.style.border = '1px solid #ccc';
        widget.style.borderRadius = '8px';
        widget.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        document.body.appendChild(widget);
        
        widget.innerHTML = '<div style="padding: 20px;">Loading ElevenLabs widget...</div>';
        
        const script = document.createElement('script');
        script.src = 'https://elevenlabs.io/convai-widget/index.js';
        script.async = true;
        script.type = 'text/javascript';
        
        script.onerror = () => {
            console.error('Failed to load ElevenLabs script');
            widget.innerHTML = '<div style="padding: 20px; color: red;">Failed to load ElevenLabs widget</div>';
        };
        
        document.body.appendChild(script);
        console.log('ElevenLabs script added');

        this.elements.elevenLabsWidget = widget;
    },

    attachEventListeners() {
        console.log('2.5. Attaching event listeners');
        
        if (!this.elements.callButton) {
            console.error('Call button not found during event attachment!');
            return;
        }

        this.elements.callButton.addEventListener('click', (e) => {
            console.log('Button clicked!');
            e.preventDefault();
            console.log('Calling toggleCallWidget');
            this.toggleCallWidget();
        });

        document.addEventListener('click', (e) => {
            console.log('Document clicked, checking if should hide widget');
            if (this.elements.elevenLabsWidget &&
                !this.elements.elevenLabsWidget.contains(e.target) &&
                !this.elements.callButton.contains(e.target)) {
                console.log('Hiding widget');
                this.elements.elevenLabsWidget.style.display = 'none';
            }
        });
    },

    toggleCallWidget() {
        console.log('Inside toggleCallWidget');
        console.log('Widget element:', this.elements.elevenLabsWidget);

        if (this.elements.elevenLabsWidget) {
            const isVisible = this.elements.elevenLabsWidget.style.display !== 'none';
            console.log('Current visibility:', !isVisible);
            
            if (isVisible) {
                this.elements.elevenLabsWidget.style.display = 'none';
            } else {
                // Position the widget relative to the call button
                const buttonRect = this.elements.callButton.getBoundingClientRect();
                
                this.elements.elevenLabsWidget.style.display = 'block';
                this.elements.elevenLabsWidget.style.position = 'fixed';
                this.elements.elevenLabsWidget.style.bottom = '150px'; // Position above the call button
                this.elements.elevenLabsWidget.style.right = '20px';   // Align with the call button
                this.elements.elevenLabsWidget.style.zIndex = '1000';
            }
        } else {
            console.error('ElevenLabs widget not initialized!');
        }
    }
};

// Initialize when DOM is loaded
console.log('Setting up DOMContentLoaded listener');
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    SpeakModule.init();
});
