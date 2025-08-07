// Build Form JavaScript - Handle dynamic image formsets
document.addEventListener('DOMContentLoaded', function() {
    const imageFormsContainer = document.getElementById('image-forms');
    const addImageBtn = document.getElementById('add-image-btn');
    const totalFormsInput = document.querySelector('#id_images-TOTAL_FORMS');
    
    const maxForms = 3; // Maximum 3 images per build
    
    // Function to count active (non-deleted) forms
    function countActiveForms() {
        const forms = imageFormsContainer.querySelectorAll('.image-upload-item');
        return forms.length; // Simplified - just count visible forms
    }
    
    // Function to get the next form index
    function getNextFormIndex() {
        return totalFormsInput ? parseInt(totalFormsInput.value) : 0;
    }
    
    // Function to update form indices
    function updateFormIndices() {
        const forms = imageFormsContainer.querySelectorAll('.image-upload-item');
        forms.forEach((form, index) => {
            // Update all form elements with the correct index
            form.querySelectorAll('input, select, textarea').forEach(input => {
                if (input.name) {
                    input.name = input.name.replace(/images-\d+/, `images-${index}`);
                    input.id = input.id.replace(/id_images-\d+/, `id_images-${index}`);
                }
            });
            
            // Update labels
            form.querySelectorAll('label').forEach(label => {
                if (label.getAttribute('for')) {
                    label.setAttribute('for', label.getAttribute('for').replace(/id_images-\d+/, `id_images-${index}`));
                }
            });
        });
        
        // Update total forms count to actual number of forms
        if (totalFormsInput) {
            totalFormsInput.value = forms.length;
        }
        
        // Update button visibility
        updateAddButtonVisibility();
    }
    
    // Function to update add button visibility
    function updateAddButtonVisibility() {
        const activeFormsCount = countActiveForms();
        console.log('Active forms:', activeFormsCount, 'Max forms:', maxForms);
        
        if (addImageBtn) {
            const shouldShow = activeFormsCount < maxForms;
            addImageBtn.style.display = shouldShow ? 'block' : 'none';
            console.log('Add button should show?', shouldShow);
        }
        
        // Update container data attribute for CSS styling
        imageFormsContainer.setAttribute('data-max-reached', activeFormsCount >= maxForms);
    }
    
    // Function to create a new image form
    function createNewImageForm() {
        const activeFormsCount = countActiveForms();
        if (activeFormsCount >= maxForms) {
            console.log('Cannot add more forms. Active forms:', activeFormsCount, 'Max:', maxForms);
            return;
        }
        
        const emptyForm = document.querySelector('#empty-image-form');
        if (!emptyForm) {
            console.log('Empty form template not found');
            return;
        }
        
        const newForm = emptyForm.cloneNode(true);
        newForm.id = '';
        newForm.style.display = 'block';
        newForm.classList.add('image-upload-item');
        
        // Calculate the next form index based on current forms
        const currentForms = imageFormsContainer.querySelectorAll('.image-upload-item');
        const formIndex = currentForms.length;
        
        console.log('Creating form with index:', formIndex, 'Current forms:', currentForms.length);
        
        // Update form indices
        newForm.querySelectorAll('input, select, textarea').forEach(input => {
            if (input.name) {
                input.name = input.name.replace(/__prefix__/g, formIndex);
                input.id = input.id.replace(/__prefix__/g, formIndex);
            }
        });
        
        newForm.querySelectorAll('label').forEach(label => {
            if (label.getAttribute('for')) {
                label.setAttribute('for', label.getAttribute('for').replace(/__prefix__/g, formIndex));
            }
        });
        
        // Add remove button functionality
        const removeBtn = newForm.querySelector('.remove-image-btn');
        if (removeBtn) {
            removeBtn.addEventListener('click', function() {
                newForm.remove();
                updateFormIndices();
            });
        }
        
        imageFormsContainer.appendChild(newForm);
        updateFormIndices(); // This will update totalFormsInput.value correctly
        updateAddButtonVisibility();
        
        console.log('Form created. Total forms now:', imageFormsContainer.querySelectorAll('.image-upload-item').length);
    }
    
    // Add event listener to add button
    if (addImageBtn) {
        addImageBtn.addEventListener('click', function(e) {
            e.preventDefault();
            createNewImageForm();
        });
    }
    
    // Add event listeners to existing remove buttons
    document.querySelectorAll('.remove-image-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const formItem = this.closest('.image-upload-item');
            formItem.remove();
            updateFormIndices();
        });
    });
    
    // Initial setup
    updateAddButtonVisibility();
    
    // Add initial empty form if no forms exist (for new builds)
    const existingActiveForms = countActiveForms();
    if (existingActiveForms === 0) {
        createNewImageForm();
    }
    
    // Function to handle primary image selection
    function handlePrimaryImageSelection() {
        const primaryCheckboxes = document.querySelectorAll('input[name*="is_primary"]');
        
        primaryCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    // Uncheck all other primary checkboxes
                    primaryCheckboxes.forEach(otherCheckbox => {
                        if (otherCheckbox !== this) {
                            otherCheckbox.checked = false;
                        }
                    });
                    
                    // Add visual indicator
                    updatePrimaryImageIndicators();
                }
            });
        });
    }
    
    // Function to update visual indicators for primary image
    function updatePrimaryImageIndicators() {
        const imageItems = document.querySelectorAll('.image-upload-item');
        
        imageItems.forEach(item => {
            const primaryCheckbox = item.querySelector('input[name*="is_primary"]');
            const isPrimary = primaryCheckbox && primaryCheckbox.checked;
            
            // Add/remove primary indicator class
            if (isPrimary) {
                item.classList.add('primary-image');
            } else {
                item.classList.remove('primary-image');
            }
        });
    }
    
    // Initialize primary image handling
    handlePrimaryImageSelection();
    
    // Re-initialize primary image handling when new forms are added
    const originalCreateNewImageForm = createNewImageForm;
    createNewImageForm = function() {
        originalCreateNewImageForm();
        handlePrimaryImageSelection();
    };
    
    // Handle file input changes to show preview
    function handleFilePreview(input) {
        const file = input.files[0];
        const previewContainer = input.closest('.image-upload-item').querySelector('.image-preview');
        
        if (file && previewContainer) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewContainer.innerHTML = `
                    <img src="${e.target.result}" alt="Preview" style="max-width: 100px; max-height: 100px; object-fit: cover;">
                `;
            };
            reader.readAsDataURL(file);
        }
    }
    
    // Add file input change listeners
    document.addEventListener('change', function(e) {
        if (e.target.type === 'file' && e.target.name && e.target.name.includes('image')) {
            handleFilePreview(e.target);
        }
    });
    
    // Handle multiple file selection (HTML5 multiple attribute)
    function handleMultipleFiles(input) {
        const files = Array.from(input.files);
        const maxFiles = maxForms - countActiveForms();
        
        files.slice(0, maxFiles).forEach((file, index) => {
            if (index === 0) {
                // Use the current form for the first file
                handleFilePreview(input);
            } else {
                // Create new forms for additional files
                createNewImageForm();
                const newForm = imageFormsContainer.lastElementChild;
                const newInput = newForm.querySelector('input[type="file"]');
                
                // Create a new FileList with just this file
                const dt = new DataTransfer();
                dt.items.add(file);
                newInput.files = dt.files;
                
                handleFilePreview(newInput);
            }
        });
    }
    
    // Enhanced file handling for drag and drop
    imageFormsContainer.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('drag-over');
    });
    
    imageFormsContainer.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
    });
    
    imageFormsContainer.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
        
        const files = Array.from(e.dataTransfer.files).filter(file => file.type.startsWith('image/'));
        const availableSlots = maxForms - countActiveForms();
        
        files.slice(0, availableSlots).forEach(file => {
            createNewImageForm();
            const newForm = this.lastElementChild;
            const input = newForm.querySelector('input[type="file"]');
            
            const dt = new DataTransfer();
            dt.items.add(file);
            input.files = dt.files;
            
            handleFilePreview(input);
        });
    });
});
