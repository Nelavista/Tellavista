// static/js/pwa-install.js
(function() {
  'use strict';
  
  let deferredPrompt;
  let installBanner;
  let isInstalled = false;
  
  // Check if already installed
  if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('📱 App is already installed');
    isInstalled = true;
  }
  
  // Create install banner element
  function createInstallBanner() {
    if (document.querySelector('.nelavista-install-banner')) return;
    
    installBanner = document.createElement('div');
    installBanner.className = 'nelavista-install-banner';
    installBanner.innerHTML = `
      <div class="content">
        <div class="icon">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="36" height="36" rx="8" fill="white" fill-opacity="0.2"/>
            <path d="M10 18L16 24L26 12" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="text">
          <p class="title">Install Nelavista</p>
          <p class="subtitle">Add to home screen for quick access</p>
        </div>
      </div>
      <div class="actions">
        <button class="download-btn" id="installBtn">Install</button>
        <button class="close-btn" id="closeBanner">×</button>
      </div>
    `;
    
    document.body.appendChild(installBanner);
    
    document.getElementById('installBtn').addEventListener('click', installApp);
    document.getElementById('closeBanner').addEventListener('click', () => {
      installBanner.remove();
      localStorage.setItem('pwa-banner-dismissed', Date.now());
    });
  }
  
  // Install function
  async function installApp() {
    if (!deferredPrompt) return;
    
    deferredPrompt.prompt();
    const result = await deferredPrompt.userChoice;
    
    if (result.outcome === 'accepted') {
      console.log('✅ App installed successfully');
      isInstalled = true;
      installBanner?.remove();
    }
    
    deferredPrompt = null;
  }
  
  // Listen for install prompt
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    const dismissed = localStorage.getItem('pwa-banner-dismissed');
    const twentyFourHours = 24 * 60 * 60 * 1000;
    
    if (!isInstalled && (!dismissed || (Date.now() - dismissed) > twentyFourHours)) {
      setTimeout(createInstallBanner, 2000);
    }
  });
  
  // Track successful installation
  window.addEventListener('appinstalled', () => {
    console.log('🎉 App installed');
    isInstalled = true;
    deferredPrompt = null;
    installBanner?.remove();
    localStorage.removeItem('pwa-banner-dismissed');
    
    // Track installation
    if (typeof gtag !== 'undefined') {
      gtag('event', 'pwa_install', {
        event_category: 'engagement',
        event_label: 'PWA Installation'
      });
    }
  });
  
  // Hide banner when app launched as PWA
  if (isInstalled) {
    const observer = new MutationObserver(() => {
      installBanner?.remove();
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
