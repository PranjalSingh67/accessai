@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  color-scheme: light;
  --bg: #f5f7fb;
  --surface: #ffffff;
  --surface-alt: #edf2f7;
  --border: #d4dce7;
  --text: #101828;
  --muted: #475467;
  --accent: #0f172a;
  --accent-hover: #1e293b;
  --success: #0f766e;
  --shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

a { color: inherit; text-decoration: none; }
img { max-width: 100%; }
button, input, textarea, select { font: inherit; }

.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
}

.skip-link:focus {
  left: 1rem;
  top: 1rem;
  z-index: 1000;
  background: #fff;
  border: 2px solid var(--text);
  padding: 0.75rem 1rem;
}

.container {
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
}

.site-header {
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  backdrop-filter: blur(10px);
  z-index: 10;
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 72px;
}

.brand-block {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
}

.brand-mark {
  width: 2rem;
  height: 2rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: white;
  border-radius: 0.5rem;
  font-size: 0.9rem;
}

.nav-list {
  display: flex;
  list-style: none;
  gap: 1.5rem;
  padding: 0;
  margin: 0;
  color: var(--muted);
}

.hero {
  padding: 5rem 0 4rem;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.3fr 0.9fr;
  gap: 2rem;
  align-items: center;
}

.eyebrow {
  margin: 0 0 1rem;
  color: var(--muted);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.74rem;
}

h1 {
  margin: 0;
  font-size: clamp(2.6rem, 4vw, 4.2rem);
  line-height: 1.08;
  letter-spacing: -0.06em;
}

.lede {
  margin-top: 1rem;
  max-width: 58ch;
  color: var(--muted);
  font-size: 1.1rem;
}

.hero-actions {
  margin-top: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

button {
  background: var(--accent);
  color: #fff;
  border: 0;
  border-radius: 0.6rem;
  padding: 0.9rem 1.4rem;
  font-weight: 600;
  cursor: pointer;
}

button:hover, button:focus-visible {
  background: var(--accent-hover);
}

.secondary-link {
  color: var(--text);
  font-weight: 600;
  border-bottom: 2px solid var(--border);
}

.panel, .feature-card, .step-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 1rem;
  box-shadow: var(--shadow);
}

.panel {
  padding: 2rem;
}

.check-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.8rem;
  color: var(--muted);
}

.check-list li::before {
  content: '✓';
  color: var(--success);
  font-weight: 700;
  margin-right: 0.75rem;
}

.section {
  padding: 4rem 0;
}

.muted-section {
  background: var(--surface-alt);
}

.section-heading {
  margin-bottom: 2rem;
}

.section-heading h2 {
  margin: 0;
  font-size: clamp(2rem, 3vw, 2.8rem);
  letter-spacing: -0.04em;
}

.feature-grid, .steps-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.2rem;
}

.feature-card, .step-card {
  padding: 1.5rem;
}

.feature-card h3, .step-card h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.feature-card p, .step-card p {
  margin: 0;
  color: var(--muted);
}

.step-card span {
  display: inline-flex;
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 999px;
  align-items: center;
  justify-content: center;
  background: var(--surface-alt);
  color: var(--text);
  font-weight: 700;
  margin-bottom: 1rem;
}

.site-footer {
  padding: 1.5rem 0 3rem;
  border-top: 1px solid var(--border);
}

.footer-inner {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  color: var(--muted);
}

@media (max-width: 900px) {
  .hero-grid, .feature-grid, .steps-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .nav-bar, .footer-inner {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav-list {
    flex-wrap: wrap;
    gap: 0.75rem 1rem;
  }

  .hero-grid, .feature-grid, .steps-grid {
    grid-template-columns: 1fr;
  }

  .hero {
    padding-top: 4rem;
  }
}
