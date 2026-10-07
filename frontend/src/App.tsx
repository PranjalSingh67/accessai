import { useEffect, useMemo, useState } from 'react';

type TabKey = 'text' | 'service' | 'image';

type ResultState = {
  summary?: string;
  simplified_explanation?: string;
  explanation?: string;
  important_information?: string[];
  required_documents?: string[];
  deadlines?: string[];
  actions?: string[];
  warnings?: string[];
  extracted_text?: string[];
  key_points?: string[];
  accessible_version?: string;
  description?: string;
  key_information?: string[];
};

const defaultText = `The eligibility requirements for the scholarship are governed by the revised policy guidelines issued by the financial aid office. Applicants must submit the completed form, a valid identity document, and proof of income by the deadline to remain eligible for consideration. Late submissions may be rejected without review.`;

const defaultService = `Application for monthly transport allowance
The last date to submit the application is 30 June 2026.
Applicants must provide Aadhaar card, income certificate, and a recent passport size photograph. Incomplete forms will be rejected. Please bring the original documents to the district office before 5:00 PM.`;

const imagePromptTemplate = 'Describe this uploaded screenshot for accessibility. Highlight important text, labels, buttons, warnings, and required actions. If there are forms, list the key fields or document steps.';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabKey>('text');
  const [textInput, setTextInput] = useState(defaultText);
  const [serviceInput, setServiceInput] = useState(defaultService);
  const [imagePrompt, setImagePrompt] = useState(imagePromptTemplate);
  const [imageName, setImageName] = useState('');
  const [fontScale, setFontScale] = useState(1);
  const [highContrast, setHighContrast] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ResultState | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    document.documentElement.style.setProperty('--font-scale', fontScale.toString());
    document.documentElement.dataset.contrast = highContrast ? 'high' : 'default';
  }, [fontScale, highContrast]);

  const activeLabel = useMemo(() => {
    switch (activeTab) {
      case 'text':
        return 'Text Simplification';
      case 'service':
        return 'Digital Service Analyzer';
      case 'image':
        return 'Image Accessibility';
      default:
        return 'Tools';
    }
  }, [activeTab]);

  const readAloud = (content: string) => {
    if (!('speechSynthesis' in window)) {
      setError('Text-to-speech is not supported in this browser.');
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(content);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  };

  const handleTextSubmit = async () => {
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/text/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textInput, mode: 'simple' }),
      });

      if (!response.ok) {
        throw new Error('Unable to simplify this text right now.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong while simplifying the text.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleServiceSubmit = async () => {
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/digital-service/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: serviceInput }),
      });

      if (!response.ok) {
        throw new Error('Unable to analyze this service content right now.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong while analyzing the service content.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageSubmit = async () => {
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const promptText = `${imagePrompt || imagePromptTemplate} ${imageName ? `Image name: ${imageName}.` : ''}`;
      const response = await fetch('http://localhost:8000/api/v1/image/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: promptText }),
      });

      if (!response.ok) {
        throw new Error('Unable to describe this image right now.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong while describing the image.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    setImageName(file.name);
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = String(reader.result ?? '');
      setImagePrompt(`${imagePromptTemplate} Uploaded file: ${file.name}. Base64 preview is available: ${dataUrl.slice(0, 200)}.`);
    };
    reader.readAsDataURL(file);
  };

  const renderResult = () => {
    if (!result) {
      return null;
    }

    const summary = result.summary ?? result.simplified_explanation ?? result.explanation ?? 'Analysis complete.';
    const keyPoints = result.key_points?.length ? result.key_points : result.important_information ?? [];
    const actions = result.actions?.length ? result.actions : result.required_actions ?? [];
    const warnings = result.warnings?.length ? result.warnings : [];
    const docs = result.required_documents ?? [];
    const deadlines = result.deadlines ?? [];
    const description = result.description ?? result.accessible_version ?? 'The image was described.';
    const extractedText = result.extracted_text ?? [];
    const imageInfo = result.key_information ?? [];

    return (
      <section className="result-panel" aria-live="polite">
        <div className="result-header">
          <h3>Result</h3>
          <button type="button" className="secondary-button" onClick={() => readAloud(String(summary))}>
            Read aloud
          </button>
        </div>

        <div className="result-block">
          <h4>Summary</h4>
          <p>{summary}</p>
        </div>

        {result.simplified_explanation || result.explanation ? (
          <div className="result-block">
            <h4>Plain-language explanation</h4>
            <p>{result.simplified_explanation ?? result.explanation}</p>
          </div>
        ) : null}

        {description && description !== 'The image was described.' ? (
          <div className="result-block">
            <h4>Image description</h4>
            <p>{description}</p>
          </div>
        ) : null}

        {keyPoints.length ? (
          <div className="result-block">
            <h4>Key points</h4>
            <ul>
              {keyPoints.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {actions.length ? (
          <div className="result-block">
            <h4>Action items</h4>
            <ul>
              {actions.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {docs.length ? (
          <div className="result-block">
            <h4>Required documents</h4>
            <ul>
              {docs.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {deadlines.length ? (
          <div className="result-block">
            <h4>Deadlines</h4>
            <ul>
              {deadlines.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {warnings.length ? (
          <div className="result-block">
            <h4>Warnings</h4>
            <ul>
              {warnings.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {extractedText.length ? (
          <div className="result-block">
            <h4>Extracted text</h4>
            <ul>
              {extractedText.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {imageInfo.length ? (
          <div className="result-block">
            <h4>Important information</h4>
            <ul>
              {imageInfo.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}
      </section>
    );
  };

  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <header className="topbar">
        <div className="container topbar-inner">
          <div className="brand" aria-label="AccessAI home">
            <span className="brand-badge">A</span>
            <span>AccessAI</span>
          </div>

          <nav aria-label="Main navigation">
            <ul className="nav-list">
              <li>
                <button type="button" className="nav-button" onClick={() => setActiveTab('text')}>
                  Text
                </button>
              </li>
              <li>
                <button type="button" className="nav-button" onClick={() => setActiveTab('service')}>
                  Services
                </button>
              </li>
              <li>
                <button type="button" className="nav-button" onClick={() => setActiveTab('image')}>
                  Images
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <main id="main-content" className="container app-shell">
        <section className="hero panel" aria-labelledby="hero-title">
          <div>
            <p className="eyebrow">Accessibility-first AI assistant</p>
            <h1 id="hero-title">Clearer information for everyday decisions.</h1>
            <p className="lead">
              AccessAI simplifies complicated language, explains official service notices, and describes images and screenshots in plain language.
            </p>
          </div>

          <div className="toolbar" aria-label="Accessibility controls">
            <label>
              Font size
              <input
                type="range"
                min="0.9"
                max="1.3"
                step="0.05"
                value={fontScale}
                onChange={(event) => setFontScale(Number(event.target.value))}
              />
            </label>

            <label className="toggle-row">
              <input
                type="checkbox"
                checked={highContrast}
                onChange={() => setHighContrast((value) => !value)}
              />
              High contrast
            </label>
          </div>
        </section>

        <section className="tool-panel panel" aria-labelledby="tool-title">
          <div className="section-heading">
            <p className="eyebrow">MVP tools</p>
            <h2 id="tool-title">{activeLabel}</h2>
          </div>

          <div className="tab-row" role="tablist" aria-label="AccessAI tools">
            {(['text', 'service', 'image'] as TabKey[]).map((tab) => (
              <button
                key={tab}
                type="button"
                role="tab"
                aria-selected={activeTab === tab}
                className={activeTab === tab ? 'tab-button active' : 'tab-button'}
                onClick={() => setActiveTab(tab)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    setActiveTab(tab);
                  }
                }}
              >
                {tab === 'text' ? 'Text Simplification' : tab === 'service' ? 'Service Analyzer' : 'Image Accessibility'}
              </button>
            ))}
          </div>

          {activeTab === 'text' && (
            <div className="workspace">
              <label htmlFor="text-input">Paste complex text</label>
              <textarea
                id="text-input"
                value={textInput}
                onChange={(event) => setTextInput(event.target.value)}
                rows={10}
                placeholder="Paste a difficult notice, policy, or form text here"
              />
              <div className="action-row">
                <button type="button" className="primary-button" onClick={handleTextSubmit} disabled={isLoading}>
                  {isLoading ? 'Processing...' : 'Simplify text'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'service' && (
            <div className="workspace">
              <label htmlFor="service-input">Paste service or legal text</label>
              <textarea
                id="service-input"
                value={serviceInput}
                onChange={(event) => setServiceInput(event.target.value)}
                rows={10}
                placeholder="Paste a government, college, bank, or job service notice here"
              />
              <div className="action-row">
                <button type="button" className="primary-button" onClick={handleServiceSubmit} disabled={isLoading}>
                  {isLoading ? 'Analyzing...' : 'Analyze service'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'image' && (
            <div className="workspace">
              <label htmlFor="image-upload">Upload screenshot or image</label>
              <input id="image-upload" type="file" accept="image/*" onChange={handleImageUpload} />

              <label htmlFor="image-prompt">Additional guidance</label>
              <textarea
                id="image-prompt"
                value={imagePrompt}
                onChange={(event) => setImagePrompt(event.target.value)}
                rows={6}
              />

              <div className="action-row">
                <button type="button" className="primary-button" onClick={handleImageSubmit} disabled={isLoading}>
                  {isLoading ? 'Describing...' : 'Describe image'}
                </button>
              </div>
            </div>
          )}

          {error && <div className="alert error" role="alert">{error}</div>}
          {renderResult()}
        </section>
      </main>
    </>
  );
}
