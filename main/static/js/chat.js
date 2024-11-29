// Chat Module
const ChatModule = {
    // DOM Elements
    elements: {
        chatToggle: null,
        chatPopup: null,
        chatClose: null,
        callButton: null,
        chatInput: null,
        sendButton: null,
        chatMessages: null,
        commonQuestions: null
    },

    // Initialize the chat module
    init() {
        this.initializeElements();
        this.attachEventListeners();
    },

    // Initialize DOM elements
    initializeElements() {
        this.elements = {
            chatToggle: document.getElementById('chatToggle'),
            chatPopup: document.getElementById('chatPopup'),
            chatClose: document.getElementById('chatClose'),
            callButton: document.getElementById('callButton'),
            chatInput: document.getElementById('chatInput'),
            sendButton: document.getElementById('sendMessage'),
            chatMessages: document.getElementById('chatMessages'),
            commonQuestions: document.querySelectorAll('.common-question')
        };
    },

    // Attach event listeners
    attachEventListeners() {
        // Toggle chat
        this.elements.chatToggle.addEventListener('click', () => {
            if (this.elements.chatPopup.classList.contains('active')) {
                this.elements.chatPopup.classList.remove('active');
            } else {
                this.elements.chatPopup.classList.add('active');
            }
        });

        // Close chat
        this.elements.chatClose.addEventListener('click', () => {
            this.elements.chatPopup.classList.remove('active');
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.elements.chatPopup.contains(e.target) && 
                !this.elements.chatToggle.contains(e.target)) {
                this.elements.chatPopup.classList.remove('active');
            }
        });

        // Call button
        this.elements.callButton.addEventListener('click', () => {
            window.location.href = 'tel:+1234567890'; // Replace with actual number
            console.log('Starting call...');
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
    },

    // Add message to chat
    addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex gap-4 max-w-2xl mb-4 ${isUser ? 'ml-auto' : ''}`;
        
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
                    <p class="bg-gray-100 p-4 rounded-lg inline-block">${message}</p>
                </div>
            `;
        }
        
        this.elements.chatMessages.appendChild(messageDiv);
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
    },

    // Send message
    sendMessage() {
        const message = this.elements.chatInput.value.trim();
        if (message) {
            this.addMessage(message, true);
            this.elements.chatInput.value = '';
            
            // Simulate bot response (replace with actual API call)
            setTimeout(() => {
                let response = "I'm processing your question. Please wait for our team to respond.";
                this.addMessage(response);
            }, 1000);
        }
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    ChatModule.init();
});
