// Shared case navigation — update this file when adding a new page.
// Each page needs: <div id="case-nav"></div> in its toolbar.

const CASE_PAGES = [
  {
    url:   "case-map.html",
    label: "Case Map",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg>`,
  },
  {
    url:   "name-Index.html",
    label: "Name Index",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  },
  {
    url:   "volume-index.html",
    label: "Vol. 1 Tracker",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><rect x="9" y="2" width="6" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M9 12h6"/><path d="M9 16h6"/></svg>`,
  },
  {
    url:   "interview-list.html",
    label: "Interview List",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>`,
  },
  {
    url:   "phone-directory.html",
    label: "Phone Directory",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.7 13.5 19.79 19.79 0 0 1 1.61 4.87 2 2 0 0 1 3.58 2.69h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 10a16 16 0 0 0 6.08 6.08l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.32z"/></svg>`,
  },
  {
    url:   "vcc-leads.html",
    label: "VCC Leads",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.7 13.5 19.79 19.79 0 0 1 1.61 4.87 2 2 0 0 1 3.58 2.69h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 10a16 16 0 0 0 6.08 6.08l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.32z"/></svg>`,
  },
  {
    url:   "e911-log.html",
    label: "E-911 Log",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M15.05 5A5 5 0 0 1 19 8.95M15.05 1A9 9 0 0 1 23 8.94m-1 7.98v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.7 13.5 19.79 19.79 0 0 1 1.61 4.87 2 2 0 0 1 3.58 2.69h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 10a16 16 0 0 0 6.08 6.08l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.32z"/></svg>`,
  },
  {
    url:   "evidence-log.html",
    label: "Evidence Log",
    icon:  `<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>`,
  },
];

// Inject shared nav button styles using CSS vars
(function injectNavStyles() {
  const style = document.createElement("style");
  style.textContent = `
    #case-nav {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      align-items: center;
    }
    .case-nav-btn {
      padding: 6px 12px;
      background: var(--accent-subtle);
      color: var(--accent);
      border: 1px solid var(--accent-dim);
      border-radius: 8px;
      font-size: .8rem;
      font-weight: 600;
      text-decoration: none;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
      transition: opacity .15s;
      font-family: inherit;
    }
    .case-nav-btn:hover { opacity: .75; }
    .theme-toggle-btn {
      padding: 6px 10px;
      background: var(--bg3);
      color: var(--text-dim);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: .8rem;
      font-weight: 600;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      cursor: pointer;
      transition: opacity .15s;
      font-family: inherit;
    }
    .theme-toggle-btn:hover { opacity: .75; }
  `;
  document.head.appendChild(style);
})();

(function () {
  const container = document.getElementById("case-nav");
  if (!container) return;
  const current = location.pathname.split("/").pop();

  // Nav links
  CASE_PAGES.forEach(p => {
    if (p.url === current) return;
    const a = document.createElement("a");
    a.href = p.url;
    a.className = "case-nav-btn";
    a.innerHTML = `${p.icon} ${p.label}`;
    container.appendChild(a);
  });

  // Theme toggle
  const moonIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
  const sunIcon  = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;

  const btn = document.createElement("button");
  btn.className = "theme-toggle-btn";

  function updateBtn() {
    const isLight = document.documentElement.dataset.theme === "light";
    btn.innerHTML = isLight ? `${moonIcon} Dark` : `${sunIcon} Light`;
    btn.title = isLight ? "Switch to dark mode" : "Switch to light mode";
  }
  updateBtn();

  btn.addEventListener("click", () => {
    const isLight = document.documentElement.dataset.theme === "light";
    if (isLight) {
      delete document.documentElement.dataset.theme;
      try { localStorage.removeItem("foia-theme"); } catch(e) {}
    } else {
      document.documentElement.dataset.theme = "light";
      try { localStorage.setItem("foia-theme", "light"); } catch(e) {}
    }
    updateBtn();
  });

  container.appendChild(btn);
})();
