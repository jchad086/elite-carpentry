/* Elite Carpentry & Renovations — site behaviour.
   No dependencies, no build step. ES5 so it runs anywhere without transpiling.
   Three jobs: the mobile nav drawer, scroll reveal, and the quote form. */
(function () {
  'use strict';

  var DESKTOP = window.matchMedia('(min-width: 940px)');

  /* --- Mobile nav drawer -------------------------------------------------- */

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  function setNav(open) {
    document.body.classList.toggle('nav-open', open);
    if (toggle) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setNav(!document.body.classList.contains('nav-open'));
    });

    // Escape closes the drawer and hands focus back to the control that opened it.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        setNav(false);
        toggle.focus();
      }
    });

    // Any nav link click closes it — same-page anchors would otherwise scroll
    // underneath an open drawer.
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });

    // Crossing into desktop layout must clear the drawer state, or body stays
    // locked with a hidden drawer.
    var onChange = function (e) { if (e.matches) setNav(false); };
    if (DESKTOP.addEventListener) DESKTOP.addEventListener('change', onChange);
    else if (DESKTOP.addListener) DESKTOP.addListener(onChange);
  }

  /* --- Scroll reveal ------------------------------------------------------ */

  var reveals = document.querySelectorAll('.reveal');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!('IntersectionObserver' in window) || reduced) {
    for (var i = 0; i < reveals.length; i++) reveals[i].classList.add('in');
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    for (var j = 0; j < reveals.length; j++) io.observe(reveals[j]);
  }

  /* --- Project carousel --------------------------------------------------- */
  /* Progressive enhancement only. The viewport is a CSS scroll-snap container,
     so every slide is reachable by scroll, swipe and keyboard with no JS at
     all — this just adds buttons and dots, and only reveals them once it runs.
     Deliberately no auto-advance: it takes control away from the reader and is
     a well-documented accessibility problem. */

  var carousel = document.querySelector('[data-carousel]');
  if (carousel) (function () {
    var viewport = carousel.querySelector('.carousel-viewport');
    var slides = [].slice.call(carousel.querySelectorAll('.slide'));
    var prev = carousel.querySelector('[data-prev]');
    var next = carousel.querySelector('[data-next]');
    var dots = [].slice.call(carousel.querySelectorAll('.car-dot'));
    if (!viewport || slides.length < 2) return;

    carousel.classList.add('is-enhanced');
    var index = 0;
    var stride = 0;

    // Measured rather than assumed to be i * width, so any gap or padding added
    // to the track later still lands on the right slide.
    function measure() {
      stride = slides.length > 1 ? slides[1].offsetLeft - slides[0].offsetLeft : 0;
    }

    function clamp(i) { return Math.max(0, Math.min(slides.length - 1, i)); }

    function sync(i) {
      index = i;
      dots.forEach(function (d, n) {
        if (n === i) d.setAttribute('aria-current', 'true');
        else d.removeAttribute('aria-current');
      });
      // Not a looping carousel, so the ends are genuinely dead. Disabling says
      // so rather than leaving a button that silently does nothing.
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === slides.length - 1;
    }

    function go(i) {
      i = clamp(i);
      sync(i);   // update state up front so rapid clicks keep advancing
      var left = slides[i].offsetLeft - slides[0].offsetLeft;
      try {
        viewport.scrollTo({ left: left, behavior: reduced ? 'auto' : 'smooth' });
      } catch (err) {
        viewport.scrollLeft = left;   // older engines: no options object
      }
    }

    // Position is derived from scrollLeft, which keeps swiping, dragging and
    // the buttons in agreement. An IntersectionObserver rooted on the viewport
    // looks like the natural fit here and is not: once the carousel scrolls out
    // of the window its root rect is empty, so it stops reporting entirely and
    // the dots silently freeze.
    function syncFromScroll() {
      if (stride) sync(clamp(Math.round(viewport.scrollLeft / stride)));
    }

    var ticking = false;
    viewport.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        syncFromScroll();
      });
    });

    // Settle-time backstop. rAF is throttled to nothing while the tab is
    // hidden, so a scroll that finishes in a background tab would otherwise
    // leave the dots stale when the reader comes back.
    if ('onscrollend' in viewport) {
      viewport.addEventListener('scrollend', syncFromScroll);
    }

    window.addEventListener('resize', measure);
    measure();

    if (prev) prev.addEventListener('click', function () { go(index - 1); });
    if (next) next.addEventListener('click', function () { go(index + 1); });
    dots.forEach(function (d) {
      d.addEventListener('click', function () { go(+d.getAttribute('data-go')); });
    });

    carousel.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(index - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); go(index + 1); }
    });

    sync(0);
  })();

  /* --- Quote form --------------------------------------------------------- */

  var form = document.getElementById('quoteForm');
  if (!form) return;

  var btn = form.querySelector('.btn-submit');
  var okMsg = document.getElementById('formOk');
  var errMsg = document.getElementById('formErr');
  var btnLabel = btn ? btn.innerHTML : '';

  function showOnly(el) {
    if (okMsg) okMsg.classList.remove('show');
    if (errMsg) errMsg.classList.remove('show');
    if (el) el.classList.add('show');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Honeypot: real people never fill this in.
    var trap = form.querySelector('input[name="_gotcha"]');
    if (trap && trap.value) return;

    // The form is novalidate so this handler always runs; validate explicitly
    // rather than letting a blank submission POST.
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // The endpoint still holds the placeholder — fail loudly rather than
    // silently swallowing a lead.
    if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
      showOnly(errMsg);
      if (errMsg) errMsg.focus();
      return;
    }

    if (btn) {
      btn.disabled = true;
      btn.innerHTML = 'Sending&hellip;';
    }
    showOnly(null);

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    })
      .then(function (res) {
        if (!res.ok) throw new Error('Bad response');
        form.reset();
        showOnly(okMsg);
        if (btn) btn.innerHTML = 'Request sent';
        if (okMsg) okMsg.focus();
      })
      .catch(function () {
        showOnly(errMsg);
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = btnLabel;
        }
      });
  });
})();
