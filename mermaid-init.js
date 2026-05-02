// Render ```mermaid fences in mdBook without requiring an mdBook preprocessor.
(function () {
  function convertMermaidBlocks() {
    const codeBlocks = document.querySelectorAll('code.language-mermaid');
    codeBlocks.forEach(function (block) {
      const pre = block.parentElement;
      if (!pre || pre.classList.contains('mermaid')) {
        return;
      }
      const replacement = document.createElement('pre');
      replacement.className = 'mermaid';
      replacement.textContent = block.textContent;
      pre.parentElement.replaceChild(replacement, pre);
    });
  }

  function isDarkTheme() {
    const darkThemes = ['ayu', 'navy', 'coal'];
    const classList = document.documentElement.classList;
    return darkThemes.some(function (theme) { return classList.contains(theme); });
  }

  async function renderMermaid() {
    convertMermaidBlocks();
    if (!document.querySelector('.mermaid') || !window.mermaid) {
      return;
    }

    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      theme: isDarkTheme() ? 'dark' : 'default',
      flowchart: { useMaxWidth: true, htmlLabels: false },
      sequence: { useMaxWidth: true }
    });

    try {
      await window.mermaid.run({ querySelector: '.mermaid' });
    } catch (error) {
      console.warn('Mermaid render failed:', error);
    }
  }

  function start() {
    renderMermaid();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  for (const themeId of ['light', 'rust', 'coal', 'navy', 'ayu']) {
    const el = document.getElementById(themeId);
    if (el) {
      el.addEventListener('click', function () { window.location.reload(); });
    }
  }
})();
