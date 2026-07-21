const demoData = window.TC2_DEMO_DATA;

let selectedSessionIndex = 0;
let selectedStrategy = "rule_based";

const elements = {
  metricCategory: document.getElementById("metric-category"),
  metricItem: document.getElementById("metric-item"),
  metricPurchase: document.getElementById("metric-purchase"),
  datasetSessions: document.getElementById("dataset-sessions"),
  datasetDetail: document.getElementById("dataset-detail"),
  categoryCoverage: document.getElementById("category-coverage"),
  baselineChart: document.getElementById("baseline-chart"),
  sessionCount: document.getElementById("session-count"),
  sessionButtons: document.getElementById("session-buttons"),
  selectedSession: document.getElementById("selected-session"),
  selectedSplit: document.getElementById("selected-split"),
  decisionIndex: document.getElementById("decision-index"),
  conversionStage: document.getElementById("conversion-stage"),
  intentProxy: document.getElementById("intent-proxy"),
  decisionSignals: document.getElementById("decision-signals"),
  prefixEvents: document.getElementById("prefix-events"),
  strategyNote: document.getElementById("strategy-note"),
  moduleGrid: document.getElementById("module-grid"),
  nextEvent: document.getElementById("next-event"),
  nextItem: document.getElementById("next-item"),
  nextCategory: document.getElementById("next-category"),
  strategyMatch: document.getElementById("strategy-match"),
  futureEvents: document.getElementById("future-events"),
  strategyButtons: Array.from(document.querySelectorAll("[data-strategy]")),
};

function pct(value) {
  if (value === null || value === undefined) {
    return "-";
  }
  return `${(value * 100).toFixed(1)}%`;
}

function label(value, fallback = "-") {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
  return String(value);
}

