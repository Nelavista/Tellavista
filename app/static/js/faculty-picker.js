// Shared searchable Faculty -> Department picker. Renders into whatever
// container/select IDs are passed in, so the same component works in both
// profile_completion_modal.html (new user onboarding) and profile.html
// (editing an existing profile) despite their slightly different markup IDs.
// Depends on FACULTY_DEPARTMENTS from faculty-departments.js being loaded first.

function initFacultyPicker(opts) {
  const facultySearch = document.getElementById(opts.facultySearchId);
  const facultyGrid = document.getElementById(opts.facultyGridId);
  const facultySelect = document.getElementById(opts.facultySelectId);
  const deptSearch = document.getElementById(opts.deptSearchId);
  const deptGrid = document.getElementById(opts.deptGridId);
  const deptSelect = document.getElementById(opts.deptSelectId);
  const deptPreview = opts.deptPreviewId ? document.getElementById(opts.deptPreviewId) : null;
  const deptPreviewName = opts.deptPreviewNameId ? document.getElementById(opts.deptPreviewNameId) : null;

  let selectedFaculty = opts.currentFaculty || '';
  let selectedDepartment = opts.currentDepartment || '';

  // A plain `select.value = 'X'` assignment is silently ignored by the browser
  // unless a matching <option> already exists in the DOM -- these hidden
  // selects only start with an empty placeholder option, so every selection
  // (including the initial pre-fill below) has to inject its own <option>
  // first. Without this, editing a profile without touching these two fields
  // would submit them as empty and wipe the student's existing faculty/department.
  function setHiddenSelectValue(selectEl, value) {
    if (!value) {
      selectEl.value = '';
      return;
    }
    let opt = Array.from(selectEl.options).find(o => o.value === value);
    if (!opt) {
      opt = document.createElement('option');
      opt.value = value;
      opt.textContent = value;
      selectEl.appendChild(opt);
    }
    selectEl.value = value;
  }

  function renderFacultyChips(filterText) {
    const q = (filterText || '').trim().toLowerCase();
    const names = Object.keys(FACULTY_DEPARTMENTS).filter(n => !q || n.toLowerCase().includes(q));

    if (names.length === 0) {
      facultyGrid.innerHTML = '<div class="picker-empty">No faculty matches "' + escapeHtml(filterText) + '"</div>';
      return;
    }

    facultyGrid.innerHTML = names.map(name => {
      const f = FACULTY_DEPARTMENTS[name];
      const isSelected = name === selectedFaculty;
      return `<button type="button" class="fd-chip${isSelected ? ' selected' : ''}" data-faculty="${escapeHtml(name)}">
        <span class="fd-emoji">${f.emoji}</span>${escapeHtml(name)}
      </button>`;
    }).join('');

    facultyGrid.querySelectorAll('.fd-chip').forEach(chip => {
      chip.addEventListener('click', () => selectFaculty(chip.dataset.faculty));
    });
  }

  function renderDeptChips(filterText) {
    if (!selectedFaculty || !FACULTY_DEPARTMENTS[selectedFaculty]) {
      deptGrid.innerHTML = '<div class="picker-empty">Select a faculty first</div>';
      deptSearch.disabled = true;
      return;
    }
    deptSearch.disabled = false;

    const q = (filterText || '').trim().toLowerCase();
    const depts = FACULTY_DEPARTMENTS[selectedFaculty].departments.filter(
      d => !q || d.value.toLowerCase().includes(q)
    );

    if (depts.length === 0) {
      deptGrid.innerHTML = '<div class="picker-empty">No department matches "' + escapeHtml(filterText) + '"</div>';
      return;
    }

    deptGrid.innerHTML = depts.map(d => {
      const isSelected = d.value === selectedDepartment;
      return `<button type="button" class="fd-chip${isSelected ? ' selected' : ''}" data-value="${escapeHtml(d.value)}" data-curriculum="${!!d.hasCurriculum}">
        <span class="fd-emoji">${d.emoji}</span>${escapeHtml(d.value)}
        ${d.hasCurriculum ? '<span class="fd-curriculum-tag">Full curriculum</span>' : ''}
      </button>`;
    }).join('');

    deptGrid.querySelectorAll('.fd-chip').forEach(chip => {
      chip.addEventListener('click', () => selectDepartment(chip.dataset.value, chip.dataset.curriculum === 'true'));
    });
  }

  function updateDeptPreview(hasCurriculum) {
    if (!deptPreview || !deptPreviewName) return;
    if (hasCurriculum) {
      deptPreviewName.textContent = selectedDepartment;
      deptPreview.classList.add('show');
    } else {
      deptPreview.classList.remove('show');
    }
  }

  function selectFaculty(name) {
    selectedFaculty = name;
    setHiddenSelectValue(facultySelect, name);
    facultySelect.dispatchEvent(new Event('change'));
    // Changing faculty invalidates a department picked under a different one.
    if (selectedDepartment && !FACULTY_DEPARTMENTS[name].departments.some(d => d.value === selectedDepartment)) {
      selectedDepartment = '';
      setHiddenSelectValue(deptSelect, '');
      deptSelect.dispatchEvent(new Event('change'));
      updateDeptPreview(false);
    }
    deptSearch.value = '';
    renderFacultyChips(facultySearch.value);
    renderDeptChips('');
  }

  function selectDepartment(value, hasCurriculum) {
    selectedDepartment = value;
    setHiddenSelectValue(deptSelect, value);
    deptSelect.dispatchEvent(new Event('change'));
    renderDeptChips(deptSearch.value);
    updateDeptPreview(hasCurriculum);
  }

  function escapeHtml(s) {
    const div = document.createElement('div');
    div.textContent = s || '';
    return div.innerHTML;
  }

  facultySearch.addEventListener('input', () => renderFacultyChips(facultySearch.value));
  deptSearch.addEventListener('input', () => renderDeptChips(deptSearch.value));

  // Pre-fill from existing profile data (editing an existing profile) before
  // the first render, so a form submit that never touches these two fields
  // still carries the student's current faculty/department instead of wiping
  // them to empty.
  if (selectedFaculty) {
    setHiddenSelectValue(facultySelect, selectedFaculty);
    facultySelect.dispatchEvent(new Event('change'));
  }
  if (selectedDepartment) {
    setHiddenSelectValue(deptSelect, selectedDepartment);
    deptSelect.dispatchEvent(new Event('change'));
    const deptMeta = selectedFaculty && FACULTY_DEPARTMENTS[selectedFaculty]
      ? FACULTY_DEPARTMENTS[selectedFaculty].departments.find(d => d.value === selectedDepartment)
      : null;
    updateDeptPreview(!!(deptMeta && deptMeta.hasCurriculum));
  }

  renderFacultyChips('');
  renderDeptChips('');
}
