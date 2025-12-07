// Gothic Literature Analysis - Main Application

let analysisData = {};
let currentText = null;

// Load analysis data
async function loadData() {
    try {
        const response = await fetch('data/analysis.json');
        analysisData = await response.json();
        console.log('Data loaded:', Object.keys(analysisData));
        initializeApp();
    } catch (error) {
        console.error('Error loading data:', error);
        showError('Failed to load analysis data');
    }
}

// Initialize application
function initializeApp() {
    populateTextList();
    populateTextSelectors();
    setupEventListeners();
}

// Populate text list in sidebar
function populateTextList() {
    const textList = document.getElementById('text-list');
    textList.innerHTML = '';

    Object.keys(analysisData).forEach(title => {
        const item = document.createElement('div');
        item.className = 'text-item';
        item.textContent = title;
        item.dataset.title = title;
        item.onclick = () => selectText(title);
        textList.appendChild(item);
    });
}

// Populate text selectors in compare view
function populateTextSelectors() {
    const select1 = document.getElementById('text1-select');
    const select2 = document.getElementById('text2-select');

    Object.keys(analysisData).forEach(title => {
        const option1 = document.createElement('option');
        option1.value = title;
        option1.textContent = title;
        select1.appendChild(option1);

        const option2 = document.createElement('option');
        option2.value = title;
        option2.textContent = title;
        select2.appendChild(option2);
    });
}

// Setup event listeners
function setupEventListeners() {
    // View mode navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => switchViewMode(btn.dataset.mode));
    });

    // Compare button
    document.getElementById('compare-btn').addEventListener('click', compareTexts);
}

// Switch view mode
function switchViewMode(mode) {
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    // Update views
    document.querySelectorAll('.view-mode').forEach(view => {
        view.classList.remove('active');
    });

    if (mode === 'single') {
        document.getElementById('single-view').classList.add('active');
    } else {
        document.getElementById('compare-view').classList.add('active');
    }
}

// Select text in single view
function selectText(title) {
    currentText = title;

    // Update active state
    document.querySelectorAll('.text-item').forEach(item => {
        item.classList.toggle('active', item.dataset.title === title);
    });

    // Display analysis
    displayAnalysis(title);
}

// Display analysis for a single text
function displayAnalysis(title) {
    const data = analysisData[title];
    const container = document.getElementById('single-analysis');

    container.innerHTML = `
        <h2>${title}</h2>

        <!-- Word Cloud -->
        <div class="analysis-section">
            <h3>Word Cloud</h3>
            <div id="wordcloud"></div>
        </div>

        <!-- Sentiment Analysis -->
        <div class="analysis-section">
            <h3>Sentiment Analysis</h3>
            <p><strong>Overall Sentiment:</strong> <span style="color: var(--accent-primary)">${capitalize(data.sentiment.overall)}</span></p>
            <div class="sentiment-display">
                ${createSentimentBar('Positive', data.sentiment.scores.positive)}
                ${createSentimentBar('Negative', data.sentiment.scores.negative)}
                ${createSentimentBar('Neutral', data.sentiment.scores.neutral)}
                ${createSentimentBar('Compound', data.sentiment.scores.compound, true)}
            </div>
        </div>

        <!-- Lexical Diversity -->
        <div class="analysis-section">
            <h3>Vocabulary & Lexical Diversity</h3>
            <div class="metrics-grid">
                ${createMetricCard('Total Words', data.lexical_diversity.total_words.toLocaleString())}
                ${createMetricCard('Unique Words', data.lexical_diversity.unique_words.toLocaleString())}
                ${createMetricCard('Type-Token Ratio', data.lexical_diversity.type_token_ratio)}
                ${createMetricCard('Content TTR', data.lexical_diversity.content_ttr)}
                ${createMetricCard('Root TTR', data.lexical_diversity.root_ttr)}
                ${createMetricCard('Lexical Density', data.lexical_diversity.lexical_density)}
            </div>
        </div>

        <!-- Topics -->
        <div class="analysis-section">
            <h3>Topic Modeling</h3>
            <div class="topics-container">
                ${data.topics.map(topic => createTopicCard(topic)).join('')}
            </div>
        </div>
    `;

    // Render word cloud
    renderWordCloud(data.word_frequencies);
}

// Create sentiment bar
function createSentimentBar(label, value, isCompound = false) {
    const percentage = isCompound ? ((value + 1) / 2 * 100) : (value * 100);
    const barClass = `bar-${label.toLowerCase()}`;

    return `
        <div class="sentiment-bar">
            <div class="sentiment-bar-label">
                <span>${label}</span>
                <span>${value.toFixed(4)}</span>
            </div>
            <div class="bar-container">
                <div class="bar-fill ${barClass}" style="width: ${percentage}%"></div>
            </div>
        </div>
    `;
}

// Create metric card
function createMetricCard(label, value) {
    return `
        <div class="metric-card">
            <div class="metric-label">${label}</div>
            <div class="metric-value">${value}</div>
        </div>
    `;
}

// Create topic card
function createTopicCard(topic) {
    const topWords = topic.words.slice(0, 8);
    return `
        <div class="topic-card">
            <div class="topic-title">Topic ${topic.topic_id + 1}</div>
            <div class="topic-words">
                ${topWords.map(w => `<span class="topic-word">${w.word}</span>`).join('')}
            </div>
        </div>
    `;
}

