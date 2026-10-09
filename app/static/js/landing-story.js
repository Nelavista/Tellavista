(function () {
  function initStoryAnimation() {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const revealTargets = [
      { element: document.querySelector('[data-fragment-reveal]'), threshold: 0.35, reducedClass: true },
      { element: document.querySelector('[data-opportunity-reveal]'), threshold: 0.12, reducedClass: false }
    ].filter((target) => target.element);

    revealTargets.forEach(({ element, threshold, reducedClass }) => {
      if (reducedMotion || !('IntersectionObserver' in window)) {
        element.classList.add('is-visible');
        if (reducedClass && reducedMotion) element.classList.add('is-reduced');
        return;
      }

      const observer = new IntersectionObserver((entries) => {
        if (!entries.some((entry) => entry.isIntersecting)) return;
        element.classList.add('is-visible');
        observer.disconnect();
      }, { threshold });

      observer.observe(element);
    });

    const badge = document.querySelector('[data-hero-badge]');
    if (!badge) return;

    if (reducedMotion) {
      badge.classList.add('is-active', 'is-reduced');
      return;
    }

    if (!('IntersectionObserver' in window)) {
      badge.classList.add('is-active');
      return;
    }

    const badgeObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.target === badge) badge.classList.toggle('is-active', entry.isIntersecting);
      });
    }, { threshold: 0.01 });

    badgeObserver.observe(badge);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStoryAnimation, { once: true });
  } else {
    initStoryAnimation();
  }
})();
