// ========================================================
// 🌌 CORE APPLICATION LOGIC FOR WEB COMPANION (docs/app.js)
// ========================================================

// 1. Core State & Local Storage Variables
let userXP = parseInt(localStorage.getItem('study_quest_xp') || '0');
let userLevel = 1 + Math.floor(userXP / 500);
let bestQuizScore = localStorage.getItem('study_quest_best_score') || 'N/A';

const QUESTIONS = [
  {
    category: "SQL",
    question: "Which of the following window functions assigns rankings with gaps in numbering if there are ties?",
    options: {
      A: "ROW_NUMBER()",
      B: "RANK()",
      C: "DENSE_RANK()",
      D: "LEAD()"
    },
    answer: "B",
    explanation: "RANK() leaves gaps in the ranking sequence when there are ties (e.g., 1, 2, 2, 4). DENSE_RANK() does not leave gaps (e.g., 1, 2, 2, 3), and ROW_NUMBER() always assigns a unique sequential integer regardless of ties."
  },
  {
    category: "SQL",
    question: "In the logical execution order of a standard SQL query, which clause is executed immediately AFTER the WHERE clause?",
    options: {
      A: "SELECT",
      B: "HAVING",
      C: "GROUP BY",
      D: "ORDER BY"
    },
    answer: "C",
    explanation: "The logical query processing order is: FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT. Therefore, GROUP BY is executed immediately after WHERE."
  },
  {
    category: "SQL",
    question: "Which index type is most suitable for indexing multi-value fields such as JSONB or Array columns in PostgreSQL?",
    options: {
      A: "B-Tree Index",
      B: "Hash Index",
      C: "GIN (Generalized Inverted Index)",
      D: "BRIN (Block Range Index)"
    },
    answer: "C",
    explanation: "GIN (Generalized Inverted Index) is designed for handling composite items where we want to index elements inside document/array structures. B-Tree is general-purpose, Hash is only for equality, and BRIN is for physically ordered data."
  },
  {
    category: "Python",
    question: "What is the average time complexity of searching for an element in a set in Python?",
    options: {
      A: "O(1)",
      B: "O(log N)",
      C: "O(N)",
      D: "O(N log N)"
    },
    answer: "A",
    explanation: "Python sets are implemented as hash tables. On average, membership tests ('element in my_set') take O(1) constant time, making them highly efficient compared to list searches which take O(N) time."
  },
  {
    category: "Python",
    question: "Which decorator from the standard library is best used to preserve the original function name and docstring when writing a custom decorator?",
    options: {
      A: "@functools.lru_cache",
      B: "@functools.wraps",
      C: "@classmethod",
      D: "@dataclass"
    },
    answer: "B",
    explanation: "@functools.wraps is a helper decorator that copies the metadata (name, docstring, arguments, etc.) of the decorated function back onto the wrapper function, preventing debugging headaches."
  },
  {
    category: "Python",
    question: "Which of the following operations is vectorized and therefore executed in fast compiled code (C/Rust) rather than Python bytecode?",
    options: {
      A: "df.apply(lambda row: row['a'] * row['b'], axis=1)",
      B: "df['a'] * df['b']",
      C: "[row[0] * row[1] for row in df.itertuples()]",
      D: "df.iterrows()"
    },
    answer: "B",
    explanation: "df['a'] * df['b'] leverages Pandas/NumPy vectorization, applying arithmetic operations at the C-level. Using apply, iterrows, or list comprehensions falls back to slower Python-level loops."
  },
  {
    category: "Machine Learning",
    question: "L1 regularization (Lasso) differs from L2 regularization (Ridge) primarily because L1:",
    options: {
      A: "Penalizes the squared magnitude of coefficients.",
      B: "Can shrink some coefficient weights all the way to absolute zero.",
      C: "Is less robust to outliers.",
      d: "Requires solving a non-convex optimization problem."
    },
    answer: "B",
    explanation: "L1 regularization adds a penalty equal to the absolute sum of the weights. This often drives coefficients to exactly zero, resulting in sparse models and serving as a feature selection tool. L2 regularization (Ridge) shrinks weights close to zero but rarely exactly to zero."
  },
  {
    category: "Machine Learning",
    question: "In the self-attention formula of the Transformer architecture, what is the purpose of dividing Query-Key dot products by the square root of key dimension (d_k)?",
    options: {
      A: "To ensure the output vectors are unit-normalized.",
      B: "To prevent the softmax function from saturating and producing extremely small gradients.",
      C: "To project the keys into a lower-dimensional subspace.",
      D: "To keep the learning rate stable across deep layers."
    },
    answer: "B",
    explanation: "Without scaling, the dot products of high-dimensional queries and keys can grow very large. This pushes the softmax function into regions with extremely small gradients (saturating), making model training stall. Scaling by 1/sqrt(d_k) mitigates this."
  },
  {
    category: "Machine Learning",
    question: "When evaluating a binary classifier on a highly imbalanced dataset (e.g., 0.1% positive class), which metric is generally preferred over standard ROC-AUC?",
    options: {
      A: "Classification Accuracy",
      B: "Precision-Recall AUC (PR-AUC)",
      C: "F1-Score macro average",
      D: "Specificity"
    },
    answer: "B",
    explanation: "ROC-AUC can look deceptively good on highly imbalanced data because it includes True Negatives in its calculation (via False Positive Rate). PR-AUC focuses exclusively on Precision and Recall, which isolates classifier performance on the rare positive class."
  }
];

