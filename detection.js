/* ==========================================================================
   DEEPGUARD AI - DETECTION PAGE DRAG-DROP & AJAX PIPELINE
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('media-dropzone');
    const fileInput = document.getElementById('media-file-input');
    const previewContainer = document.getElementById('preview-container');
    const mediaPreview = document.getElementById('media-preview');
    const fileInfoCard = document.getElementById('file-info-card');
    const analyzeBtn = document.getElementById('analyze-btn');
    const progressOverlay = document.getElementById('progress-overlay');
    const progressStatusText = document.getElementById('progress-status-text');
    const progressStepList = document.getElementById('progress-step-list');

    const videoConfigGroup = document.getElementById('video-config-group');
    const frameSlider = document.getElementById('frame-count-slider');
    const frameCountVal = document.getElementById('frame-count-val');

    let selectedFile = null;

    if (!dropzone || !fileInput) return;

    // Frame slider change
    if (frameSlider && frameCountVal) {
        frameSlider.addEventListener('input', (e) => {
            frameCountVal.textContent = e.target.value;
        });
    }

    // Dropzone click triggers input
    dropzone.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'INPUT') {
            fileInput.click();
        }
    });

    // Dragover events
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    function handleFileSelection(file) {
        const validExtensions = ['jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi'];
        const ext = file.name.split('.').pop().lowerCase || file.name.split('.').pop().toLowerCase();

        if (!validExtensions.includes(ext)) {
            showToast('Unsupported file type. Please upload JPG, PNG, MP4, MOV, or AVI.', 'danger');
            return;
        }

        selectedFile = file;

        // Render preview
        mediaPreview.innerHTML = '';
        const isVideo = ['mp4', 'mov', 'avi'].includes(ext);

        if (isVideo) {
            const videoElem = document.createElement('video');
            videoElem.src = URL.createObjectURL(file);
            videoElem.controls = true;
            videoElem.className = 'img-fluid rounded';
            mediaPreview.appendChild(videoElem);
            if (videoConfigGroup) videoConfigGroup.style.display = 'block';
        } else {
            const imgElem = document.createElement('img');
            imgElem.src = URL.createObjectURL(file);
            imgElem.className = 'img-fluid rounded';
            mediaPreview.appendChild(imgElem);
            if (videoConfigGroup) videoConfigGroup.style.display = 'none';
        }

        // Show file details
        document.getElementById('info-filename').textContent = file.name;
        document.getElementById('info-filetype').textContent = isVideo ? 'Video' : 'Image';
        document.getElementById('info-filesize').textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';

        previewContainer.style.display = 'block';
        fileInfoCard.style.display = 'block';
        analyzeBtn.style.display = 'inline-flex';
        dropzone.style.display = 'none';
    }

    // Reset button
    const changeFileBtn = document.getElementById('change-file-btn');
    if (changeFileBtn) {
        changeFileBtn.addEventListener('click', () => {
            selectedFile = null;
            fileInput.value = '';
            previewContainer.style.display = 'none';
            fileInfoCard.style.display = 'none';
            analyzeBtn.style.display = 'none';
            dropzone.style.display = 'block';
        });
    }

    // Analyze Media Submit
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', () => {
            if (!selectedFile) return;

            const formData = new FormData();
            formData.append('media', selectedFile);
            
            const demoModeCheckbox = document.getElementById('demo-mode-checkbox');
            if (demoModeCheckbox) {
                formData.append('demo_mode', demoModeCheckbox.checked ? 'true' : 'false');
            }

            if (frameSlider) {
                formData.append('frame_count', frameSlider.value);
            }

            // Start progress animation modal overlay
            progressOverlay.style.display = 'flex';
            document.querySelector('.media-preview-container')?.classList.add('scanning');

            runProgressSteps(() => {
                fetch('/api/detect', {
                    method: 'POST',
                    body: formData
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = data.redirect_url;
                    } else {
                        progressOverlay.style.display = 'none';
                        document.querySelector('.media-preview-container')?.classList.remove('scanning');
                        showToast(data.error || 'Detection failed.', 'danger');
                    }
                })
                .catch(err => {
                    progressOverlay.style.display = 'none';
                    document.querySelector('.media-preview-container')?.classList.remove('scanning');
                    showToast('Server communication error. Please try again.', 'danger');
                });
            });
        });
    }

    function runProgressSteps(onComplete) {
        const steps = [
            "Initializing AI analysis pipeline...",
            "Detecting faces using OpenCV...",
            "Extracting spatial and video frames...",
            "Running PyTorch neural artifact classifier...",
            "Generating verified AI security report..."
        ];

        let index = 0;
        const interval = setInterval(() => {
            if (index < steps.length) {
                if (progressStatusText) progressStatusText.textContent = steps[index];
                const stepElem = document.getElementById(`progress-step-${index + 1}`);
                if (stepElem) {
                    stepElem.classList.add('completed');
                    stepElem.querySelector('.step-icon').textContent = '✓';
                }
                index++;
            } else {
                clearInterval(interval);
                onComplete();
            }
        }, 500);
    }

    function showToast(message, type = 'info') {
        alert(message); // Standard alert fallback or custom toast
    }
});
