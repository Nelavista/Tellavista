(function () {
  const dialog = document.getElementById('logoutConfirmDialog');
  if (!dialog) return;

  const confirmButton = dialog.querySelector('[data-logout-confirm]');
  const cancelButton = dialog.querySelector('[data-logout-cancel]');
  let pendingLogout = null;

  document.addEventListener('click', function (event) {
    const trigger = event.target.closest('[data-confirm-logout]');
    if (!trigger) return;

    event.preventDefault();
    pendingLogout = trigger;
    if (typeof dialog.showModal === 'function') {
      dialog.showModal();
    } else if (window.confirm('Are you sure you want to log out of Nelavista?')) {
      window.location.assign(trigger.href);
    }
  });

  confirmButton.addEventListener('click', function () {
    if (pendingLogout) window.location.assign(pendingLogout.href);
  });

  cancelButton.addEventListener('click', function () {
    dialog.close();
  });

  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener('close', function () {
    if (pendingLogout) pendingLogout.focus();
    pendingLogout = null;
  });
})();
