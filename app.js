const modules = [
  {
    id: "constitutional",
    name: "Constitutional Law",
    difficulty: 0.72,
    skills: ["fundamental rights", "judicial review", "reasonable restrictions"],
    practice: "Apply Article 14 tests to a classification-based policy dispute."
  },
  {
    id: "criminal",
    name: "Criminal Law",
    difficulty: 0.68,
    skills: ["mens rea", "actus reus", "defences"],
    practice: "Identify offence elements and possible defences in a theft scenario."
  },
  {
    id: "contract",
    name: "Contract Law",
    difficulty: 0.58,
    skills: ["offer", "acceptance", "consideration", "breach"],
    practice: "Draft an issue-rule-application-conclusion answer for breach of contract."
  },
  {
    id: "torts",
    name: "Law of Torts",
    difficulty: 0.61,
    skills: ["duty of care", "negligence", "damages"],
    practice: "Analyze negligence using duty, breach, causation, and damage."
  },
  {
    id: "evidence",
    name: "Evidence Law",
    difficulty: 0.75,
    skills: ["admissibility", "burden of proof", "cross examination"],
    practice: "Decide whether a disputed document is admissible and reliable."
  }
];

const scenarios = [
  {
    title: "Contract breach in an online coaching agreement",
    facts: "A student paid for a six-month legal coaching program. The institute promised weekly moot sessions but delivered only two sessions in three months.",
    task: "Frame issues, identify contract principles, and suggest remedies."
  },
  {
    title: "Constitutional challenge to campus speech rules",
    facts: "A university restricts student debates on public policy unless prior approval is granted by a disciplinary committee.",
    task: "Analyze fundamental rights, reasonable restrictions, and proportionality."
  },
  {
    title: "Criminal liability in a mistaken identity case",
    facts: "A witness identifies an accused under poor lighting. The accused claims alibi and challenges the reliability of testimony.",
    task: "Assess mens rea, evidence reliability, and burden of proof."
  },
  {
    title: "Negligence in a legal aid clinic",
    facts: "A clinic misses a limitation deadline after accepting a client's documents and assigning a student volunteer.",
    task: "Discuss duty of care, breach, causation, and professional responsibility."
  }
];

const legalKeywords = {
  contract: ["offer", "acceptance", "consideration", "breach", "damages", "consent", "remedy"],
  reasoning: ["issue", "rule", "apply", "application", "conclusion", "precedent", "court", "held"],
  evidence: ["burden", "proof", "admissible", "reliable", "witness"],
  constitutional: ["rights", "restriction", "proportionality", "article", "equality"]
};

const neuronReasons = [
  {
    name: "N1",
    pattern: "quiz and reasoning readiness",
    reason: "This neuron becomes active when quiz performance and legal reasoning are strong enough to show conceptual readiness."
  },
  {
    name: "N2",
    pattern: "consistency weakness",
    reason: "This neuron reacts to study consistency. Low consistency can increase intervention risk even when quiz score is acceptable."
  },
  {
    name: "N3",
    pattern: "topic difficulty pressure",
    reason: "This neuron focuses on subject difficulty. Harder topics like Evidence or Constitutional Law can raise the risk signal."
  },
  {
    name: "N4",
    pattern: "student level adjustment",
    reason: "This neuron adjusts the prediction using beginner, intermediate, or advanced level information."
  },
  {
    name: "N5",
    pattern: "combined low-performance risk",
    reason: "This neuron becomes active when multiple weak signals appear together, such as low quiz score plus low reasoning score."
  },
  {
    name: "N6",
    pattern: "learning recovery signal",
    reason: "This neuron captures positive recovery signs, mainly consistency and enough readiness to continue without heavy intervention."
  }
];

const state = {
  scenarioIndex: 0,
  dlModel: null,
  selectedNeuron: null
};

const $ = (id) => document.getElementById(id);

