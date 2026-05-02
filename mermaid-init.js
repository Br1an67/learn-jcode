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

    const dark = isDarkTheme();
    const themeVariables = dark ? {
      background: '#002b36',
      primaryColor: '#073642',
      primaryTextColor: '#eee8d5',
      primaryBorderColor: '#268bd2',
      lineColor: '#93a1a1',
      secondaryColor: '#123f4c',
      tertiaryColor: '#002b36',
      noteBkgColor: '#073642',
      noteTextColor: '#eee8d5',
      actorBkg: '#073642',
      actorBorder: '#2aa198',
      actorTextColor: '#eee8d5',
      signalColor: '#93a1a1',
      signalTextColor: '#eee8d5'
    } : {
      background: '#fdf6e3',
      primaryColor: '#eee8d5',
      primaryTextColor: '#073642',
      primaryBorderColor: '#268bd2',
      lineColor: '#586e75',
      secondaryColor: '#f3ecd8',
      tertiaryColor: '#fdf6e3',
      noteBkgColor: '#eee8d5',
      noteTextColor: '#073642',
      actorBkg: '#eee8d5',
      actorBorder: '#268bd2',
      actorTextColor: '#073642',
      signalColor: '#586e75',
      signalTextColor: '#073642'
    };

    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'loose',
      theme: 'base',
      themeVariables,
      flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis',
        nodeSpacing: 58,
        rankSpacing: 76,
        padding: 16,
        wrappingWidth: 150
      },
      sequence: {
        useMaxWidth: true,
        diagramMarginX: 42,
        diagramMarginY: 18,
        actorMargin: 68,
        messageMargin: 44,
        boxMargin: 12,
        noteMargin: 12
      }
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
