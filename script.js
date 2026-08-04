// ============ Preferencia de movimiento reducido ============
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ============ Menú móvil ============
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
});

navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  });
});

// ============ Efecto de escritura en la terminal ============
function typeLine(el, text, speed = 28) {
  return new Promise(resolve => {
    if (prefersReducedMotion) {
      el.textContent = text;
      resolve();
      return;
    }
    let i = 0;
    (function step() {
      el.textContent = text.slice(0, i);
      i++;
      if (i <= text.length) {
        setTimeout(step, speed);
      } else {
        resolve();
      }
    })();
  });
}

async function runTerminal() {
  const outLines = document.querySelectorAll('#terminalBody .out');
  for (const el of outLines) {
    const text = el.getAttribute('data-type') || '';
    await typeLine(el, text);
    await new Promise(r => setTimeout(r, prefersReducedMotion ? 0 : 250));
  }
}
runTerminal();

// ============ Revelado al hacer scroll ============
const revealEls = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

revealEls.forEach(el => observer.observe(el));

// ============ Nav con fondo al hacer scroll ============
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.style.borderBottomColor = window.scrollY > 20 ? 'var(--border)' : 'transparent';
});

// ============ Formulario de contacto ============
// Nota: esto no envía datos a ningún servidor. Reemplaza esta lógica
// por una integración real (Formspree, EmailJS, tu propio backend, etc.)
const form = document.getElementById('contactForm');
const formResponse = document.getElementById('formResponse');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = form.name.value.trim();
  const email = form.email.value.trim();
  const message = form.message.value.trim();

  const subject = encodeURIComponent(`Contacto desde el portafolio — ${name}`);
  const body = encodeURIComponent(`${message}\n\n— ${name} (${email})`);
  window.location.href = `mailto:alex.rivera@example.com?subject=${subject}&body=${body}`;

  formResponse.textContent = '> Abriendo tu cliente de correo...';
  form.reset();
});
