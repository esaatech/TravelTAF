document.addEventListener('DOMContentLoaded', function() {
    const contentBlocksContainer = document.querySelector('.content-blocks-container');
    const contentBlocksInput = document.getElementById('id_content_blocks');

    // Block types configuration
    const blockTypes = {
        paragraph: {
            icon: 'text',
            label: 'Paragraph'
        },
        image: {
            icon: 'image',
            label: 'Image'
        },
        table: {
            icon: 'table',
            label: 'Table'
        },
        list: {
            icon: 'list',
            label: 'List'
        },
        quote: {
            icon: 'quote',
            label: 'Quote'
        }
    };

    // Initialize content blocks editor
    function initializeBlocksEditor() {
        // Add block type selector
        const blockTypeSelector = createBlockTypeSelector();
        contentBlocksContainer.appendChild(blockTypeSelector);

        // Load existing blocks
        let existingBlocks = [];
        try {
            existingBlocks = JSON.parse(contentBlocksInput.value);
        } catch (e) {
            existingBlocks = [];
        }

        // Render existing blocks
        existingBlocks.forEach(block => {
            renderContentBlock(block);
        });
    }

    // Create and render content blocks
    function renderContentBlock(blockData) {
        // Create block container
        const blockElement = document.createElement('div');
        blockElement.className = 'content-block';
        
        // Render different block types
        switch(blockData.type) {
            case 'paragraph':
                renderParagraphBlock(blockElement, blockData);
                break;
            case 'image':
                renderImageBlock(blockElement, blockData);
                break;
            // Add other block type renderers
        }

        contentBlocksContainer.appendChild(blockElement);
    }

    initializeBlocksEditor();
});
