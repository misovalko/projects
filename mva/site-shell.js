(function () {
  'use strict';

  function activateTeaching(menu) {
    menu.querySelectorAll('.menulink a.active').forEach(function (a) {
      a.classList.remove('active');
    });
    var teaching = menu.querySelector('.menulink a[href="/mva-ml-graphs.html"], .menulink a[href$="/mva-ml-graphs.html"]');
    if (teaching) teaching.classList.add('active');
  }

  function hydrateNavigation() {
    var current = document.getElementById('menu');
    if (!current) return;

    fetch('/site-nav-fragment.html', { cache: 'no-cache' })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.text();
      })
      .then(function (html) {
        var holder = document.createElement('div');
        holder.innerHTML = html.trim();
        var canonical = holder.querySelector('#menu');
        if (!canonical) throw new Error('Canonical navigation fragment has no #menu');
        activateTeaching(canonical);
        current.replaceWith(canonical);
      })
      .catch(function (error) {
        console.warn('Could not hydrate canonical site navigation; using static fallback.', error);
        activateTeaching(current);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrateNavigation, { once: true });
  } else {
    hydrateNavigation();
  }
})();