// Document Elements
const elLevel = document.getElementById('user-level');
const elXP = document.getElementById('user-xp');
const elPercent = document.getElementById('curriculum-percent');
const elQuizRecord = document.getElementById('quiz-record');

// Update UI stats initially
function updateGlobalStats() {
  elLevel.textContent = userLevel;
  elXP.textContent = `${userXP} XP`;
  elQuizRecord.textContent = bestQuizScore;
}
updateGlobalStats();

// 2. Tab Navigation
document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.nav-tab');
  const contents = document.querySelectorAll('.tab-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      contents.forEach(c => c.classList.remove('active'));

      tab.classList.add('active');
      const tabName = tab.getAttribute('data-tab');
      document.getElementById(`tab-${tabName}`).classList.add('active');
      
      // Initialize specific tab logic on focus
      if (tabName === 'neuralnet') {
        initNeuralNet();
      } else if (tabName === 'benchmarks') {
        drawBenchmarkChart();
      }
    });
  });
});

// 3. Quiz Arena Module
let currentQuestionIndex = 0;
let quizScore = 0;
let userAnswers = [];

const quizIntro = document.getElementById('quiz-intro-screen');
const quizActive = document.getElementById('quiz-active-screen');
const quizResult = document.getElementById('quiz-result-screen');

const startQuizBtn = document.getElementById('start-quiz-btn');
const quizNextBtn = document.getElementById('quiz-next-btn');
const quizExitBtn = document.getElementById('quiz-exit-btn');
const retryQuizBtn = document.getElementById('retry-quiz-btn');

startQuizBtn.addEventListener('click', startQuiz);
quizNextBtn.addEventListener('click', loadNextQuestion);
quizExitBtn.addEventListener('click', exitQuiz);
retryQuizBtn.addEventListener('click', startQuiz);

function startQuiz() {
  currentQuestionIndex = 0;
  quizScore = 0;
  userAnswers = [];
  
  quizIntro.style.display = 'none';
  quizResult.style.display = 'none';
  quizActive.style.display = 'block';
  
  loadQuestion();
}

function loadQuestion() {
  quizNextBtn.style.display = 'none';
  document.getElementById('quiz-explanation-box').style.display = 'none';
  
  const q = QUESTIONS[currentQuestionIndex];
  
  // Update header progress
  document.getElementById('quiz-category').textContent = q.category;
  document.getElementById('quiz-q-counter').textContent = `Question ${currentQuestionIndex + 1} of ${QUESTIONS.length}`;
  
  const progressPercent = ((currentQuestionIndex + 1) / QUESTIONS.length) * 100;
  document.getElementById('quiz-bar-fill').style.width = `${progressPercent}%`;
  
  // Set question text
  document.getElementById('quiz-question-text').textContent = q.question;
  
  // Build Options HTML
  const optionsContainer = document.getElementById('quiz-options-container');
  optionsContainer.innerHTML = '';
  
  Object.keys(q.options).forEach(key => {
    const optionBtn = document.createElement('div');
    optionBtn.className = 'quiz-option';
    optionBtn.innerHTML = `<span class="option-prefix">${key}:</span> <span class="option-text">${q.options[key]}</span>`;
    optionBtn.addEventListener('click', () => selectOption(key, optionBtn));
    optionsContainer.appendChild(optionBtn);
  });
}

