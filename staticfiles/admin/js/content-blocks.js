document.addEventListener('DOMContentLoaded', function() {
    const contentSection = document.querySelector('.content-blocks-section');
    const contentInput = document.getElementById('id_content_blocks');
    let blocks = [];

    // Create interface container
    const editorContainer = document.createElement('div');
    editorContainer.className = 'content-blocks-editor';

    // Create toolbar
    const toolbar = document.createElement('div');
    toolbar.className = 'content-blocks-toolbar';
    toolbar.innerHTML = `
        <button type="button" class="add-block-btn" data-type="text">Add Text</button>
        <button type="button" class="add-block-btn" data-type="image">Add Image</button>
        <button type="button" class="add-block-btn" data-type="table">Add Table</button>
        <button type="button" class="add-block-btn" data-type="list">Add List</button>
        <button type="button" class="add-block-btn" data-type="quote">Add Quote</button>
    `;

    // Create blocks container
    const blocksContainer = document.createElement('div');
    blocksContainer.className = 'blocks-container';

    // Add components to the editor
    editorContainer.appendChild(toolbar);
    editorContainer.appendChild(blocksContainer);
    contentSection.appendChild(editorContainer);

    // Handle block addition
    toolbar.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-block-btn')) {
            const blockType = e.target.dataset.type;
            addNewBlock(blockType);
        }
    });

    // Function to add new block
    function addNewBlock(type) {
        const blockElement = document.createElement('div');
        blockElement.className = 'content-block';
        blockElement.dataset.type = type;

        let blockContent = '';
        switch(type) {
            case 'text':
                blockContent = `
                    <div class="block-header">Text Block</div>
                    <textarea class="block-content" rows="4"></textarea>
                `;
                break;
            case 'image':
                blockContent = `
                    <div class="block-header">Image Block</div>
                    <input type="file" class="block-content" accept="image/*">
                    <input type="text" class="image-caption" placeholder="Image caption">
                `;
                break;
            case 'table':
                blockContent = `
                    <div class="block-header">Table Block</div>
                    <div class="table-controls">
                        <input type="number" class="rows" value="2" min="1" placeholder="Rows">
                        <input type="number" class="cols" value="2" min="1" placeholder="Columns">
                        <button type="button" class="create-table">Create Table</button>
                    </div>
                    <div class="table-container"></div>
                `;
                break;
            case 'list':
                blockContent = `
                    <div class="block-header">List Block</div>
                    <select class="list-type">
                        <option value="ul">Unordered List</option>
                        <option value="ol">Ordered List</option>
                    </select>
                    <div class="list-items">
                        <input type="text" class="list-item" placeholder="List item">
                    </div>
                    <button type="button" class="add-list-item">Add Item</button>
                `;
                break;
            case 'quote':
                blockContent = `
                    <div class="block-header">Quote Block</div>
                    <textarea class="block-content" rows="3"></textarea>
                    <input type="text" class="quote-source" placeholder="Quote source">
                `;
                break;
        }

        // Add control buttons
        blockContent += `
            <div class="block-controls">
                <button type="button" class="move-up">↑</button>
                <button type="button" class="move-down">↓</button>
                <button type="button" class="delete-block">Delete</button>
            </div>
        `;

        blockElement.innerHTML = blockContent;
        blocksContainer.appendChild(blockElement);
        updateContentInput();

        // Add event listeners for the new block
        initializeBlockListeners(blockElement);
    }

    // Initialize block event listeners
    function initializeBlockListeners(block) {
        // Delete block
        block.querySelector('.delete-block').addEventListener('click', () => {
            block.remove();
            updateContentInput();
        });

        // Move block up
        block.querySelector('.move-up').addEventListener('click', () => {
            if (block.previousElementSibling) {
                block.parentNode.insertBefore(block, block.previousElementSibling);
                updateContentInput();
            }
        });

        // Move block down
        block.querySelector('.move-down').addEventListener('click', () => {
            if (block.nextElementSibling) {
                block.parentNode.insertBefore(block.nextElementSibling, block);
                updateContentInput();
            }
        });

        // Handle content changes
        const contentElement = block.querySelector('.block-content');
        if (contentElement) {
            contentElement.addEventListener('change', updateContentInput);
            contentElement.addEventListener('input', updateContentInput);
        }
    }

    // Update hidden input with current blocks data
    function updateContentInput() {
        const blocks = [];
        blocksContainer.querySelectorAll('.content-block').forEach(block => {
            const blockData = {
                type: block.dataset.type,
                content: block.querySelector('.block-content')?.value || ''
            };

            // Add additional data based on block type
            switch(block.dataset.type) {
                case 'image':
                    blockData.caption = block.querySelector('.image-caption')?.value || '';
                    break;
                case 'quote':
                    blockData.source = block.querySelector('.quote-source')?.value || '';
                    break;
            }

            blocks.push(blockData);
        });

        contentInput.value = JSON.stringify(blocks);
    }

    // Load existing content if any
    try {
        const existingContent = JSON.parse(contentInput.value || '[]');
        existingContent.forEach(block => {
            addNewBlock(block.type);
            // TODO: Populate block content
        });
    } catch (e) {
        console.error('Error loading existing content:', e);
    }
});
