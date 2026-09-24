document.addEventListener('DOMContentLoaded', () => {
    const fileUploadContainer = document.getElementById('file-upload-container');
    const photoInput = document.getElementById('photo');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const removeImgBtn = document.getElementById('remove-img');
    
    if (fileUploadContainer && photoInput) {
        fileUploadContainer.addEventListener('click', (e) => {
            if (e.target !== removeImgBtn) {
                photoInput.click();
            }
        });
        
        fileUploadContainer.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadContainer.style.borderColor = 'var(--primary)';
        });
        
        fileUploadContainer.addEventListener('dragleave', (e) => {
            e.preventDefault();
            fileUploadContainer.style.borderColor = 'var(--border)';
        });
        
        fileUploadContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadContainer.style.borderColor = 'var(--border)';
            if (e.dataTransfer.files.length) {
                photoInput.files = e.dataTransfer.files;
                handleFileSelect();
            }
        });
        
        photoInput.addEventListener('change', handleFileSelect);
        
        removeImgBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            photoInput.value = '';
            imagePreview.classList.add('hidden');
        });
        
        function handleFileSelect() {
            if (photoInput.files && photoInput.files[0]) {
                const file = photoInput.files[0];
                
                // Validate size (5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('File is too large. Maximum size is 5MB.');
                    photoInput.value = '';
                    return;
                }
                
                // Validate type
                const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
                if (!validTypes.includes(file.type)) {
                    alert('Invalid file type. Only JPG, PNG, and WEBP are allowed.');
                    photoInput.value = '';
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    imagePreview.classList.remove('hidden');
                };
                reader.readAsDataURL(file);
            }
        }
    }
    
    // Handle form submissions
    const reportLostForm = document.getElementById('report-lost-form');
    const reportFoundForm = document.getElementById('report-found-form');
    
    function submitForm(form, endpoint) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const formMessage = document.getElementById('form-message');
            const submitBtn = form.querySelector('button[type="submit"]');
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            fetch(endpoint, {
                method: 'POST',
                body: formData // Fetch API automatically sets correct multipart headers
            })
            .then(res => {
                if (res.status === 401) {
                    window.location.href = '/login';
                    throw new Error('Not authenticated');
                }
                return res.json();
            })
            .then(data => {
                if (data.success) {
                    formMessage.textContent = 'Report submitted successfully!';
                    formMessage.className = 'alert-success';
                    formMessage.style.display = 'block';
                    form.reset();
                    if(imagePreview) imagePreview.classList.add('hidden');
                    
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Error submitting report.');
                }
            })
            .catch(err => {
                if (err.message !== 'Not authenticated') {
                    formMessage.textContent = err.message;
                    formMessage.className = 'alert-error';
                    formMessage.style.display = 'block';
                }
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Report';
            });
        });
    }
    
    if (reportLostForm) submitForm(reportLostForm, '/api/items/lost');
    if (reportFoundForm) submitForm(reportFoundForm, '/api/items/found');
});
