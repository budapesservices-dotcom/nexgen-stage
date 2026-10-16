(() => {
  document.documentElement.classList.add('has-js');

  const toggle = document.querySelector('[data-nav-toggle]');
  const navigation = document.querySelector('[data-site-nav]');
  const label = toggle?.querySelector('.sr-only');

  if (!toggle || !navigation || !label) return;

  const closeNavigation = (restoreFocus = false) => {
    toggle.setAttribute('aria-expanded', 'false');
    label.textContent = 'Open navigation';
    navigation.classList.remove('is-open');
    document.body.classList.remove('nav-is-open');

    if (restoreFocus) toggle.focus();
  };

  const openNavigation = () => {
    toggle.setAttribute('aria-expanded', 'true');
    label.textContent = 'Close navigation';
    navigation.classList.add('is-open');
    document.body.classList.add('nav-is-open');
  };

  toggle.addEventListener('click', () => {
    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
    isExpanded ? closeNavigation() : openNavigation();
  });

  navigation.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => closeNavigation());
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      closeNavigation(true);
    }
  });

  document.addEventListener('click', (event) => {
    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
    if (isExpanded && !navigation.contains(event.target) && !toggle.contains(event.target)) {
      closeNavigation();
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 760) closeNavigation();
  }, { passive: true });
})();