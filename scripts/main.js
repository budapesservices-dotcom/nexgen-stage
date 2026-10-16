(() => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const navigation = document.querySelector('[data-site-nav]');

  if (!toggle || !navigation) return;

  const closeNavigation = () => {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.querySelector('.sr-only').textContent = 'Open navigation';
    navigation.classList.remove('is-open');
    document.body.classList.remove('nav-is-open');
  };

  const openNavigation = () => {
    toggle.setAttribute('aria-expanded', 'true');
    toggle.querySelector('.sr-only').textContent = 'Close navigation';
    navigation.classList.add('is-open');
    document.body.classList.add('nav-is-open');
  };

  toggle.addEventListener('click', () => {
    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
    isExpanded ? closeNavigation() : openNavigation();
  });

  navigation.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeNavigation);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNavigation();
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 760) closeNavigation();
  }, { passive: true });
})();