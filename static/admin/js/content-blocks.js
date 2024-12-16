document.addEventListener('DOMContentLoaded', function() {
    const contentSection = document.querySelector('.content-blocks-section');
    const contentInput = document.getElementById('id_content_blocks');
    
    // Create the editor container
    const editorContainer = document.createElement('div');
    editorContainer.className = 'content-editor-container';

    // Create toolbar
    const toolbar = document.createElement('div');
    toolbar.className = 'editor-toolbar';
    toolbar.innerHTML = `
        <div class="toolbar-group">
            <select class="format-select">
                <option value="p">Normal Text</option>
                <option value="h1">Heading 1</option>
                <option value="h2">Heading 2</option>
                <option value="h3">Heading 3</option>
            </select>
        </div>
        <div class="toolbar-group">
            <button type="button" data-command="bold" title="Bold"><strong>B</strong></button>
            <button type="button" data-command="italic" title="Italic"><em>I</em></button>
            <button type="button" data-command="underline" title="Underline"><u>U</u></button>
        </div>
        <div class="toolbar-group">
            <button type="button" data-command="insertUnorderedList" title="Bullet List">•</button>
            <button type="button" data-command="insertOrderedList" title="Numbered List">1.</button>
        </div>
        <div class="toolbar-group">
            <button type="button" data-command="createLink" title="Insert Link">🔗</button>
            <button type="button" data-command="insertTable" title="Insert Table">📊</button>
        </div>
    `;

    // Create editor area
    const editor = document.createElement('div');
    editor.className = 'content-editor';
    editor.contentEditable = true;
    editor.innerHTML = contentInput.value || '<p><br></p>';

    // Add components to container
    editorContainer.appendChild(toolbar);
    editorContainer.appendChild(editor);
    contentSection.appendChild(editorContainer);

    // Add event handlers for toolbar
    function initializeEditor(editor, toolbar) {
        // Handle toolbar button clicks
        toolbar.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const command = button.dataset.command;
                
                switch(command) {
                    case 'createLink':
                        const url = prompt('Enter URL:');
                        if (url) {
                            document.execCommand('createLink', false, url);
                        }
                        break;
                        
                    case 'insertTable':
                        insertTable();
                        break;
                        
                    default:
                        // Handle standard formatting commands
                        document.execCommand(command, false, null);
                        break;
                }
                
                // Update button states
                updateToolbarState();
            });
        });

        // Handle text format selection
        const formatSelect = toolbar.querySelector('.format-select');
        formatSelect.addEventListener('change', () => {
            const format = formatSelect.value;
            document.execCommand('formatBlock', false, `<${format}>`);
        });

        // Function to insert table
        function insertTable() {
            const rows = prompt('Number of rows:', '3');
            const cols = prompt('Number of columns:', '3');
            
            if (rows && cols) {
                let tableHTML = '<table style="width:100%; border-collapse: collapse; margin: 15px 0;">';
                
                // Create header row
                tableHTML += '<tr>';
                for (let j = 0; j < cols; j++) {
                    tableHTML += '<th style="border: 1px solid #ddd; padding: 8px;">Header ' + (j + 1) + '</th>';
                }
                tableHTML += '</tr>';
                
                // Create body rows
                for (let i = 0; i < rows - 1; i++) {
                    tableHTML += '<tr>';
                    for (let j = 0; j < cols; j++) {
                        tableHTML += '<td style="border: 1px solid #ddd; padding: 8px;">Cell ' + (i + 1) + ',' + (j + 1) + '</td>';
                    }
                    tableHTML += '</tr>';
                }
                tableHTML += '</table>';
                
                document.execCommand('insertHTML', false, tableHTML);
            }
        }

        // Update toolbar state based on current selection
        function updateToolbarState() {
            toolbar.querySelectorAll('button[data-command]').forEach(button => {
                const command = button.dataset.command;
                if (['bold', 'italic', 'underline', 'insertUnorderedList', 'insertOrderedList'].includes(command)) {
                    button.classList.toggle('active', document.queryCommandState(command));
                }
            });

            // Update format select
            const formatSelect = toolbar.querySelector('.format-select');
            const currentBlock = document.queryCommandValue('formatBlock');
            if (currentBlock) {
                formatSelect.value = currentBlock.replace(/[<>]/g, '');
            }
        }

        // Add selection change listener
        editor.addEventListener('mouseup', updateToolbarState);
        editor.addEventListener('keyup', updateToolbarState);

        // Save content to hidden input when changed
        function saveContent() {
            contentInput.value = editor.innerHTML;
        }

        // Add content change listeners
        editor.addEventListener('input', saveContent);
        editor.addEventListener('change', saveContent);

        // Handle paste to clean up content
        editor.addEventListener('paste', (e) => {
            e.preventDefault();
            const text = e.clipboardData.getData('text/plain');
            document.execCommand('insertText', false, text);
        });

        // Initialize toolbar state
        updateToolbarState();
    }

    // Initialize the editor
    initializeEditor(editor, toolbar);
});
