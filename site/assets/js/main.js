/* WOW PRINT — Interaktionen & Animationen */
(function () {
  'use strict';

  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var hasGsap = typeof window.gsap !== 'undefined';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  if (hasGsap && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  /* ---------- Smooth scroll ---------- */
  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true });
    if (hasGsap) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href');
        if (id.length > 1 && $(id)) { e.preventDefault(); lenis.scrollTo(id, { offset: -60 }); }
      });
    });
  }

  /* ---------- Text splitting ---------- */
  $$('[data-split]').forEach(function (el) {
    var html = el.innerHTML.trim();
    // Nur reiner Text bzw. <em>/<br> werden in Wörter zerlegt
    var tmp = document.createElement('div');
    tmp.innerHTML = html;
    var out = '';
    tmp.childNodes.forEach(function (node) {
      if (node.nodeType === 3) {
        node.textContent.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          out += /^\s+$/.test(w) ? ' ' : '<span class="word"><span>' + w + '</span></span>';
        });
      } else if (node.nodeName === 'BR') {
        out += '<br>';
      } else {
        out += '<span class="word"><span>' + node.outerHTML + '</span></span>';
      }
    });
    el.innerHTML = out;
  });

  /* ---------- Preloader ---------- */
  var preloader = $('.preloader');
  var firstVisit = false;
  try { firstVisit = !sessionStorage.getItem('wow-visited'); sessionStorage.setItem('wow-visited', '1'); } catch (e) {}

  function intro() {
    if (!hasGsap || reduce) return;
    var tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
    tl.from('.hero h1 .line > span, .page-hero h1 .line > span', { yPercent: 110, duration: 1.4, stagger: .09 })
      .from('.hero-media img', { scale: 1.25, duration: 2, ease: 'power3.out' }, 0)
      .from('.hero-media', { clipPath: 'inset(0 0 0 100%)', duration: 1.5, ease: 'expo.inOut' }, 0)
      .from('.hero-bgword', { xPercent: -8, opacity: 0, duration: 2 }, 0)
      .from('.hero-bottom > *, .page-hero .breadcrumb, .page-hero .eyebrow', { y: 24, opacity: 0, duration: 1.1, stagger: .08 }, .35)
      .from('.page-hero .bg-num', { y: 60, opacity: 0, duration: 1.6 }, .1)
      .from('.site-header .wrap > *', { y: -20, opacity: 0, duration: 1, stagger: .06 }, .2);
  }

  if (preloader && firstVisit && hasGsap && !reduce) {
    preloader.classList.add('is-active');
    if (lenis) lenis.stop();
    var count = { v: 0 };
    var countEl = $('.preloader-count', preloader);
    var tl = gsap.timeline();
    tl.from('.preloader-word span', { yPercent: 120, duration: 1, stagger: .08, ease: 'expo.out' })
      .to(count, { v: 100, duration: 1.4, ease: 'power2.inOut', onUpdate: function () { countEl.textContent = Math.round(count.v); } }, 0)
      .to('.preloader-word', { scale: 1.08, duration: 1.4, ease: 'none' }, 0)
      .to('.preloader-word span', { color: '#f6f5f1', duration: .2, stagger: .05 }, 1.1)
      .to(preloader, { clipPath: 'inset(0 0 100% 0)', duration: 1, ease: 'expo.inOut', onComplete: function () {
        preloader.remove(); if (lenis) lenis.start();
      } }, 1.55)
      .add(intro, 1.75);
  } else {
    if (preloader) preloader.remove();
    var pt0 = $('.page-transition');
    if (pt0 && hasGsap && !reduce && !firstVisit) {
      gsap.set('.page-transition span', { scaleY: 1 });
      gsap.to('.page-transition span:first-child', { scaleY: 0, transformOrigin: 'top', duration: .8, ease: 'expo.inOut' });
      gsap.to('.page-transition span:last-child', { scaleY: 0, transformOrigin: 'bottom', duration: .8, ease: 'expo.inOut' });
      gsap.delayedCall(.25, intro);
    } else {
      intro();
    }
  }

  /* ---------- Page transitions ---------- */
  var pt = $('.page-transition');
  if (pt && hasGsap && !reduce) {
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      var href = a.getAttribute('href');
      if (!href || a.target === '_blank' || a.hasAttribute('download') || href.charAt(0) === '#' || /^(mailto|tel|javascript):/.test(href)) return;
      var url = new URL(a.href, location.href);
      if (url.origin !== location.origin) return;
      if (url.pathname === location.pathname && url.hash) return;
      e.preventDefault();
      document.body.classList.remove('menu-open');
      gsap.set('.page-transition span:first-child', { transformOrigin: 'bottom' });
      gsap.set('.page-transition span:last-child', { transformOrigin: 'top' });
      gsap.to('.page-transition span', { scaleY: 1, duration: .7, ease: 'expo.inOut', stagger: .06, onComplete: function () { location.href = a.href; } });
    });
    window.addEventListener('pageshow', function (e) {
      if (e.persisted) gsap.set('.page-transition span', { scaleY: 0 });
    });
  }

  /* ---------- Header ---------- */
  var header = $('.site-header');
  var lastY = 0;
  function onScroll() {
    var y = window.scrollY;
    if (!header) return;
    header.classList.toggle('is-scrolled', y > 40);
    if (!document.body.classList.contains('menu-open')) header.classList.toggle('is-hidden', y > 300 && y > lastY);
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menu ---------- */
  var burger = $('.burger');
  var menu = $('.menu');
  var menuOpen = false;
  function setMenu(open) {
    menuOpen = open;
    document.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open);
    menu.setAttribute('aria-hidden', !open);
    if (lenis) open ? lenis.stop() : lenis.start();
    if (hasGsap && !reduce) {
      if (open) {
        gsap.set(menu, { visibility: 'visible' });
        gsap.to(menu, { clipPath: 'inset(0 0 0% 0)', duration: .9, ease: 'expo.inOut' });
        gsap.fromTo('.menu-links a', { yPercent: 110 }, { yPercent: 0, duration: 1, stagger: .06, ease: 'expo.out', delay: .35 });
        gsap.fromTo('.menu-side > *', { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: .8, stagger: .07, delay: .5 });
      } else {
        gsap.to(menu, { clipPath: 'inset(0 0 100% 0)', duration: .8, ease: 'expo.inOut', onComplete: function () { gsap.set(menu, { visibility: 'hidden' }); } });
      }
    } else {
      menu.style.visibility = open ? 'visible' : 'hidden';
      menu.style.clipPath = open ? 'inset(0 0 0% 0)' : 'inset(0 0 100% 0)';
    }
    if (open) { var f = $('.menu-links a'); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 400); }
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(!menuOpen); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menuOpen) { setMenu(false); burger.focus(); } });
  }

  /* ---------- Cursor ---------- */
  var cursor = $('.cursor');
  if (cursor && finePointer && hasGsap) {
    var dot = $('.cursor-dot', cursor), ring = $('.cursor-ring', cursor), label = $('.cursor-ring span', cursor);
    var xDot = gsap.quickTo(dot, 'x', { duration: .1 }), yDot = gsap.quickTo(dot, 'y', { duration: .1 });
    var xRing = gsap.quickTo(ring, 'x', { duration: .45, ease: 'power3' }), yRing = gsap.quickTo(ring, 'y', { duration: .45, ease: 'power3' });
    window.addEventListener('mousemove', function (e) { xDot(e.clientX); yDot(e.clientY); xRing(e.clientX); yRing(e.clientY); });
    document.addEventListener('mouseleave', function () { cursor.classList.add('is-hidden'); });
    document.addEventListener('mouseenter', function () { cursor.classList.remove('is-hidden'); });
    document.addEventListener('mouseover', function (e) {
      var l = e.target.closest('[data-cursor]');
      var a = e.target.closest('a, button, summary, label, input[type=range], .choice');
      cursor.classList.toggle('is-label', !!l);
      cursor.classList.toggle('is-link', !l && !!a);
      if (l) label.textContent = l.getAttribute('data-cursor');
    });
  }

  /* ---------- Magnetic ---------- */
  if (finePointer && hasGsap && !reduce) {
    $$('[data-magnetic]').forEach(function (el) {
      var s = parseFloat(el.getAttribute('data-magnetic')) || .3;
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        gsap.to(el, { x: (e.clientX - r.left - r.width / 2) * s, y: (e.clientY - r.top - r.height / 2) * s, duration: .6, ease: 'power3.out' });
      });
      el.addEventListener('mouseleave', function () { gsap.to(el, { x: 0, y: 0, duration: .9, ease: 'elastic.out(1, .4)' }); });
    });
  }

  /* ---------- Scroll animations ---------- */
  if (hasGsap && window.ScrollTrigger && !reduce) {
    // Reveal
    gsap.set('[data-reveal]', { opacity: 0 });
    ScrollTrigger.batch('[data-reveal]', {
      start: 'top 88%', once: true,
      onEnter: function (els) { gsap.fromTo(els, { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 1.2, ease: 'expo.out', stagger: .08 }); }
    });

    // Wörter
    $$('[data-split]').forEach(function (el) {
      if (el.closest('.hero, .page-hero')) {
        gsap.from($$('.word > span', el), { yPercent: 110, duration: 1.2, ease: 'expo.out', stagger: .03, delay: .5 });
        return;
      }
      gsap.from($$('.word > span', el), { yPercent: 110, duration: 1.2, ease: 'expo.out', stagger: .04, scrollTrigger: { trigger: el, start: 'top 88%' } });
    });

    // Zeilen-Headlines ausserhalb des Heros
    $$('[data-lines]').forEach(function (el) {
      gsap.from($$('.line > span', el), { yPercent: 110, duration: 1.3, ease: 'expo.out', stagger: .08, scrollTrigger: { trigger: el, start: 'top 85%' } });
    });

    // Parallax
    $$('[data-parallax]').forEach(function (el) {
      var amt = parseFloat(el.getAttribute('data-parallax')) || .15;
      gsap.fromTo(el, { yPercent: -amt * 50 }, { yPercent: amt * 50, ease: 'none', scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    // Hero
    if ($('.hero')) {
      gsap.to('.hero-media img', { yPercent: 12, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
      gsap.to('.hero-bgword', { xPercent: -18, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
      gsap.to('.hero-content', { yPercent: -18, opacity: .2, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'center top', end: 'bottom top', scrub: true } });
    }

    // Statement: Wort für Wort
    $$('.statement-text').forEach(function (el) {
      var parts = [];
      el.childNodes.forEach(function (n) { parts.push(n); });
      el.innerHTML = '';
      parts.forEach(function (n) {
        var isEm = n.nodeName === 'EM';
        var text = n.textContent;
        text.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) { el.appendChild(document.createTextNode(' ')); return; }
          var s = document.createElement(isEm ? 'em' : 'span');
          s.className = 'w'; s.textContent = w; el.appendChild(s);
        });
      });
      gsap.to($$('.w', el), { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: true } });
    });

    // Prozess-Linie
    $$('.process-line i').forEach(function (line) {
      gsap.fromTo(line, { '--p': 0 }, { '--p': 1, ease: 'none', scrollTrigger: { trigger: '.process-steps', start: 'top 80%', end: 'bottom 55%', scrub: true } });
    });
    $$('.process .step').forEach(function (s, i) {
      gsap.from(s, { y: 40, opacity: 0, duration: 1, ease: 'expo.out', delay: i * .08, scrollTrigger: { trigger: '.process-steps', start: 'top 80%' } });
    });

    // CTA Fill
    $$('.cta-title .fill').forEach(function (el) {
      gsap.fromTo(el, { '--fill': '0%' }, { '--fill': '100%', ease: 'none', scrollTrigger: { trigger: el, start: 'top 90%', end: 'top 45%', scrub: true } });
    });

    // Horizontale Projekte
    var mm = gsap.matchMedia();
    mm.add('(min-width: 900px)', function () {
      var track = $('.projects-track');
      if (!track) return;
      var dist = function () { return track.scrollWidth - window.innerWidth; };
      gsap.to(track, {
        x: function () { return -dist(); }, ease: 'none',
        scrollTrigger: { trigger: '.projects-pin', start: 'top top', end: function () { return '+=' + dist(); }, pin: true, scrub: 1, invalidateOnRefresh: true }
      });
    });

    // Service-Karten
    ScrollTrigger.batch('.service-card', {
      start: 'top 90%', once: true,
      onEnter: function (els) { gsap.from(els, { y: 60, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: .07 }); }
    });

    // Footer-Riesenwort
    if ($('.footer-giant')) {
      gsap.from('.footer-giant span', { yPercent: 60, opacity: 0, duration: 1.2, ease: 'expo.out', stagger: .04, scrollTrigger: { trigger: '.footer-giant', start: 'top 95%' } });
    }

    window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  }

  /* ---------- Marquee ---------- */
  $$('.marquee').forEach(function (m) {
    var track = $('.marquee-track', m);
    var group = $('.marquee-group', m);
    if (!track || !group) return;
    track.appendChild(group.cloneNode(true)).setAttribute('aria-hidden', 'true');
    if (reduce) return;
    var dir = m.hasAttribute('data-reverse') ? 1 : -1;
    var x = 0, speed = 1, w = group.offsetWidth;
    window.addEventListener('resize', function () { w = group.offsetWidth; });
    if (lenis) lenis.on('scroll', function (e) { speed = 1 + Math.min(Math.abs(e.velocity) * .25, 8); });
    (function loop() {
      x += dir * .6 * speed;
      speed += (1 - speed) * .05;
      if (x <= -w) x += w; if (x > 0) x -= w;
      track.style.transform = 'translate3d(' + x + 'px,0,0)';
      requestAnimationFrame(loop);
    })();
  });

  /* ---------- Hover-Bild in Service-Liste ---------- */
  var hoverImg = $('.hover-img');
  if (hoverImg && finePointer && hasGsap) {
    var img = $('img', hoverImg);
    var hx = gsap.quickTo(hoverImg, 'left', { duration: .6, ease: 'power3' }), hy = gsap.quickTo(hoverImg, 'top', { duration: .6, ease: 'power3' });
    $$('.svc-row').forEach(function (row) {
      row.addEventListener('mouseenter', function () { img.src = row.getAttribute('data-img'); hoverImg.classList.add('is-visible'); });
      row.addEventListener('mouseleave', function () { hoverImg.classList.remove('is-visible'); });
    });
    window.addEventListener('mousemove', function (e) { hx(e.clientX); hy(e.clientY); });
  }

  /* ---------- Projekte filtern ---------- */
  $$('.filters').forEach(function (bar) {
    var cards = $$('.work-card');
    bar.addEventListener('click', function (e) {
      var chip = e.target.closest('.chip');
      if (!chip) return;
      $$('.chip', bar).forEach(function (c) { c.classList.toggle('is-active', c === chip); c.setAttribute('aria-pressed', c === chip); });
      var f = chip.getAttribute('data-filter');
      cards.forEach(function (c) { c.classList.toggle('is-out', f !== 'all' && c.getAttribute('data-cat') !== f); });
      if (hasGsap && !reduce) gsap.fromTo(cards.filter(function (c) { return !c.classList.contains('is-out'); }), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: .9, ease: 'expo.out', stagger: .06 });
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    });
  });

  /* ---------- Vorher / Nachher ---------- */
  $$('.ba').forEach(function (ba) {
    var input = $('input', ba);
    var set = function () { ba.style.setProperty('--pos', input.value + '%'); };
    input.addEventListener('input', set); set();
    if (hasGsap && !reduce && window.ScrollTrigger) {
      var o = { v: 85 };
      gsap.to(o, { v: 50, duration: 1.6, ease: 'expo.inOut', scrollTrigger: { trigger: ba, start: 'top 70%' }, onUpdate: function () { input.value = o.v; set(); } });
    }
  });

  /* ---------- Öffnungszeiten-Status ---------- */
  function openStatus() {
    var parts;
    try {
      parts = new Intl.DateTimeFormat('de-CH', { timeZone: 'Europe/Zurich', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    } catch (e) { return; }
    var get = function (t) { var p = parts.find(function (x) { return x.type === t; }); return p ? p.value : ''; };
    var day = get('weekday').replace('.', '');
    var mins = parseInt(get('hour'), 10) * 60 + parseInt(get('minute'), 10);
    var weekday = ['Mo', 'Di', 'Mi', 'Do', 'Fr'].indexOf(day) > -1;
    var open = weekday && ((mins >= 540 && mins < 720) || (mins >= 840 && mins < 1020));
    var text;
    if (open) text = mins < 720 ? 'Jetzt geöffnet · bis 12:00' : 'Jetzt geöffnet · bis 17:00';
    else if (weekday && mins >= 720 && mins < 840) text = 'Mittagspause · ab 14:00 wieder da';
    else if (weekday && mins < 540) text = 'Geschlossen · öffnet um 09:00';
    else text = 'Geschlossen · Mo–Fr ab 09:00';
    $$('.open-status').forEach(function (el) { el.classList.toggle('is-open', open); $('span', el).textContent = text; });
  }
  openStatus(); setInterval(openStatus, 60000);

  /* ---------- Offert-Wizard ---------- */
  var wizard = $('.wizard');
  if (wizard) {
    var steps = $$('fieldset', wizard);
    var marks = $$('.wizard-progress li', wizard);
    var back = $('.back', wizard), next = $('.next', wizard), submit = $('.submit', wizard), err = $('.wizard-error', wizard);
    var cur = 0;
    var params = new URLSearchParams(location.search);
    var pre = params.get('leistung');
    if (pre) $$('input[name="leistung[]"]', wizard).forEach(function (i) { if (i.value === pre) i.checked = true; });

    var show = function (i) {
      steps.forEach(function (s, j) { s.classList.toggle('is-current', j === i); });
      marks.forEach(function (m, j) { m.classList.toggle('is-current', j === i); m.classList.toggle('is-done', j < i); });
      back.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      submit.hidden = i !== steps.length - 1;
      err.textContent = '';
      if (hasGsap && !reduce) gsap.from(steps[i].children, { y: 30, opacity: 0, duration: .8, ease: 'expo.out', stagger: .05 });
      cur = i;
    };
    var valid = function (i) {
      var s = steps[i];
      if (s.hasAttribute('data-require-one') && !$$('input[type=checkbox]:checked', s).length) {
        err.textContent = 'Bitte wählen Sie mindestens eine Leistung aus.'; return false;
      }
      var fields = $$('input, textarea, select', s);
      for (var k = 0; k < fields.length; k++) {
        if (!fields[k].checkValidity()) { fields[k].reportValidity(); return false; }
      }
      return true;
    };
    var scrollTop = function () {
      var top = wizard.getBoundingClientRect().top + window.scrollY - 120;
      if (lenis) lenis.scrollTo(top); else window.scrollTo({ top: top, behavior: 'smooth' });
    };
    next.addEventListener('click', function () { if (valid(cur)) { show(cur + 1); scrollTop(); } });
    back.addEventListener('click', function () { show(cur - 1); scrollTop(); });
    wizard.addEventListener('submit', function (e) {
      if (!valid(cur)) { e.preventDefault(); return; }
      var total = 0;
      $$('input[type=file]', wizard).forEach(function (f) { if (f.files[0]) total += f.files[0].size; });
      if (total > 8 * 1024 * 1024) { e.preventDefault(); err.textContent = 'Die Dateien sind zusammen grösser als 8 MB. Bitte verkleinern oder per E-Mail nachreichen.'; }
    });
    show(0);
  }

  /* ---------- Dropzones ---------- */
  $$('.dropzone').forEach(function (dz) {
    var input = $('input', dz), title = $('strong', dz), small = $('small', dz);
    var origT = title.textContent, origS = small.textContent;
    ['dragenter', 'dragover'].forEach(function (ev) { dz.addEventListener(ev, function () { dz.classList.add('is-drag'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { dz.addEventListener(ev, function () { dz.classList.remove('is-drag'); }); });
    input.addEventListener('change', function () {
      var f = input.files[0];
      dz.classList.toggle('has-file', !!f);
      title.textContent = f ? f.name : origT;
      small.textContent = f ? (f.size / 1024 / 1024).toFixed(2) + ' MB · Klicken zum Ändern' : origS;
    });
  });

  /* ---------- Jahr ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
