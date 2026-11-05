    const DOCS_INDEX = @@INDEX_JSON@@;
    const DEFAULT_PAGE_ID = "@@DEFAULT_PAGE@@";
    let currentPageId = DEFAULT_PAGE_ID;

    const prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const scrollBehavior = prefersReducedMotion ? "auto" : "smooth";

    /* ---------- Navigation drawer (phones and tablets) ---------- */
    function setSidebarOpen(open) {
      const sb = document.getElementById("left-sidebar");
      const bd = document.getElementById("sidebar-backdrop");
      const btn = document.getElementById("menu-btn");
      if (sb) sb.classList.toggle("open", open);
      if (bd) bd.classList.toggle("open", open);
      if (btn) btn.setAttribute("aria-expanded", open ? "true" : "false");
    }

    function toggleMobileSidebar() {
      const sb = document.getElementById("left-sidebar");
      setSidebarOpen(!(sb && sb.classList.contains("open")));
    }

    function closeMobileSidebar() {
      setSidebarOpen(false);
    }

    /* ---------- Table of contents ---------- */
    function renderToc(pageId) {
      const tocContainer = document.getElementById("toc-container");
      const mobileTocContainer = document.getElementById("mobile-toc-container");
      const mobileTocDetails = document.getElementById("mobile-toc-details");
      const pageObj = DOCS_INDEX.find(p => p.id === pageId);
      if (!pageObj || !pageObj.toc || pageObj.toc.length === 0) {
        const emptyHtml = '<span class="toc-link">No subsections</span>';
        if (tocContainer) tocContainer.innerHTML = emptyHtml;
        if (mobileTocContainer) mobileTocContainer.innerHTML = emptyHtml;
        if (mobileTocDetails) mobileTocDetails.open = false;
        return;
      }
      const linksHtml = pageObj.toc.map(item => {
        const cls = item.level === 3 ? "toc-link toc-level-3" : "toc-link";
        const safeTitle = item.title.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        return `<a href="#${item.id}" class="${cls}" onclick="closeMobileToc()">${safeTitle}</a>`;
      }).join("");
      if (tocContainer) tocContainer.innerHTML = linksHtml;
      if (mobileTocContainer) mobileTocContainer.innerHTML = linksHtml;
      if (mobileTocDetails) mobileTocDetails.open = false;
    }

    function closeMobileToc() {
      const mobileTocDetails = document.getElementById("mobile-toc-details");
      if (mobileTocDetails) mobileTocDetails.open = false;
    }

    /* Keep the visible page title first in document order, so the one h1 a reader (or tool) meets first is the one on screen. */
    function keepVisibleTitleFirst(article, showHome) {
      const home = document.getElementById("home");
      const pane = document.getElementById("main-content");
      if (!pane || !pane.parentNode) return;
      const firstArticle = pane.querySelector(".docs-article");
      if (firstArticle && firstArticle !== article) pane.insertBefore(article, firstArticle);
      if (home) {
        if (showHome) pane.parentNode.insertBefore(home, pane);
        else pane.parentNode.appendChild(home);
      }
    }

    /* ---------- Page routing (all pages are pre-rendered; this only shows one) ---------- */
    function navigateToPage(pageId, scrollTargetId) {
      const targetArticle = document.getElementById("page-" + pageId);
      if (!targetArticle) return;

      closeMobileSidebar();

      document.querySelectorAll(".docs-article").forEach(el => el.classList.add("hidden"));
      targetArticle.classList.remove("hidden");

      document.querySelectorAll(".nav-item").forEach(btn => btn.classList.remove("active"));
      const activeBtn = document.getElementById("nav-" + pageId);
      if (activeBtn) {
        activeBtn.classList.add("active");
        activeBtn.setAttribute("aria-current", "page");
        document.querySelectorAll(".nav-item").forEach(btn => { if (btn !== activeBtn) btn.removeAttribute("aria-current"); });
      }

      currentPageId = pageId;
      /* The home view leads the default page; a deep link to one of its sections shows that section directly. */
      const showHome = pageId === DEFAULT_PAGE_ID && !scrollTargetId;
      document.body.classList.toggle("is-home", showHome);
      keepVisibleTitleFirst(targetArticle, showHome);
      renderToc(pageId);
      observeReveals();

      if (scrollTargetId) {
        const anchorEl = document.getElementById(scrollTargetId) || document.getElementById(scrollTargetId.replace(/-+/g, "-"));
        if (anchorEl) {
          anchorEl.scrollIntoView({ behavior: scrollBehavior });
          history.replaceState(null, "", "#" + anchorEl.id);
          return;
        }
      }
      window.scrollTo({ top: 0, behavior: "instant" });
      history.replaceState(null, "", "#" + pageId);
    }

    function navigateToHash(hashValue) {
      const cleanHash = (hashValue || "").replace(/^#/, "");
      if (!cleanHash) return;
      const directPage = DOCS_INDEX.find(p => p.id === cleanHash);
      if (directPage) {
        navigateToPage(directPage.id);
        return;
      }
      for (const p of DOCS_INDEX) {
        if (cleanHash.startsWith(p.id + "-")) {
          navigateToPage(p.id, cleanHash);
          return;
        }
      }
      const existingEl = document.getElementById(cleanHash);
      if (existingEl) {
        existingEl.scrollIntoView({ behavior: scrollBehavior });
      }
    }

    /* ---------- Code blocks ---------- */
    function copyCodeBlock(btn) {
      const wrapper = btn.closest(".code-block-wrapper");
      if (!wrapper) return;
      const codeEl = wrapper.querySelector("code");
      if (!codeEl) return;
      const text = codeEl.innerText;
      const done = () => {
        const orig = btn.getAttribute("data-label") || btn.innerText;
        btn.setAttribute("data-label", orig);
        btn.innerText = "Copied";
        setTimeout(() => { btn.innerText = orig; }, 1500);
      };
      const fallback = () => {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.setAttribute("readonly", "");
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else {
        fallback();
      }
    }

    /* ---------- Theme and tool (Antigravity / Claude Code / Codex) ---------- */
    function syncThemeButton() {
      const btn = document.getElementById("theme-toggle-btn");
      if (!btn) return;
      const dark = document.documentElement.getAttribute("data-theme") === "dark";
      btn.textContent = dark ? "Light mode" : "Dark mode";
      btn.setAttribute("aria-pressed", dark ? "true" : "false");
    }

    function toggleTheme() {
      const root = document.documentElement;
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("agy_docs_theme", next); } catch (e) {}
      syncThemeButton();
    }

    function setTool(tool) {
      if (tool !== "antigravity" && tool !== "claude" && tool !== "codex") return;
      document.documentElement.setAttribute("data-tool", tool);
      try { localStorage.setItem("pantheon_docs_tool", tool); } catch (e) {}
      document.querySelectorAll("[data-set-tool]").forEach(btn => {
        btn.setAttribute("aria-pressed", btn.getAttribute("data-set-tool") === tool ? "true" : "false");
      });
    }

    document.querySelectorAll("[data-set-tool]").forEach(btn => {
      btn.addEventListener("click", () => setTool(btn.getAttribute("data-set-tool")));
    });

    /* ---------- Search ---------- */
    const searchInput = document.getElementById("docs-search-input");
    const searchDropdown = document.getElementById("search-results");
    const topbar = document.querySelector(".topbar");

    function escapeHtml(s) {
      return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function toggleSearchRow() {
      if (!topbar) return;
      const open = topbar.classList.toggle("search-open");
      if (open && searchInput) searchInput.focus();
    }

    if (searchInput && searchDropdown) {
      searchInput.addEventListener("input", () => {
        const q = searchInput.value.trim().toLowerCase();
        if (q.length < 2) {
          searchDropdown.classList.remove("open");
          searchDropdown.innerHTML = "";
          return;
        }

        const hits = [];
        for (const page of DOCS_INDEX) {
          const hay = (page.title + " " + page.search_text).toLowerCase();
          const idx = hay.indexOf(q);
          if (idx !== -1) {
            const start = Math.max(0, idx - 45);
            const snippet = page.search_text.substring(start, start + 140);
            hits.push({ page, snippet });
          }
        }

        if (hits.length === 0) {
          searchDropdown.innerHTML = '<div class="search-hit"><div class="search-hit-snippet">No matching documents found.</div></div>';
        } else {
          searchDropdown.innerHTML = hits.slice(0, 10).map(h => `
            <button type="button" class="search-hit" role="option" onclick="selectSearchResult('${h.page.id}')">
              <div class="search-hit-title">${escapeHtml(h.page.title)} <span>${escapeHtml(h.page.path)}</span></div>
              <div class="search-hit-snippet">...${escapeHtml(h.snippet)}...</div>
            </button>
          `).join("");
        }
        searchDropdown.classList.add("open");
      });

      document.addEventListener("click", (e) => {
        if (!e.target.closest(".search-wrapper")) {
          searchDropdown.classList.remove("open");
        }
      });

      document.addEventListener("keydown", (e) => {
        const typing = /^(input|textarea|select)$/i.test(document.activeElement && document.activeElement.tagName);
        if (e.key === "/" && !typing) {
          e.preventDefault();
          if (topbar && window.matchMedia("(max-width: 680px)").matches) topbar.classList.add("search-open");
          searchInput.focus();
        } else if (e.key === "Escape") {
          searchDropdown.classList.remove("open");
          closeMobileSidebar();
        }
      });
    }

    function selectSearchResult(pageId) {
      if (searchDropdown) searchDropdown.classList.remove("open");
      navigateToPage(pageId);
    }

    /* ---------- Entrance motion: opacity and transform only, skipped for reduced motion ---------- */
    let revealObserver = null;
    function observeReveals() {
      if (!revealObserver) return;
      document.querySelectorAll(".reveal:not(.in):not([data-observed])").forEach((el) => {
        el.setAttribute("data-observed", "");
        revealObserver.observe(el);
      });
    }

    function initReveals() {
      if (prefersReducedMotion || !("IntersectionObserver" in window)) return;
      const selector = ".home h1, .home-sentence, .home-actions, .live-panel, .home-goals, .home-tabs, .article-body > .doc-h2, .article-body > .code-block-wrapper, .article-body > .table-responsive, .article-body > .callout, .article-body > .frontmatter-card, .article-body > .invoke-card";
      document.querySelectorAll(selector).forEach((el, i) => {
        el.classList.add("reveal");
        el.style.setProperty("--d", Math.min(i % 4, 3) * 70 + "ms");
      });
      revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            revealObserver.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
      observeReveals();
      document.documentElement.classList.add("reveal-ready");
      /* Safety net: never leave content hidden if the observer does not fire. */
      setTimeout(() => document.querySelectorAll(".reveal:not(.in)").forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.top < window.innerHeight) el.classList.add("in");
      }), 1200);
    }

    /* ---------- Group tabs on the home view (all panels show, stacked, when scripting is off) ---------- */
    function initGroupTabs() {
      const tabs = Array.from(document.querySelectorAll('.tabs [role="tab"]'));
      if (!tabs.length) return;
      const panelFor = (tab) => document.getElementById(tab.getAttribute("aria-controls"));
      const select = (tab, focus) => {
        tabs.forEach((t) => {
          const on = t === tab;
          t.setAttribute("aria-selected", on ? "true" : "false");
          t.tabIndex = on ? 0 : -1;
          const panel = panelFor(t);
          if (panel) panel.hidden = !on;
        });
        if (focus) tab.focus();
        try { localStorage.setItem("pantheon_docs_group", tab.getAttribute("data-group")); } catch (e) {}
      };
      let initial = tabs[0];
      try {
        const saved = localStorage.getItem("pantheon_docs_group");
        initial = tabs.find((t) => t.getAttribute("data-group") === saved) || tabs[0];
      } catch (e) {}
      select(initial, false);
      tabs.forEach((tab, i) => {
        tab.addEventListener("click", () => select(tab, false));
        tab.addEventListener("keydown", (e) => {
          const last = tabs.length - 1;
          const next = e.key === "ArrowRight" ? tabs[i === last ? 0 : i + 1]
            : e.key === "ArrowLeft" ? tabs[i === 0 ? last : i - 1]
            : e.key === "Home" ? tabs[0]
            : e.key === "End" ? tabs[last] : null;
          if (next) { e.preventDefault(); select(next, true); }
        });
      });
    }

    window.addEventListener("hashchange", () => {
      const hash = window.location.hash.replace(/^#/, "");
      if (hash) navigateToHash(hash);
    });

    /* ---------- Init ---------- */
    (function init() {
      syncThemeButton();
      setTool(document.documentElement.getAttribute("data-tool") || "antigravity");
      initGroupTabs();
      initReveals();

      const hash = window.location.hash.replace(/^#/, "");
      if (hash) {
        navigateToHash(hash);
        return;
      }
      renderToc(currentPageId);
    })();

    /* ---------- Downloader OS Tabs (Antigravity style) ---------- */
    function setInstallerTab(os) {
      document.querySelectorAll('.os-pill').forEach(function(pill) {
        var isMatch = pill.id === 'os-btn-' + os;
        pill.classList.toggle('active', isMatch);
      });
      document.querySelectorAll('.installer-panel').forEach(function(p) {
        p.classList.toggle('hidden', p.id !== 'os-panel-' + os);
      });
      try { localStorage.setItem('pantheon_installer_os', os); } catch (e) {}
    }

    function initInstallerOs() {
      var os = 'windows';
      try {
        var saved = localStorage.getItem('pantheon_installer_os');
        if (saved === 'windows' || saved === 'macos' || saved === 'linux') {
          os = saved;
        } else {
          var ua = navigator.userAgent || '';
          if (/Macintosh|Mac OS X/i.test(ua)) os = 'macos';
          else if (/Linux/i.test(ua)) os = 'linux';
        }
      } catch (e) {}
      setInstallerTab(os);
    }

    initInstallerOs();