// Render word cloud using D3
function renderWordCloud(wordFrequencies) {
    const container = document.getElementById('wordcloud');
    container.innerHTML = '';

    // Convert to array and scale
    const words = Object.entries(wordFrequencies).map(([word, freq]) => ({
        text: word,
        size: freq
    }));

    // Find max frequency for scaling
    const maxFreq = Math.max(...words.map(w => w.size));
    const minSize = 12;
    const maxSize = 80;

    // Scale word sizes
    words.forEach(w => {
        w.size = minSize + (w.size / maxFreq) * (maxSize - minSize);
    });

    const width = container.offsetWidth;
    const height = 400;

    const layout = d3.layout.cloud()
        .size([width, height])
        .words(words)
        .padding(5)
        .rotate(() => (Math.random() > 0.5 ? 0 : 90))
        .font('Georgia')
        .fontSize(d => d.size)
        .on('end', draw);

    layout.start();

    function draw(words) {
        const svg = d3.select('#wordcloud')
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        const g = svg.append('g')
            .attr('transform', `translate(${width / 2},${height / 2})`);

        g.selectAll('text')
            .data(words)
            .enter()
            .append('text')
            .style('font-size', d => `${d.size}px`)
            .style('font-family', 'Georgia')
            .style('fill', () => {
                const colors = ['#e94560', '#533483', '#0f3460', '#4caf50', '#ff9800'];
                return colors[Math.floor(Math.random() * colors.length)];
            })
            .attr('text-anchor', 'middle')
            .attr('transform', d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
            .text(d => d.text)
            .style('opacity', 0)
            .transition()
            .duration(1000)
            .style('opacity', 1);
    }
}

// Compare two texts
function compareTexts() {
    const text1 = document.getElementById('text1-select').value;
    const text2 = document.getElementById('text2-select').value;

    if (!text1 || !text2) {
        alert('Please select both texts to compare');
        return;
    }

    if (text1 === text2) {
        alert('Please select two different texts');
        return;
    }

    displayComparison(text1, text2);
}

// Display comparison
function displayComparison(title1, title2) {
    const data1 = analysisData[title1];
    const data2 = analysisData[title2];
    const container = document.getElementById('comparison-results');

    container.innerHTML = `
        <h2>Comparative Analysis</h2>

        <div class="comparison-grid" style="margin-bottom: 30px;">
            <div class="comparison-item">
                <h3>${title1}</h3>
            </div>
            <div class="comparison-item">
                <h3>${title2}</h3>
            </div>
        </div>

        <!-- Sentiment Comparison -->
        <div class="analysis-section">
            <h3>Sentiment Comparison</h3>
            <div class="comparison-grid">
                <div class="comparison-item">
                    <p><strong>Overall:</strong> ${capitalize(data1.sentiment.overall)}</p>
                    <div class="sentiment-display" style="flex-direction: column;">
                        ${createSentimentBar('Positive', data1.sentiment.scores.positive)}
                        ${createSentimentBar('Negative', data1.sentiment.scores.negative)}
                        ${createSentimentBar('Neutral', data1.sentiment.scores.neutral)}
                        ${createSentimentBar('Compound', data1.sentiment.scores.compound, true)}
                    </div>
                </div>
                <div class="comparison-item">
                    <p><strong>Overall:</strong> ${capitalize(data2.sentiment.overall)}</p>
                    <div class="sentiment-display" style="flex-direction: column;">
                        ${createSentimentBar('Positive', data2.sentiment.scores.positive)}
                        ${createSentimentBar('Negative', data2.sentiment.scores.negative)}
                        ${createSentimentBar('Neutral', data2.sentiment.scores.neutral)}
                        ${createSentimentBar('Compound', data2.sentiment.scores.compound, true)}
                    </div>
                </div>
            </div>
        </div>

        <!-- Lexical Diversity Comparison -->
        <div class="analysis-section">
            <h3>Vocabulary & Lexical Diversity Comparison</h3>
            <div class="comparison-grid">
                <div class="comparison-item">
                    <div class="metrics-grid">
                        ${createMetricCard('Total Words', data1.lexical_diversity.total_words.toLocaleString())}
                        ${createMetricCard('Unique Words', data1.lexical_diversity.unique_words.toLocaleString())}
                        ${createMetricCard('TTR', data1.lexical_diversity.type_token_ratio)}
                        ${createMetricCard('Content TTR', data1.lexical_diversity.content_ttr)}
                        ${createMetricCard('Root TTR', data1.lexical_diversity.root_ttr)}
                        ${createMetricCard('Lexical Density', data1.lexical_diversity.lexical_density)}
                    </div>
                </div>
                <div class="comparison-item">
                    <div class="metrics-grid">
                        ${createMetricCard('Total Words', data2.lexical_diversity.total_words.toLocaleString())}
                        ${createMetricCard('Unique Words', data2.lexical_diversity.unique_words.toLocaleString())}
                        ${createMetricCard('TTR', data2.lexical_diversity.type_token_ratio)}
                        ${createMetricCard('Content TTR', data2.lexical_diversity.content_ttr)}
                        ${createMetricCard('Root TTR', data2.lexical_diversity.root_ttr)}
                        ${createMetricCard('Lexical Density', data2.lexical_diversity.lexical_density)}
                    </div>
                </div>
            </div>
        </div>

        <!-- Topics Comparison -->
        <div class="analysis-section">
            <h3>Topic Comparison</h3>
            <div class="comparison-grid">
                <div class="comparison-item">
                    <div class="topics-container">
                        ${data1.topics.map(topic => createTopicCard(topic)).join('')}
                    </div>
                </div>
                <div class="comparison-item">
                    <div class="topics-container">
                        ${data2.topics.map(topic => createTopicCard(topic)).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Utility functions
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function showError(message) {
    const container = document.getElementById('single-analysis');
    container.innerHTML = `
        <div class="welcome-message">
            <h2>Error</h2>
            <p>${message}</p>
        </div>
    `;
}

// Initialize app on page load
window.addEventListener('DOMContentLoaded', loadData);
