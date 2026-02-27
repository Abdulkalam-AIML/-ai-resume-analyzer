document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('resume-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const analyzeBtn = document.getElementById('analyze-btn');
    const jdText = document.getElementById('jd-text');
    const loader = document.getElementById('loader');
    const resultsPlaceholder = document.getElementById('results-placeholder');
    const dashboardContent = document.getElementById('dashboard-content');
    const downloadBtn = document.getElementById('download-btn');

    let analysisData = null;

    // File Input Change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        fileNameDisplay.textContent = file ? file.name : 'No file chosen';
    });

    // Analyze Button Click
    analyzeBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert('Please select a resume file first!');
            return;
        }

        const formData = new FormData();
        formData.append('resume', file);
        formData.append('jd', jdText.value);

        // UI State: Loading
        loader.classList.remove('hidden');
        resultsPlaceholder.classList.add('hidden');
        dashboardContent.classList.add('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to analyze resume');
            }

            analysisData = data;
            renderResults(data);

            // Success Animation
            if (data.ats_score >= 80) {
                confetti({
                    particleCount: 150,
                    spread: 70,
                    origin: { y: 0.6 },
                    colors: ['#3b82f6', '#1e3a8a', '#8b5cf6']
                });
            }

        } catch (error) {
            alert('Error: ' + error.message);
            resultsPlaceholder.classList.remove('hidden');
        } finally {
            loader.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    // Render Results to UI
    function renderResults(data) {
        dashboardContent.classList.remove('hidden');
        
        // Metrics
        document.getElementById('ats-score').textContent = `${data.ats_score}/100`;
        document.getElementById('ats-progress').style.width = `${data.ats_score}%`;
        
        document.getElementById('match-percent').textContent = `${data.match_percent}%`;
        document.getElementById('match-progress').style.width = `${data.match_percent}%`;

        // Tabs Content
        renderTabContent('detected-skills', data.detected_skills, 'No major skills detected.');
        renderTabContent('missing-keywords', data.missing_keywords, 'Great! No major skills missing.', 'success');
        renderTabContent('recommendations', data.recommendations, 'No specific recommendations.', 'tip');
    }

    function renderTabContent(containerId, items, emptyMsg, type = 'info') {
        const container = document.getElementById(containerId);
        if (!items || items.length === 0) {
            container.innerHTML = `<p class="info-msg">${emptyMsg}</p>`;
            return;
        }

        if (containerId === 'recommendations') {
            container.innerHTML = `<ul>${items.map(item => `<li>${item}</li>`).join('')}</ul>`;
        } else {
            container.innerHTML = `<div class="pill-container">${items.map(item => `<span class="pill ${type}">${item}</span>`).join('')}</div>`;
        }
    }

    // Tab Switching
    document.querySelector('.tab-header').addEventListener('click', (e) => {
        if (e.target.classList.contains('tab-btn')) {
            const tabId = e.target.getAttribute('data-tab');
            
            // Remove active classes
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
            
            // Add active classes
            e.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }
    });

    // Download PDF
    downloadBtn.addEventListener('click', async () => {
        if (!analysisData) return;

        try {
            const response = await fetch('/generate-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(analysisData)
            });

            if (!response.ok) throw new Error('Failed to generate PDF');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Resume_Analysis_${analysisData.ats_score}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (error) {
            alert('PDF Generation Error: ' + error.message);
        }
    });
});
