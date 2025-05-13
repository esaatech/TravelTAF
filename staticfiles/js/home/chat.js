// Chat Module

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


const ChatModule = {
    // Add marked configuration
    markedConfig: {
        async: false,
        breaks: true,
        gfm: true,
        pedantic: false,
        sanitize: false,
        smartLists: true,
        smartypants: true
    },

    // DOM Elements
    elements: {
        chatToggle: null,
        chatPopup: null,
        chatClose: null,
        chatInput: null,
        sendButton: null,
        chatMessages: null,
        commonQuestions: null,
        typingIndicator: null,
        chatWidget: null
    },

    // Initialize the chat module
    init() {
        this.initializeElements();
        this.attachEventListeners();
        this.setupMarked();
    },

    // Initialize DOM elements
    initializeElements() {
        this.elements = {
            chatToggle: document.getElementById('chatToggle'),
            chatPopup: document.getElementById('chatPopup'),
            chatClose: document.getElementById('chatClose'),
            chatInput: document.getElementById('chatInput'),
            sendButton: document.getElementById('sendMessage'),
            chatMessages: document.getElementById('chatMessages'),
            commonQuestions: document.querySelectorAll('.common-question'),
            chatWidget: document.querySelector('.chat-widget')
        };
        this.createTypingIndicator();
    },

    // Create typing indicator element
    createTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'flex gap-4 max-w-2xl mb-4 typing-indicator hidden';
        typingDiv.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#1980e6" viewBox="0 0 256 256">
                    <path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm16-40a8,8,0,0,1-8,8,16,16,0,0,1-16-16V128a8,8,0,0,1,0-16,16,16,0,0,1,16,16v40A8,8,0,0,1,144,176ZM112,84a12,12,0,1,1,12,12A12,12,0,0,1,112,84Z"></path>
                </svg>
            </div>
            <div class="flex-1">
                <div class="bg-gray-100 p-4 rounded-lg inline-flex gap-1">
                    <span class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0s"></span>
                    <span class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
                    <span class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
                </div>
            </div>
        `;
        // Remove from DOM when hidden
        typingDiv.addEventListener('transitionend', () => {
            if (typingDiv.classList.contains('hidden')) {
                typingDiv.remove();
            }
        });
        this.elements.typingIndicator = typingDiv;
    },

    // Updated scrollToBottom method
    scrollToBottom() {
        const chatMessages = this.elements.chatMessages;
        const lastMessage = chatMessages.lastElementChild;
        
        if (lastMessage) {
            lastMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    },

    // Updated addMessage method with debugging
    addMessage(message, isUser = false, showButton = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex gap-4 max-w-2xl mb-4 ${isUser ? 'ml-auto' : ''}`;
        
        let processedMessage = message;
        if (!isUser) {
            console.log('Original message:', message);
            try {
                processedMessage = marked.parse(message);
                console.log('Processed markdown:', processedMessage);
            } catch (error) {
                console.error('Markdown parsing error:', error);
                processedMessage = message;
            }
        }
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="flex-1">
                    <p class="bg-blue-600 text-white p-4 rounded-lg inline-block">${message}</p>
                </div>
                <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
                        <path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm56-88a56,56,0,1,1-56-56A56.06,56.06,0,0,1,184,128Z"></path>
                    </svg>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#1980e6" viewBox="0 0 256 256">
                        <path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm16-40a8,8,0,0,1-8,8,16,16,0,0,1-16-16V128a8,8,0,0,1,0-16,16,16,0,0,1,16,16v40A8,8,0,0,1,144,176ZM112,84a12,12,0,1,1,12,12A12,12,0,0,1,112,84Z"></path>
                    </svg>
                </div>
                <div class="flex-1">
                    <div class="bg-gray-100 p-4 rounded-lg markdown-content">${processedMessage}</div>
                    ${showButton ? `
                        <button class="mt-2 bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors">
                            Speak to an Agent
                        </button>
                    ` : ''}
                </div>
            `;
        }
        
        this.elements.chatMessages.appendChild(messageDiv);
        
        // Apply styles to markdown content
        if (!isUser) {
            const markdownContent = messageDiv.querySelector('.markdown-content');
            this.applyMarkdownStyles(markdownContent);
        }
        
        setTimeout(() => {
            this.scrollToBottom();
        }, 0);
    },

    // Add method to apply Markdown styles
    applyMarkdownStyles(element) {
        // Add Tailwind classes for Markdown elements
        element.querySelectorAll('h1').forEach(el => {
            el.className = 'text-2xl font-bold mb-4 mt-2';
        });
        
        element.querySelectorAll('h2').forEach(el => {
            el.className = 'text-xl font-bold mb-3 mt-2';
        });
        
        element.querySelectorAll('h3').forEach(el => {
            el.className = 'text-lg font-bold mb-2 mt-2';
        });
        
        element.querySelectorAll('ul').forEach(el => {
            el.className = 'list-disc pl-6 mb-4';
        });
        
        element.querySelectorAll('ol').forEach(el => {
            el.className = 'list-decimal pl-6 mb-4';
        });
        
        element.querySelectorAll('li').forEach(el => {
            el.className = 'mb-1';
        });
        
        element.querySelectorAll('p').forEach(el => {
            el.className = 'mb-4';
        });
        
        element.querySelectorAll('strong').forEach(el => {
            el.className = 'font-bold';
        });
        
        element.querySelectorAll('em').forEach(el => {
            el.className = 'italic';
        });
        
        element.querySelectorAll('code').forEach(el => {
            el.className = 'bg-gray-200 px-1 rounded';
        });
        
        element.querySelectorAll('pre').forEach(el => {
            el.className = 'bg-gray-800 text-white p-4 rounded mb-4 overflow-x-auto';
        });
    },

    // Updated showTypingIndicator
    showTypingIndicator() {
        this.createTypingIndicator();
        this.elements.chatMessages.appendChild(this.elements.typingIndicator);
        
        setTimeout(() => {
            this.elements.typingIndicator.classList.remove('hidden');
            this.scrollToBottom();
        }, 0);
    },

    // Hide typing indicator
    hideTypingIndicator() {
        if (this.elements.typingIndicator) {
            this.elements.typingIndicator.classList.add('hidden');
        }
    },

    // Attach event listeners
    attachEventListeners() {
        // Toggle chat
        this.elements.chatToggle.addEventListener('click', () => {
            this.elements.chatPopup.classList.add('active');
            this.elements.chatWidget.style.display = 'none';
        });

        // Close chat
        this.elements.chatClose.addEventListener('click', () => {
            this.elements.chatPopup.classList.remove('active');
            this.elements.chatWidget.style.display = 'block';
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.elements.chatPopup.contains(e.target) && 
                !this.elements.chatToggle.contains(e.target)) {
                this.elements.chatPopup.classList.remove('active');
                this.elements.chatWidget.style.display = 'block';
            }
        });

        // Common questions
        this.elements.commonQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const questionText = question.textContent.trim();
                this.elements.chatInput.value = questionText;
            });
        });

        // Send message button
        this.elements.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });

        // Enter key for sending message
        this.elements.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Update send button styles
        this.elements.sendButton.classList.add('disabled:opacity-50', 'disabled:cursor-not-allowed');
        this.elements.chatInput.classList.add('disabled:bg-gray-100', 'disabled:cursor-not-allowed');
    },

    // Updated sendMessage method with response logging
    async sendMessage() {
        const message = this.elements.chatInput.value.trim();
        if (message) {
            try {
                this.elements.chatInput.disabled = true;
                this.elements.sendButton.disabled = true;
                
                this.addMessage(message, true);
                this.elements.chatInput.value = '';
                this.showTypingIndicator();
                
                const response = await fetch('/api/agent/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken(),
                    },
                    body: JSON.stringify({ message })
                });
                
                const data = await response.json();
                console.log('API Response:', data);
                
                this.hideTypingIndicator();
                
                if (response.ok) {
                    // Use data.message and data.show_button
                    const sanitizedResponse = data.message
                        ? data.message
                            .replace(/&/g, '&amp;')
                            .replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;')
                        : '';
                    console.log('Sanitized Response:', sanitizedResponse);
                    this.addMessage(sanitizedResponse, false, data.show_button);
                } else {
                    throw new Error(data.message || 'An error occurred');
                }
                
            } catch (error) {
                console.error('Error:', error);
                this.hideTypingIndicator();
                this.addMessage('Sorry, there was an error processing your message. Please try again later.');
            } finally {
                this.elements.chatInput.disabled = false;
                this.elements.sendButton.disabled = false;
                this.elements.chatInput.focus();
            }
        }
    },

    // Add method to get CSRF token
    getCSRFToken() {
        const name = 'csrftoken';
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
    },

    // Add method to load chat history (optional)
    async loadChatHistory() {
        try {
            const response = await fetch('/api/agent/chat/history/', {
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                // Clear existing messages
                this.elements.chatMessages.innerHTML = '';
                // Add each message from history
                data.forEach(item => {
                    if (item.message) {
                        this.addMessage(item.message, true);
                    }
                    if (item.response) {
                        this.addMessage(item.response, false);
                    }
                });
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    },

    // Setup marked configuration
    setupMarked() {
        marked.setOptions(this.markedConfig);
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    ChatModule.init();
});
