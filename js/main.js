/* CloudxAi · CloudDIET — interactions */
(function () {
  // Theme toggle (light / dark) — initial theme already set by inline <head> script
  const themeBtns = document.querySelectorAll('[data-set-theme]');
  const syncTheme = () => {
    const t = document.documentElement.getAttribute('data-theme') || 'light';
    themeBtns.forEach((b) => b.classList.toggle('active', b.dataset.setTheme === t));
  };
  themeBtns.forEach((b) => b.addEventListener('click', () => {
    document.documentElement.setAttribute('data-theme', b.dataset.setTheme);
    try { localStorage.setItem('theme', b.dataset.setTheme); } catch (e) {}
    syncTheme();
  }));
  syncTheme();

  const nav = document.querySelector('.nav');

  // Sticky nav: frosted glass on scroll
  const onScroll = () => {
    if (window.scrollY > 24) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  const menuBtn = document.querySelector('.menu-btn');
  const mobile = document.querySelector('.mobile-menu');
  const closeBtn = document.querySelector('.mm-close');
  const open = () => { mobile.classList.add('open'); document.body.style.overflow = 'hidden'; };
  const close = () => { mobile.classList.remove('open'); document.body.style.overflow = ''; };
  if (menuBtn) menuBtn.addEventListener('click', open);
  if (closeBtn) closeBtn.addEventListener('click', close);
  if (mobile) mobile.querySelectorAll('a').forEach(a => a.addEventListener('click', close));

  // Scroll reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.anim-up').forEach(el => io.observe(el));

  // Count-up for elements with data-count
  const fmt = (n, el) => {
    const pre = el.dataset.prefix || '';
    const suf = el.dataset.suffix || '';
    const target = parseFloat(el.dataset.count);
    const dec = Number.isInteger(target) ? 0 : 1;        // keep decimals (e.g. 3.8)
    return pre + n.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf;
  };
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const target = parseFloat(el.dataset.count);
      const dur = 1400; const start = performance.now();
      const tick = (now) => {
        const p = Math.min((now - start) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = fmt(target * eased, el);
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      countIO.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach(el => countIO.observe(el));

  // ---- Hero: subtle floating SVG paths (ported from the "floating-paths" component) ----
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // exact path formula from the component
  const pathData = (position, i) =>
    `M-${380 - i * 5 * position} -${189 + i * 6}C-${380 - i * 5 * position} -${189 + i * 6} -${312 - i * 5 * position} ${216 - i * 6} ${152 - i * 5 * position} ${343 - i * 6}C${616 - i * 5 * position} ${470 - i * 6} ${684 - i * 5 * position} ${875 - i * 6} ${684 - i * 5 * position} ${875 - i * 6}`;

  const buildPaths = () => {
    const NS = 'http://www.w3.org/2000/svg';
    const wrap = document.createElement('div');
    wrap.className = 'hero-paths';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 696 316');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    // brand-coloured gradient stroke (matches site palette)
    const defs = document.createElementNS(NS, 'defs');
    defs.innerHTML = '<linearGradient id="pathGrad" x1="0" y1="0" x2="1" y2="1">'
      + '<stop offset="0" stop-color="#21B7FF"/><stop offset="0.5" stop-color="#9B5CFF"/>'
      + '<stop offset="1" stop-color="#E0218A"/></linearGradient>';
    svg.appendChild(defs);
    for (let i = 0; i < 26; i++) {
      const p = document.createElementNS(NS, 'path');
      p.setAttribute('d', pathData(-1, i));
      p.setAttribute('stroke', 'url(#pathGrad)');
      p.setAttribute('stroke-width', (0.6 + i * 0.04).toFixed(2));
      p.setAttribute('stroke-opacity', (0.06 + i * 0.016).toFixed(3));
      svg.appendChild(p);
    }
    wrap.appendChild(svg);
    return { wrap, svg };
  };

  document.querySelectorAll('.hero, .page-hero').forEach((hero) => {
    const host = hero.querySelector('.hero-bg') || hero;
    const grid = host.querySelector('.hero-grid');
    const { wrap } = buildPaths();          // static paths; gentle drift is a CSS transform (GPU)
    host.appendChild(wrap);
    if (reduce) return;

    // slight mouse parallax — transform only (compositor), so it never fights scrolling
    let tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
    const loop = () => {
      cx += (tx - cx) * 0.07; cy += (ty - cy) * 0.07;
      wrap.style.transform = `translate3d(${(cx * 12).toFixed(2)}px, ${(cy * 12).toFixed(2)}px, 0)`;
      if (grid) grid.style.transform = `translate3d(${(cx * -5).toFixed(2)}px, ${(cy * -5).toFixed(2)}px, 0)`;
      raf = (Math.abs(tx - cx) > 0.0006 || Math.abs(ty - cy) > 0.0006) ? requestAnimationFrame(loop) : null;
    };
    const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      tx = (e.clientX - r.left) / r.width - 0.5;
      ty = (e.clientY - r.top) / r.height - 0.5;
      kick();
    });
    hero.addEventListener('pointerleave', () => { tx = 0; ty = 0; kick(); });
  });
})();