function selectOption(selectedKey, optionBtn) {
  const q = QUESTIONS[currentQuestionIndex];
  const allOptionBtns = document.querySelectorAll('.quiz-option');
  
  // Disable further clicks
  allOptionBtns.forEach(btn => btn.classList.add('disabled'));
  
  const isCorrect = selectedKey === q.answer;
  if (isCorrect) {
    optionBtn.classList.add('correct');
    quizScore++;
  } else {
    optionBtn.classList.add('incorrect');
    // Highlight correct answer as well
    allOptionBtns.forEach(btn => {
      if (btn.querySelector('.option-prefix').textContent.startsWith(q.answer)) {
        btn.classList.add('correct');
        btn.classList.remove('disabled'); // Ensure correct styling
      }
    });
  }
  
  // Show explanation
  document.getElementById('quiz-explanation-text').textContent = q.explanation;
  document.getElementById('quiz-explanation-box').style.display = 'block';
  
  // Update actions
  quizNextBtn.style.display = 'block';
  if (currentQuestionIndex === QUESTIONS.length - 1) {
    quizNextBtn.textContent = 'Finish & Show Results 🏁';
  } else {
    quizNextBtn.textContent = 'Next Question ➡️';
  }
}

function loadNextQuestion() {
  currentQuestionIndex++;
  if (currentQuestionIndex < QUESTIONS.length) {
    loadQuestion();
  } else {
    showResults();
  }
}

function exitQuiz() {
  if (confirm("Are you sure you want to exit the Certification Arena? Progress will be lost.")) {
    quizActive.style.display = 'none';
    quizResult.style.display = 'none';
    quizIntro.style.display = 'block';
  }
}

async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

function showResults() {
  quizActive.style.display = 'none';
  quizResult.style.display = 'block';
  
  const percent = (quizScore / QUESTIONS.length) * 100;
  
  // Save record score
  if (bestQuizScore === 'N/A' || quizScore > parseInt(bestQuizScore.split('/')[0])) {
    bestQuizScore = `${quizScore}/${QUESTIONS.length}`;
    localStorage.setItem('study_quest_best_score', bestQuizScore);
    updateGlobalStats();
  }
  
  document.getElementById('result-subtitle').textContent = `You scored ${quizScore}/${QUESTIONS.length} (${percent.toFixed(1)}%)`;
  
  const passed = quizScore >= 8;
  if (passed) {
    document.getElementById('result-title').textContent = "🛡️ Course Cleared!";
    document.getElementById('result-pass-actions').style.display = 'block';
    document.getElementById('result-fail-actions').style.display = 'none';
    
    // Reward XP once on first pass
    if (userXP === 0) {
      userXP += 1000;
      userLevel = 1 + Math.floor(userXP / 500);
      localStorage.setItem('study_quest_xp', userXP.toString());
      updateGlobalStats();
    }
  } else {
    document.getElementById('result-title').textContent = "⚠️ Try Again, Initiate!";
    document.getElementById('result-pass-actions').style.display = 'none';
    document.getElementById('result-fail-actions').style.display = 'block';
  }
}

// Certificate Generation
const generateBtn = document.getElementById('generate-web-cert-btn');
const downloadCertMdBtn = document.getElementById('download-cert-md-btn');

