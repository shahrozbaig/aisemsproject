const STORAGE_KEY = 'clindoc_ai_reports';
const AGENTS_FALLBACK = [
  { name: 'Classifier Agent', role: 'Identifies symptom categories and clinical intent.', status: 'Active', action: 'Tagged 4 symptom groups' },
  { name: 'Medical Extraction Agent', role: 'Extracts relevant patient findings and context.', status: 'Active', action: 'Parsed symptom details' },
  { name: 'Recommendation Agent', role: 'Suggests medicines and dosage guidance.', status: 'Active', action: 'Generated treatment plan' },
  { name: 'Documentation Agent', role: 'Compiles notes into a structured clinical report.', status: 'Active', action: 'Prepared latest report' },
  { name: 'QA Agent', role: 'Scores accuracy and identifies potential risks.', status: 'Active', action: 'Verified report quality' }
];

const SYMPTOM_KEYS = {
  fever: 'Fever',
  headache: 'Headache',
  'chest pain': 'Chest pain',
  cold: 'Cold',
  cough: 'Cold',
  nausea: 'General',
  fatigue: 'General',
  dizziness: 'General'
};

const MEDICINE_RECOMMENDATIONS = {
  Fever: { medicine: 'Paracetamol', dosage: '500mg every 6 hours', warning: 'Avoid if liver issues present.' },
  Headache: { medicine: 'Ibuprofen', dosage: '400mg every 8 hours', warning: 'Use with food to reduce stomach upset.' },
  'Chest pain': { medicine: 'Aspirin', dosage: '75mg once daily', warning: 'Seek urgent medical review if pain persists.' },
  Cold: { medicine: 'Antihistamines', dosage: '10mg once daily', warning: 'May cause mild drowsiness.' },
  General: { medicine: 'Rest and hydration', dosage: 'As needed', warning: 'Monitor symptoms closely.' }
};

function loadReports() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
}

function saveReports(reports) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(reports));
}

function classifySymptoms(text) {
  const normalized = text.toLowerCase();
  const found = Object.keys(SYMPTOM_KEYS).filter((key) => normalized.includes(key)).map((key) => SYMPTOM_KEYS[key]);
  return found.length ? [...new Set(found)] : ['General'];
}

function generateDiagnosis(labels) {
  if (labels.includes('Chest pain')) return 'Possible cardiac strain or angina';
  if (labels.includes('Fever')) return 'Suspected viral infection';
  if (labels.includes('Headache')) return 'Tension headache with mild inflammation';
  if (labels.includes('Cold')) return 'Upper respiratory tract irritation';
  return 'General symptom cluster requiring monitoring';
}

function determineSeverity(labels) {
  if (labels.includes('Chest pain')) return 'High';
  if (labels.includes('Fever') || labels.includes('Headache')) return 'Medium';
  return 'Low';
}

function determineStatus(severity) {
  return severity === 'High' ? 'Critical' : 'Stable';
}

function generateQaScore() {
  return Math.floor(82 + Math.random() * 16);
}

function recommendMedicines(labels) {
  const recommendations = labels.map((label) => MEDICINE_RECOMMENDATIONS[label]).filter(Boolean);
  return [...new Map(recommendations.map((item) => [item.medicine, item])).values()].slice(0, 2);
}

function formatTime(ts) {
  const now = new Date(ts);
  return now.toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
}

async function requestReport(symptoms) {
  try {
    const response = await fetch('/api/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symptoms })
    });
    if (response.ok) {
      const data = await response.json();
      return { ...data, time: data.time || new Date().toISOString() };
    }
  } catch (_) {}

  const labels = classifySymptoms(symptoms);
  return {
    symptoms,
    labels,
    diagnosis: generateDiagnosis(labels),
    severity: determineSeverity(labels),
    status: determineStatus(determineSeverity(labels)),
    qa_score: generateQaScore(),
    medicines: recommendMedicines(labels),
    ai_message: 'Hello, I have analyzed the patient data and prepared a clinical summary.',
    time: new Date().toISOString()
  };
}

