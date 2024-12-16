document.addEventListener('DOMContentLoaded', function() {
    console.log('Content blocks JS loaded');

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
            console.log('Toolbar button clicked:', e.target.dataset.type);
            addNewBlock(e.target.dataset.type);
        }
    });

    // Function to add new block
    function addNewBlock(type) {
        console.log('Adding new block of type:', type);
        const blockElement = document.createElement('div');
        blockElement.className = 'content-block';
        blockElement.dataset.type = type;

        let blockContent = '';
        switch(type) {
            case 'text':
                blockContent = `
                    <div class="block-header">Text Block</div>
                    <div class="text-formatting-toolbar">
                        <button type="button" class="format-btn" data-format="bold">
                            <strong>B</strong>
                        </button>
                        <button type="button" class="format-btn" data-format="italic">
                            <em>I</em>
                        </button>
                        <button type="button" class="format-btn" data-format="underline">
                            <u>U</u>
                        </button>
                        <button type="button" class="format-btn" data-format="link">
                            🔗
                        </button>
                        <select class="heading-select">
                            <option value="p">Paragraph</option>
                            <option value="h2">Heading 2</option>
                            <option value="h3">Heading 3</option>
                            <option value="h4">Heading 4</option>
                        </select>
                    </div>
                    <div class="text-editor" contenteditable="true"></div>
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
                console.log('Creating table block interface');
                blockContent = `
                    <div class="block-header">Table Block</div>
                    <div class="table-controls">
                        <input type="number" class="rows" value="2" min="1" placeholder="Rows">
                        <input type="number" class="cols" value="2" min="1" placeholder="Columns">
                        <button type="button" class="create-table-btn">Create Table</button>
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

        // Initialize listeners immediately after adding the block
        console.log('Initializing block listeners');
        initializeBlockListeners(blockElement);
    }

    // Initialize block event listeners
    function initializeBlockListeners(block) {
        console.log('Setting up listeners for block:', block.dataset.type);

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

        // Table creation listener
        const createTableBtn = block.querySelector('.create-table-btn');
        if (createTableBtn) {
            console.log('Found create table button, adding listener');
            createTableBtn.addEventListener('click', () => {
                console.log('Create table button clicked');
                const rows = parseInt(block.querySelector('.rows').value) || 2;
                const cols = parseInt(block.querySelector('.cols').value) || 2;
                console.log(`Creating table with ${rows} rows and ${cols} columns`);
                createTable(block, rows, cols);
            });
        }

        if (block.dataset.type === 'text') {
            const toolbar = block.querySelector('.text-formatting-toolbar');
            const editor = block.querySelector('.text-editor');

            // Format buttons
            toolbar.querySelectorAll('.format-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    
                    // Make sure editor has focus
                    editor.focus();
                    
                    const format = btn.dataset.format;
                    
                    if (format === 'link') {
                        const url = prompt('Enter URL:');
                        if (url) {
                            document.execCommand('createLink', false, url);
                        }
                    } else {
                        // Check current state of the command
                        const isFormatActive = document.queryCommandState(format);
                        
                        if (isFormatActive) {
                            // If format is active, remove it
                            if (format === 'bold') document.execCommand('removeFormat', false, 'bold');
                            if (format === 'italic') document.execCommand('removeFormat', false, 'italic');
                            if (format === 'underline') document.execCommand('removeFormat', false, 'underline');
                            btn.classList.remove('active');
                        } else {
                            // If format is not active, apply it
                            document.execCommand(format, false, null);
                            btn.classList.add('active');
                        }
                    }
                    
                    // Update toolbar state after format change
                    updateToolbarState(toolbar);
                });
            });

            // Function to update toolbar state
            function updateToolbarState(toolbar) {
                const formats = ['bold', 'italic', 'underline'];
                formats.forEach(format => {
                    const button = toolbar.querySelector(`[data-format="${format}"]`);
                    if (button) {
                        const isActive = document.queryCommandState(format);
                        button.classList.toggle('active', isActive);
                    }
                });
            }

            // Update toolbar state when text is selected
            editor.addEventListener('mouseup', () => {
                updateToolbarState(toolbar);
            });

            // Update toolbar state when keyboard is used
            editor.addEventListener('keyup', () => {
                updateToolbarState(toolbar);
            });

            // Heading select
            const headingSelect = toolbar.querySelector('.heading-select');
            if (headingSelect) {
                headingSelect.addEventListener('change', () => {
                    editor.focus();
                    const tag = headingSelect.value;
                    document.execCommand('formatBlock', false, `<${tag}>`);
                });
            }

            // Update content when text changes
            editor.addEventListener('input', () => {
                updateContentInput();
            });
        }
    }

    // Add this new function to create tables
    function createTable(block, rows, cols) {
        console.log('Creating table structure');
        const tableContainer = block.querySelector('.table-container');
        let tableHTML = '<table class="content-table">';
        
        // Create header row
        tableHTML += '<thead><tr>';
        for (let j = 0; j < cols; j++) {
            tableHTML += `<th><input type="text" placeholder="Header ${j + 1}"></th>`;
        }
        tableHTML += '</tr></thead>';
        
        // Create body rows
        tableHTML += '<tbody>';
        for (let i = 0; i < rows - 1; i++) {
            tableHTML += '<tr>';
            for (let j = 0; j < cols; j++) {
                tableHTML += `<td><input type="text" placeholder="Cell ${i + 1},${j + 1}"></td>`;
            }
            tableHTML += '</tr>';
        }
        tableHTML += '</tbody></table>';
        
        console.log('Setting table HTML');
        tableContainer.innerHTML = tableHTML;
        
        // Add to content blocks data
        updateContentInput();
    }

    // Update hidden input with current blocks data
    function updateContentInput() {
        const blocks = [];
        blocksContainer.querySelectorAll('.content-block').forEach(block => {
            if (block.dataset.type === 'table') {
                const tableData = {
                    type: 'table',
                    headers: [],
                    rows: []
                };
                
                // Get headers
                const headerCells = block.querySelectorAll('thead input');
                headerCells.forEach(cell => {
                    tableData.headers.push(cell.value || '');
                });
                
                // Get rows
                const bodyRows = block.querySelectorAll('tbody tr');
                bodyRows.forEach(row => {
                    const rowData = [];
                    row.querySelectorAll('input').forEach(cell => {
                        rowData.push(cell.value || '');
                    });
                    tableData.rows.push(rowData);
                });
                
                blocks.push(tableData);
            } else {
                // Handle other block types as before
                blocks.push({
                    type: block.dataset.type,
                    content: block.querySelector('.block-content')?.value || ''
                });
            }
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
