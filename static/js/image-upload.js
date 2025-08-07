// Simplified Multiple Image Upload System
// Select up to 3 images at once, first is primary automatically
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('multiple-images');
    const previewContainer = document.getElementById('image-previews');
    
    if (!fileInput || !previewContainer) return;
    
    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        
        // Clear previous previews
        previewContainer.innerHTML = '';
        
        // Limit to 3 files
        if (files.length > 3) {
            alert('You can only select up to 3 images. Only the first 3 will be used.');
            // Update the file input to only include first 3 files
            const dt = new DataTransfer();
            files.slice(0, 3).forEach(file => dt.items.add(file));
            fileInput.files = dt.files;
        }
        
        // Create previews for selected files
        const filesToShow = files.slice(0, 3);
        filesToShow.forEach((file, index) => {
            if (file.type.startsWith('image/')) {
                createImagePreview(file, index);
            }
        });
    });
    
    // Create image preview
    function createImagePreview(file, index) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewDiv = document.createElement('div');
            previewDiv.className = 'image-preview-item mb-3 p-3 border rounded';
            previewDiv.setAttribute('data-index', index);
            
            const isPrimary = index === 0;
            const fileSize = (file.size / 1024 / 1024).toFixed(2);
            
            previewDiv.innerHTML = `
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <div class="preview-wrapper position-relative">
                            <img src="${e.target.result}" alt="Preview ${index + 1}" 
                                 style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 4px;">
                            ${isPrimary ? '<span class="primary-badge position-absolute top-0 start-0 bg-warning text-dark px-2 py-1 rounded" style="font-size: 0.75rem; z-index: 10;">⭐ PRIMARY</span>' : ''}
                        </div>
                        <small class="text-muted d-block mt-2">
                            <strong>${file.name}</strong> (${fileSize} MB)
                        </small>
                        ${fileSize > 10 ? '<div class="text-danger small mt-1">⚠️ File too large (max 10MB)</div>' : ''}
                    </div>
                    <div class="col-md-4 text-end">
                        <button type="button" class="btn btn-sm btn-outline-danger remove-preview-btn" data-index="${index}">
                            🗑️ Remove
                        </button>
                    </div>
                </div>
            `;
            
            previewContainer.appendChild(previewDiv);
            
            // Add remove functionality
            const removeBtn = previewDiv.querySelector('.remove-preview-btn');
            removeBtn.addEventListener('click', function() {
                removeFileFromInput(index);
                updatePreviews();
            });
        };
        
        reader.readAsDataURL(file);
    }
    
    // Remove file from input by index
    function removeFileFromInput(indexToRemove) {
        const dt = new DataTransfer();
        const files = Array.from(fileInput.files);
        
        files.forEach((file, index) => {
            if (index !== indexToRemove) {
                dt.items.add(file);
            }
        });
        
        fileInput.files = dt.files;
    }
    
    // Update all previews after removal
    function updatePreviews() {
        previewContainer.innerHTML = '';
        const files = Array.from(fileInput.files);
        
        files.forEach((file, index) => {
            if (file.type.startsWith('image/')) {
                createImagePreview(file, index);
            }
        });
        
        // If no files remain, clear the input
        if (files.length === 0) {
            fileInput.value = '';
        }
    }
    
    // Form validation on submit
    const form = document.getElementById('build-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const files = Array.from(fileInput.files);
            
            // Check file sizes
            const oversizedFiles = files.filter(file => file.size > 10 * 1024 * 1024);
            if (oversizedFiles.length > 0) {
                e.preventDefault();
                alert(`The following files are too large (max 10MB):\n${oversizedFiles.map(f => f.name).join('\n')}`);
                return false;
            }
            
            // Check file types
            const invalidFiles = files.filter(file => !file.type.startsWith('image/'));
            if (invalidFiles.length > 0) {
                e.preventDefault();
                alert(`The following files are not valid images:\n${invalidFiles.map(f => f.name).join('\n')}`);
                return false;
            }
        });
    }
    
    // Handle existing image deletions
    const existingImages = document.querySelectorAll('.existing-image');
    existingImages.forEach(imageDiv => {
        const deleteCheckbox = imageDiv.querySelector('input[type="checkbox"][name*="DELETE"]');
        if (deleteCheckbox) {
            deleteCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    imageDiv.style.opacity = '0.5';
                    imageDiv.style.textDecoration = 'line-through';
                } else {
                    imageDiv.style.opacity = '1';
                    imageDiv.style.textDecoration = 'none';
                }
            });
        }
    });
});
