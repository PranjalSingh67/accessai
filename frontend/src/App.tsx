const features = [
  {
    title: 'Understand Images',
    description: 'Image descriptions, key text extraction, and screen-reader-ready summaries.'
  },
  {
    title: 'Understand Audio',
    description: 'Transcripts, summaries, and priority actions from spoken content.'
  },
  {
    title: 'Simplify Text',
    description: 'Plain-language explanations, definitions, and high-level action points.'
  },
  {
    title: 'Digital Services',
    description: 'Break down forms, notices, and instructions into simple required steps.'
  }
];

export default function App() {
  return (
    <>
      <a className="skip-link" href="#main-content">Skip to content</a>

      <header className="site-header">
        <div className="container nav-bar">
          <div className="brand-block" aria-label="AccessAI home">
            <span className="brand-mark">A</span>
            <span>AccessAI</span>
          </div>
          <nav aria-label="Main navigation">
            <ul className="nav-list">
              <li><a href="#features">Features</a></li>
              <li><a href="#workflow">Workflow</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </nav>
        </div>
      </header>

      <main id="main-content">
        <section className="hero">
          <div className="container hero-grid">
            <div>
              <p className="eyebrow">Accessibility-first AI</p>
              <h1>Make digital information accessible to everyone.</h1>
              <p className="lede">
                AccessAI transforms complex digital content into clear, structured information for people with visual, hearing, and cognitive accessibility needs.
              </p>
              <div className="hero-actions">
                <button type="button">Try AccessAI</button>
                <a href="#features" className="secondary-link">Explore features</a>
              </div>
            </div>

            <div className="panel">
              <h2>What AccessAI does</h2>
              <ul className="check-list">
                <li>Reads important text from images and forms</li>
                <li>Summarizes audio and spoken information</li>
                <li>Explains complex text in simpler language</li>
                <li>Steps through required actions and deadlines clearly</li>
              </ul>
            </div>
          </div>
        </section>

        <section id="features" className="section">
          <div className="container">
            <div className="section-heading">
              <p className="eyebrow">Core features</p>
              <h2>Designed for everyday accessibility tasks</h2>
            </div>

            <div className="feature-grid">
              {features.map((feature) => (
                <article key={feature.title} className="feature-card">
                  <h3>{feature.title}</h3>
                  <p>{feature.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="workflow" className="section muted-section">
          <div className="container">
            <div className="section-heading">
              <p className="eyebrow">Workflow</p>
              <h2>From content to clear action</h2>
            </div>

            <div className="steps-grid">
              <div className="step-card">
                <span>01</span>
                <h3>Input</h3>
                <p>Upload an image, audio, or paste text from a public service or digital form.</p>
              </div>
              <div className="step-card">
                <span>02</span>
                <h3>Analyze</h3>
                <p>AI identifies what matters, extracts important information, and structures the result.</p>
              </div>
              <div className="step-card">
                <span>03</span>
                <h3>Accessible output</h3>
                <p>Key actions, warnings, deadlines, and clear summaries are delivered in a simple format.</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer id="contact" className="site-footer">
        <div className="container footer-inner">
          <p>AccessAI</p>
          <p>Built for practical accessibility and clearer digital experiences.</p>
        </div>
      </footer>
    </>
  );
}
