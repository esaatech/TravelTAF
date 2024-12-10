class CoverLetterUtils {
    constructor() {
        // File upload related elements
        this.fileInput = document.querySelector('input[type="file"]');
        this.filePreview = document.getElementById('filePreview');
        this.clearFileButton = document.getElementById('clearFile');
        
        // Response related elements
        this.results = document.getElementById('results');
        this.coverLetterContent = document.getElementById('coverLetterContent');
        this.copyButton = document.getElementById('copyButton');
        this.downloadButton = document.getElementById('downloadButton');
        this.editButton = document.getElementById('editButton');

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File upload handling
        if (this.fileInput && this.clearFileButton) {
            this.fileInput.addEventListener('change', () => this.handleFileUpload());
            this.clearFileButton.addEventListener('click', (e) => this.clearFileUpload(e));
        }

        // Response handling
        if (this.copyButton) {
            this.copyButton.addEventListener('click', () => this.copyToClipboard());
        }
        if (this.downloadButton) {
            this.downloadButton.addEventListener('click', () => this.downloadAsPDF());
        }
        if (this.editButton) {
            this.editButton.addEventListener('click', () => this.makeEditable());
        }
    }

    handleFileUpload() {
        if (this.fileInput.files.length > 0) {
            const file = this.fileInput.files[0];
            if (this.filePreview) {
                this.filePreview.textContent = file.name;
                this.filePreview.parentElement.classList.remove('hidden');
            }
        }
    }

    clearFileUpload(event) {
        event.preventDefault();
        if (this.fileInput) {
            // Create a new file input
            const newFileInput = document.createElement('input');
            newFileInput.type = 'file';
            newFileInput.name = this.fileInput.name;
            newFileInput.accept = this.fileInput.accept;
            newFileInput.className = this.fileInput.className;
            
            // Replace old input with new one
            this.fileInput.parentNode.replaceChild(newFileInput, this.fileInput);
            this.fileInput = newFileInput;
            
            // Re-attach event listener
            this.fileInput.addEventListener('change', () => this.handleFileUpload());
        }
        
        if (this.filePreview) {
            this.filePreview.parentElement.classList.add('hidden');
            this.filePreview.textContent = '';
        }
    }

    async copyToClipboard() {
        try {
            const content = this.coverLetterContent.innerText;
            await navigator.clipboard.writeText(content);
            this.showToast('Cover letter copied to clipboard!');
        } catch (err) {
            this.showToast('Failed to copy to clipboard', true);
        }
    }

    downloadAsPDF() {
        const element = this.coverLetterContent;
        const opt = {
            margin: [0.5, 0.5],
            filename: 'cover-letter.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { 
                scale: 2,
                useCORS: true
            },
            jsPDF: { 
                unit: 'in', 
                format: 'letter', 
                orientation: 'portrait'
            }
        };

        // Show loading toast
        this.showToast('Generating PDF...');

        // Generate PDF
        html2pdf()
            .from(element)
            .set(opt)
            .save()
            .then(() => {
                this.showToast('PDF downloaded successfully!');
            })
            .catch(error => {
                console.error('PDF generation failed:', error);
                this.showToast('Failed to generate PDF', true);
            });
    }

    makeEditable() {
        if (!this.coverLetterContent.isContentEditable) {
            this.coverLetterContent.contentEditable = true;
            this.coverLetterContent.classList.add('border', 'border-blue-300', 'p-4', 'rounded');
            this.editButton.textContent = 'Save Changes';
            this.showToast('You can now edit the cover letter');
        } else {
            this.coverLetterContent.contentEditable = false;
            this.coverLetterContent.classList.remove('border', 'border-blue-300', 'p-4', 'rounded');
            this.editButton.textContent = 'Edit Letter';
            this.showToast('Changes saved');
        }
    }

    showToast(message, isError = false) {
        // Remove any existing toasts
        const existingToasts = document.querySelectorAll('.toast-message');
        existingToasts.forEach(toast => toast.remove());

        // Create new toast
        const toast = document.createElement('div');
        toast.className = `toast-message fixed bottom-4 left-4 px-6 py-3 rounded-lg shadow-lg ${
            isError ? 'bg-red-500' : 'bg-green-500'
        } text-white transform transition-all duration-300 ease-in-out z-50`;
        
        // Add styles for initial position (off-screen)
        toast.style.transform = 'translateY(100%)';
        toast.style.opacity = '0';
        
        // Create message container with flex
        const messageContainer = document.createElement('div');
        messageContainer.className = 'flex items-center space-x-2';
        
        // Add icon based on type
        const icon = document.createElement('span');
        if (isError) {
            icon.innerHTML = `
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>`;
        } else {
            icon.innerHTML = `
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M5 13l4 4L19 7" />
                </svg>`;
        }
        
        // Add message text
        const text = document.createElement('span');
        text.textContent = message;
        
        // Assemble toast
        messageContainer.appendChild(icon);
        messageContainer.appendChild(text);
        toast.appendChild(messageContainer);
        document.body.appendChild(toast);

        // Trigger animation
        requestAnimationFrame(() => {
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
        });

        // Remove after delay
        setTimeout(() => {
            toast.style.transform = 'translateY(100%)';
            toast.style.opacity = '0';
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.parentElement.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.coverLetterUtils = new CoverLetterUtils();
}); 