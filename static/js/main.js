/**
 * CyberLex India — Main JavaScript
 * Handles: Theme, Language, Search, Particles, Toast, Loading
 */

// ── State ──────────────────────────────────────────────────────
let currentLang = localStorage.getItem('lang') || 'en';
let isDarkTheme = localStorage.getItem('theme') !== 'light';

// ── Init ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initParticles();
    initNavbar();
    initLanguage();
    initSearch();
    initMobileMenu();
    animateOnScroll();
});

// ── Theme ──────────────────────────────────────────────────────
function initTheme() {
    const theme = localStorage.getItem('theme') || 'dark';
    isDarkTheme = theme === 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeIcon();
}

function toggleTheme() {
    isDarkTheme = !isDarkTheme;
    const theme = isDarkTheme ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeIcon();
}

function updateThemeIcon() {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = isDarkTheme ? 'fas fa-moon' : 'fas fa-sun';
    }
}

document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);

// ── Particles ──────────────────────────────────────────────────
function initParticles() {
    const container = document.getElementById('particles');
    if (!container) return;

    for (let i = 0; i < 25; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            left: ${Math.random() * 100}%;
            width: ${Math.random() * 3 + 1}px;
            height: ${Math.random() * 3 + 1}px;
            animation-delay: ${Math.random() * 15}s;
            animation-duration: ${Math.random() * 20 + 15}s;
            opacity: ${Math.random() * 0.5 + 0.1};
        `;
        container.appendChild(particle);
    }
}

// ── Navbar ─────────────────────────────────────────────────────
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ── Mobile Menu ────────────────────────────────────────────────
function initMobileMenu() {
    const btn = document.getElementById('mobileMenuBtn');
    const links = document.getElementById('navLinks');

    btn?.addEventListener('click', () => {
        links?.classList.toggle('open');
        // Animate hamburger
        const spans = btn.querySelectorAll('span');
        if (links?.classList.contains('open')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
        } else {
            spans[0].style.transform = '';
            spans[1].style.opacity = '';
            spans[2].style.transform = '';
        }
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!btn?.contains(e.target) && !links?.contains(e.target)) {
            links?.classList.remove('open');
        }
    });
}

// ── Language ───────────────────────────────────────────────────
function initLanguage() {
    // Set current language display
    updateLangDisplay(currentLang);

    // Language dropdown toggle
    const langBtn = document.getElementById('langBtn');
    const langDropdown = document.getElementById('langDropdown');

    langBtn?.addEventListener('click', (e) => {
        e.stopPropagation();
        langDropdown?.classList.toggle('open');
    });

    document.addEventListener('click', () => {
        langDropdown?.classList.remove('open');
    });

    // Language option selection
    document.querySelectorAll('.lang-option').forEach(option => {
        option.addEventListener('click', async () => {
            const lang = option.dataset.lang;
            currentLang = lang;
            localStorage.setItem('lang', lang);
            updateLangDisplay(lang);

            // Update active state
            document.querySelectorAll('.lang-option').forEach(o => o.classList.remove('active'));
            option.classList.add('active');
            langDropdown?.classList.remove('open');

            // Translate UI elements
            await translateUI(lang);
        });
    });

    // Apply saved language on load
    if (currentLang !== 'en') {
        translateUI(currentLang);
        document.querySelectorAll('.lang-option').forEach(o => {
            o.classList.toggle('active', o.dataset.lang === currentLang);
        });
    }
}

function updateLangDisplay(lang) {
    const display = document.getElementById('currentLang');
    if (display) {
        display.textContent = lang.toUpperCase();
    }
}

async function translateUI(lang) {
    if (lang === 'en') {
        // Restore default English translations
        const defaults = {
            home: 'Home', laws: 'Laws', feedback: 'Feedback',
            listen: 'Listen', section: 'Section', punishment: 'Punishment & Penalty',
            example: 'Real-life Example', explanation: 'Explanation',
            back_to_laws: 'Back to All Laws',
            submit: 'Submit', your_name: 'Your Name', your_message: 'Your Message'
        };
        applyTranslations(defaults);
        return;
    }

    try {
        const res = await fetch(`/api/translations/${lang}`);
        const translations = await res.json();
        applyTranslations(translations);
    } catch (e) {
        console.error('Failed to load translations:', e);
    }
}

function applyTranslations(translations) {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (translations[key]) {
            el.textContent = translations[key];
        }
    });

    // Update placeholder
    const searchInput = document.getElementById('searchInput');
    if (searchInput && translations.search_placeholder) {
        searchInput.placeholder = translations.search_placeholder;
    }
}

// ── Search ─────────────────────────────────────────────────────
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchClear = document.getElementById('searchClear');

    if (!searchInput) return;

    let debounceTimer;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();

        // Show/hide clear button
        searchClear?.classList.toggle('visible', query.length > 0);

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            searchResults?.classList.remove('open');
            return;
        }

        debounceTimer = setTimeout(() => performSearch(query), 300);
    });

    searchClear?.addEventListener('click', () => {
        searchInput.value = '';
        searchClear.classList.remove('visible');
        searchResults?.classList.remove('open');
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchResults?.contains(e.target)) {
            searchResults?.classList.remove('open');
        }
    });
}

async function performSearch(query) {
    const searchResults = document.getElementById('searchResults');
    if (!searchResults) return;

    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const results = await res.json();

        if (results.length === 0) {
            searchResults.innerHTML = '<div style="padding:16px;text-align:center;color:var(--text-muted);font-size:14px;">No results found</div>';
        } else {
            searchResults.innerHTML = results.map(r => `
                <a href="/law/${r.slug}" class="search-result-item">
                    <span class="result-section">${r.section}</span>
                    <span class="result-title">${r.title}</span>
                    <span class="result-cat">${r.category}</span>
                </a>
            `).join('');
        }

        searchResults.classList.add('open');
    } catch (e) {
        console.error('Search failed:', e);
    }
}

// ── Toast Notifications ────────────────────────────────────────
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMessage');
    if (!toast || !toastMsg) return;

    const icons = { success: 'fa-check-circle', error: 'fa-exclamation-circle', info: 'fa-info-circle' };
    const icon = toast.querySelector('i');
    if (icon) icon.className = `fas ${icons[type] || icons.success}`;

    toastMsg.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');

    setTimeout(() => toast.classList.remove('show'), 4000);
}

// ── Loading ────────────────────────────────────────────────────
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay?.classList.add('show');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay?.classList.remove('show');
}

// ── Scroll Animations ──────────────────────────────────────────
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = `${i * 0.05}s`;
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.law-card, .feature-card, .content-card').forEach(el => {
        observer.observe(el);
    });
}

// Make functions available globally
window.showToast = showToast;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
