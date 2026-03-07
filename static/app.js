const form = document.getElementById('analyse-form');
const websiteInput = document.getElementById('website');
const categoryInput = document.getElementById('category');
const categoryLabel = document.getElementById('category-label');
const submitBtn = document.getElementById('submit-btn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoading = submitBtn.querySelector('.btn-loading');
const errorEl = document.getElementById('error');
const resultsEl = document.getElementById('results');
const scoreValue = document.getElementById('score-value');
const mentionsCount = document.getElementById('mentions-count');
const promptsCount = document.getElementById('prompts-count');
const promptResultsEl = document.getElementById('prompt-results');
const suggestionsListEl = document.getElementById('suggestions-list');

// Update "What does X do?" label when website changes
if (websiteInput && categoryLabel) {
  websiteInput.addEventListener('input', () => {
    const site = websiteInput.value.trim();
    const domain = site ? extractDomain(site) : 'your website';
    categoryLabel.textContent = `What does ${domain} do?`;
  });
}

function extractDomain(url) {
  let s = url.toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0];
  return s || 'your website';
}

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.hidden = false;
  resultsEl.hidden = true;
}

function hideError() {
  errorEl.hidden = true;
}

function setLoading(loading) {
  submitBtn.disabled = loading;
  btnText.hidden = loading;
  btnLoading.hidden = !loading;
}

function renderResults(data) {
  scoreValue.textContent = Math.round(data.visibility_score);
  mentionsCount.textContent = data.mentions_found;
  promptsCount.textContent = data.prompts_tested;

  promptResultsEl.innerHTML = data.prompt_results
    .map((r) => `
      <div class="prompt-item ${r.mentioned ? 'mentioned' : ''}">
        <span class="status">${r.mentioned ? '✓' : '—'}</span>
        <span>${escapeHtml(r.prompt)}</span>
      </div>
    `)
    .join('');

  suggestionsListEl.innerHTML = data.suggestions
    .map(
      (s) => `
      <li>
        <span class="type">${formatType(s.type)}</span>
        <span>${escapeHtml(s.suggestion)}</span>
      </li>
    `
    )
    .join('');

  resultsEl.hidden = false;
}

function formatType(type) {
  const map = {
    keyword_swap: 'Keyword swap',
    add_keyword: 'Add keyword',
    keep_keyword: 'Keep keyword',
    general_tip: 'Tip',
  };
  return map[type] || type;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Scroll-triggered animation for example output
const exampleEl = document.getElementById('example-output');
if (exampleEl && 'IntersectionObserver' in window) {
  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) e.target.classList.add('visible');
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
  );
  obs.observe(exampleEl);
}

if (form) form.addEventListener('submit', async (e) => {
  e.preventDefault();
  hideError();

  const website = websiteInput.value.trim();
  const category = categoryInput.value.trim();

  if (!website) {
    showError('Please enter your website.');
    return;
  }
  if (!category) {
    showError('Please describe what your website does (e.g. pdf editor, productivity app).');
    return;
  }

  setLoading(true);
  resultsEl.hidden = true;

  try {
    const base = window.location.origin;
    const res = await fetch(`${base}/analyse`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ website, category }),
    });

    const data = await res.json();

    if (!res.ok) {
      showError(data.detail || 'Something went wrong. Please try again.');
      return;
    }

    renderResults(data);
    resultsEl.scrollIntoView({ behavior: 'smooth' });
  } catch (err) {
    showError('Could not reach the server. Please try again.');
  } finally {
    setLoading(false);
  }
});
