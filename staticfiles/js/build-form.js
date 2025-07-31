/* Build Form JavaScript */
document.addEventListener('DOMContentLoaded', function() {
    // Handle primary image selection (only one can be primary)
    const primaryCheckboxes = document.querySelectorAll('input[name*="is_primary"]');
    
    primaryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                // Uncheck all other primary checkboxes
                primaryCheckboxes.forEach(other => {
                    if (other !== this) {
                        other.checked = false;
                    }
                });
            }
        });
    });
    
    // Handle delete checkbox styling
    const deleteCheckboxes = document.querySelectorAll('input[name*="DELETE"]');
    
    deleteCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const container = this.closest('.image-upload-item');
            if (this.checked) {
                container.classList.add('to-delete');
            } else {
                container.classList.remove('to-delete');
            }
        });
    });
    
    // File size validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file && file.size > 10 * 1024 * 1024) { // 10MB
                alert('File size must be under 10MB');
                this.value = '';
            }
        });
    });
});
