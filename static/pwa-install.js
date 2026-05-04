// pwa-install.js
// Custom install banner for Nelavista PWA

(function() {
  'use strict';

  let deferredPrompt;

  // Check if already running in standalone mode (installed)
  if (window.matchMedia('(display-mode: standalone)').matches) {
    return; // App already installed, no need to prompt
  }

  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the default mini-info bar
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;

    // Only show banner once per page load (no duplicate)
    if (!document.getElementById('nelavista-install-banner')) {
      createInstallBanner();
    }
  });

  function createInstallBanner() {
    // Inject styles for animation and layout
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slideDown {
        from { transform: translateY(-100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
      .nelavista-install-banner {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 99999;
        background: linear-gradient(135deg, #00D9FF, #0099CC);
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        animation: slideDown 0.4s ease-out;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
      }
      .nelavista-install-banner .content {
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .nelavista-install-banner .icon svg {
        width: 36px;
        height: 36px;
      }
      .nelavista-install-banner .text {
        line-height: 1.3;
      }
      .nelavista-install-banner .title {
        font-size: 14px;
        font-weight: 700;
        margin: 0;
      }
      .nelavista-install-banner .subtitle {
        font-size: 12px;
        opacity: 0.9;
        margin: 0;
      }
      .nelavista-install-banner .actions {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .nelavista-install-banner .download-btn {
        background: #ffffff;
        color: #00A8CC;
        border: none;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.1s;
      }
      .nelavista-install-banner .download-btn:active {
        transform: scale(0.96);
      }
      .nelavista-install-banner .close-btn {
        background: none;
        border: none;
        color: #fff;
        font-size: 22px;
        cursor: pointer;
        opacity: 0.7;
        line-height: 1;
        padding: 0 4px;
      }
    `;
    document.head.appendChild(style);

    // Download SVG icon
    const downloadIconSVG = `
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2V16M12 16L8 11M12 16L16 11" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M4 17V21H20V17" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `;

    // Build banner DOM
    const banner = document.createElement('div');
    banner.id = 'nelavista-install-banner';
    banner.className = 'nelavista-install-banner';
    banner.innerHTML = `
      <div class="content">
        <div class="icon">${downloadIconSVG}</div>
        <div class="text">
          <div class="title">Download Nelavista</div>
          <div class="subtitle">Install for faster access &amp; offline use</div>
        </div>
      </div>
      <div class="actions">
        <button class="download-btn" id="nelavista-download-btn">Download</button>
        <button class="close-btn" id="nelavista-close-btn">&times;</button>
      </div>
    `;
    document.body.appendChild(banner);

    // Download button handler
    document.getElementById('nelavista-download-btn').addEventListener('click', async () => {
      if (!deferredPrompt) return;
      // Show the install prompt
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      console.log(`User response to install prompt: ${outcome}`);
      // Clear the saved prompt, it can't be used again
      deferredPrompt = null;
      // Remove banner after interaction (installed or not)
      banner.remove();
    });

    // Close button handler
    document.getElementById('nelavista-close-btn').addEventListener('click', () => {
      banner.remove();
      // Note: deferredPrompt remains untouched; user could still install via other trigger if implemented
    });
  }

  // Listen for app installed event to clean up
  window.addEventListener('appinstalled', () => {
    console.log('Nelavista PWA installed successfully');
    const banner = document.getElementById('nelavista-install-banner');
    if (banner) banner.remove();
    deferredPrompt = null;
  });

})();