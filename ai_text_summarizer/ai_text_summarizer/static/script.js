const summarizeBtn = document.getElementById('summarizeBtn');
const inputEl = document.getElementById('inputText');
const loader = document.getElementById('loader');
const resultEl = document.getElementById('summaryContent');
const toast = document.getElementById('toast');
const themeToggle = document.getElementById('theme-toggle');

function showToast(msg, timeout = 4000) {
	toast.textContent = msg;
	toast.classList.remove('hidden');
	setTimeout(() => toast.classList.add('hidden'), timeout);
}

function setLoading(on) {
	if (on) {
		loader.classList.remove('hidden');
		summarizeBtn.disabled = true;
	} else {
		loader.classList.add('hidden');
		summarizeBtn.disabled = false;
	}
}

async function summarize() {
	const text = inputEl.value.trim();
	if (!text) {
		showToast('Please enter text to summarize');
		return;
	}

	setLoading(true);

	try {
		const resp = await fetch('/api/summarize', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ text })
		});

		const data = await resp.json();

		if (!resp.ok) {
			if (data && data.error === 'missing_model') {
				showToast(data.message);
			} else {
				showToast('Server error: ' + (data.detail || 'Unknown'));
			}
			resultEl.textContent = '';
			return;
		}

		resultEl.textContent = data.summary || 'No summary returned.';
	} catch (err) {
		console.error(err);
		showToast('Network error. Is the backend running?');
	} finally {
		setLoading(false);
	}
}

summarizeBtn.addEventListener('click', summarize);

themeToggle.addEventListener('click', () => {
	document.body.classList.toggle('dark');
});