generateBtn.addEventListener('click', async () => {
  const nameInput = document.getElementById('student-name').value.trim() || 'Graduate';
  const dateStr = new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  
  // Generate token matching the Python verification signature
  const salt = "AI_DATA_SCIENCE_QUEST_SALT_2026";
  const hashInput = `${nameInput}|${dateStr}|${quizScore}|${salt}`;
  const signature = await sha256(hashInput);
  
  const payload = {
    name: nameInput,
    date: dateStr,
    score: `${quizScore}/9`,
    signature: signature
  };
  
  const payloadJson = JSON.stringify(payload);
  const token = btoa(unescape(encodeURIComponent(payloadJson)));
  
  // Build LinkedIn integration links
  const encodedName = encodeURIComponent("AI & Data Science Core Curriculum");
  const encodedOrg = encodeURIComponent("AI Data Science Resources");
  const encodedUrl = encodeURIComponent("https://github.com/saitejabandaru-in/AI-Data-Science-Resources");
  
  const linkedinAddUrl = `https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name=${encodedName}&organizationName=${encodedOrg}&certUrl=${encodedUrl}`;
  const linkedinShareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`;
  
  // Update Buttons
  document.getElementById('linkedin-add-badge-btn').href = linkedinAddUrl;
  document.getElementById('linkedin-share-badge-btn').href = linkedinShareUrl;
  
  // Configure Markdown download content
  downloadCertMdBtn.onclick = () => {
    const mdContent = `# 🏆 Certificate of Completion

Presented to: **${nameInput}**  
Date of Achievement: **${dateStr}**
Issued By: **[saitejabandaru.com](https://saitejabandaru.com)**
Authorized Signature: **Sai Teja Bandaru** (Founder & Instructor)

---

### 🎓 Modules Mastered
- **Advanced SQL Database Systems:** Logical Execution Order, Window Functions, Query Optimization.
- **Python & High-Performance Data Engineering:** Functional Decorators, Generators, Vectorization pipelines (Pandas & Polars).
- **Core Machine Learning & Deep Architectures:** Statistical Math, Tree-based Ensembles, Gradient Descent, Transformers, and Retrieval-Augmented Generation (RAG).

### 🛡️ Verified Achievement
This certificate verifies successful completion of the comprehensive technical examination hosted at [saitejabandaru-in/AI-Data-Science-Resources](https://github.com/saitejabandaru-in/AI-Data-Science-Resources).

---
<!-- VERIFICATION_TOKEN: ${token} -->
`;
    
    const blob = new Blob([mdContent], { type: 'text/markdown' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'CERTIFICATE.md';
    link.click();
  };
  
  document.getElementById('share-section-box').style.display = 'block';
  alert(`✨ Certificate created for ${nameInput}! Add to profile or download CERTIFICATE.md to open a PR.`);
});


// 4. Neural Network Lab (Perceptron Simulation)
let canvas, ctx;
let points = [];
let weights = [0.1, -0.2, 0.3]; // w0 (bias), w1, w2
let nnLR = 0.1;
let nnEpochCount = 0;
let isTraining = false;
let trainIntervalId = null;

function initNeuralNet() {
  canvas = document.getElementById('perceptron-canvas');
  if (!canvas) return;
  ctx = canvas.getContext('2d');
  
  // Event Listeners
  document.getElementById('nn-lr').addEventListener('input', (e) => {
    nnLR = parseFloat(e.target.value);
    document.getElementById('nn-lr-val').textContent = nnLR.toFixed(3);
  });
  
  document.getElementById('nn-dataset').addEventListener('change', generateData);
  document.getElementById('nn-step-btn').onclick = stepTraining;
  document.getElementById('nn-run-btn').onclick = toggleRunTraining;
  document.getElementById('nn-reset-btn').onclick = resetWeights;
  
  generateData();
  drawSimulation();
}

function generateData() {
  points = [];
  const type = document.getElementById('nn-dataset').value;
  const count = 60;
  
  for (let i = 0; i < count; i++) {
    let x = Math.random() * 2 - 1; // -1 to 1
    let y = Math.random() * 2 - 1;
    let label = 0;
    
    if (type === 'linearly_separable') {
      // separator line: y = 0.3*x - 0.1
      label = (y > 0.3 * x - 0.1) ? 1 : -1;
    } else if (type === 'noisy_separable') {
      label = (y > -0.5 * x + 0.2) ? 1 : -1;
      // Inject noise
      if (Math.random() < 0.08) label = -label;
    } else {
      // circular XOR structure
      label = (x * x + y * y < 0.4) ? 1 : -1;
    }
    
    points.push({ x, y, label });
  }
  
  resetWeights();
}

function resetWeights() {
  weights = [
    Math.random() * 0.4 - 0.2, // bias (w0)
    Math.random() * 2 - 1,     // w1
    Math.random() * 2 - 1      // w2
  ];
  nnEpochCount = 0;
  isTraining = false;
  if (trainIntervalId) clearInterval(trainIntervalId);
  document.getElementById('nn-run-btn').textContent = '🚀 Run Training (Auto)';
  document.getElementById('nn-run-btn').className = 'btn btn-green';
  
  evaluateStats();
  drawSimulation();
}

function drawSimulation() {
  if (!ctx) return;
  // Clear Canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  const w = canvas.width;
  const h = canvas.height;
  
  // Coordinate transformers: [-1, 1] to screen [0, width]
  const toScreenX = (val) => (val + 1) * 0.5 * w;
  const toScreenY = (val) => (1 - val) * 0.5 * h; // invert Y for standard math orientation
  
  // 1. Draw grid lines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let i = -10; i <= 10; i += 2) {
    let gridVal = i / 10;
    // vertical
    ctx.moveTo(toScreenX(gridVal), 0);
    ctx.lineTo(toScreenX(gridVal), h);
    // horizontal
    ctx.moveTo(0, toScreenY(gridVal));
    ctx.lineTo(w, toScreenY(gridVal));
  }
  ctx.stroke();
  
  // 2. Draw Decision Boundary Line (w0 + w1*x + w2*y = 0)
  // Equation: y = -(w1*x + w0) / w2
  ctx.strokeStyle = '#99E2B4';
  ctx.lineWidth = 3;
  ctx.beginPath();
  
  const xStart = -1.0;
  const yStart = -(weights[1] * xStart + weights[0]) / weights[2];
  const xEnd = 1.0;
  const yEnd = -(weights[1] * xEnd + weights[0]) / weights[2];
  
  ctx.moveTo(toScreenX(xStart), toScreenY(yStart));
  ctx.lineTo(toScreenX(xEnd), toScreenY(yEnd));
  ctx.stroke();
  
  // 3. Draw Points
  points.forEach(p => {
    ctx.fillStyle = (p.label === 1) ? '#EF4444' : '#4F7CAC';
    ctx.beginPath();
    ctx.arc(toScreenX(p.x), toScreenY(p.y), 6, 0, 2 * Math.PI);
    ctx.fill();
    
    // Add thin border to show classification validation
    const activation = weights[0] + weights[1] * p.x + weights[2] * p.y;
    const predicted = activation >= 0 ? 1 : -1;
    ctx.strokeStyle = (predicted === p.label) ? 'rgba(153, 226, 180, 0.6)' : 'rgba(239, 68, 68, 0.8)';
    ctx.lineWidth = 2;
    ctx.stroke();
  });
}

function evaluateStats() {
  let errors = 0;
  let loss = 0;
  
  points.forEach(p => {
    const activation = weights[0] + weights[1] * p.x + weights[2] * p.y;
    const predicted = activation >= 0 ? 1 : -1;
    if (predicted !== p.label) {
      errors++;
      loss += Math.pow(p.label - activation, 2);
    }
  });
  
  const accuracy = ((points.length - errors) / points.length) * 100;
  loss = loss / points.length;
  
  document.getElementById('nn-epochs').textContent = nnEpochCount;
  document.getElementById('nn-accuracy').textContent = `${accuracy.toFixed(0)}%`;
  document.getElementById('nn-loss').textContent = loss.toFixed(2);
  
  if (accuracy === 100) {
    document.getElementById('nn-status').className = 'text-green';
    document.getElementById('nn-status').textContent = 'Trained ✅';
  }
  
  return accuracy;
}

function stepTraining() {
  nnEpochCount++;
  
  // Shuffle points to stabilize learning
  const shuffled = [...points].sort(() => Math.random() - 0.5);
  
  shuffled.forEach(p => {
    const activation = weights[0] + weights[1] * p.x + weights[2] * p.y;
    const predicted = activation >= 0 ? 1 : -1;
    
    if (predicted !== p.label) {
      // Perceptron learning rule: weight_delta = learning_rate * (label - predicted) * input
      const error = p.label - predicted;
      weights[0] += nnLR * error * 1.0; // bias weight
      weights[1] += nnLR * error * p.x;
      weights[2] += nnLR * error * p.y;
    }
  });
  
  const acc = evaluateStats();
  drawSimulation();
  
  if (acc === 100 && isTraining) {
    toggleRunTraining();
  }
}

function toggleRunTraining() {
  if (isTraining) {
    isTraining = false;
    clearInterval(trainIntervalId);
    document.getElementById('nn-run-btn').textContent = '🚀 Run Training (Auto)';
    document.getElementById('nn-run-btn').className = 'btn btn-green';
  } else {
    isTraining = true;
    document.getElementById('nn-run-btn').textContent = '🛑 Stop Training';
    document.getElementById('nn-run-btn').className = 'btn btn-secondary';
    
    trainIntervalId = setInterval(() => {
      stepTraining();
      if (nnEpochCount >= 200) {
        toggleRunTraining();
        alert("Epoch limit reached (200). Training halted.");
      }
    }, 120);
  }
}


// 5. Benchmark Visualizer
function drawBenchmarkChart() {
  const canvas = document.getElementById('benchmark-chart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  const w = canvas.width;
  const h = canvas.height;
  
  // Data Definition
  const engines = [
    { name: "Pure Python", time: 2400, color: '#F59E0B', ratio: "1x (Base)" },
    { name: "Pandas (C Vectorized)", time: 120, color: '#4F7CAC', ratio: "20x Faster" },
    { name: "Polars (Rust Engine)", time: 8, color: '#99E2B4', ratio: "300x Faster" }
  ];
  
  const maxTime = 2400; // to scale the heights
  const chartHeight = h - 100;
  const colWidth = 100;
  const startX = 120;
  
  // Draw Axis lines
  ctx.strokeStyle = 'rgba(255,255,255,0.15)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  // Y-axis
  ctx.moveTo(startX, 30);
  ctx.lineTo(startX, chartHeight + 30);
  // X-axis
  ctx.moveTo(startX, chartHeight + 30);
  ctx.lineTo(w - 50, chartHeight + 30);
  ctx.stroke();
  
  // Grid Lines & Labels
  ctx.fillStyle = '#A0AAB2';
  ctx.font = '10px Inter, sans-serif';
  ctx.textAlign = 'right';
  
  for (let val = 0; val <= maxTime; val += 600) {
    let yPos = chartHeight + 30 - (val / maxTime) * chartHeight;
    ctx.fillText(`${val} ms`, startX - 15, yPos + 4);
    
    ctx.strokeStyle = 'rgba(255,255,255,0.03)';
    ctx.beginPath();
    ctx.moveTo(startX, yPos);
    ctx.lineTo(w - 50, yPos);
    ctx.stroke();
  }
  
  // Draw Bars
  engines.forEach((eng, idx) => {
    const barX = startX + 60 + idx * 180;
    const barHeight = (eng.time / maxTime) * (chartHeight - 20); // cap slightly below top
    const barY = chartHeight + 30 - barHeight;
    
    // Create Gradient
    const gradient = ctx.createLinearGradient(barX, barY, barX, chartHeight + 30);
    gradient.addColorStop(0, eng.color);
    gradient.addColorStop(1, '#1C2B36');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(barX, barY, colWidth, barHeight);
    
    // Draw Bar value label
    ctx.fillStyle = '#E6EEF3';
    ctx.font = 'bold 12px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${eng.time} ms`, barX + colWidth / 2, barY - 10);
    
    // Draw Speed Ratio
    ctx.fillStyle = eng.color;
    ctx.font = 'bold 11px Inter, sans-serif';
    ctx.fillText(eng.ratio, barX + colWidth / 2, barY - 26);
    
    // Draw X-Axis Label
    ctx.fillStyle = '#E6EEF3';
    ctx.font = '600 12px Outfit, sans-serif';
    ctx.fillText(eng.name, barX + colWidth / 2, chartHeight + 52);
  });
}
