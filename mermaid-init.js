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

  function renderMermaid() {
    convertMermaidBlocks();
    if (!document.querySelector('.mermaid') || !window.mermaid) {
      return;
    }
    window.mermaid.initialize({
      startOnLoad: true,
      theme: isDarkTheme() ? 'dark' : 'default'
    });
  }

  function loadMermaid() {
    if (window.mermaid) {
      renderMermaid();
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
    script.onload = renderMermaid;
    document.head.appendChild(script);
  }

  window.addEventListener('load', loadMermaid);
})();
