document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('[role="tab"]');
  const tabPanels = document.querySelectorAll('[role="tabpanel"]');

  function activateTab(tab) {
    // Deactivate all tabs
    tabs.forEach(t => {
      t.setAttribute('aria-selected', 'false');
      t.setAttribute('tabindex', '-1');
    });

    // Hide all tab panels
    tabPanels.forEach(panel => panel.classList.add('is-hidden'));

    // Activate the selected tab
    tab.setAttribute('aria-selected', 'true');
    tab.setAttribute('tabindex', '0');
    tab.focus();

    // Show the associated tab panel
    const panelId = tab.getAttribute('aria-controls');
    const panel = document.getElementById(panelId);
    if (panel) {
      panel.classList.remove('is-hidden');
    }
  }

  // Add click event listeners to tabs
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      activateTab(tab);
    });
  });

  // Activate the first tab by default on page load
  if (tabs.length > 0) {
    activateTab(tabs[0]);
  }
});

// 100% vibe coded Javacript ✅
// i went through the code, tested it and removed what wasn't needed, but i don't know JavaScript. I had an AI assist me with this. 🤖