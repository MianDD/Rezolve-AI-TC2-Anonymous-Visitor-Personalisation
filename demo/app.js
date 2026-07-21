const demoData = window.TC2_DEMO_DATA;

let selectedSessionIndex = 0;
let selectedStrategy = "rule_based";

const elements = {
  metricCategory: document.getElementById("metric-category"),
  metricItem: document.getElementById("metric-item"),
  metricPurchase: document.getElementById("metric-purchase"),
  sessionCount: document.getElementById("session-count"),
  sessionButtons: document.getElementById("session-buttons"),
  selectedSession: document.getElementById("selected-session"),
  selectedSplit: document.getElementById("selected-split"),
  decisionIndex: document.getElementById("decision-index"),
  conversionStage: document.getElementById("conversion-stage"),
  intentProxy: document.getElementById("intent-proxy"),
  prefixEvents: document.getElementById("prefix-events"),
  moduleGrid: document.getElementById("module-grid"),
  nextEvent: document.getElementById("next-event"),
  nextItem: document.getElementById("next-item"),
  nextCategory: document.getElementById("next-category"),
  strategyMatch: document.getElementById("strategy-match"),
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

function itemLabel(value) {
  return value === null || value === undefined ? "Unknown item" : `Item ${value}`;
}

function categoryLabel(value) {
  return value === null || value === undefined ? "Unknown category" : `Category ${value}`;
}

function moduleLabel(value) {
  return titleCase(value);
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

function renderSessionButtons() {
  elements.sessionCount.textContent = `${demoData.sessions.length} shown`;
  elements.sessionButtons.innerHTML = "";
  demoData.sessions.forEach((session, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `session-button${index === selectedSessionIndex ? " is-active" : ""}`;
    button.innerHTML = `
      ${session.session_id}
      <span>${titleCase(session.intent_proxy)} · ${session.split}</span>
    `;
    button.addEventListener("click", () => {
      selectedSessionIndex = index;
      render();
    });
    elements.sessionButtons.appendChild(button);
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

function renderModules(session) {
  const modules = session.impressions.filter(
    (impression) => impression.experiment_group === selectedStrategy
  );
  elements.moduleGrid.innerHTML = "";
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
        <p class="module-type">${moduleLabel(module.module_type)}</p>
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
  elements.nextEvent.textContent = titleCase(next.event_type);
  elements.nextItem.textContent = itemLabel(next.item_id);
  elements.nextCategory.textContent = categoryLabel(next.category_id);
}

function renderSelectedSession() {
  const session = demoData.sessions[selectedSessionIndex];
  elements.selectedSession.textContent = session.session_id;
  elements.selectedSplit.textContent = session.split;
  elements.decisionIndex.textContent = `After ${session.decision_event_index} events`;
  elements.conversionStage.textContent = titleCase(session.final_conversion_stage);
  elements.intentProxy.textContent = titleCase(session.intent_proxy);
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
