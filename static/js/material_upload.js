// Shared "contribute a material" flow -- backs templates/components/material_upload_modal.html.
// One implementation used from materials.html, course_detail.html, and topic_detail.html
// instead of three separate hand-typed upload forms.
//
// Pages that include the modal may set window.currentUserName (prefill) and
// window.onMaterialUploaded (a callback invoked with the created material's dict on
// success, so the including page can refresh its own view instead of this script
// guessing what "refresh" means on every page).

let _uploadCourses = [];
let _uploadCoursesLoaded = false;

async function loadUploadCourseOptions() {
    const select = document.getElementById('materialCourseSelect');
    const typeSelect = document.getElementById('materialType');
    if (!select) return;
    try {
        const res = await fetch('/api/upload-course-picker-data');
        const data = await res.json();
        _uploadCourses = data.courses || [];
        _uploadCoursesLoaded = true;
        if (!_uploadCourses.length) {
            select.innerHTML = '<option value="">No courses mapped for your department yet</option>';
        } else {
            select.innerHTML = '<option value="">Select your course</option>' +
                _uploadCourses.map(c => `<option value="${c.id}">${c.code} — ${c.title}</option>`).join('');
        }
        if (typeSelect) {
            typeSelect.innerHTML = '<option value="">Select type</option>' +
                (data.material_types || []).map(t => `<option value="${t.value}">${t.label}</option>`).join('');
        }
    } catch (e) {
        select.innerHTML = '<option value="">Couldn\'t load courses -- try again</option>';
    }
}

async function onUploadCourseChange(preselectTopicId) {
    const courseId = document.getElementById('materialCourseSelect').value;
    const topicSelect = document.getElementById('materialTopicSelect');
    if (!topicSelect) return;
    topicSelect.innerHTML = '<option value="">Whole course (no specific topic)</option>';
    if (!courseId) return;
    try {
        const res = await fetch(`/api/courses/${courseId}/topics`);
        const data = await res.json();
        (data.topics || []).forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = t.title;
            topicSelect.appendChild(opt);
        });
        if (preselectTopicId) topicSelect.value = String(preselectTopicId);
    } catch (e) {
        // Non-fatal -- topic is optional, course-level upload still works.
    }
}

async function openUploadModal(courseId, topicId) {
    const modal = document.getElementById('uploadModal');
    if (!modal) return;
    modal.classList.add('show');

    const authorInput = document.getElementById('materialAuthor');
    if (authorInput && !authorInput.value && typeof window.currentUserName === 'string') {
        authorInput.value = window.currentUserName;
    }

    if (!_uploadCoursesLoaded) await loadUploadCourseOptions();

    if (courseId) {
        const select = document.getElementById('materialCourseSelect');
        select.value = String(courseId);
        await onUploadCourseChange(topicId);
    }
}

function closeUploadModal() {
    const modal = document.getElementById('uploadModal');
    if (modal) modal.classList.remove('show');
    const errBox = document.getElementById('uploadFormError');
    if (errBox) errBox.style.display = 'none';
}

async function handleMaterialUpload(e) {
    e.preventDefault();
    const btn = document.getElementById('uploadSubmitBtn');
    const errBox = document.getElementById('uploadFormError');
    errBox.style.display = 'none';
    btn.disabled = true;
    btn.textContent = 'Uploading…';
    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('uploadProgressFill');
    progressDiv.style.display = 'block';

    const formData = new FormData();
    formData.append('file', document.getElementById('materialFile').files[0]);
    formData.append('title', document.getElementById('materialTitle').value);
    formData.append('course_id', document.getElementById('materialCourseSelect').value);
    formData.append('topic_id', document.getElementById('materialTopicSelect').value);
    formData.append('material_type', document.getElementById('materialType').value);
    formData.append('author', document.getElementById('materialAuthor').value);
    formData.append('description', document.getElementById('materialDesc').value);

    try {
        let pct = 0;
        const interval = setInterval(() => { pct = Math.min(pct + 15, 85); progressFill.style.width = pct + '%'; }, 300);
        const res = await fetch('/api/upload-material', { method: 'POST', body: formData });
        clearInterval(interval);
        progressFill.style.width = '100%';
        const data = await res.json();

        if (data.success) {
            closeUploadModal();
            document.getElementById('uploadForm').reset();
            if (typeof window.onMaterialUploaded === 'function') {
                window.onMaterialUploaded(data.material);
            } else {
                alert('Uploaded! Track its review status on My Uploads.');
            }
        } else {
            errBox.textContent = data.error || 'Upload failed.';
            errBox.style.display = 'block';
        }
    } catch (err) {
        errBox.textContent = 'Upload error: ' + err.message;
        errBox.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Upload & share';
        progressDiv.style.display = 'none';
        progressFill.style.width = '0%';
    }
}

window.openUploadModal = openUploadModal;
window.closeUploadModal = closeUploadModal;
window.handleMaterialUpload = handleMaterialUpload;
window.onUploadCourseChange = onUploadCourseChange;