function titleCase(value) {
  return label(value).replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function compactNumber(value) {
  return new Intl.NumberFormat("en-US").format(value);
}

function itemLabel(value) {
  return value === null || value === undefined ? "Unknown item" : `Item ${value}`;
}

function categoryLabel(value) {
  return value === null || value === undefined ? "Unknown category" : `Category ${value}`;
}

function eventBadgeClass(eventType) {
  if (eventType === "transaction") {
    return "badge rose";
  }
  if (eventType === "add_to_cart") {
    return "badge gold";
  }
  return "badge";
}

function renderMetrics() {
  elements.metricCategory.textContent = pct(demoData.metrics.next_category_recent_rule_test_accuracy);
  elements.metricItem.textContent = pct(demoData.metrics.next_item_recent_rule_test_accuracy);
  elements.metricPurchase.textContent = pct(demoData.metrics.purchase_early_cart_test_f1);
}

function renderDatasetOverview() {
  const summary = demoData.dataset_summary;
  elements.datasetSessions.textContent = `${compactNumber(summary.sessions)} sessions`;
  elements.datasetDetail.textContent = `${compactNumber(summary.events)} events, ${compactNumber(summary.labels)} labels, ${compactNumber(summary.homepage_impressions)} simulated impressions.`;
  elements.categoryCoverage.textContent = pct(summary.decision_category_coverage);
}

function renderBaselineChart() {
  const cards = demoData.baseline_cards || [];
  const maxValue = Math.max(...cards.map((card) => card.value || 0), 1);
  elements.baselineChart.innerHTML = "";
  cards.forEach((card) => {
    const row = document.createElement("article");
    row.className = "baseline-row";
    const width = `${((card.value || 0) / maxValue) * 100}%`;
    row.innerHTML = `
      <div class="baseline-label">
        <strong>${card.label}</strong>
        <span>${card.model} - ${card.unit}</span>
      </div>
      <div class="bar-wrap" aria-hidden="true">
        <div class="bar-fill" style="width: ${width}"></div>
      </div>
      <strong class="baseline-value">${pct(card.value)}</strong>
    `;
    row.setAttribute("aria-label", `${card.label}: ${pct(card.value)} using ${card.model}`);
    elements.baselineChart.appendChild(row);
  });
}

function renderSessionButtons() {
  elements.sessionCount.textContent = `${demoData.sessions.length} shown`;
  elements.sessionButtons.innerHTML = "";
  demoData.sessions.forEach((session, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `session-button${index === selectedSessionIndex ? " is-active" : ""}`;
    button.innerHTML = `
      ${session.session_id}
      <span>${titleCase(session.intent_proxy)} - ${session.split}</span>
    `;
    button.addEventListener("click", () => {
      selectedSessionIndex = index;
      render();
    });
    elements.sessionButtons.appendChild(button);
  });
}

function renderDecisionSignals(session) {
  const signals = session.decision_signals;
  const items = [
    ["Prefix events", signals.prefix_event_count],
    ["Views", signals.prefix_view_count],
    ["Early carts", signals.prefix_add_to_cart_count],
    ["Unique items", signals.prefix_unique_items],
    ["Last category", categoryLabel(signals.last_category_id)],
    ["Frequent category", categoryLabel(signals.most_frequent_category_id)],
  ];
  elements.decisionSignals.innerHTML = "";
  items.forEach(([name, value]) => {
    const chip = document.createElement("div");
    chip.className = "signal-chip";
    chip.innerHTML = `<span>${name}</span><strong>${label(value)}</strong>`;
    elements.decisionSignals.appendChild(chip);
  });
}

function renderPrefix(session) {
  elements.prefixEvents.innerHTML = "";
  session.prefix.forEach((event) => {
    const row = document.createElement("li");
    row.className = "event-card";
    row.innerHTML = `
      <div class="event-topline">
        <strong>${itemLabel(event.item_id)}</strong>
        <span class="${eventBadgeClass(event.event_type)}">${titleCase(event.event_type)}</span>
      </div>
      <div class="event-meta">
        <span>${categoryLabel(event.category_id)}</span>
        <span>+${Number(event.seconds_from_session_start).toFixed(0)}s</span>
      </div>
    `;
    elements.prefixEvents.appendChild(row);
  });
}

function strategyText(session) {
  const signals = session.decision_signals;
  if (selectedStrategy === "control") {
    return "Control uses train-period global popularity only. It does not react to this visitor's early-session behaviour.";
  }
  const category = categoryLabel(signals.most_frequent_category_id ?? signals.last_category_id);
  if (signals.prefix_add_to_cart_count > 0) {
    return `Rule based uses early cart activity plus current category context (${category}) before choosing modules.`;
  }
  return `Rule based uses the most recent or most frequent early-session category (${category}) before choosing modules.`;
}

function renderModules(session) {
  const modules = session.impressions.filter(
    (impression) => impression.experiment_group === selectedStrategy
  );
  elements.moduleGrid.innerHTML = "";
  elements.strategyNote.textContent = strategyText(session);
  modules.forEach((module) => {
    const card = document.createElement("article");
    card.className = `module-card${module.simulated_click ? " is-match" : ""}`;
    card.innerHTML = `
      <div>
        <div class="module-topline">
          <span class="module-rank">#${module.rank}</span>
          <span class="${module.simulated_click ? "badge" : "badge gold"}">
            ${module.simulated_click ? "Matched" : "Shown"}
          </span>
        </div>
        <p class="module-type">${titleCase(module.module_type)}</p>
      </div>
      <div class="module-meta">
        <span>${itemLabel(module.content_item_id)}</span>
        <span>${categoryLabel(module.content_category_id)}</span>
      </div>
    `;
    elements.moduleGrid.appendChild(card);
  });

  const matchCount = modules.filter((module) => module.simulated_click).length;
  elements.strategyMatch.textContent = `${matchCount}/${modules.length} modules`;
}

function renderOutcome(session) {
  const next = session.next_event;
  const summary = session.future_summary;
  elements.nextEvent.textContent = titleCase(next.event_type);
  elements.nextItem.textContent = itemLabel(next.item_id);
  elements.nextCategory.textContent = categoryLabel(next.category_id);
  elements.futureEvents.textContent = `${summary.events_after_decision} total, ${summary.add_to_cart_events_after_decision} cart, ${summary.transactions_after_decision} purchase`;
}

function renderSelectedSession() {
  const session = demoData.sessions[selectedSessionIndex];
  elements.selectedSession.textContent = session.session_id;
  elements.selectedSplit.textContent = session.split;
  elements.decisionIndex.textContent = `After ${session.decision_event_index} events`;
  elements.conversionStage.textContent = titleCase(session.final_conversion_stage);
  elements.intentProxy.textContent = titleCase(session.intent_proxy);
  renderDecisionSignals(session);
  renderPrefix(session);
  renderModules(session);
  renderOutcome(session);
}

function renderStrategyButtons() {
  elements.strategyButtons.forEach((button) => {
    const isActive = button.dataset.strategy === selectedStrategy;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
}

function render() {
  renderMetrics();
  renderDatasetOverview();
  renderBaselineChart();
  renderSessionButtons();
  renderStrategyButtons();
  renderSelectedSession();
}

elements.strategyButtons.forEach((button) => {
  button.addEventListener("click", () => {
    selectedStrategy = button.dataset.strategy;
    render();
  });
});

render();
