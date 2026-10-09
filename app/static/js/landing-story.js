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
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStoryAnimation, { once: true });
  } else {
    initStoryAnimation();
  }
})();
