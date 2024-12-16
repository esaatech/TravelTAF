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
                        <div class="format-group">
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
                        </div>
                        <div class="format-group">
                            <button type="button" class="format-btn" data-format="p">P</button>
                        </div>
                        <div class="format-group">
                            <button type="button" class="format-btn" data-format="h2">H2</button>
                            <button type="button" class="format-btn" data-format="h3">H3</button>
                            <button type="button" class="format-btn" data-format="h4">H4</button>
                        </div>
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
                    editor.focus();
                    
                    const format = btn.dataset.format;
                    
                    // Handle different format types
                    if (['h2', 'h3', 'h4', 'p'].includes(format)) {
                        // Handle headings and paragraph
                        const isCurrentFormat = document.queryCommandValue('formatBlock') === format;
                        
                        if (isCurrentFormat) {
                            // If current format is active, convert to paragraph
                            document.execCommand('formatBlock', false, '<p>');
                            toolbar.querySelectorAll('.format-btn[data-format^="h"]').forEach(b => b.classList.remove('active'));
                            toolbar.querySelector('.format-btn[data-format="p"]').classList.add('active');
                        } else {
                            // Apply new format
                            document.execCommand('formatBlock', false, `<${format}>`);
                            toolbar.querySelectorAll('.format-btn[data-format^="h"], .format-btn[data-format="p"]').forEach(b => b.classList.remove('active'));
                            btn.classList.add('active');
                        }
                    } else if (format === 'link') {
                        const url = prompt('Enter URL:');
                        if (url) {
                            document.execCommand('createLink', false, url);
                        }
                    } else {
                        // Handle other formatting (bold, italic, underline)
                        const isFormatActive = document.queryCommandState(format);
                        document.execCommand(format, false, null);
                        btn.classList.toggle('active', !isFormatActive);
                    }
                    
                    updateToolbarState(toolbar);
                });
            });

            // Function to update toolbar state
            function updateToolbarState(toolbar) {
                // Check basic formats
                ['bold', 'italic', 'underline'].forEach(format => {
                    const button = toolbar.querySelector(`[data-format="${format}"]`);
                    if (button) {
                        button.classList.toggle('active', document.queryCommandState(format));
                    }
                });

                // Check current block format
                const currentFormat = document.queryCommandValue('formatBlock').replace(/[<>]/g, '');
                toolbar.querySelectorAll('.format-btn[data-format^="h"], .format-btn[data-format="p"]').forEach(btn => {
                    btn.classList.toggle('active', btn.dataset.format === currentFormat);
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
            const headingSelect = block.querySelector('.heading-select');
            if (headingSelect) {
                headingSelect.addEventListener('change', () => {
                    const tag = headingSelect.value;
                    if (!tag) return; // Skip if no value selected
                    
                    editor.focus();
                    const selection = window.getSelection();
                    const range = selection.getRangeAt(0);
                    
                    // Get the current block element
                    let currentBlock = range.commonAncestorContainer;
                    while (currentBlock && currentBlock.nodeType === 3) {
                        currentBlock = currentBlock.parentNode;
                    }
                    
                    // Create new element with selected tag
                    const newElement = document.createElement(tag);
                    newElement.innerHTML = currentBlock.innerHTML || '';
                    
                    // Replace the current block with new element
                    if (currentBlock && currentBlock.parentNode) {
                        currentBlock.parentNode.replaceChild(newElement, currentBlock);
                    } else {
                        // If no current block, wrap selection in new element
                        range.surroundContents(newElement);
                    }
                    
                    // Reset selection
                    headingSelect.value = '';
                    updateContentInput();
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