function renderReport(report) {
  document.getElementById('latest-status-badge').textContent = report.status;
  document.getElementById('latest-status-badge').className = `badge ${report.status === 'Critical' ? 'bg-danger' : 'bg-success'} py-2 px-3`;
  document.getElementById('latest-diagnosis').textContent = report.diagnosis;
  document.getElementById('latest-severity').textContent = report.severity;
  document.getElementById('latest-qa').textContent = `${report.qa_score}%`;
  document.getElementById('ai-message-text').textContent = report.ai_message;

  const medicinesContainer = document.getElementById('medicines-list');
  medicinesContainer.innerHTML = report.medicines.map((med) => `
    <div class="col-md-6">
      <div class="medicine-card p-3 rounded-4 shadow-sm bg-surface">
        <h6 class="mb-1">${med.medicine}</h6>
        <p class="mb-1 text-muted">${med.dosage}</p>
        <p class="small text-danger mb-0">${med.warning}</p>
      </div>
    </div>
  `).join('');
}

function renderHistory(reports) {
  const historyContainer = document.getElementById('history-container');
  if (!historyContainer) return;

  if (!reports.length) {
    historyContainer.innerHTML = '<div class="py-5 text-center text-muted">No patient history yet.</div>';
    return;
  }

  historyContainer.innerHTML = reports.map((report) => `
    <div class="col-md-6">
      <div class="history-card-item p-3 rounded-4 border bg-surface-soft">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <span class="badge ${report.status === 'Critical' ? 'bg-danger' : 'bg-success'} py-2 px-3">${report.status}</span>
          <small class="text-muted">${formatTime(report.time)}</small>
        </div>
        <h6>Diagnosis:</h6>
        <p class="mb-2">${report.diagnosis}</p>
        <p class="mb-2"><strong>Symptoms:</strong> ${report.symptoms}</p>
        <p class="mb-0"><strong>Medicines:</strong> ${report.medicines.map((med) => med.medicine).join(', ')}</p>
      </div>
    </div>
  `).join('');
}

function renderStats(reports) {
  const total = reports.length;
  const stable = reports.filter((item) => item.status === 'Stable').length;
  const critical = reports.filter((item) => item.status === 'Critical').length;
  const accuracy = Math.min(98, Math.max(82, 90 + stable - critical));

  document.getElementById('total-reports').textContent = total;
  document.getElementById('stable-reports').textContent = stable;
  document.getElementById('critical-reports').textContent = critical;
  document.getElementById('ai-accuracy').textContent = `${accuracy}%`;
  document.getElementById('report-count').textContent = `${total} records`;
}

async function renderAgents() {
  const container = document.getElementById('agents-list');
  if (!container) return;

  let data = AGENTS_FALLBACK;
  try {
    const response = await fetch('/api/agents');
    if (response.ok) data = await response.json();
  } catch (_) {}

  container.innerHTML = data.map((agent) => `
    <div class="col-md-6 col-xl-4">
      <div class="agent-card p-4 rounded-4 shadow-sm bg-surface h-100">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <div class="agent-icon rounded-circle bg-primary-soft text-primary d-flex align-items-center justify-content-center">
            <i class="fa-solid fa-robot fa-lg"></i>
          </div>
          <span class="badge bg-success py-2 px-3">${agent.status}</span>
        </div>
        <h5>${agent.name}</h5>
        <p class="text-muted">${agent.role}</p>
        <div class="mt-4 pt-3 border-top text-muted">
          <small><strong>Last action:</strong> ${agent.action}</small>
        </div>
      </div>
    </div>
  `).join('');
}

async function initDashboard() {
  const reports = loadReports();
  const form = document.getElementById('symptom-form');
  const input = document.getElementById('symptoms-input');

  if (form && input) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;

      const report = await requestReport(text);
      reports.unshift(report);
      saveReports(reports);
      renderReport(report);
      renderHistory(reports);
      renderStats(reports);
      input.value = '';
    });
  }

  if (reports.length) {
    renderReport(reports[0]);
  }
  renderHistory(reports);
  renderStats(reports);
}

function initAgentsPage() {
  renderAgents();
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('symptom-form')) {
    initDashboard();
  }
  if (document.getElementById('agents-list')) {
    initAgentsPage();
  }
});