function getProfile() {
  return {
    level: $("studentLevel").value,
    track: $("track").value,
    quiz: Number($("quizScore").value),
    reasoning: Number($("reasoningScore").value),
    consistency: Number($("consistencyScore").value)
  };
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function sigmoid(value) {
  return 1 / (1 + Math.exp(-value));
}

function relu(value) {
  return Math.max(0, value);
}

function reluDerivative(value) {
  return value > 0 ? 1 : 0;
}

function seededRandom(seed) {
  const value = Math.sin(seed) * 10000;
  return value - Math.floor(value);
}

function buildDlDataset() {
  const rows = [];
  for (let i = 1; i <= 180; i += 1) {
    const quiz = 20 + seededRandom(i * 3) * 78;
    const reasoning = 15 + seededRandom(i * 5) * 80;
    const consistency = 10 + seededRandom(i * 7) * 90;
    const difficulty = 0.50 + seededRandom(i * 11) * 0.35;
    const level = Math.floor(seededRandom(i * 13) * 3);
    const conceptLoad = 0.4 + seededRandom(i * 17) * 0.6;
    const readiness = quiz * 0.34 + reasoning * 0.36 + consistency * 0.22 + level * 5 - difficulty * 24 - conceptLoad * 10;
    const risk = readiness < 49 ? 1 : 0;
    rows.push({
      x: [quiz / 100, reasoning / 100, consistency / 100, difficulty, level / 2],
      y: risk
    });
  }
  return rows;
}

function createDlModel() {
  const inputSize = 5;
  const hiddenSize = 6;
  const w1 = Array.from({ length: hiddenSize }, (_, h) =>
    Array.from({ length: inputSize }, (_, i) => (seededRandom((h + 1) * (i + 3)) - 0.5) * 0.8)
  );
  const b1 = Array.from({ length: hiddenSize }, () => 0);
  const w2 = Array.from({ length: hiddenSize }, (_, h) => (seededRandom((h + 5) * 19) - 0.5) * 0.8);
  return { w1, b1, w2, b2: 0 };
}

function forwardDl(model, x) {
  const hiddenRaw = model.w1.map((weights, h) =>
    weights.reduce((sum, weight, i) => sum + weight * x[i], model.b1[h])
  );
  const hidden = hiddenRaw.map(relu);
  const outputRaw = hidden.reduce((sum, value, h) => sum + value * model.w2[h], model.b2);
  return { hiddenRaw, hidden, output: sigmoid(outputRaw) };
}

function trainDlModel() {
  const dataset = buildDlDataset();
  const model = createDlModel();
  const learningRate = 0.08;
  const epochs = 360;
  let lastLoss = 0;

  for (let epoch = 0; epoch < epochs; epoch += 1) {
    let totalLoss = 0;
    dataset.forEach(row => {
      const pass = forwardDl(model, row.x);
      const prediction = pass.output;
      const error = prediction - row.y;
      totalLoss += -(row.y * Math.log(prediction + 1e-7) + (1 - row.y) * Math.log(1 - prediction + 1e-7));

      const outputGradient = error;
      const oldW2 = [...model.w2];

      for (let h = 0; h < model.w2.length; h += 1) {
        model.w2[h] -= learningRate * outputGradient * pass.hidden[h];
      }
      model.b2 -= learningRate * outputGradient;

      for (let h = 0; h < model.w1.length; h += 1) {
        const hiddenGradient = outputGradient * oldW2[h] * reluDerivative(pass.hiddenRaw[h]);
        for (let i = 0; i < model.w1[h].length; i += 1) {
          model.w1[h][i] -= learningRate * hiddenGradient * row.x[i];
        }
        model.b1[h] -= learningRate * hiddenGradient;
      }
    });
    lastLoss = totalLoss / dataset.length;
  }

  const correct = dataset.filter(row => {
    const predicted = forwardDl(model, row.x).output >= 0.5 ? 1 : 0;
    return predicted === row.y;
  }).length;

  state.dlModel = model;
  renderDlPrediction({
    epochs,
    loss: lastLoss,
    accuracy: correct / dataset.length
  });
}

function getDlInput(profile) {
  const levelValue = { beginner: 0, intermediate: 0.5, advanced: 1 }[profile.level];
  const selected = modules.find(module => module.id === profile.track) || modules[0];
  return [profile.quiz / 100, profile.reasoning / 100, profile.consistency / 100, selected.difficulty, levelValue];
}

function renderDlPrediction(metrics = null) {
  if (!state.dlModel) {
    $("hiddenActivations").innerHTML = Array.from({ length: 6 }, (_, i) => `
      <button class="activation-cell" type="button" data-neuron="${i}">
        <span>N${i + 1}: --</span>
        <div class="activation-track"><div class="activation-fill" style="--value: 0%"></div></div>
      </button>
    `).join("");
    bindNeuronClicks();
    return;
  }

  const profile = getProfile();
  const pass = forwardDl(state.dlModel, getDlInput(profile));
  const risk = Math.round(pass.output * 100);
  $("dlRiskValue").textContent = `${risk}%`;
  $("dlDecision").textContent = risk >= 50 ? "Intervention" : "Normal";
  $("dlStatus").textContent = "Trained in-browser using backpropagation on synthetic student-learning records.";

  if (metrics) {
    $("dlEpochs").textContent = metrics.epochs;
    $("dlLoss").textContent = metrics.loss.toFixed(3);
    $("dlAccuracy").textContent = `${Math.round(metrics.accuracy * 100)}%`;
  }

  $("hiddenActivations").innerHTML = pass.hidden.map((value, i) => {
    const pct = clamp(Math.round(value * 100), 0, 100);
    const activeClass = state.selectedNeuron === i ? " active" : "";
    return `
      <button class="activation-cell${activeClass}" type="button" data-neuron="${i}">
        <span>N${i + 1}: ${pct}%</span>
        <div class="activation-track"><div class="activation-fill" style="--value: ${pct}%"></div></div>
      </button>
    `;
  }).join("");
  bindNeuronClicks();
  if (state.selectedNeuron !== null) {
    showNeuronExplanation(state.selectedNeuron);
  }
}

function bindNeuronClicks() {
  document.querySelectorAll(".activation-cell").forEach(cell => {
    cell.addEventListener("click", () => {
      const index = Number(cell.dataset.neuron);
      state.selectedNeuron = index;
      renderDlPrediction();
      showNeuronExplanation(index);
    });
  });
}

function showNeuronExplanation(index) {
  const profile = getProfile();
  const info = neuronReasons[index];
  if (!state.dlModel) {
    $("neuronExplanation").textContent = `${info.name} checks ${info.pattern}. Train the neural network first to see the real activation reason.`;
    return;
  }

  const pass = forwardDl(state.dlModel, getDlInput(profile));
  const activation = clamp(Math.round(pass.hidden[index] * 100), 0, 100);
  const selected = modules.find(module => module.id === profile.track) || modules[0];
  const signal = activation >= 70 ? "high" : activation >= 35 ? "medium" : "low";
  const profileText = `Current inputs: quiz ${profile.quiz}%, reasoning ${profile.reasoning}%, consistency ${profile.consistency}%, topic ${selected.name}, difficulty ${Math.round(selected.difficulty * 100)}%, level ${profile.level}.`;
  $("neuronExplanation").innerHTML = `
    <strong>${info.name} - ${info.pattern}</strong><br>
    Activation is <strong>${activation}% (${signal})</strong>. ${info.reason}<br>
    ${profileText}
  `;
}

function calculateMastery(profile) {
  const levelBoost = { beginner: -8, intermediate: 0, advanced: 8 }[profile.level];
  return modules.map((module, index) => {
    const trackBoost = module.id === profile.track ? 9 : 0;
    const difficultyPenalty = module.difficulty * 18;
    const spread = (index - 2) * 3;
    const value = clamp(
      Math.round(profile.quiz * 0.42 + profile.reasoning * 0.38 + profile.consistency * 0.20 + levelBoost + trackBoost - difficultyPenalty + spread),
      18,
      96
    );
    return { ...module, mastery: value };
  });
}

function renderMastery() {
  const profile = getProfile();
  $("quizOut").textContent = `${profile.quiz}%`;
  $("reasoningOut").textContent = `${profile.reasoning}%`;
  $("consistencyOut").textContent = `${profile.consistency}%`;
  renderDashboardHighlights(profile);

  const rows = calculateMastery(profile)
    .map(module => `
      <div class="bar-row">
        <div class="bar-meta">
          <span>${module.name}</span>
          <span>${module.mastery}%</span>
        </div>
        <div class="bar-track"><div class="bar-fill" style="--value: ${module.mastery}%"></div></div>
      </div>
    `)
    .join("");
  $("masteryBars").innerHTML = rows;
  renderRecommendations();
  renderAgentPlan();
  renderDlPrediction();
}

function renderDashboardHighlights(profile) {
  const readiness = clamp(Math.round(profile.quiz * 0.36 + profile.reasoning * 0.38 + profile.consistency * 0.26), 0, 100);
  $("progressCircle").style.setProperty("--score", readiness);
  $("progressScore").textContent = `${readiness}%`;
  $("progressLabel").textContent = readiness >= 78 ? "Strong" : readiness >= 58 ? "Developing" : "Needs support";

  document.querySelectorAll(".subject-badges span").forEach(badge => {
    badge.classList.toggle("active", badge.dataset.track === profile.track);
  });
}

function renderRecommendations() {
  const profile = getProfile();
  const ranked = calculateMastery(profile)
    .map(module => {
      const weakness = 100 - module.mastery;
      const relevance = module.id === profile.track ? 18 : 0;
      const readiness = profile.consistency * 0.12;
      const score = Math.round(weakness * 0.62 + module.difficulty * 20 + relevance + readiness);
      return { ...module, score };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  $("recommendationGrid").innerHTML = ranked.map((module, index) => `
    <div class="module-card">
      <span class="score-chip">Priority ${index + 1} | Match score ${module.score}</span>
      <strong>${module.name}</strong>
      <p><b>Focus skills:</b> ${module.skills.join(", ")}</p>
      <p><b>Practice:</b> ${module.practice}</p>
    </div>
  `).join("");
}

function analyzeAnswer() {
  const text = $("answerText").value.trim().toLowerCase();
  const tokens = text.split(/[^a-z]+/).filter(Boolean);
  const wordCount = tokens.length;
  const unique = new Set(tokens).size;
  const density = wordCount ? unique / wordCount : 0;

  const categoryScores = Object.entries(legalKeywords).map(([category, words]) => {
    const hits = words.filter(word => text.includes(word));
    return { category, hits, score: hits.length };
  });

  const totalHits = categoryScores.reduce((sum, item) => sum + item.score, 0);
  const structureScore = ["issue", "rule", "apply", "conclusion", "because", "therefore"].filter(word => text.includes(word)).length;
  const score = clamp(Math.round(totalHits * 7 + structureScore * 8 + Math.min(wordCount, 130) * 0.18 + density * 18), 12, 96);

  let band = "Developing";
  if (score >= 78) band = "Strong";
  else if (score >= 58) band = "Competent";

  $("qualityBadge").textContent = `${band} | ${score}%`;

  const gaps = [];
  if (!text.includes("issue")) gaps.push("State the legal issue explicitly before applying rules.");
  if (!text.includes("precedent")) gaps.push("Refer to precedent or authority to support the conclusion.");
  if (!text.includes("remedy") && !text.includes("damages")) gaps.push("Add remedy analysis, especially damages or specific relief.");
  if (wordCount < 70) gaps.push("Expand factual application; the answer is concise for a full case brief.");
  if (!gaps.length) gaps.push("Reasoning structure is clear; improve by adding one counter-argument.");

  const strengths = categoryScores
    .filter(item => item.score > 0)
    .map(item => `${item.category}: ${item.hits.join(", ")}`);

  $("analysisResult").innerHTML = `
    <p><strong>Detected understanding:</strong> ${strengths.length ? strengths.join(" | ") : "limited legal concept coverage detected"}</p>
    <ul class="diagnostic-list">
      ${gaps.map(gap => `<li>${gap}</li>`).join("")}
    </ul>
    <p><strong>Tutor response:</strong> Start with IRAC, connect each fact to a legal rule, then close with a justified remedy. The next practice module is selected from your weakest mastery area.</p>
  `;
}

function renderScenario() {
  const item = scenarios[state.scenarioIndex % scenarios.length];
  $("scenarioBox").innerHTML = `
    <h4>${item.title}</h4>
    <p><strong>Facts:</strong> ${item.facts}</p>
    <p><strong>Student task:</strong> ${item.task}</p>
    <p><strong>Generated challenge:</strong> Prepare one argument for the petitioner, one for the respondent, and one likely judicial question.</p>
  `;
}

function renderAgentPlan() {
  const profile = getProfile();
  const weakest = calculateMastery(profile).sort((a, b) => a.mastery - b.mastery)[0];
  const plan = [
    `Assess ${weakest.name} again with a 5-question diagnostic quiz.`,
    `Assign one guided case brief focused on ${weakest.skills[0]}.`,
    `Generate a short explanation if the student misses two linked concepts.`,
    `Escalate to faculty review if mastery remains below 45% after three attempts.`
  ];
  $("agentPlan").innerHTML = plan.map(item => `<li>${item}</li>`).join("");
}

function resetProfile() {
  $("studentLevel").value = "intermediate";
  $("track").value = "contract";
  $("quizScore").value = 64;
  $("reasoningScore").value = 58;
  $("consistencyScore").value = 71;
  renderMastery();
  analyzeAnswer();
}

function bindEvents() {
  ["studentLevel", "track", "quizScore", "reasoningScore", "consistencyScore"].forEach(id => {
    $(id).addEventListener("input", renderMastery);
  });
  $("recommendBtn").addEventListener("click", renderRecommendations);
  $("analyzeBtn").addEventListener("click", analyzeAnswer);
  $("trainDlBtn").addEventListener("click", trainDlModel);
  $("themeToggle").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
  });
  $("resetBtn").addEventListener("click", resetProfile);
  $("scenarioBtn").addEventListener("click", () => {
    state.scenarioIndex += 1;
    renderScenario();
  });
  $("sampleAnswerBtn").addEventListener("click", () => {
    $("answerText").value = "The issue is whether the accused or defendant is legally liable based on the facts. The rule requires proof of each legal element and the court must apply precedent carefully. Because the facts show breach, causation, and damages, the claimant can seek a remedy. A counter argument is that consent or lack of proof may reduce liability.";
    analyzeAnswer();
  });
}

bindEvents();
renderMastery();
analyzeAnswer();
renderScenario();
renderDlPrediction();
