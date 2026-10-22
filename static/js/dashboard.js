/* ============================================================
   HalluciGuard AI — Dashboard JS
   Theme toggle, sidebar, spinners, counter animations
   ============================================================ */

// ---------- Theme ----------
function getTheme() { return localStorage.getItem('hg_theme') || 'dark'; }

function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('hg_theme', t);
  const icon = document.getElementById('themeIcon');
  if (icon) icon.className = t === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
}

function toggleTheme() {
  applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
}

// ---------- Sidebar ----------
let sidebarCollapsed = localStorage.getItem('hg_sidebar') === '1';

function applySidebar() {
  const sidebar = document.getElementById('sidebar');
  const main    = document.getElementById('mainContent');
  if (!sidebar) return;
  if (sidebarCollapsed) {
    sidebar.classList.add('collapsed');
    if (main) main.classList.add('expanded');
  } else {
    sidebar.classList.remove('collapsed');
    if (main) main.classList.remove('expanded');
  }
}

function toggleSidebar() {
  sidebarCollapsed = !sidebarCollapsed;
  localStorage.setItem('hg_sidebar', sidebarCollapsed ? '1' : '0');
  applySidebar();
}

// ---------- Spinner ----------
function showSpinner(msg) {
  const overlay = document.getElementById('spinnerOverlay');
  const text    = document.getElementById('spinnerText');
  if (overlay) {
    if (text && msg) text.textContent = msg;
    overlay.classList.add('show');
  }
}
function hideSpinner() {
  const overlay = document.getElementById('spinnerOverlay');
  if (overlay) overlay.classList.remove('show');
}

// ---------- Counter Animation ----------
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const raw    = el.getAttribute('data-count');
    const target = parseFloat(raw);
    if (isNaN(target)) return;
    const isFloat   = raw.includes('.');
    const duration  = 1400;
    const startTime = performance.now();

    function update(now) {
      const progress = Math.min((now - startTime) / duration, 1);
      const ease     = 1 - Math.pow(1 - progress, 3);
      const current  = target * ease;
      el.textContent = isFloat ? current.toFixed(1) : Math.floor(current).toLocaleString();
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  });
}

// ---------- Copy Text ----------
function copyText(text) {
  navigator.clipboard.writeText(text).then(() => showToast('Copied!', 'success'));
}

// ---------- Toast ----------
function showToast(msg, type = 'info') {
  const colors = {
    success: '#10b981', danger: '#ef4444', warning: '#f59e0b', info: '#3b82f6'
  };
  const div = document.createElement('div');
  div.style.cssText = `
    position:fixed;bottom:24px;right:24px;z-index:99999;
    background:var(--bg-secondary);border:1px solid var(--border);
    border-left:3px solid ${colors[type] || colors.info};
    color:var(--text-1);padding:12px 18px;border-radius:10px;
    font-size:13px;font-weight:500;
    box-shadow:0 8px 24px rgba(0,0,0,0.3);
    animation:slideInToast 0.3s ease;
  `;
  div.textContent = msg;
  document.body.appendChild(div);
  setTimeout(() => div.remove(), 3000);
}

// Inject toast animation
const styleTag = document.createElement('style');
styleTag.textContent = `@keyframes slideInToast{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}`;
document.head.appendChild(styleTag);

// ---------- Init ----------
document.addEventListener('DOMContentLoaded', () => {
  applyTheme(getTheme());
  applySidebar();
  animateCounters();

  // Auto-dismiss alerts after 5 seconds
  document.querySelectorAll('.alert').forEach(a => {
    setTimeout(() => { if (a.parentNode) a.classList.remove('show'); }, 5000);
  });
});
