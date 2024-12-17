/**
 * SpeakModule - ElevenLabs Voice Integration
 * 
 * A module that integrates ElevenLabs' conversational AI widget into the application.
 * Provides voice interaction capabilities through a floating widget interface.
 * 
 * Module Structure:
 * {
 *   elements: {
 *     elevenLabsWidget: ElevenLabs widget instance
 *     callButton: Button to toggle widget visibility
 *   }
 * }
 * 
 * Required DOM Elements:
 * #callButton - Button element to trigger widget display
 * 
 * Initialization Flow:
 * 1. init() - Main initialization function
 * 2. initializeElements() - DOM element setup
 * 3. attachEventListeners() - Event binding
 * 4. initializeElevenLabs() - Widget creation and setup
 * 
 * Widget Configuration:
 * - agent-id: 'FyamG7HPN1mpqH5gAcjK'
 * - Dimensions: 100px x 100px
 * - Styling: White background, rounded corners, shadow
 * - Position: Fixed, bottom-right corner
 * 
 * Functions:
 * 
 * init()
 * - Entry point for module initialization
 * - Coordinates all setup functions
 * - Logs initialization progress
 * 
 * initializeElements()
 * - Finds and stores DOM element references
 * - Sets up initial element state
 * 
 * initializeElevenLabs()
 * - Creates ElevenLabs widget element
 * - Loads required script
 * - Handles loading errors
 * - Sets initial widget styling
 * 
 * attachEventListeners()
 * - Sets up click handlers for widget toggle
 * - Implements click-outside-to-close functionality
 * - Manages widget visibility
 * 
 * toggleCallWidget()
 * - Controls widget visibility
 * - Positions widget relative to call button
 * - Handles show/hide logic
 * 
 * Event Handling:
 * - Button click detection
 * - Document click for outside clicks
 * - Script loading error handling
 * 
 * Widget Positioning:
 * - Bottom: 150px from bottom
 * - Right: 20px from right
 * - z-index: 1000 for overlay
 * 
 * Error Handling:
 * - Script loading failures
 * - Missing DOM elements
 * - Widget initialization issues
 * 
 * Dependencies:
 * - ElevenLabs Convai Widget (https://elevenlabs.io/convai-widget/index.js)
 * - Modern browser with custom elements support
 * 
 * Debug Features:
 * - Extensive console logging
 * - State change tracking
 * - Element existence verification
 * 
 * Security Considerations:
 * - External script loading
 * - Cross-origin resource handling
 * - DOM manipulation safety
 * 
 * Performance:
 * - Async script loading
 * - Event delegation
 * - Efficient DOM updates
 */

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
