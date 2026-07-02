// ===================== Nav toggle =====================
const navToggle = document.getElementById('navToggle');
const mainNav = document.getElementById('mainNav');

navToggle?.addEventListener('click', () => {
  mainNav.classList.toggle('open');
});

mainNav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => mainNav.classList.remove('open'));
});

// ===================== YouTube Shorts (click-to-load) =====================
document.querySelectorAll('.short-card').forEach((card) => {
  card.addEventListener('click', () => {
    const videoId = card.dataset.videoId;
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&playsinline=1`;
    iframe.title = 'YouTube Short';
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture';
    iframe.allowFullscreen = true;
    card.innerHTML = '';
    card.appendChild(iframe);
  }, { once: true });
});

// ===================== Cursor dot =====================
const cursorDot = document.getElementById('cursorDot');
if (cursorDot) {
  window.addEventListener('mousemove', (e) => {
    cursorDot.style.left = `${e.clientX}px`;
    cursorDot.style.top = `${e.clientY}px`;
  });
  document.querySelectorAll('a, button, .gallery-grid img').forEach((el) => {
    el.addEventListener('mouseenter', () => cursorDot.style.transform = 'translate(-50%, -50%) scale(1.8)');
    el.addEventListener('mouseleave', () => cursorDot.style.transform = 'translate(-50%, -50%) scale(1)');
  });
}

// ===================== Lightbox =====================
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightboxImg');
const lightboxClose = document.getElementById('lightboxClose');

document.querySelectorAll('.gallery-grid img').forEach((img) => {
  img.addEventListener('click', () => {
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightbox.classList.add('active');
  });
});

function closeLightbox() {
  lightbox.classList.remove('active');
  lightboxImg.src = '';
}

lightboxClose?.addEventListener('click', closeLightbox);
lightbox?.addEventListener('click', (e) => {
  if (e.target === lightbox) closeLightbox();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeLightbox();
});

// ===================== Scroll reveal =====================
const revealTargets = document.querySelectorAll(
  '.highlight-card, .about-photo, .about-copy, .gallery-grid img, .show-row, .press-list li'
);
revealTargets.forEach((el) => el.setAttribute('data-reveal', ''));

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);
revealTargets.forEach((el) => observer.observe(el));

// ===================== Header shrink on scroll =====================
const header = document.getElementById('siteHeader');
window.addEventListener('scroll', () => {
  header.style.boxShadow = window.scrollY > 20 ? '0 4px 20px rgba(0,0,0,0.35)' : 'none';
});

// ===================== Contact form (mailto handoff) =====================
const contactForm = document.getElementById('contactForm');
const formNote = document.getElementById('formNote');
const BUSINESS_EMAIL = 'joleenreacts@gmail.com';

contactForm?.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.getElementById('cf-name').value;
  const email = document.getElementById('cf-email').value;
  const message = document.getElementById('cf-message').value;

  const subject = `Booking / Inquiry from ${name}`;
  const body = `${message}\n\n— ${name} (${email})`;
  const mailtoLink = `mailto:${BUSINESS_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

  window.location.href = mailtoLink;
  formNote.textContent = 'Opening your email client, addressed to joleenreacts@gmail.com...';
  formNote.style.color = '#ffe600';
});

// ===================== Footer year =====================
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();
