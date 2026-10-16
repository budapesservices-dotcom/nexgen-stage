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
    link.addEventListener('click', () => {
      navigation.querySelectorAll('details[open]').forEach((menu) => { menu.open = false; });
      closeNavigation();
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;

    const openDropdown = navigation.querySelector('details[open]');
    if (openDropdown) {
      openDropdown.open = false;
      openDropdown.querySelector('summary')?.focus();
    }

    if (toggle.getAttribute('aria-expanded') === 'true') {
      closeNavigation(true);
    }
  });

  document.addEventListener('click', (event) => {
    navigation.querySelectorAll('details[open]').forEach((menu) => {
      if (!menu.contains(event.target)) menu.open = false;
    });

    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
    if (isExpanded && !navigation.contains(event.target) && !toggle.contains(event.target)) {
      closeNavigation();
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 760) closeNavigation();
  }, { passive: true });
})();